from LeagueData.Database import Champion, ChampionStats, Item, ItemGold, ItemImage, ItemStats, ItemMaps, engine
from league_of_legends_api.Api.leaugue_api import LeagueStaticDataDragon
from sqlalchemy.orm import scoped_session, sessionmaker


session = scoped_session(sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)


class ChampionHandler:

    def save_champions(self):
        response = LeagueStaticDataDragon.get_all_champions_static()
        new_champions_counter, updated_champions_counter = 0, 0
        champions = response['data']
        for champion in champions.items():
            champion = champion[1]
            champion_old = session.query(Champion).filter_by(key=champion['key']).first()
            if champion_old is None:
                champion_obj = self._make_champion(champion)
                champion_stats_obj = self._make_champion_stats(champion)
                new_champions_counter += 1
            else:
                champion_obj = self._update_champion(champion_old, champion)
                champion_stats_old = session.query(ChampionStats).filter_by(key=champion['key']).first()
                champion_stats_obj = self._update_champion_stats(champion_stats_old, champion)
                updated_champions_counter += 1
            if champion_obj and champion_stats_obj:
                session.add(champion_obj)
                session.add(champion_stats_obj)
        session.commit()
        print(f"Current Game Version: {response['version']}\n{new_champions_counter} Champions added "
              f"\n{updated_champions_counter} Champions updated")

    def _make_champion(self, data):
        if all(key in data.keys() for key in ['key', 'name', 'title', 'blurb', 'info']):
            champ = Champion(data['key'], data['name'], data['title'], data['blurb'],
                             data['info']['attack'], data['info']['defense'], data['info']['magic'],
                             data['info']['difficulty'])
            return champ

    def _make_champion_stats(self, data):
        if all(key in data.keys() for key in ['key', 'stats']):
            stats = data['stats']
            stats['key'] = data['key']
            return ChampionStats(**stats)

    def _update_champion(self, champion_old, data):
        info = data.pop('info')
        for key, value in data.items():
            setattr(champion_old, key, value)
        for key, value in info.items():
            setattr(champion_old, key, value)
        return champion_old

    def _update_champion_stats(self, champion_stats_old, data):
        stats = data['stats']
        stats['championId'] = data['key']
        for key, value in stats.items():
            setattr(champion_stats_old, key, value)
        return champion_stats_old


class ItemHandler:

    def save_items(self):
        response = LeagueStaticDataDragon.get_all_items_static(language='en_US')
        for _id, item in response['data'].items():
            image = self._make_item_images(item.pop('image'), _id)
            gold = self._make_item_gold(item.pop('gold'), _id)
            item.pop('maps')
            #maps = self._make_item_maps(item.pop('maps'), _id)
            stats = self._make_item_stats(item.pop('stats'), _id)
            item = self._make_item(item, _id)
            if session.query(Item).filter_by(id=_id).first() is None:
                session.add(image), session.add(gold), session.add(stats), session.add(item)
        session.commit()

    def _make_item(self, data, _id):
        data['id'] = _id
        for key in ['effect', 'depth', 'consumed', 'stacks', 'consumeOnFull', 'from', 'into', 'specialRecipe', 'inStore', 'hideFromAll', 'requiredChampion', 'requiredAlly']:
            if key in data.keys():
                del data[key]
        item = Item(**data)
        return item

    def _make_item_images(self, data, _id):
        image = ItemImage(_id, data['full'], data['sprite'], data['group'], data['x'], data['y'], data['w'], data['h'])
        return image

    def _make_item_gold(self, data, _id):
        gold = ItemGold(_id, data['base'], data['purchasable'], data['total'], data['sell'])
        return gold

    def _make_item_maps(self, data, _id):
        maps = ItemMaps(_id, data['10'], data['11'], data['12'], data['22'])
        return maps

    def _make_item_stats(self, data, _id):
        data['id'] = _id
        stats = ItemStats(data)
        return stats

