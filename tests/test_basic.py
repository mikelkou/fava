from favapy import fava
from scvi.data import synthetic_iid

adata = synthetic_iid()


def test_favapy():
    FAVA_network = fava.cook(
        data=adata,
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
