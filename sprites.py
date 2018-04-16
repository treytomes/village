
from villagelib import *

import pygame

npc_male_1 = create_npc_sprite("./assets/sprites/npc_male_1.png", (
	(32, 112, 248),	# primary - blue shirt
	(168, 80, 8),	# secondary - brown hair
	(248, 152, 96)	# tertiary - light skin
))

npc_male_2 = create_npc_sprite("./assets/sprites/npc_male_1.png", (
	(248, 112, 32),	# primary - orange shirt
	(0, 0, 0),		# secondary - black hair
	(94, 50, 18)	# tertiary - dark skin
))

npc_male_3 = create_npc_sprite("./assets/sprites/npc_male_1.png", (
	(32, 112, 32),	# primary - dark green shirt
	(168, 80, 8),	# secondary - brown hair
	(248, 152, 96)	# tertiary - light skin
))

rydia_old = create_npc_sprite("./assets/sprites/rydia_old.png", (
	(96, 112, 224),	# primary - indigo? shirt
	(144, 248, 32), # secondary - green hair
	(248, 160, 80)	# tertiary - light skin
))
