# <img src="https://user-images.githubusercontent.com/81096946/177743627-2e6a7447-3fc1-48a8-a6bb-003a3ace223a.png" alt="fava" width="150"/> FAVA: Functional Associations using Variational Autoencoders


[![PyPI version](https://badge.fury.io/py/favapy.svg)](https://badge.fury.io/py/favapy)
[![Documentation Status](https://readthedocs.org/projects/fava/badge/?version=latest)](https://fava.readthedocs.io/en/latest/?badge=latest)
![example workflow](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)

<!-- ![Fava](https://user-images.githubusercontent.com/81096946/177743627-2e6a7447-3fc1-48a8-a6bb-003a3ace223a.png) -->
FAVA is a method used to construct protein networks based on omics data such as single-cell RNA sequencing (scRNA-seq) and proteomics. Existing protein networks are often biased towards well-studied proteins, limiting their ability to reveal functions of understudied proteins. FAVA addresses this issue by leveraging omics data that are not influenced by literature bias.
Read the [documentation](https://fava.readthedocs.io/en/latest/).


![Screenshot 2023-08-17 at 10 14 20](https://github.com/mikelkou/fava/assets/81096946/416deeeb-ce89-4ed7-8e2a-6703616552ab)


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

-cor Type of correlation method ('pearson' or 'spearman'). Default value = 'pearson'

-c The cut-off on the Correlation scores.The scores can range from 1 (high correlation) to -1 (high anti-correlation). This option overwrites the number of interactions. Default value = None.

-d The dimensions of the intermediate\hidden layer. Default value depends on the input size.

-l The dimensions of the latent space. Default value depends on the size of the hidden layer.

-e The number of epochs. Default value = 50.

-b The  batch size. Default value = 32.


```

If FAVA is useful for your research, consider citing [FAVA BiorXiv](https://doi.org/10.1101/2022.07.06.499022).

#### Other Relevant publications:
[The STRING database in 2023](https://doi.org/10.1093/nar/gkac1000).
