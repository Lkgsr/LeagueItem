from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, BigInteger, Float

Base = declarative_base()
engine = create_engine('sqlite:///LeagueData/LeagueStaticData.db')
#Base.metadata.bind = engine


class ChampionStats(Base):

    __tablename__ = "ChampionStats"

    key = Column(Integer, primary_key=True)
    hp = Column(Float)
    hp_per_level = Column(Float)
    mp = Column(Float)
    mp_per_level = Column(Float)
    move_speed = Column(Float)
    armor = Column(Float)
    armor_per_level = Column(Float)
    spell_block = Column(Float)
    spell_block_perlevel = Column(Float)
    attackrange = Column(Float)
    hp_regen = Column(Float)
    hp_regen_per_level = Column(Float)
    mp_regen = Column(Float)
    mp_regen_per_level = Column(Float)
    crit = Column(Float)
    crit_per_level = Column(Float)
    attack_damage = Column(Float)
    attack_damage_per_level = Column(Float)
    attack_speed = Column(Float)
    attack_speed_per_level = Column(Float)

    def __init__(self, key, hp, hpperlevel, mp, mpperlevel, movespeed, armor, armorperlevel, spellblock, spellblockperlevel,
                 attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel, crit, critperlevel, attackdamage,
                 attackdamageperlevel, attackspeedperlevel, attackspeed):
        self.key = key
        self.hp = hp
        self.hp_per_level = hpperlevel
        self.mp = mp
        self.mp_per_level = mpperlevel
        self.move_speed = movespeed
        self.armor = armor
        self.armor_per_level = armorperlevel
        self.spell_block = spellblock
        self.spell_block_per_level = spellblockperlevel
        self.attack_range = attackrange
        self.hp_regen = hpregen
        self.hp_regen_per_level = hpregenperlevel
        self.mp_regen = mpregen
        self.mp_regen_per_level = mpregenperlevel
        self.crit = crit
        self.crit_per_level = critperlevel
        self.attack_damage = attackdamage
        self.attack_damage_per_level = attackdamageperlevel
        self.attack_speed_per_level = attackspeedperlevel
        self.attack_speed = attackspeed


class Champion(Base):

    __tablename__ = "Champion"

    key = Column(Integer, primary_key=True)
    name = Column(String)
    tittle = Column(String)
    blurb = Column(String)
    attack = Column(Integer)
    defense = Column(Integer)
    magic = Column(Integer)
    difficulty = Column(Integer)

    def __init__(self, key, name, tittle, blurb, attack, defense, magic, difficulty):
        self.key = key
        self.name = name
        self.tittle = tittle
        self.blurb = blurb
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.difficulty = difficulty


class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    colloq = Column(String)
    plaintext = Column(String)
    tags = Column(String)

    def __init__(self, id, name, description, colloq, plaintext, tags):
        self.id = id
        self.name = str(name)
        self.description = str(description)
        self.colloq = str(colloq)
        self.plaintext = str(plaintext)
        self.tags = str(tags)


class ItemImage(Base):

    __tablename__ = 'ItemImage'

    id = Column(Integer, primary_key=True)
    full = Column(String)
    sprite = Column(String)
    group = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)

    def __init__(self, id, full, sprite, group, x, y, w, h):
        self.id = id
        self.full = full
        self.sprite = sprite
        self.group = group
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class ItemGold(Base):

    __tablename__ = 'ItemGold'

    id = Column(Integer, primary_key=True)
    base = Column(Integer)
    purchasable = Column(String)
    total = Column(Integer)
    sell = Column(Integer)

    def __init__(self, id, base, purchasable, total, sell):
        self.id = id
        self.base = base
        self.purchasable = purchasable
        self.total = total
        self.sell = sell


class ItemMaps(Base):

    __tablename__ = 'ItemMaps'

    id = Column(Integer, primary_key=True)
    twisted_treeline = Column(String) #id = 10
    summoner_s_rift = Column(String) #id = 11
    howling_abyss = Column(String) #id= 12
    unknown = Column(String) #id = 22

    def __init__(self, id, twisted_treeline, summoner_s_rift, howling_abyss, unknown):
        self.id = id
        self.twisted_treeline = twisted_treeline
        self.summoner_s_rift = summoner_s_rift
        self.howling_abyss = howling_abyss
        self.unknown = unknown


class ItemStats(Base):

    __tablename__ = 'ItemStats'

    id = Column(Integer, primary_key=True)
    FlatHPPoolMod = Column(Integer, default=0)
    rFlatHPModPerLevel = Column(Integer, default=0)
    FlatMPPoolMod = Column(Integer, default=0)
    rFlatMPModPerLevel = Column(Integer, default=0)
    PercentHPPoolMod = Column(Integer, default=0)
    PercentMPPoolMod = Column(Integer, default=0)
    FlatHPRegenMod = Column(Integer, default=0)
    rFlatHPRegenModPerLevel = Column(Integer, default=0)
    PercentHPRegenMod = Column(Integer, default=0)
    FlatMPRegenMod = Column(Integer, default=0)
    rFlatMPRegenModPerLevel = Column(Integer, default=0)
    PercentMPRegenMod = Column(Integer, default=0)
    FlatArmorMod = Column(Integer, default=0)
    rFlatArmorModPerLevel = Column(Integer, default=0)
    PercentArmorMod = Column(Integer, default=0)
    rFlatArmorPenetrationMod = Column(Integer, default=0)
    rFlatArmorPenetrationModPerLevel = Column(Integer, default=0)
    rPercentArmorPenetrationMod = Column(Integer, default=0)
    rPercentArmorPenetrationModPerLevel = Column(Integer, default=0)
    FlatPhysicalDamageMod = Column(Integer, default=0)
    rFlatPhysicalDamageModPerLevel = Column(Integer, default=0)
    PercentPhysicalDamageMod = Column(Integer, default=0)
    FlatMagicDamageMod = Column(Integer, default=0)
    rFlatMagicDamageModPerLevel = Column(Integer, default=0)
    PercentMagicDamageMod = Column(Integer, default=0)
    FlatMovementSpeedMod = Column(Integer, default=0)
    rFlatMovementSpeedModPerLevel = Column(Integer, default=0)
    PercentMovementSpeedMod = Column(Integer, default=0)
    rPercentMovementSpeedModPerLevel = Column(Integer, default=0)
    FlatAttackSpeedMod = Column(Integer, default=0)
    PercentAttackSpeedMod = Column(Integer, default=0)
    rPercentAttackSpeedModPerLevel = Column(Integer, default=0)
    rFlatDodgeMod = Column(Integer, default=0)
    rFlatDodgeModPerLevel = Column(Integer, default=0)
    PercentDodgeMod = Column(Integer, default=0)
    FlatCritChanceMod = Column(Integer, default=0)
    rFlatCritChanceModPerLevel = Column(Integer, default=0)
    PercentCritChanceMod = Column(Integer, default=0)
    FlatCritDamageMod = Column(Integer, default=0)
    rFlatCritDamageModPerLevel = Column(Integer, default=0)
    PercentCritDamageMod = Column(Integer, default=0)
    FlatBlockMod = Column(Integer, default=0)
    PercentBlockMod = Column(Integer, default=0)
    FlatSpellBlockMod = Column(Integer, default=0)
    rFlatSpellBlockModPerLevel = Column(Integer, default=0)
    PercentSpellBlockMod = Column(Integer, default=0)
    FlatEXPBonus = Column(Integer, default=0)
    PercentEXPBonus = Column(Integer, default=0)
    rPercentCooldownMod = Column(Integer, default=0)
    rPercentCooldownModPerLevel = Column(Integer, default=0)
    rFlatTimeDeadMod = Column(Integer, default=0)
    rFlatTimeDeadModPerLevel = Column(Integer, default=0)
    rPercentTimeDeadMod = Column(Integer, default=0)
    rPercentTimeDeadModPerLevel = Column(Integer, default=0)
    rFlatGoldPer10Mod = Column(Integer, default=0)
    rFlatMagicPenetrationMod = Column(Integer, default=0)
    rFlatMagicPenetrationModPerLevel = Column(Integer, default=0)
    rPercentMagicPenetrationMod = Column(Integer, default=0)
    rPercentMagicPenetrationModPerLevel = Column(Integer, default=0)
    FlatEnergyRegenMod = Column(Integer, default=0)
    rFlatEnergyRegenModPerLevel = Column(Integer, default=0)
    FlatEnergyPoolMod = Column(Integer, default=0)
    rFlatEnergyModPerLevel = Column(Integer, default=0)
    PercentLifeStealMod = Column(Integer, default=0)
    PercentSpellVampMod = Column(Integer, default=0)

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


Base.metadata.create_all(engine)
