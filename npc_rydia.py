# 
# script_globals = dict()
# script_locals = dict()
# exec(open("./npc1.py").read(), script_globals, script_locals)
#
# script_locals['touched']()
#

npc_sprite_path = "./assets/sprites/rydia_old.png"
palette = (
    (96, 112, 224),  # primary - indigo? shirt
    (144, 248, 32),  # secondary - green hair
    (248, 160, 80)  # tertiary - light skin
)

name = "Rydia"
is_pushable = True


def on_create(self):
    self.character.face_south()


def on_touched(self, touched_by):
    self.wave()
    self.speak(f"{self.character.name}: How are you today?")

