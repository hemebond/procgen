#!/usr/bin/env python


"""Distutils distribution file"""


from setuptools import setup, find_packages

import game.common
import sys

if sys.argv[1] == 'install':
    print '** Do not install from setup.py. Just run the game by typing "python terrainui.py"'
    sys.exit(1)

setup(name='procgen',
      version=game.common.version,
      scripts=['terrainui.py'],
      entry_points = {
        'console_scripts' : [
            'terrainui = terrainui.terrainui',
        ]
      },      
      description='Procedural content generation system',
      author='Paul Paterson',
      author_email='ppaterson@gmail.com',
      url='URL',
      download_url=('http://perpetualpyramid.com/procgen-%s.tar.gz' % game.common.version),

      include_package_data=True,
      zip_safe=False,

      packages=[
        'serge', 'serge.blocks', 'serge.tools', 'serge.tools.template', 'game',
        'serge.blocks.concurrent', 'serge.blocks.concurrent.futures',
        'terrain', 'terrain.builders', 'terrain.renderers',
      ],
      package_dir={'':'.'},

      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Puzzle Games",
        ],
       install_requires=[
       # 'pygame', 'networkx', 'pymunk',
       ],
       long_description='''\
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


''',
         )
     
