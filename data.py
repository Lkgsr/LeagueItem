from sklearn import preprocessing
from tqdm import tqdm
import numpy as np
import pickle
from Data.StaticChampionData import champion_id_to_stats, item_id_to_index, item_shoes_to_index
import tools


def _split_items(items):
    """:param items List of indexes from item_ids
       :return tuple of np.array with item indexes and np.array with shoe indexes """
    y_shoes, y_items = [], []
    for x in items:
        shoes = item_shoes_to_index.get(int(x))
        if shoes:
            y_shoes.append(shoes)
        item = item_id_to_index.get(int(x))
        if item:
            y_items.append(item)
    return np.array(y_items), np.array(y_shoes)


def prepare_data(limit, path='Data', save=False):
    """
    Prepares the Data for the model
    :param limit: the number on the end of the file name which indicates the amount of sample per champ that are available
    :param path: the path to the folder which contains the data
    :param save: if you want to save the prepared data to pickle files for faster data loading's if you rerun the model
    :return: np.arrays of the prepared data
    """
    # Create Scaler and fit it to all the champion stats that exists
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    min_max_scaler = min_max_scaler.fit(np.array([stat for stat in champion_id_to_stats.values()]))
    x_champion, x_spells, x_stats, x_enemies, y_items, y_items_shoes = [], [], [], [], [], []
    with open(f'{path}/champion_{limit}.txt', 'r') as file_champion, open(f'{path}/enemy_{limit}.txt', 'r') as file_enemies, open(
            f'{path}/spells_{limit}.txt', 'r') as file_spells, open(f'{path}/items_{limit}.txt', 'r') as file_items:
        files = zip(file_champion.readlines(), file_spells.readlines(), file_enemies.readlines(), file_items.readlines())
        for champion, spells, enemies, items in tqdm(files):
            champ = int(champion.replace('\n', ''))
            x_champion.append(np.array(champ))
            x_enemies.append(np.array([int(x) for x in enemies.replace('\n', '').split(',')]))
            # replace the Item Ids with there indexes for a fast one hot encoding
            items, shoes = _split_items(items.replace('\n', '').split(','))
            y_items.append(np.array(items))
            y_items_shoes.append(np.array(shoes))
            x_stats.append(np.array(champion_id_to_stats.get(champ)))
            x_spells.append(np.array([x for x in spells.replace('\n', '').split(',')]))
    # Data to np array, transform labels to one hot encoding and scale the stats between 0 and 1
    x_champion, x_enemies, x_stats, x_spells = np.array(x_champion), np.array(x_enemies), np.array(x_stats), np.array(x_spells)
    y_items = tools.item_to_categorical(y_items, size=106)
    y_items_shoes = tools.item_to_categorical(y_items_shoes, size=7)
    x_stats = min_max_scaler.transform(x_stats)
    if save:
        with open(f'{path}/champion.pickle', 'wb') as file_champion, open(f'{path}/enemy.pickle', 'wb') as \
                file_enemies, open(f'{path}/spells.pickle', 'wb') as file_spells, open(f'{path}/items.pickle', 'wb') as\
                file_items, open(f'{path}/stats.pickle', 'wb') as file_stats, open(f'{path}/shoes.pickle', 'wb') as file_shoes:
            pickle.dump(x_champion, file_champion), pickle.dump(x_enemies, file_enemies)
            pickle.dump(x_spells, file_spells), pickle.dump(y_items, file_items)
            pickle.dump(x_stats, file_stats), pickle.dump(y_items_shoes, file_shoes)
    print(f'Champion Shape: {x_champion.shape}, Enemies Shape: {x_enemies.shape}, Spells Shape: {x_spells.shape}, Stats'
          f' Shape: {x_stats.shape}, Items Shape: {y_items.shape}, Item Shoes Shape {y_items_shoes.shape}')
    return x_champion, x_enemies, x_spells, x_stats, y_items, y_items_shoes


def load_pickle_files(path='Data'):
    """
    Loads the pickle files with the prepared Data
    :param path: path to the pickle files
    :return: np.arrays of the prepared data
    """
    with open(f'{path}/champion.pickle', 'rb') as file_champion, open(f'{path}/enemy.pickle', 'rb') as file_enemies, \
            open(f'{path}/spells.pickle', 'rb') as file_spells, open(f'{path}/items.pickle', 'rb') as file_items, open(
            f'{path}/stats.pickle', 'rb') as file_stats, open(f'{path}/shoes.pickle', 'rb') as file_shoes:
        x_champion, x_enemies, x_spells = pickle.load(file_champion), pickle.load(file_enemies), pickle.load(file_spells)
        x_stats, y_items, y_items_shoes = pickle.load(file_stats), pickle.load(file_items), pickle.load(file_shoes)
    print('Files Loaded')
    return x_champion, x_enemies, x_spells, x_stats, y_items, y_items_shoes
