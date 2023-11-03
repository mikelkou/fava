import logging
import argparse
import warnings

warnings.filterwarnings("ignore")

import os
import anndata
import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras import layers
from keras import backend as K


config = tf.compat.v1.ConfigProto()
config.intra_op_parallelism_threads = 1
config.inter_op_parallelism_threads = 1
tf.compat.v1.Session(config=config)

logger = logging.getLogger().setLevel(logging.INFO)


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + "\n"


warnings.formatwarning = custom_formatwarning


def argument_parser():
    parser = argparse.ArgumentParser(
        description="Infer Functional Associations using Variational Autoencoders on -Omics data."
    )
    parser.add_argument("input_file", type=str, help="The absolute path of the data.")
    parser.add_argument(
        "output_file", type=str, help="The absolute path where the output will be saved"
    )
    parser.add_argument(
        "-t",
        "--data_type",
        type=str,
        default="tsv",
        choices=["tsv", "csv"],
        help="Type of input data.",
    )
    parser.add_argument(
        "-n",
        dest="interaction_count",
        type=int,
        default=100000,
        help="The number of interactions in the output file.",
    )
    parser.add_argument(
        "-c",
        dest="CC_cutoff",
        type=float,
        default=None,
        help="The cut-off on the Correlation scores.",
    )
    parser.add_argument(
        "-d",
        dest="hidden_layer",
        default=None,
        type=int,
        help="Intermediate/hidden layer dimensions",
    )
    parser.add_argument(
        "-l", dest="latent_dim", default=None, type=int, help="Latent space dimensions"
    )
    parser.add_argument(
        "-e", dest="epochs", type=int, default=50, help="How many epochs?"
    )
    parser.add_argument(
        "-b", dest="batch_size", type=int, default=32, help="batch_size"
    )
    parser.add_argument(
        "-cor",
        "--correlation_type",
        type=str,
        default="pearson",
        choices=["pearson", "spearman"],
        help="Type of correlation to use (Pearson or Spearman).",
    )

    args = parser.parse_args()
    return args


def load_data(input_file, data_type):
    """
    Loads and preprocesses data from a file.

    Parameters
    ----------
    input_file : str
        Path to the input file.
    data_type : str
        Type of the data file ('tsv' or 'csv').

    Returns
    -------
    expr : np.ndarray
        Processed data array.
    row_names : list
        List of row names corresponding to the data.
    """
    row_names = []
    array = []
    with open(input_file, "r", encoding="utf-8") as infile:
        next(infile)
        for line in infile:
            if data_type == "tsv":
                line = line.split("\t")
            else:
                line = line.split(",")
            row_names.append(line[0])
            array.append(line[1:])

    expr = np.asarray(array, dtype=np.float32)

    if np.all(expr >= 0):
        expr = np.log2(1 + expr[:])
    else:
        logging.warn(
            " Negative values are detected, so log2 normalization is not applied."
        )

    # expr = expr / np.max(expr, axis=1, keepdims=True)
    constant = 1e-8  # small constant to avoid division by zero
    expr = (expr - np.min(expr, axis=1, keepdims=True)) / (
        np.max(expr, axis=1, keepdims=True)
        - np.min(expr, axis=1, keepdims=True)
        + constant
    )
    expr = np.nan_to_num(expr)
    return expr, row_names


class VAE(keras.Model):
    """
    Variational Autoencoder model class.

    Parameters
    ----------
    opt : tf.keras.optimizers.Optimizer
        Optimizer for the model.
    x_train : np.ndarray
        Training data.
    x_test : np.ndarray
        Test data.
    batch_size : int
        Batch size for training.
    original_dim : int
        Dimension of the input data.
    hidden_layer : int
        Number of units in the hidden layer.
    latent_dim : int
        Dimension of the latent space.
    epochs : int
        Number of training epochs.
    """

    def __init__(
        self,
        opt,
        x_train,
        x_test,
        batch_size,
        original_dim,
        hidden_layer,
        latent_dim,
        epochs,
    ):
        super(VAE, self).__init__()
        inputs = keras.Input(shape=(original_dim,))
        h = layers.Dense(hidden_layer, activation="relu")(inputs)

        z_mean = layers.Dense(latent_dim)(h)
        z_log_sigma = layers.Dense(latent_dim)(h)

        # Sampling
        def sampling(args):
            z_mean, z_log_sigma = args
            epsilon = K.random_normal(
                shape=(K.shape(z_mean)[0], latent_dim), mean=0.0, stddev=0.1
            )
            return z_mean + K.exp(z_log_sigma) * epsilon

        z = layers.Lambda(sampling)([z_mean, z_log_sigma])

        # Create encoder
        encoder = keras.Model(inputs, [z_mean, z_log_sigma, z], name="encoder")
        self.encoder = encoder
        # Create decoder
        latent_inputs = keras.Input(shape=(latent_dim,), name="z_sampling")
        x = layers.Dense(hidden_layer, activation="relu")(latent_inputs)  # relu

        outputs = layers.Dense(original_dim, activation="sigmoid")(x)
        decoder = keras.Model(latent_inputs, outputs, name="decoder")
        self.decoder = decoder

        # instantiate VAE model
        outputs = decoder(encoder(inputs)[2])
        vae = keras.Model(inputs, outputs, name="vae_mlp")

        # loss
        reconstruction_loss = keras.losses.mean_squared_error(inputs, outputs)
        reconstruction_loss *= original_dim
        kl_loss = 1 + z_log_sigma - K.square(z_mean) - K.exp(z_log_sigma)
        kl_loss = K.sum(kl_loss, axis=-1)
        kl_loss *= -0.5
        vae_loss = K.mean(0.9 * (reconstruction_loss) + 0.1 * (kl_loss))
        vae.add_loss(vae_loss)

        vae.compile(optimizer=opt, loss="mean_squared_error", metrics=["accuracy"])
        vae.fit(
            x_train,
            x_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_test, x_test),
        )


def create_protein_pairs(x_test_encoded, row_names, correlation_type="pearson"):
    """
    Create pairs of proteins based on their encoded latent spaces.

    Parameters
    ----------
    x_test_encoded : np.ndarray
        Encoded latent spaces.
    row_names : list
        List of row names corresponding to the data.
    correlation_type : str
        Type of correlation to use (Pearson or Spearman).

    Returns
    -------
    correlation_df : pd.DataFrame
        DataFrame containing protein pairs and correlation scores.
    """
    # Concatenate latent spaces
    df_x_test_encoded_0 = pd.DataFrame(x_test_encoded[0, :, :])
    df_x_test_encoded_1 = pd.DataFrame(x_test_encoded[1, :, :])
    df_x_test_encoded_2 = pd.DataFrame(x_test_encoded[2, :, :])

    df_x_test_encoded_01 = pd.merge(
        df_x_test_encoded_0, df_x_test_encoded_1, left_index=True, right_index=True
    )
    df_x_test_encoded = pd.merge(
        df_x_test_encoded_01, df_x_test_encoded_2, left_index=True, right_index=True
    )

    df_x_test_encoded = np.asarray(df_x_test_encoded)

    # Correlation of the latent space: Pearson or Spearman
    if correlation_type == "spearman":
        corr = pd.DataFrame(df_x_test_encoded.T).corr(method="spearman")
        corr.columns = corr.index = row_names
    else:
        corr = np.corrcoef(df_x_test_encoded)
        corr = pd.DataFrame(corr, columns=row_names, index=row_names)

    correlation_df = corr.stack().reset_index()

    # set column names
    correlation_df.columns = ["Protein_1", "Protein_2", "Score"]
    return correlation_df


def pairs_after_cutoff(correlation, interaction_count=100000, CC_cutoff=None):
    """
    Filter protein pairs based on correlation scores and cutoffs.

    Parameters
    ----------
    correlation : pd.DataFrame
        DataFrame containing protein pairs and correlation scores.
    interaction_count : int, optional
        Maximum number of interactions to include, by default 100000.
    CC_cutoff : float, optional
        Correlation Coefficient cutoff, by default None.

    Returns
    -------
    correlation_df_new : pd.DataFrame
        Filtered DataFrame with selected protein pairs.
    """
    if CC_cutoff is not None and isinstance(CC_cutoff, (int, float)):
        logging.info(" A cut-off of " + str(CC_cutoff) + " is applied.")
        correlation_df_new = correlation.loc[(correlation["Score"] >= CC_cutoff)]
    else:
        correlation_df_new = correlation.iloc[:interaction_count, :]
        logging.warn(
            " The number of interactions in the output file is "
            + str(interaction_count)
            + " in which both directions are included: proteinA - proteinB and proteinB - proteinA."
        )
    return correlation_df_new


def cook(
    data,
    log2_normalization=True,
    hidden_layer=None,
    latent_dim=None,
    epochs=50,
    batch_size=32,
    interaction_count=100000,
    correlation_type="pearson",
    CC_cutoff=None,
):
    """
    Preprocess data, train a Variational Autoencoder (VAE), and create filtered protein pairs.

    Parameters
    ----------
    data : np.ndarray or anndata._core.anndata.AnnData
        Input data or AnnData object.
    log2_normalization : bool, optional
        Whether to apply log2 normalization, by default True.
    hidden_layer : int, optional
        Number of units in the hidden layer, by default None.
    latent_dim : int, optional
        Dimension of the latent space, by default None.
    epochs : int, optional
        Number of training epochs, by default 50.
    batch_size : int, optional
        Batch size for training, by default 32.
    interaction_count : int, optional
        Maximum number of interactions to include, by default 100000.
    correlation_type : str, optional
        Type of correlation to use (Pearson or Spearman), by default Pearson.
    CC_cutoff : float, optional
        Correlation Coefficient cutoff, by default None.

    Returns
    -------
    final_pairs : pd.DataFrame
        Filtered protein pairs based on correlation and cutoffs.
    """
    if type(data) == anndata._core.anndata.AnnData:
        x = data.X.T
        row_names = data.var.index
    else:
        x = np.asarray(data, dtype=np.float32)
        row_names = data.index

    if np.any(x < 0):
        log2_normalization = False
        logging.warn(
            " Negative values are detected or log2_normalization was set to False, so log2 normalization is not applied."
        )

    if log2_normalization == True:
        x = np.log2(1 + x[:])
        logging.warn(" log2 normalization is applied.")

    x = x / np.max(x, axis=1, keepdims=True)
    x = np.nan_to_num(x)

    original_dim = x.shape[1]
    if hidden_layer == None:
        if original_dim >= 2000:
            hidden_layer = 1000
        if original_dim > 500 and original_dim < 2000:
            hidden_layer = 500
        if original_dim <= 500:
            hidden_layer = 50

    if latent_dim == None:
        if hidden_layer >= 1000:
            latent_dim = 100
        if hidden_layer >= 500 and hidden_layer < 1000:
            latent_dim = 50
        if hidden_layer <= 500:
            latent_dim = 5

    opt = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=0.001)
    x_train = x_test = np.array(x)
    vae = VAE(
        opt, x_train, x_test, batch_size, original_dim, hidden_layer, latent_dim, epochs
    )
    x_test_encoded = np.array(vae.encoder.predict(x_test, batch_size=batch_size))
    correlation = create_protein_pairs(x_test_encoded, row_names, correlation_type)
    final_pairs = correlation[correlation.iloc[:, 0] != correlation.iloc[:, 1]]
    final_pairs = final_pairs.sort_values(by=["Score"], ascending=False)
    final_pairs = pairs_after_cutoff(
        correlation=final_pairs,
        interaction_count=interaction_count,
        CC_cutoff=CC_cutoff,
    )
    return final_pairs


def main():
    """
    Main function for preprocessing data, training VAE, and saving results.

    This function loads data, applies preprocessing, trains a Variational Autoencoder (VAE),
    calculates correlation scores between encoded latent spaces, filters protein pairs based
    on correlation and cutoffs, and finally saves the results to a file.
    """
    args = argument_parser()

    x, row_names = load_data(args.input_file, args.data_type)
    original_dim = x.shape[1]

    if args.hidden_layer == None:
        if original_dim >= 2000:
            args.hidden_layer = 1000
        if original_dim > 500 and original_dim < 2000:
            args.hidden_layer = 500
        if original_dim <= 500:
            args.hidden_layer = 50

    if args.latent_dim == None:
        if args.hidden_layer >= 1000:
            args.latent_dim = 100
        if args.hidden_layer >= 500 and args.hidden_layer < 1000:
            args.latent_dim = 50
        if args.hidden_layer <= 500:
            args.latent_dim = 5

    opt = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=0.001)
    x_train = x_test = np.array(x)
    vae = VAE(
        opt,
        x_train,
        x_test,
        args.batch_size,
        original_dim,
        args.hidden_layer,
        args.latent_dim,
        args.epochs,
    )
    x_test_encoded = np.array(vae.encoder.predict(x_test, batch_size=args.batch_size))

    logging.info(f" Calculating {args.correlation_type} correlation scores.")
    correlation = create_protein_pairs(x_test_encoded, row_names, args.correlation_type)

    final_pairs = correlation[correlation.iloc[:, 0] != correlation.iloc[:, 1]]
    final_pairs = final_pairs.sort_values(by=["Score"], ascending=False)
    final_pairs = pairs_after_cutoff(
        correlation=final_pairs,
        interaction_count=args.interaction_count,
        CC_cutoff=args.CC_cutoff,
    )
    final_pairs.Score = final_pairs.Score.astype(float).round(5)
    logging.warn(
        " If it is not the desired cut-off, please check again the value assigned to the related parameter (-n or interaction_count | -c or CC_cutoff)."
    )

    logging.info(" Saving the file with the interactions in the chosen directory ...")

    # Save the file
    np.savetxt(args.output_file, final_pairs, fmt="%s")
    logging.info(
        " Congratulations! A file is waiting for you here: " + args.output_file
    )


if __name__ == "__main__":
    main()
