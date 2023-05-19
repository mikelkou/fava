# FAVA: Functional Associations using Variational Autoencoders
<!-- ![Fava](https://user-images.githubusercontent.com/81096946/177743627-2e6a7447-3fc1-48a8-a6bb-003a3ace223a.png) -->
<img src="https://user-images.githubusercontent.com/81096946/177743627-2e6a7447-3fc1-48a8-a6bb-003a3ace223a.png" alt="fava" width="500"/>

Protein networks are commonly used for understanding the interplay between proteins in the cell as well as for visualizing omics data. Unfortunately, most existing high-quality networks are heavily biased by data availability, in the sense that well-studied proteins have many more interactions than understudied proteins. To create networks that can help elucidate functions for the latter, we must start from data that are not affected by this literature bias, in other words, from omics data such as single cell RNA-seq (scRNA-seq) and proteomics. While networks can be inferred from such data through simple co-expression analysis, this approach does not work well due to high sparseness (many transcripts/proteins are not consistently observed in each cell/sample) and redundancy (many similar cells/samples are analyzed) of such data. We have therefore developed FAVA, Functional Associations using Variational Autoencoders, which deals with both issues by compressing these high-dimensional data into a dense, low-dimensional latent space. Calculating correlations in this latent space results in much improved networks compared to the original representation for large-scale scRNA-seq and proteomics data from the Human Protein Atlas, and from PRIDE, respectively. Additionally, these networks, which given the nature of the input data should be free of literature bias, have much better coverage of understudied proteins than existing networks.

[![PyPI version](https://badge.fury.io/py/favapy.svg)](https://badge.fury.io/py/favapy)
[![Documentation Status](https://readthedocs.org/projects/fava/badge/?version=latest)](https://fava.readthedocs.io/en/latest/?badge=latest)

## Data availability
[The Combined Network](https://doi.org/10.5281/zenodo.6803472)

## Installation:
```
pip install favapy
```

## favapy as Python library
Read the jupyter-notebook: [How_to_use_favapy_in_a_notebook](https://github.com/mikelkou/fava/blob/main/How_to_use_favapy_in_a_notebook.ipynb)

favapy supports both AnnData objects and count/abundance matrices.


## Command line interface
Run favapy from the command line as follows:
```
favapy <path-to-data-file> <path-to-save-output>
```

### Optional parameters:
```

-t Type of input data ('tsv' or 'csv'). Default value = 'tsv'.

-n The number of interactions in the output file (with both directions, proteinA-proteinB and proteinB-proteinA). Default value = 100000.

-c The cut-off on the Pearson Correlation scores. This option overwrites the number of interactions. Default value = None.

-d The dimensions of the intermediate\hidden layer. Default value depends on the input size.

-l The dimensions of the latent space. Default value depends on the size of the hidden layer.

-e The number of epochs. Default value = 50.

-b The  batch size. Default value = 32.

```

If FAVA is useful for your research, consider citing [FAVA BiorXiv](https://doi.org/10.1101/2022.07.06.499022).

#### Other Relevant publications:
[The STRING database in 2023](https://doi.org/10.1093/nar/gkac1000).
