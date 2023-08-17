Command Line Interface
----------------------

Run FAVA from the command line as follows:

.. code-block:: bash

   favapy <path-to-data-file> <path-to-save-output>

Optional parameters:

``-t`` Type of input data ('tsv' or 'csv'). Default value = 'tsv'.

``-n`` The number of interactions in the output file (with both directions, proteinA-proteinB and proteinB-proteinA). Default value = 100000.

``-c`` The cut-off on the Pearson Correlation scores. The scores can range from 1 (high correlation) to -1 (high anti-correlation). This option overwrites the number>

``-d`` The dimensions of the intermediate/hidden layer. Default value depends on the input size.

``-l`` The dimensions of the latent space. Default value depends on the size of the hidden layer.

``-e`` The number of epochs. Default value = 50.

``-b`` The batch size. Default value = 32.
