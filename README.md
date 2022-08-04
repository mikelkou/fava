# FAVA: Functional Associations using Variational Autoencoders
![Fava](https://user-images.githubusercontent.com/81096946/177743627-2e6a7447-3fc1-48a8-a6bb-003a3ace223a.png)

Protein networks are commonly used for understanding the interplay between proteins in the cell as well as for visualizing omics data. Unfortunately, most existing high-quality networks are heavily biased by data availability, in the sense that well-studied proteins have many more interactions than understudied proteins. To create networks that can help elucidate functions for the latter, we must start from data that are not affected by this literature bias, in other words, from omics data such as single cell RNA-seq (scRNA-seq) and proteomics. While networks can be inferred from such data through simple co-expression analysis, this approach does not work well due to high sparseness (many transcripts/proteins are not consistently observed in each cell/sample) and redundancy (many similar cells/samples are analyzed) of such data. We have therefore developed FAVA, Functional Associations using Variational Autoencoders, which deals with both issues by compressing these high-dimensional data into a dense, low-dimensional latent space. We demonstrate that calculating correlations in this latent space results in much improved networks compared to the original representation for large-scale scRNA-seq and proteomics data from the Human Protein Atlas, and from PRIDE, respectively. We show that these networks, which given the nature of the input data should be free of literature bias, indeed have much better coverage of understudied proteins than existing networks.


## Data availability
#### Human Protein Atlas
https://www.proteinatlas.org/humanproteome/single+cell+type 

#### PRIDE - Proteomics Identification Database - EMBL-EBI
https://www.ebi.ac.uk/pride/ 

#### Combined network
The Network: https://doi.org/10.5281/zenodo.6803472 


## Installation:
`pip install favapy`

## Command line interface
Run favapy from the command line as follows:

`favapy -data_path <path-to-data-file> -save_path <path-to-save-output>`


### Optional parameters:

`--i` The dimensions of the intermediate\hidden layer. Default value = 500.

`--l` The dimensions of the latent space. Default value = 100.

`--e` The number of epochs. Default value = 100.

`--bs` The  batch size. Default value = 32.

`--ct` The cut-off on the Pearson Correlation scores. Default value = 0.7.




