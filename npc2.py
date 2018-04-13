# 
# script_globals = dict()
# script_locals = dict()
# exec(open("./npc1.py").read(), script_globals, script_locals)
#
# script_locals['touched']()
#

npc_sprite_path = "./assets/sprites/npc_male_1.png"
palette = (
    (248, 112, 32),  # primary - orange shirt
    (0, 0, 0),  # secondary - black hair
    (94, 50, 18)  # tertiary - dark skin
)

name = "Greg"
is_pushable = False


def on_create(self):
    self.character.face_west()


def on_collided(self, collided_by, delta_x, delta_y):
    print(f"{self.character.name}: Watch your step!")


def on_touched(self, touched_by):
    self.speak(f"{self.character.name}: How are you today?")
