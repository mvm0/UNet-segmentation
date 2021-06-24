from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger, EarlyStopping
from keras.metrics import MeanIoU
from keras.models import load_model
from keras.optimizers import *
import tensorflow as tf
import model as m
import prepareData as pD


# Функция вычисления коэффициента Дайса
def dice_coefficient(y_true, y_pred):
    numerator = 2 * tf.reduce_sum(y_true * y_pred)
    denominator = tf.reduce_sum(y_true + y_pred)
    return numerator / (denominator + tf.keras.backend.epsilon())


# Функция тренировки нейронной сети
def trainNN(currentModel=None, epochs=100):
    model = m.vgg16_encoder_unet(input_shape=(512, 512, 3), weights='imagenet')
    if currentModel != None:
        dependencies = {
            'dice_coefficient': dice_coefficient
        }
        custom_objects = dependencies
        model = load_model(currentModel, custom_objects=dependencies)
    for index in range(41):
        model.layers[index].trainable = True
    model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy',
                  metrics=['accuracy', MeanIoU(num_classes=2), dice_coefficient])
    callbacks = [
        ModelCheckpoint('unet.h5', monitor='loss', verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor="loss", patience=5, factor=0.1, verbose=1),
        CSVLogger("data.csv"),
        EarlyStopping(monitor="loss", patience=10)
    ]

    model.fit(pD.train_generator(batch_size=8),
              steps_per_epoch=200,
              epochs=epochs,
              validation_data=pD.train_generator(batch_size=8),
              validation_steps=50,
              callbacks=callbacks)