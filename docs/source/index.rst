Welcome to favapy’s documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Introduction
   -------------

Protein networks are commonly used for understanding the interplay between proteins in the cell as well as for visualizing omics data. Unfortunately, most existing high-quality networks are heavily biased by data availability, in the sense that well-studied proteins have many more interactions than understudied proteins. To create networks that can help elucidate functions for the latter, we must start from data that are not affected by this literature bias, in other words, from omics data such as single cell RNA-seq (scRNA-seq) and proteomics. While networks can be inferred from such data through simple co-expression analysis, this approach does not work well due to high sparseness (many transcripts/proteins are not consistently observed in each cell/sample) and redundancy (many similar cells/samples are analyzed) of such data. We have therefore developed FAVA, Functional Associations using Variational Autoencoders, which deals with both issues by compressing these high-dimensional data into a dense, low-dimensional latent space. Calculating correlations in this latent space results in much improved networks compared to the original representation for large-scale scRNA-seq and proteomics data from the Human Protein Atlas, and from PRIDE, respectively. Additionally, these networks, which given the nature of the input data should be free of literature bias, have much better coverage of understudied proteins than existing networks.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Installation
   -------------

You can install FAVA using pip:

.. code-block:: bash

   pip install favapy

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Using FAVA as a Python library
   ------------------------------

You can use FAVA as a Python library. Refer to the following Jupyter notebook for instructions on how to use FAVA in a notebook:

- `How_to_use_favapy_in_a_notebook.ipynb <https://github.com/mikelkou/fava/blob/main/How_to_use_favapy_in_a_notebook.ipynb>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Command Line Interface
   ----------------------

Run FAVA from the command line as follows:

.. code-block:: bash

   favapy <path-to-data-file> <path-to-save-output>

Optional parameters:

``-t`` Type of input data ('tsv' or 'csv'). Default value = 'tsv'.

``-n`` The number of interactions in the output file (with both directions, proteinA-proteinB and proteinB-proteinA). Default value = 100000.

``-c`` The cut-off on the Pearson Correlation scores. The scores can range from 1 (high correlation) to -1 (high anti-correlation). This option overwrites the number of interactions. Default value = None.

``-d`` The dimensions of the intermediate/hidden layer. Default value depends on the input size.

``-l`` The dimensions of the latent space. Default value depends on the size of the hidden layer.

``-e`` The number of epochs. Default value = 50.

``-b`` The batch size. Default value = 32.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Tutorials
   ---------
   
.. toctree::
   :maxdepth: 2

   ../../How_to_use_favapy_in_a_notebook.ipynb

