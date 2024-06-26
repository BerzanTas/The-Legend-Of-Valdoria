WIDTH = 1280
HEIGTH = 720

FPS = 60

TILESIZE = 64

PLAYER_SPEED = 3

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

FIREBALL_DELAY = 1


ANIMATION_SPEED = 0.2
ATTACK_ANIMATION_SPEED = 0.3
FIREBALL_SPEED = 4
FIREBALL_RADIUS = 200


# UI

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
MANA_BAR_WIDTH = 140
SPELL_BOX_SIZE = 70
STAT_BOX_SIZE = 50
UI_FONT = 'img/font/Lora.ttf'
UI_FONT_SIZE = 22
SPELL_FONT = 'img/font/Lora-Bold.ttf'

# kolory
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
COOLDOWN_COLOR = 'red'

HEALTH_COLOR = 'red'
MANA_COLOR = 'blue'
EXP_COLOR = '#ad9115'
UI_BORDER_COLOR_ACTIVE = 'gold'

# informacje o zaklęciach

spell_data = {
    'fireball': {'cooldown': 1000, 'damage': 10, 'mana': 5, 'img': 'img/spells/fireballicon.png'},
    'laserbeam': {'cooldown': 12000, 'damage': 80, 'mana': 20,'img': 'img/spells/laserbeamicon.png'},
    'heal': {'cooldown': 20000, 'heal_percent': 0.2, 'mana': 30,'img': 'img/spells/healicon.png'}
}

##SLIME
slime_width = 32
slime_height = 32
slime_speed = 400
slime_animation = 0.1

##SKELETON 
skeleton_width = 48
skeleton_height = 48
skeleton_speed = 400
skeleton_animation = 0.2

WORLD_MAP = [
    ['g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 'tr1', 'g', 'g', 'kr', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'tr1', 'g', 'g', 'dc', 'g', 'g', 'g', 'tr1', 'g', 'g'],
    ['g', 'tr1', 'g', 'g', 'g', 'g', 'kr', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'tr2', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g'],
    ['g', 'tr2', 'g', 'kr', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 's', 'tr1', 'g', 'g', 'dc', 'g', 'w', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
    ['g', 'tb', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'x', 'sk', 'g', 'tr1', 'g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'dc', 'g', 'tr1', 'g', 'g', 'kr', 'g'],
    ['g', 'p', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'w', 'g', 'tr1', 'g', 'tr1', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'x', 'g', 'g', 'g', 'g'],
    ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'kr', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'dc', 'sk', 'g', 'g', 'g', 'g', 'g', 'g'],
    ['g', 'tr1', 'g', 'g', 'tr1', 'g', 'g', 'x', 'g', 'g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 'g', 'tr2', 'g', 'tr1', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g'],
    ['g', 'g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 's', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'tr2', 'g', 'g', 'g'],
    ['g', 'x', 'tr1', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'tr1', 'g'],
    ['s', 'g', 'kr', 'g', 'g', 'g', 'g', 's', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'hd', 'dc', 'g', 'g', 'g'],
    ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'hd', 'g', 'g', 'tr1', 'g', 'g', 'sk', 'g', 'dc', 'g'],
    ['g', 'g', 'g', 'tr1', 'g', 's', 'g', 'g', 'g', 'g', 'g', 's', 'g', 'g', 'g', 'dc', 'g', 'tr2', 'g', 'g', 'g', 'g', 'g', 'hd', 'dc', 'g', 'g', 'g', 'g', 'dc'],
    ['tr1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
    ['g', 'tr1', 'g', 'g', 'dc', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 's', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g'],
    ['g', 'tr2', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'dc', 'g', 'sk', 'g', 'g', 'bld', 'g', 'dc'],
    ['g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'x', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'borne', 'g', 'g'],
    ['g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'tr2', 'g', 'g', 'g', 'tr1'],
    ['g', 'g', 'g', 'g', 'dc', 'g', 's', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'tr1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g'],
    ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'dc', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']
]



MAP_WIDTH = len(WORLD_MAP[0]) * TILESIZE
MAP_HEIGHT = len(WORLD_MAP) * TILESIZE


nightborne_width = 80
nightborne_height = 80
nightborne_speed = 0.2