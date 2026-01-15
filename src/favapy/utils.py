"""Utility functions for data preprocessing and correlation analysis."""

from __future__ import annotations

import logging
import time
from typing import Optional, Union

import numpy as np
import pandas as pd
import anndata
from scipy import stats


def _top_k_sorted_indices(arr: np.ndarray, k: int) -> np.ndarray:
    """Return indices of top k values, sorted descending."""
    if k <= 0:
        return np.array([], dtype=np.intp)
    if k >= len(arr):
        return np.argsort(arr)[::-1]
    top = np.argpartition(arr, -k)[-k:]
    return top[np.argsort(arr[top])[::-1]]


def _preprocess_expression(x: np.ndarray) -> np.ndarray:
    """
    Apply log2 transformation and min-max normalization to expression data.

    Combines both preprocessing steps:
    1. Log2 transformation (skipped if negative values detected)
    2. Min-max normalization to [0, 1] range

    Parameters
    ----------
    x : np.ndarray
        Expression matrix with shape (n_genes, n_features).

    Returns
    -------
    x : np.ndarray
        Preprocessed expression matrix with values in [0, 1] range.
    """
    # Step 1: Apply log2 transformation if data is non-negative
    if np.any(x < 0):
        logging.warning("Negative values detected, skipping log2 normalization.")
    else:
        x = np.log2(1 + x)

    # Step 2: Apply robust min-max normalization
    constant = 1e-8  # Small constant to avoid division by zero
    row_min = np.min(x, axis=1, keepdims=True)
    row_max = np.max(x, axis=1, keepdims=True)
    x = (x - row_min) / (row_max - row_min + constant)
    x = np.nan_to_num(x)  # Handle NaN values

    return x


def _load_data(input_file: str, data_type: str) -> tuple[np.ndarray, list[str]]:
    """
    Loads data from a file.

    Parameters
    ----------
    input_file : str
        Path to the input file.
    data_type : str
        Type of the data file ('tsv' or 'csv').

    Returns
    -------
    expr : np.ndarray
        Data array with shape (n_genes, n_samples).
    row_names : list[str]
        List of row names (gene/protein identifiers).
    """
    sep = "\t" if data_type == "tsv" else ","
    df = pd.read_csv(input_file, sep=sep, index_col=0)
    return df.values.astype(np.float32), df.index.tolist()


def _extract_data(
    data: Union[anndata.AnnData, pd.DataFrame], layer: Optional[str] = None
) -> tuple[np.ndarray, list[str]]:
    """
    Extract matrix and gene names from AnnData or pandas DataFrame.

    Parameters
    ----------
    data : anndata.AnnData or pd.DataFrame
        Input data. AnnData with genes in var, cells in obs.
        DataFrame with genes as index (rows), cells as columns.
    layer : str, optional
        For AnnData input, which layer to use. If None, uses X (default layer).

    Returns
    -------
    x : np.ndarray
        Expression matrix with shape (n_genes, n_cells).
    row_names : list[str]
        Gene/protein names.

    Raises
    ------
    ValueError
        If input type is not supported or data structure is invalid.
    """
    if isinstance(data, anndata.AnnData):
        # AnnData input
        if layer is not None:
            if layer not in data.layers:
                raise ValueError(
                    f"Layer '{layer}' not found in AnnData object. "
                    f"Available layers: {list(data.layers.keys())}"
                )
            x_matrix = data.layers[layer]
        else:
            x_matrix = data.X

        # Convert sparse to dense if needed
        if hasattr(x_matrix, "toarray"):
            x = x_matrix.toarray()
        else:
            x = np.asarray(x_matrix)

        # Transpose to (genes, cells) - AnnData stores (cells, genes)
        x = x.T
        row_names = data.var.index.tolist()

    elif isinstance(data, pd.DataFrame):
        # pandas DataFrame input (index = genes, columns = cells)
        x = data.values
        row_names = data.index.tolist()

    else:
        raise ValueError(
            f"Unsupported input type: {type(data).__name__}. "
            f"Expected anndata.AnnData or pd.DataFrame."
        )

    # Ensure float32 dtype and validate 2D shape
    x = np.asarray(x, dtype=np.float32)
    if x.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {x.shape}.")
    if x.shape[0] == 0 or x.shape[1] == 0:
        raise ValueError(f"Empty data matrix with shape {x.shape}.")

    return x, row_names


def _create_protein_pairs(
    x_test_encoded: np.ndarray,
    row_names: list[str],
    correlation_type: str = "pearson",
    interaction_count: int = 100000,
    CC_cutoff: Optional[float] = None,
) -> pd.DataFrame:
    """
    Create pairs of proteins based on their encoded latent spaces.

    FAVA uses ALL THREE VAE encoder outputs (z_mean, z_log_sigma, z) concatenated
    to create a richer representation for correlation analysis. This captures:
    - z_mean: Mean latent embedding
    - z_log_sigma: Uncertainty/variance in latent space
    - z: Stochastic sample from the distribution

    Parameters
    ----------
    x_test_encoded : np.ndarray
        Encoded latent spaces with shape (3, n_samples, latent_dim)
        where dim 0 contains [z_mean, z_log_sigma, z]
    row_names : list[str]
        List of row names corresponding to the data.
    correlation_type : str
        Type of correlation to use ('pearson' or 'spearman').
    interaction_count : int, optional
        Maximum number of interactions to include, by default 100000.
    CC_cutoff : float, optional
        Correlation Coefficient cutoff, by default None.

    Returns
    -------
    pairs_df : pd.DataFrame
        DataFrame containing filtered protein pairs and correlation scores,
        sorted by score descending.
    """
    start_time = time.time()

    # Reshape from (3, n_samples, latent_dim) to (n_samples, 3*latent_dim)
    n_outputs, n_samples, latent_dim = x_test_encoded.shape
    x_concat = x_test_encoded.transpose(1, 0, 2).reshape(n_samples, -1)

    # Compute correlation matrix using NumPy/SciPy (faster than pandas)
    # x_concat is (n_genes, 3*latent_dim), correlate rows (genes)
    if correlation_type == "pearson":
        corr_matrix = np.corrcoef(x_concat)
    elif correlation_type == "spearman":
        # axis=1 means rows are variables (genes), columns are observations (features)
        corr_matrix, _ = stats.spearmanr(x_concat, axis=1)
    else:
        raise ValueError(
            f"Invalid correlation_type: '{correlation_type}'. "
            f"Expected 'pearson' or 'spearman'."
        )

    # Extract upper triangle only (avoids AB-BA duplicates and self-loops)
    n_genes = len(row_names)
    upper_idx = np.triu_indices(n_genes, k=1)
    scores = corr_matrix[upper_idx]

    # Get sorted indices of pairs to keep
    if CC_cutoff is not None:
        logging.info(f" A cut-off of {CC_cutoff} is applied.")
        mask = scores >= CC_cutoff
        valid = np.where(mask)[0]
        sorted_idx = valid[np.argsort(scores[valid])[::-1]]
    else:
        if interaction_count is not None:
            k = min(interaction_count, len(scores))
            logging.warning(f" The number of interactions in the output file is {k}.")
        else:
            k = len(scores)
        sorted_idx = _top_k_sorted_indices(scores, k)

    filtered_i = upper_idx[0][sorted_idx]
    filtered_j = upper_idx[1][sorted_idx]
    filtered_scores = scores[sorted_idx]

    # Create DataFrame only for filtered pairs
    pairs_df = pd.DataFrame(
        {
            "Protein_1": [row_names[i] for i in filtered_i],
            "Protein_2": [row_names[j] for j in filtered_j],
            "Score": filtered_scores,
        }
    )

    end_time = time.time()
    logging.info(f"Total time taken: {end_time - start_time:.2f} seconds")

    return pairs_df
