import numpy as np
from tqdm import tqdm
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import Callback
from LeagueData.Database import Item
from LeagueData.DatabaseHandler import session
import operator
from Data.StaticChampionData import index_to_item_id, champion_id_to_name, index_to_item_shoes
from keras import backend as K
import random
import logging


def decode(predictions, length, shoes=False):
    """:param predictions List of List's with the predictions
       :param length how many items you want to return from your prediction list
       :param shoes if you predicting shoes or not"""
    labeled_prediction = []
    for prediction in predictions:
        mapped_items = {}
        for index, value in enumerate(prediction):
            if shoes:
                mapped_items[index_to_item_shoes.get(index)] = value
            else:
                mapped_items[index_to_item_id.get(index)] = value
        sorted_items = sorted(mapped_items.items(), key=operator.itemgetter(1), reverse=True)
        mapped_items = {}
        if length:
            sorted_items = sorted_items[:length]
        for _id, value in sorted_items:
            item = session.query(Item).filter_by(id=_id).first()
            if item:
                name = item.name
            else:
                name = _id
            mapped_items[name] = float(f'{value:0.2f}')
        labeled_prediction.append(mapped_items)
    return labeled_prediction


def configure_tf_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
    config.log_device_placement = False  # to log device placement (on which device the operation ran)
    sess = tf.Session(config=config)
    set_session(sess)


def item_to_categorical(items, size):
    """The fast one hot encoding
    :param items List of list with indexes
    :param size The size of the One Hot encoded vector. must be big enough to hold all the indexes
    :return np.array with the list of one hot encodings """
    one_hot = []
    for item in tqdm(items):
        one = np.zeros(size,)
        for x in item:
            one[x] = 1
        one_hot.append(one)
    return np.array(one_hot)


class CustomCallback(Callback):

    def __init__(self, length=7, debug=False):
        """
        A Custom Callback that decodes one random validation prediction and print or log it
        :param length: length for decoding
        :param debug: logs the print statement to tools.log
        """
        super(CustomCallback, self).__init__()
        self.debug = debug
        self.length = length
        if debug:
            logging.basicConfig(filename='tools.log', level=logging.DEBUG)
        self.var_y_true = tf.Variable(0., validate_shape=False)
        self.var_y_pred = tf.Variable(0., validate_shape=False)
        self.var_y_shoes_true = tf.Variable(0., validate_shape=False)
        self.var_y_shoes_pred = tf.Variable(0., validate_shape=False)
        self.var_x_champion = tf.Variable(0., validate_shape=False)
        self.var_x_enemies = tf.Variable(0., validate_shape=False)

    def on_epoch_end(self, epoch, logs=None):
        index = random.randint(0, len(K.eval(self.var_y_true))-1)
        champion = champion_id_to_name.get(K.eval(self.var_x_champion)[index][0])
        enemies = str([champion_id_to_name.get(enemy) for enemy in K.eval(self.var_x_enemies)[index]]).replace('[', '').replace(']', '')
        item_pred = decode([K.eval(self.var_y_pred)[index]], self.length)
        item_true = decode([K.eval(self.var_y_true)[index]], self.length)
        shoes_pred = decode([K.eval(self.var_y_shoes_pred)[index]], length=self.length, shoes=True)
        shoes_true = decode([K.eval(self.var_y_shoes_true)[index]], length=self.length, shoes=True)
        print(f'Champion: {champion}, Enemy Team: {enemies}\n'
              f'Predicted Build: {item_pred[0]}\nTrue Build: {item_true[0]}\n'
              f'Predicted Shoes: {shoes_pred[0]}\nTrue Shoes: {shoes_true[0]}')
        if self.debug:
            logging.debug(f'\nChampion: {champion}, Enemy Team: {enemies}\n'
                          f'Predicted Build: {item_pred[0]}\nTrue Build: {item_true[0]}\n'
                          f'Predicted Shoes: {shoes_pred[0]}\nTrue Shoes: {shoes_true[0]}')



