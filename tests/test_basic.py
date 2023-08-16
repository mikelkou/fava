import pandas as pd
from favapy import fava

data = pd.read_csv(
    "/Users/tgn531/Desktop/fava/data/Example_dataset_GSE75748_sc_cell_type_ec.tsv",
    sep="\t",
).iloc[:100, :100]


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
