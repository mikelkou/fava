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



## FAVA graph report

The undirected graph FAVA has 16.79K nodes and 511.05K edges. The graph contains 124 connected components, with the largest one containing 16.51K nodes and the smallest one containing 2 nodes. The RAM requirements for the nodes and edges data structures are 2.38MB and 1.44MB respectively.

[*The graph report has been computed with the GRAPE library*](https://github.com/AnacletoLAB/grape)

### Degree centrality

The minimum node degree is 1, the maximum node degree is 526, the mode degree is 1, the mean degree is 60.88 and the node degree median is 24.

The nodes with the highest degree centrality are 9606.ENSP00000229270 (degree 526), 9606.ENSP00000327070 (degree 522), 9606.ENSP00000334042 (degree 522), 9606.ENSP00000307940 (degree 515) and 9606.ENSP00000317780 (degree 513).

### Weights

The minimum edge weight is 0.15, the maximum edge weight is 0.999238 and the total edge weight is 253114.01640087366. The RAM requirement for the edge weights data structure is 4.09MB.

### Topological Oddities

A topological oddity is a set of nodes in the graph that  _may be derived_  by an error during the generation of the edge list of the graph and, depending on the task, could bias the results of topology-based models. In the following paragraph, we will describe the detected topological oddities.

#### Node tuples

A node tuple is a connected component composed of two nodes. We have detected 97 node tuples in the graph, involving a total of 194 nodes (1.16%) and 97 edges. The detected node tuples are:

-   Node tuple containing the nodes 9606.ENSP00000240285 and 9606.ENSP00000480439.    
-   Node tuple containing the nodes 9606.ENSP00000368592 and 9606.ENSP00000318029.    
-   Node tuple containing the nodes 9606.ENSP00000254661 and 9606.ENSP00000477017.    
-   Node tuple containing the nodes 9606.ENSP00000370297 and 9606.ENSP00000359782.    
-   Node tuple containing the nodes 9606.ENSP00000363913 and 9606.ENSP00000343171.    
-   Node tuple containing the nodes 9606.ENSP00000363040 and 9606.ENSP00000343957.    
-   Node tuple containing the nodes 9606.ENSP00000357736 and 9606.ENSP00000406674.    
-   Node tuple containing the nodes 9606.ENSP00000328625 and 9606.ENSP00000272937.    
-   Node tuple containing the nodes 9606.ENSP00000344446 and 9606.ENSP00000282096.    
-   Node tuple containing the nodes 9606.ENSP00000308714 and 9606.ENSP00000334501.    
-   Node tuple containing the nodes 9606.ENSP00000427130 and 9606.ENSP00000360436.    
-   Node tuple containing the nodes 9606.ENSP00000257894 and 9606.ENSP00000474529.    
-   Node tuple containing the nodes 9606.ENSP00000312224 and 9606.ENSP00000243578.    
-   Node tuple containing the nodes 9606.ENSP00000243938 and 9606.ENSP00000371512.    
-   Node tuple containing the nodes 9606.ENSP00000298699 and 9606.ENSP00000334289.    

And other 82 node tuples.

#### Dendritic trees

A dendritic tree is a tree-like structure starting from a root node that is part of another strongly connected component. We have detected 10 dendritic trees in the graph, involving a total of 36 nodes (0.21%) and 72 edges, with the largest one involving 5 nodes and 10 edges. The detected dendritic trees, sorted by decreasing size, are:

1.  Dendritic tree starting from the root node 9606.ENSP00000357594 (degree 5), and containing 5 nodes, with a maximal depth of 2, which are 9606.ENSP00000430950, 9606.ENSP00000327890 (degree 3), 9606.ENSP00000483430, 9606.ENSP00000229332 and 9606.ENSP00000331698.    
2.  Dendritic tree starting from the root node 9606.ENSP00000380488 (degree 4), and containing 5 nodes, with a maximal depth of 3, which are 9606.ENSP00000256857 (degree 4), 9606.ENSP00000331746, 9606.ENSP00000250351, 9606.ENSP00000358884 and 9606.ENSP00000433490.    
3.  Dendritic tree starting from the root node 9606.ENSP00000363089 (degree 22), and containing 4 nodes, with a maximal depth of 3, which are 9606.ENSP00000411584, 9606.ENSP00000355304 (degree 3), 9606.ENSP00000485010 and 9606.ENSP00000303864.    
4.  Dendritic tree starting from the root node 9606.ENSP00000434830 (degree 10), and containing 4 nodes, with a maximal depth of 2, which are 9606.ENSP00000262041, 9606.ENSP00000374377, 9606.ENSP00000321684 and 9606.ENSP00000256186.    
5.  Dendritic tree starting from the root node 9606.ENSP00000429726 (degree 362), and containing 3 nodes, with a maximal depth of 2, which are 9606.ENSP00000303096 (degree 3), 9606.ENSP00000449137 and 9606.ENSP00000269127.    
6.  Dendritic tree starting from the root node 9606.ENSP00000371333 (degree 32), and containing 3 nodes, with a maximal depth of 2, which are 9606.ENSP00000291890 (degree 3), 9606.ENSP00000314806 and 9606.ENSP00000258613.    

And other 4 dendritic trees.

#### Stars

A star is a tree with a maximal depth of one, where nodes with maximal unique degree one are connected to a central root node with a high degree. We have detected 8 stars in the graph, involving a total of 24 nodes (0.14%) and 32 edges. The detected stars are:

-   Star starting from the root node 9606.ENSP00000339577 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000294413 and 9606.ENSP00000360217.    
-   Star starting from the root node 9606.ENSP00000262186 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000326630 and 9606.ENSP00000301972.    
-   Star starting from the root node 9606.ENSP00000331734 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000416673 and 9606.ENSP00000346345.    
-   Star starting from the root node 9606.ENSP00000393099 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000398410 and 9606.ENSP00000237163.    
-   Star starting from the root node 9606.ENSP00000252939 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000263054 and 9606.ENSP00000356213.    
-   Star starting from the root node 9606.ENSP00000284509 (degree 2), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000361788 and 9606.ENSP00000258930.    

And other 2 stars.

#### Dendritic stars

A dendritic star is a dendritic tree with a maximal depth of one, where nodes with maximal unique degree one are connected to a central root node with high degree and inside a strongly connected component. We have detected 85 dendritic stars in the graph, involving a total of 190 nodes (1.13%) and 380 edges (0.04%), with the largest one involving 4 nodes and 8 edges. The detected dendritic stars, sorted by decreasing size, are:

1.  Dendritic star starting from the root node 9606.ENSP00000377140 (degree 9), and containing 4 nodes, with a maximal depth of 1, which are 9606.ENSP00000331636, 9606.ENSP00000476792, 9606.ENSP00000315743 and 9606.ENSP00000363431.    
2.  Dendritic star starting from the root node 9606.ENSP00000341021 (degree 6), and containing 4 nodes, with a maximal depth of 1, which are 9606.ENSP00000441930, 9606.ENSP00000362131, 9606.ENSP00000342836 and 9606.ENSP00000261340.    
3.  Dendritic star starting from the root node 9606.ENSP00000358644 (degree 9), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000390407, 9606.ENSP00000344865 and 9606.ENSP00000396085.    
4.  Dendritic star starting from the root node 9606.ENSP00000459043 (degree 6), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000485526, 9606.ENSP00000321874 and 9606.ENSP00000454380.    
5.  Dendritic star starting from the root node 9606.ENSP00000370997 (degree 17), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000264711, 9606.ENSP00000308461 and 9606.ENSP00000290536.    
6.  Dendritic star starting from the root node 9606.ENSP00000311957 (degree 12), and containing 3 nodes, with a maximal depth of 1, which are 9606.ENSP00000393987, 9606.ENSP00000397073 and 9606.ENSP00000337797.    

And other 79 dendritic stars.

#### Dendritic tendril stars

A dendritic tendril star is a dendritic tree with a depth greater than one, where the arms of the star are tendrils. We have detected 13 dendritic tendril stars in the graph, involving a total of 42 nodes (0.25%) and 84 edges, with the largest one involving 4 nodes and 8 edges. The detected dendritic tendril stars, sorted by decreasing size, are:

1.  Dendritic tendril star starting from the root node 9606.ENSP00000367714 (degree 12), and containing 4 nodes, with a maximal depth of 3, which are 9606.ENSP00000484411, 9606.ENSP00000337852, 9606.ENSP00000386498 and 9606.ENSP00000417207.    
2.  Dendritic tendril star starting from the root node 9606.ENSP00000353044 (degree 80), and containing 4 nodes, with a maximal depth of 2, which are 9606.ENSP00000328768, 9606.ENSP00000463752, 9606.ENSP00000443133 and 9606.ENSP00000372649.    
3.  Dendritic tendril star starting from the root node 9606.ENSP00000334441 (degree 5), and containing 4 nodes, with a maximal depth of 3, which are 9606.ENSP00000394033, 9606.ENSP00000357927, 9606.ENSP00000274382 and 9606.ENSP00000361036.    
4.  Dendritic tendril star starting from the root node 9606.ENSP00000367428 (degree 140), and containing 3 nodes, with a maximal depth of 2, which are 9606.ENSP00000452398, 9606.ENSP00000435355 and 9606.ENSP00000342609.    
5.  Dendritic tendril star starting from the root node 9606.ENSP00000343200 (degree 19), and containing 3 nodes, with a maximal depth of 2, which are 9606.ENSP00000454748, 9606.ENSP00000469445 and 9606.ENSP00000335147.    
6.  Dendritic tendril star starting from the root node 9606.ENSP00000471477 (degree 6), and containing 3 nodes, with a maximal depth of 2, which are 9606.ENSP00000309087, 9606.ENSP00000341581 and 9606.ENSP00000371824.    

And other 7 dendritic tendril stars.

#### Tendrils

A tendril is a path starting from a node of degree one, connected to a strongly connected component. We have detected 971 tendrils in the graph, involving a total of 1.07K nodes (6.37%) and 2.14K edges (0.21%), with the largest one involving 4 nodes and 8 edges. The detected tendrils, sorted by decreasing size, are:

1.  Tendril starting from the root node 9606.ENSP00000387124 (degree 3), and containing 4 nodes, with a maximal depth of 4, which are 9606.ENSP00000342008, 9606.ENSP00000475521, 9606.ENSP00000440638 and 9606.ENSP00000472409.    
2.  Tendril starting from the root node 9606.ENSP00000274361 (degree 10), and containing 4 nodes, with a maximal depth of 4, which are 9606.ENSP00000293922, 9606.ENSP00000400482, 9606.ENSP00000364107 and 9606.ENSP00000364110.    
3.  Tendril starting from the root node 9606.ENSP00000360025 (degree 5), and containing 3 nodes, with a maximal depth of 3, which are 9606.ENSP00000252799, 9606.ENSP00000422769 and 9606.ENSP00000362690.    
4.  Tendril starting from the root node 9606.ENSP00000477841 (degree 5), and containing 3 nodes, with a maximal depth of 3, which are 9606.ENSP00000395007, 9606.ENSP00000410890 and 9606.ENSP00000338572.    
5.  Tendril starting from the root node 9606.ENSP00000393847 (degree 3), and containing 3 nodes, with a maximal depth of 3, which are 9606.ENSP00000386923, 9606.ENSP00000378118 and 9606.ENSP00000371644.    
6.  Tendril starting from the root node 9606.ENSP00000417161 (degree 9), and containing 3 nodes, with a maximal depth of 3, which are 9606.ENSP00000205143, 9606.ENSP00000283228 and 9606.ENSP00000352527.    

And other 965 tendrils.

## Embedding using First-order LINE
Using a simple first-order LINE model trained and evaluated using a 70/30 split, we obtain a significant separability of existing and non existing edges. Most outstandng, we observe that traditional edge metrics (Adamic-Adar, Jaccard) are extremely predictive.

![First_order_line](https://github.com/LucaCappelletti94/fava/blob/main/line_model.png?raw=true)

**TSNE decomposition and properties distribution of the FAVA test graph using the First-order LINE node embedding:**  **(a)**  _Node degrees heatmap_. **(b)**  _Connected components_: 'Main component' in blue, 'Tuples' in orange, 'Triples' in red, and 'Minor components' in cyan. The components do not appear to form recognizable clusters (Balanced accuracy: 26.02% ± 0.74%). **(c)**  _Existent and non-existent edges_: 'Non-existent' in blue and 'Existent' in orange. The edge prediction form some clusters (Balanced accuracy: 75.31% ± 0.36%). **(d)**  _Euclidean distance heatmap_. This metric is an outstanding edge prediction feature (Balanced accuracy: 90.86% ± 0.14%). **(e)**  _Cosine similarity heatmap_. This metric is an outstanding edge prediction feature (Balanced accuracy: 90.86% ± 0.14%). Do note that the cosine similarity has been shifted from the range of [-1, 1] to the range [0, 2] to be visualized in a logarithmic heatmap. **(f)**  _Adamic-Adar heatmap_. This metric is a good edge prediction feature (Balanced accuracy: 90.00% ± 0.32%). **(g)**  _Jaccard Coefficient heatmap_. This metric is an outstanding edge prediction feature (Balanced accuracy: 91.72% ± 0.23%). **(h)**  _Preferential Attachment heatmap_. This metric may be considered an edge prediction feature (Balanced accuracy: 56.70% ± 0.52%). **(j)**  _Resource Allocation Index heatmap_. This metric is an outstanding edge prediction feature (Balanced accuracy: 90.80% ± 0.30%). **(k)**  _Edge weights heatmap_. **(i)**  _Euclidean distance distribution._ Euclidean distance values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(l)**  _Cosine similarity distribution._ Cosine similarity values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(m)**  _Adamic-Adar distribution._ Adamic-Adar values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(n)**  _Jaccard Coefficient distribution._ Jaccard Coefficient values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(o)**  _Preferential Attachment distribution._ Preferential Attachment values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(p)**  _Resource Allocation Index distribution._ Resource Allocation Index values are on the horizontal axis and edge counts are on the vertical axis on a logarithmic scale. **(q)**  _Edge weights distribution._ Edge weights on the horizontal axis and edge counts on the vertical axis on a logarithmic scale.  
In the heatmaps, **a**, **d**, **e**, **f**, **g**, **h**, **j**, and **k**, low and high values appear in red and blue hues, respectively. Intermediate values appear in either a yellow or cyan hue. The values are on a logarithmic scale The separability considerations for figures **b**, **c**, **d**, **e**, **f**, **g**, **h**, and **j** derive from evaluating a Decision Tree trained on five Monte Carlo holdouts, with a 70/30 split between training and test sets. We have sampled 10.0 thousand existing and 10.0 thousand non-existing edges. We have sampled the non-existent edges' source and destination nodes by avoiding any disconnected nodes present in the graph to avoid biases.