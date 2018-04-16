# 
# script_globals = dict()
# script_locals = dict()
# exec(open("./npc1.py").read(), script_globals, script_locals)
#
# script_locals['touched']()
#

npc_sprite_path = "./assets/sprites/npc_male_1.png"
palette = (
    (248, 32, 32),  # primary - blue shirt
    (0, 0, 0),  # secondary - black hair
    (248, 152, 96)  # tertiary - light skin
)

name = "Innkeeper"
is_pushable = False


def on_create(self):
    self.character.face_south()


def on_touched(self, touched_by):
    self.speak(f"{self.character.name}: Welcome to the inn!")
