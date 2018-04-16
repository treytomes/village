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


num_speaks = 0
def on_touched(self, touched_by):
    # TODO: Need a better way of tracking state variables.
    if self.character.locals["num_speaks"] == 0:
        self.speak(f"Hello {touched_by.name}!")
        self.character.locals["num_speaks"] += 1
    else:
        # TODO: After nodding, he needs to resume facing east.
        self.nod()
        self.speak("Yes, I know what you mean.")
