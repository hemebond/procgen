"""The start screen for the game"""

import os
import pygame
import glob

import serge.sound
import serge.actor
import serge.visual
import serge.events
import serge.common
import serge.blocks.utils
import serge.blocks.visualblocks
import serge.blocks.behaviours
import serge.blocks.actors
import serge.blocks.layout

from theme import G, theme
import common 

import terrain.generator


class StartScreen(serge.blocks.actors.ScreenActor):
    """The logic for the start screen"""
    
    def __init__(self, options):
        """Initialise the screen"""
        super(StartScreen, self).__init__('item', 'main-screen')
        self.options = options

    def addedToWorld(self, world):
        """The start screen was added to the world"""
        super(StartScreen, self).addedToWorld(world)
        #
        # Logo
        the_theme = theme.getTheme('start-screen')
        L = the_theme.getProperty
        logo = serge.blocks.utils.addSpriteActorToWorld(world, 'logo', 'logo', 'icon', 'foreground', 
            center_position=L('logo-position'))
        bg = serge.blocks.utils.addSpriteActorToWorld(world, 'bg', 'bg', 'map', 'background',
            center_position=L('bg-position'))
        #
        serge.blocks.utils.addTextItemsToWorld(world, [
                    ('v' + common.version, 'version'),
                    # ('Help', 'help',  serge.blocks.utils.worldCallback('help-screen', 'click')),
                    # ('Credits', 'credits',  serge.blocks.utils.worldCallback('credits-screen', 'click')),
                    # ('Achievements', 'achievements', serge.blocks.utils.worldCallback('achievements-screen', 'click')),
                    ('Choose filename', 'filename-label'),
                ],
                the_theme, 'foreground')
        #
        # The menu of files
        filenames = common.getFilenames('(\w+)')
        self.file_menu = serge.blocks.utils.addActorToWorld(
            world,
            serge.blocks.actors.ToggledMenu(
                'menu', 'file-menu', filenames,
                serge.blocks.layout.VerticalBar(
                    'vbar', 'vbar',
                    background_colour=L('menu-back-colour'),
                    background_layer='main',
                    item_width=L('menu-item-width'),
                    item_height=L('menu-item-height'),
                ),
                default=None,
                on_colour=L('menu-on-colour'),
                off_colour=L('menu-off-colour'),
                mouse_over_colour=L('menu-on-colour'),
                font_colour=L('menu-font-colour'),
                font_size=L('menu-font-size'),
                width=L('menu-width'),
                height=L('menu-height'),
                callback=self.startMain,
            ),
            layer_name='ui',
            center_position=L('menu-position'),
        )
        #
        # Focus manager
        self.focus_manager = serge.blocks.utils.addActorToWorld(
            world,
            serge.blocks.actors.FocusManager(
                'entry', 'focus-manager'
            )
        )

    def updateActor(self, interval, world):
        """Update this actor"""
        super(StartScreen, self).updateActor(interval, world)
            
    def startMain(self, obj, arg):
        """Start the main screen"""
        #
        # Create the generator
        name = self.file_menu.getSelection()
        filename = '%s.xml' % name
        self.file_menu.clearSelection()
        common.FILENAME = filename
        common.BASE_FILENAME = name
        #
        serge.sound.Sounds.play('click')
        self.engine.setCurrentWorldByName('main-screen')


def main(options):
    """Create the main logic"""
    #
    # The behaviour manager
    world = serge.engine.CurrentEngine().getWorld('start-screen')
    manager = serge.blocks.behaviours.BehaviourManager('behaviours', 'behaviours')
    world.addActor(manager)
    manager.assignBehaviour(None, serge.blocks.behaviours.KeyboardQuit(), 'keyboard-quit')
    #
    # The screen actor
    s = StartScreen(options)
    world.addActor(s)
    #
    # Screenshots
    if options.screenshot:
        manager.assignBehaviour(None, 
            serge.blocks.behaviours.SnapshotOnKey(key=pygame.K_s, size=G('screenshot-size')
                , overwrite=False, location='screenshots'), 'screenshots')

