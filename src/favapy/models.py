"""Variational Autoencoder (VAE) model for FAVA."""

from __future__ import annotations

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import backend as K


class VAE(tf.keras.Model):
    """
    Variational Autoencoder model class.

    Parameters
    ----------
    opt : tf.keras.optimizers.Optimizer
        Optimizer for the model.
    x_train : np.ndarray
        Training data.
    x_test : np.ndarray
        Test data.
    batch_size : int
        Batch size for training.
    original_dim : int
        Dimension of the input data.
    hidden_layer : int
        Number of units in the hidden layer.
    latent_dim : int
        Dimension of the latent space.
    epochs : int
        Number of training epochs.
    """

    def __init__(
        self,
        opt: tf.keras.optimizers.Optimizer,
        x_train: np.ndarray,
        x_test: np.ndarray,
        batch_size: int,
        original_dim: int,
        hidden_layer: int,
        latent_dim: int,
        epochs: int,
    ) -> None:
        super(VAE, self).__init__()

        # Store parameters for use in train_step
        self.original_dim = original_dim
        self.latent_dim = latent_dim

        # Build encoder
        inputs = tf.keras.Input(shape=(original_dim,))
        h = layers.Dense(hidden_layer, activation="relu")(inputs)

        z_mean = layers.Dense(latent_dim)(h)
        z_log_sigma = layers.Dense(latent_dim)(h)

        # Sampling
        def sampling(args):
            z_mean, z_log_sigma = args
            epsilon = K.random_normal(
                shape=(K.shape(z_mean)[0], latent_dim), mean=0.0, stddev=0.1
            )
            return z_mean + K.exp(z_log_sigma) * epsilon

        z = layers.Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_sigma])

        # Create encoder
        self.encoder = tf.keras.Model(inputs, [z_mean, z_log_sigma, z], name="encoder")

        # Create decoder
        latent_inputs = tf.keras.Input(shape=(latent_dim,), name="z_sampling")
        x = layers.Dense(hidden_layer, activation="relu")(latent_inputs)
        outputs = layers.Dense(original_dim, activation="sigmoid")(x)
        self.decoder = tf.keras.Model(latent_inputs, outputs, name="decoder")

        # Compile model (loss is computed in train_step)
        self.compile(optimizer=opt, metrics=["mse"])

        # Train the model
        self.fit(
            x_train,
            x_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_test, x_test),
        )

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        """Forward pass through the VAE."""
        z_mean, z_log_sigma, z = self.encoder(inputs)
        reconstructed = self.decoder(z)
        return reconstructed

    def _compute_loss(self, x: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        """Compute VAE loss (reconstruction + KL divergence)."""
        z_mean, z_log_sigma, z = self.encoder(x)
        reconstructed = self.decoder(z)

        reconstruction_loss = K.mean(K.square(x - reconstructed), axis=-1)
        reconstruction_loss *= self.original_dim

        kl_loss = 1 + z_log_sigma - K.square(z_mean) - K.exp(z_log_sigma)
        kl_loss = K.sum(kl_loss, axis=-1) * -0.5

        total_loss = K.mean((0.9 * reconstruction_loss) + (0.1 * kl_loss))
        return total_loss, reconstructed

    def train_step(self, data: tuple) -> dict[str, tf.Tensor]:
        """Custom training step with VAE loss."""
        x, _ = data

        with tf.GradientTape() as tape:
            total_loss, reconstructed = self._compute_loss(x)

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.compiled_metrics.update_state(x, reconstructed)

        return {"loss": total_loss, **{m.name: m.result() for m in self.metrics}}

    def test_step(self, data: tuple) -> dict[str, tf.Tensor]:
        """Custom validation step with VAE loss."""
        x, _ = data
        total_loss, reconstructed = self._compute_loss(x)
        self.compiled_metrics.update_state(x, reconstructed)

        return {"loss": total_loss, **{m.name: m.result() for m in self.metrics}}
