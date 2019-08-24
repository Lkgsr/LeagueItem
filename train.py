from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.layers import Input, BatchNormalization, Flatten, Embedding, Dense, concatenate, Activation, Dropout
from keras. models import Model
import time
from data import load_pickle_files, prepare_data
import numpy as np
from tools import configure_tf_session, CustomCallback
import tensorflow as tf


def prepare_model():

    stats = Input(shape=(20,), name='Champion-Stats')
    stats_norm = BatchNormalization()(stats)

    champion = Input(shape=(1, ), name='Champion-Ids')
    champions_embedding = Embedding(556, 145, name='Champion-Ids-Embedding', input_length=1)(champion)
    champions_vec = Flatten(name='Flatten-Champion-Embeddings')(champions_embedding)
    champion_norm = BatchNormalization()(champions_vec)

    spells = Input(shape=(2,), name='Spells')
    spells_embedding = Embedding(800, 16, name='Spells-Embedding', input_length=2)(spells)
    spells_vec = Flatten(name='Flatten-Spells-Embeddings')(spells_embedding)
    spell_norm = BatchNormalization()(spells_vec)

    enemy = Input(shape=(5,), name='Enemy-Champion-Ids')
    enemy_embedding = Embedding(556*5, 145*5, name='Enemy-Champion-Ids-Embedding', input_length=5)(enemy)
    enemy_vec = Flatten(name='Flatten-Enemy-Champions-Embeddings')(enemy_embedding)
    enemy_norm = BatchNormalization()(enemy_vec)

    champ_stats = concatenate([champion_norm, enemy_norm, spell_norm, stats_norm])

    dense_item = Dense(1024)(champ_stats)
    dense_item = BatchNormalization()(dense_item)
    dense_item = Activation('relu')(dense_item)
    dense_item = Dropout(0.8)(dense_item)
    dense_item = Dense(512)(dense_item)
    dense_item = BatchNormalization()(dense_item)
    dense_item = Activation('relu')(dense_item)
    dense_item = Dropout(0.8)(dense_item)
    dense_item = Dense(256)(dense_item)
    dense_item = BatchNormalization()(dense_item)
    dense_item = Activation('relu')(dense_item)
    dense_item = Dropout(0.8)(dense_item)
    dense_item = Dense(256)(dense_item)
    dense_item = BatchNormalization()(dense_item)
    dense_item = Activation('relu')(dense_item)
    dense_item = Dropout(0.8)(dense_item)

    output_all = Dense(106, activation='sigmoid', name='ItemsOutput')(dense_item)
    output_shoes = Dense(7, activation='sigmoid', name='ShoesOutput')(dense_item)
    model = Model(inputs=[champion, enemy, spells, stats], outputs=[output_all, output_shoes])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def train(name, batch_size, epochs, limit, load_from_pickle_file=False):
    """
    Run this to train the model
    :param name: Nome of the model and log files
    :param batch_size: the size of the batches which get feed into the network
    :param epochs: how often the network goes over the trainings data
    :param limit: the number on the end of trainings data the files.    which indicates the amount of sample per champ that are available
    :param load_from_pickle_file: if you all ready saved the trainings data to pickle files or you run the training for a second time
    :return: Nothing
    """
    configure_tf_session()
    if load_from_pickle_file:
        x_new_champion, x_new_enemies, x_spells, x_new_stats, y_new_items, y_new_items_shoes = load_pickle_files()
    else:
        x_new_champion, x_new_enemies, x_spells, x_new_stats, y_new_items, y_new_items_shoes = prepare_data(save=True, limit=limit)
    model = prepare_model()
    testing = CustomCallback(debug=True)
    fetches = [tf.assign(testing.var_y_true, model.targets[0], validate_shape=False),
               tf.assign(testing.var_y_pred, model.outputs[0], validate_shape=False),
               tf.assign(testing.var_y_shoes_true, model.targets[1], validate_shape=False),
               tf.assign(testing.var_y_shoes_pred, model.outputs[1], validate_shape=False),
               tf.assign(testing.var_x_champion, model.inputs[0], validate_shape=False),
               tf.assign(testing.var_x_enemies, model.inputs[1], validate_shape=False)]
    model._function_kwargs = {'fetches': fetches}
    p = np.random.permutation(len(x_new_champion))
    x_new_champion, y_new_items, x_spells, x_new_enemies, y_new_items_shoes = x_new_champion[p], y_new_items[p], x_spells[p], x_new_enemies[p], y_new_items_shoes[p]
    tensor_board = TensorBoard(log_dir=f'logs/{name}_{batch_size}_{int(time.time())}')
    checkpoint = ModelCheckpoint(f'models/{name}_{batch_size}_{int(time.time())}', monitor='val_ItemsOutput_acc', verbose=3, save_best_only=True, mode='max')
    model.fit([x_new_champion, x_new_enemies, x_spells, x_new_stats], [y_new_items, y_new_items_shoes], validation_split=0.2, epochs=epochs,
              batch_size=batch_size, callbacks=[tensor_board, checkpoint, testing], shuffle=True)
