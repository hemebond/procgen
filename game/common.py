"""Common elements"""

import os
import re
import glob

import serge.engine
import serge.common
import serge.blocks.scores

log = serge.common.getLogger('Game')
from theme import G

version = '0.2'


# The generator filename in use by the application
FILENAME = None

# Base filename for parameter files
BASE_FILENAME = None
SPECIFIC_NAME = ''

# The file select screen
FILE_SELECTION = None

#
# Events
#
# Put events here with names E_MY_EVENT
# and they will be registered automatically
#
# E_GAME_STARTED = 'game-started'


def getFilenames(pattern):
    """Return the filenames to show"""
    files = set()
    for filename in glob.glob(os.path.join('inputfiles', '*.xml')):
        name = os.path.splitext(os.path.split(filename)[1])[0]
        match = re.match(pattern, name)
        if match:
            files.add(match.groups()[0])
    #
    return sorted(list(files))
