import os
import pandas as pd

from favapy import fava

data_dir = os.environ.get("DATA_DIR")
if data_dir is None:
    raise ValueError("DATA_DIR environment variable not set")

data_file_path = os.path.join(data_dir, "Example_dataset_GSE75748_sc_cell_type_ec.tsv")

data = pd.read_csv(data_file_path, sep="\t").iloc[:100, :100]


def test_favapy():
    FAVA_network = fava.cook(
        data=data,
        log2_normalization=True,
        hidden_layer=None,
        latent_dim=None,
        epochs=10,
        batch_size=32,
        interaction_count=100,
    )
    return FAVA_network


FAVA_network = test_favapy()

# tests __repr__
print(FAVA_network)
