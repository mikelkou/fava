import logging
import argparse
import warnings
warnings.filterwarnings("ignore")

import os
import time
import anndata
import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras import layers
from keras import backend as K


config = tf.compat.v1.ConfigProto()
config.intra_op_parallelism_threads = 1
config.inter_op_parallelism_threads = 1
tf.compat.v1.Session(config=config)

logger = logging.getLogger().setLevel(logging.INFO)

def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = custom_formatwarning

def argument_parser():
    parser = argparse.ArgumentParser(
        description="Infer Functional Associations using Variational Autoencoders on -Omics data."
    )
    parser.add_argument('input_file', type=str, 
                        help='The absolute path of the data.')
    parser.add_argument('output_file', type=str,
                        help='The absolute path where the output will be saved')
    parser.add_argument('-t', '--data_type', type=str, default='tsv', choices=['tsv', 'csv'], 
                        help='Type of input data.')
    parser.add_argument('-n', dest='interaction_count', type=int, default=100000,
                    help='The number of interactions in the output file.')
    parser.add_argument('-c', dest='PCC_cutoff', type=float, default=None,
                    help='The cut-off on the Pearson Correlation scores.')
    parser.add_argument('-d', dest='hidden_layer', default=None, type=int,
                        help='Intermediate/hidden layer dimensions')
    parser.add_argument('-l', dest='latent_dim', default=None, type=int,
                        help='Latent space dimensions')
    parser.add_argument('-e', dest='epochs', type=int, default=50,
                        help='How many epochs?')
    parser.add_argument('-b', dest='batch_size', type=int, default=32,
                        help='batch_size')

    args = parser.parse_args()
    return args


def load_data(input_file,data_type):
    """Loads the data and preprocesses it."""
    row_names = []
    array = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        next(infile)
        for line in infile:
            if data_type == 'tsv': 
                line = line.split("\t")
            else:
                line = line.split(",")
            row_names.append(line[0])
            array.append(line[1:])

    expr = np.asarray(array, dtype=np.float32)
    
    if np.all(expr >= 0):
        expr = np.log2(1+expr[:])
    else:
        logging.warn(" Negative values are detected, so log2 normalization is not applied.")
    
    # expr = expr / np.max(expr, axis=1, keepdims=True)
    constant = 1e-8  # small constant to avoid division by zero
    expr = (expr - np.min(expr, axis=1, keepdims=True)) / (np.max(expr, axis=1, keepdims=True) - np.min(expr, axis=1, keepdims=True) + constant)
    expr = np.nan_to_num(expr)
    return expr, row_names


class VAE(keras.Model):
    def __init__(self, opt, x_train, x_test, batch_size, original_dim, hidden_layer, latent_dim, epochs):
        super(VAE, self).__init__()
        inputs = keras.Input(shape=(original_dim,))
        h = layers.Dense(hidden_layer, activation='relu')(inputs)
        
        z_mean = layers.Dense(latent_dim)(h)
        z_log_sigma = layers.Dense(latent_dim)(h)

        # Sampling
        def sampling(args):
            z_mean, z_log_sigma = args
            epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim),
                                    mean=0., stddev=0.1)
            return z_mean + K.exp(z_log_sigma) * epsilon

        z = layers.Lambda(sampling)([z_mean, z_log_sigma])

        # Create encoder
        encoder = keras.Model(inputs, [z_mean, z_log_sigma, z], name='encoder')
        self.encoder = encoder
        # Create decoder
        latent_inputs = keras.Input(shape=(latent_dim,), name='z_sampling')
        x = layers.Dense(hidden_layer, activation='relu')(latent_inputs) #relu

        outputs = layers.Dense(original_dim, activation='sigmoid')(x)    
        decoder = keras.Model(latent_inputs, outputs, name='decoder')
        self.decoder = decoder
        
        # instantiate VAE model
        outputs = decoder(encoder(inputs)[2])
        vae = keras.Model(inputs, outputs, name='vae_mlp')
        
        # loss
        reconstruction_loss = keras.losses.mean_squared_error(inputs, outputs)
        reconstruction_loss *= original_dim        
        kl_loss = 1 + z_log_sigma - K.square(z_mean) - K.exp(z_log_sigma)
        kl_loss = K.sum(kl_loss, axis=-1)
        kl_loss *= -0.5   
        vae_loss = K.mean(0.9*(reconstruction_loss) + 0.1*(kl_loss))
        vae.add_loss(vae_loss)
        
        vae.compile(optimizer= opt, loss='mean_squared_error', metrics=['accuracy'])
        vae.fit(x_train, x_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, x_test))


def create_protein_pairs(x_test_encoded, row_names):
    # Concatenate latent spaces
    df_x_test_encoded_0 = pd.DataFrame(x_test_encoded[0,:,:])
    df_x_test_encoded_1 = pd.DataFrame(x_test_encoded[1,:,:])
    df_x_test_encoded_2 = pd.DataFrame(x_test_encoded[2,:,:])

    df_x_test_encoded_01 = pd.merge(df_x_test_encoded_0, df_x_test_encoded_1, left_index=True, right_index=True)
    df_x_test_encoded = pd.merge(df_x_test_encoded_01, df_x_test_encoded_2, left_index=True, right_index=True)

    df_x_test_encoded = np.asarray(df_x_test_encoded)
    # Correlation of the latent space
    # Pearson or Spearman
    corr_pears = np.corrcoef(df_x_test_encoded)
    corr_pears = pd.DataFrame(corr_pears, columns= row_names, index=row_names)
    correlation_df = corr_pears.stack().reset_index()

    #set column names
    correlation_df.columns = ['Protein_1','Protein_2','Score']
    return correlation_df


def pairs_after_cutoff(correlation, interaction_count=100000, PCC_cutoff=None):
    if PCC_cutoff is not None and isinstance(PCC_cutoff, (int, float)):
        logging.info(" A cut-off of " + str(PCC_cutoff) + " is applied.")
        correlation_df_new = correlation.loc[(correlation['Score'] >= PCC_cutoff)]
    else:
        correlation_df_new = correlation.head(interaction_count+1)
        logging.warn(" The number of interactions in the output file is " + str(interaction_count) + " in which both directions are included: proteinA - proteinB and proteinB - proteinA.")
    return correlation_df_new

def cook(data,
	log2_normalization = True,
	hidden_layer = None,
        latent_dim = None,
        epochs = 50,
        batch_size = 32,
        interaction_count = 100000,
        PCC_cutoff = None,
        ):
    
    if type(data)==anndata._core.anndata.AnnData:
        x = data.X.T
        row_names = data.var.index
    else:
        x = np.asarray(data, dtype=np.float32)
        row_names = data.index
    
    if np.any(x < 0):
        log2_normalization = False
        logging.warn(" Negative values are detected or log2_normalization was set to False, so log2 normalization is not applied.")
    
    if log2_normalization == True:
        x = np.log2(1+x[:])
        logging.warn(" log2 normalization is applied.")

    x = x / np.max(x, axis=1, keepdims=True)
    x = np.nan_to_num(x)
    
    original_dim = x.shape[1]
    if hidden_layer==None:
        if original_dim >= 2000:
            hidden_layer = 1000
        if original_dim > 500 and original_dim < 2000:
            hidden_layer = 500
        if original_dim <= 500:
            hidden_layer = 50

    if latent_dim==None:
        if hidden_layer >= 1000:
            latent_dim = 100
        if hidden_layer >= 500 and hidden_layer < 1000:
            latent_dim = 50
        if hidden_layer <= 500:
            latent_dim = 5

    opt = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=0.001)
    x_train = x_test = np.array(x) 
    vae = VAE(opt, x_train, x_test, batch_size, original_dim, hidden_layer, latent_dim, epochs)
    x_test_encoded = np.array(vae.encoder.predict(x_test, batch_size=batch_size))
    correlation = create_protein_pairs(x_test_encoded, row_names)
    final_pairs =  pairs_after_cutoff(correlation, interaction_count=interaction_count, PCC_cutoff=PCC_cutoff)
    final_pairs = final_pairs[final_pairs.iloc[:,0] != final_pairs.iloc[:,1]]
    final_pairs = final_pairs.sort_values(by=['Score'], ascending=False)
    return final_pairs


def main():
    args = argument_parser()

    x, row_names = load_data(args.input_file,args.data_type)
    original_dim = x.shape[1]
    
    if args.hidden_layer==None:
        if original_dim >= 2000:
            args.hidden_layer = 1000
        if original_dim > 500 and original_dim < 2000:
            args.hidden_layer = 500
        if original_dim <= 500:
            args.hidden_layer = 50

    if args.latent_dim==None:
        if args.hidden_layer >= 1000:
            args.latent_dim = 100
        if args.hidden_layer >= 500 and args.hidden_layer < 1000:
            args.latent_dim = 50
        if args.hidden_layer <= 500:
            args.latent_dim = 5

    opt = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=0.001)
    x_train = x_test = np.array(x) 
    vae = VAE(opt, x_train, x_test, args.batch_size, original_dim, args.hidden_layer, args.latent_dim, args.epochs)
    x_test_encoded = np.array(vae.encoder.predict(x_test, batch_size=args.batch_size))
    
    logging.info(" Calculating Pearson correlation scores.")

    correlation = create_protein_pairs(x_test_encoded, row_names)    
    final_pairs =  pairs_after_cutoff(correlation, interaction_count=args.interaction_count, PCC_cutoff=args.PCC_cutoff)
    logging.warn(" If it is not the desired cut-off, please check again the value assigned to the related parameter (-n or interaction_count | -c or PCC_cutoff).")

    final_pairs = final_pairs[final_pairs.iloc[:,0] != final_pairs.iloc[:,1]]
    final_pairs = final_pairs.sort_values(by=['Score'], ascending=False)
    logging.info(" Saving the file with the interactions in the chosen directory ...")

    # Save the file
    np.savetxt(args.output_file, final_pairs, fmt='%s')
    logging.info(" Congratulations! A file is waitiing for you here: " + args.output_file)


if __name__ == "__main__":
    main()
