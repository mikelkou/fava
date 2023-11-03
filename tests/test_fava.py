import os
import pandas as pd
import pytest
from pathlib import Path

from favapy import fava


@pytest.fixture
def data_dir() -> Path:
    data_dir = os.environ.get("DATA_DIR")
    if data_dir is None:
        raise ValueError("DATA_DIR environment variable not set")
    else:
        return Path(data_dir)


@pytest.fixture
def test_dataset(data_dir) -> pd.DataFrame:
    data_file_path = data_dir / "Example_dataset_GSE75748_sc_cell_type_ec.tsv"
    return pd.read_csv(data_file_path, sep="\t").iloc[:100, :100]


def test_favapy(test_dataset):
    FAVA_network = fava.cook(
        data=test_dataset,
        log2_normalization=True,
        hidden_layer=None,
        latent_dim=None,
        epochs=10,
        batch_size=32,
        interaction_count=100,
    )
    return FAVA_network
