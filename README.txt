ProcGen
-------

A procedural content generation system and user interface. The "terrain" module is a modular
system for generating procedural content such as,

- landscapes
- rogue-like dungeons
- doom-like dungeons
- caves
- mazes

The system is configured with an XML file that defines what procedural modules are used
and what their initial parameters are.

The user interface allows you to play around with the parameters and see what the impact
is of them.

The generation system can be used live in games (using the terrain module and the XML files)
or you can export the created content to TILED xml files and load them into your
game in that way.


Requires: Python 2.6+, pygame 1.9+

To run the game:

    python procgen.py
    

Thanks for playing!

What's new
----------

v0.1
    - First version of the system
v0.2
    - Added island generator to detect islands in a sea terrain
    - Added port creator to add ports to islands
    - Added loading and saving of specific parameter configurations
    - UI now supports parameter pages to better separate different settings
    - UI reports when a tiled file is written