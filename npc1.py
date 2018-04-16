# 
# script_globals = dict()
# script_locals = dict()
# exec(open("./npc1.py").read(), script_globals, script_locals)
#
# script_locals['touched']()
#

npc_sprite_path = "./assets/sprites/npc_male_1.png"
palette = (
    (32, 112, 248),  # primary - blue shirt
    (168, 80, 8),  # secondary - brown hair
    (248, 152, 96)  # tertiary - light skin
)

name = "Peter"


def on_create(self):
    self.character.face_east()


def on_collided(self, collided_by, delta_x, delta_y):
    print(f"{self.character.name} collided: ({collided_by.name}, {delta_x}, {delta_y})")


def on_touched(self, touched_by):
    self.speak(f"Hello {touched_by.name}!")
