import logging
import argparse
import warnings
warnings.filterwarnings("ignore")

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

logger = logging.getLogger(__name__)

def load_data(data_path):
    """Loads the data and preprocesses it."""
    row_names = []
    array = []
    with open(data_path, 'r', encoding='utf-8') as infile:
        next(infile)
        for line in infile:
            line = line.split("\t")
            row_names.append(line[0])
            array.append(line[1:])

    expr = np.asarray(array, dtype=np.float32)
    expr = np.log2(1+expr[:])
    expr = expr / np.max(expr, axis=1, keepdims=True)
    expr = np.nan_to_num(expr)
    return expr, row_names


class VAE(keras.Model):
    def __init__(self, opt, x_train, x_test, batch_size, original_dim, intermediate_dim, latent_dim, epochs):
        super(VAE, self).__init__()
        inputs = keras.Input(shape=(original_dim,))
        h = layers.Dense(intermediate_dim, activation='relu')(inputs)
        
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
        x = layers.Dense(intermediate_dim, activation='relu')(latent_inputs) #relu

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


def pairs_after_cutoff(correlation, PCC_cutoff=0.7):
    correlation_df_new = correlation.loc[(correlation['Score'] >= PCC_cutoff)]
    return correlation_df_new


def main(data_path,
         save_path,
         intermediate_dim=500,
         latent_dim=50,
         epochs=100,
         batch_size=32,
         PCC_cutoff=0.7):

    x, row_names = load_data(data_path)
    original_dim = x.shape[1]
    
    opt = tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=0.001)
    x_train = x_test = np.array(x) 
    vae = VAE(opt, x_train, x_test, batch_size, original_dim, intermediate_dim, latent_dim, epochs)
    x_test_encoded = np.array(vae.encoder.predict(x_test, batch_size=batch_size))
    correlation = create_protein_pairs(x_test_encoded, row_names)
    final_pairs =  pairs_after_cutoff(correlation,PCC_cutoff=PCC_cutoff)
    final_pairs = final_pairs[final_pairs.iloc[:,0] != final_pairs.iloc[:,1]]
    final_pairs = final_pairs.sort_values(by=['Score'], ascending=False)

    logger.info("Saving the file with the interactions in the chosen directory ...")

    # Save the file
    np.savetxt(save_path, final_pairs, fmt='%s')


if __name__ == "__main__":
    def argument_parser():
        parser = argparse.ArgumentParser(
            description="Infer Functional Associations using Variational Autoencoders on -Omics data."
        )
        parser.add_argument('data_path', type=str, 
                            help='The absolute path of the data.')
        parser.add_argument('save_path', type=str,
                            help='The absolute path where the output will be saved')
        parser.add_argument('--i', dest='intermediate_dim', default=500,
                            help='Intermediate/hidden layer dimensions')
        parser.add_argument('--l', dest='latent_dim', default=100,
                            help='Latent space dimensions')
        parser.add_argument('--e', dest='epochs', type=int, default=100,
                            help='How many epochs?')
        parser.add_argument('--bs', dest='batch_size', type=int, default=32,
                            help='batch_size')
        parser.add_argument('--ct', dest='PCC_cutoff', default=0.7,
                            help='PCC_cutoff')
        args = parser.parse_args()
        return args

    args = argument_parser()
    main(data_path = args.data_path,
        save_path = args.save_path,
        intermediate_dim = args.intermediate_dim,
         latent_dim = args.latent_dim,
         epochs = args.epochs,
         batch_size = args.batch_size,
         PCC_cutoff = args.PCC_cutoff
        )
