# village
Old-school RPG simulator.

Contains a lot of sprites and tiles from Final Fantasy 2,
with various degrees of modification by myself.

## Objects

Maps are made using the Tiled map editor.
The Tiled maps recognize the following object types:
* TRANSITION
  * Target Map: Name of the Tiled map to load when this transition is used.
  * Target X: X-coordinate in pixels to move the player to.
  * Target Y: Y-coordinate in pixels to move the player to.
* SCRIPT
  * Script Path: The path to a Python script to load into a ScriptedCharacterController object.

These objects will be created at the pixel position specified on the Tiled map.
The size of the object currently does not matter.