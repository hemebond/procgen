"""The help screen for the game"""

import pygame
import glob
import os
import serge.actor
import serge.visual
import serge.events
import serge.common
import serge.blocks.utils
import serge.blocks.visualblocks
import serge.blocks.behaviours
import serge.blocks.actors

from theme import G, theme
import common 


class FileSelectScreen(serge.blocks.actors.ScreenActor):
    """The logic for the help screen"""
    
    def __init__(self, options):
        """Initialise the screen"""
        super(FileSelectScreen, self).__init__('item', 'file-select-screen')
        self.options = options
        self.do_it_callback = None

    def addedToWorld(self, world):
        """The screen was added to the world"""
        super(FileSelectScreen, self).addedToWorld(world)
        #
        L = theme.getTheme('file-select-screen').getProperty
        #
        # The menu of files
        filenames = common.getFilenames('(\w+)')
        self.file_menu = serge.blocks.utils.addActorToWorld(
            self.world,
            serge.blocks.actors.ToggledMenu(
                'menu', 'file-menu', filenames,
                serge.blocks.layout.VerticalBar(
                    'vbar', 'file-menu-bar',
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
                callback=self.fileSelected,
            ),
            layer_name='ui',
            center_position=L('file-menu-position'),
        )
        #
        # Render Filename
        self.filename = serge.blocks.utils.addActorToWorld(
            self.world,
            serge.blocks.actors.TextEntryWidget(
                'entry', 'filename', L('filename-width'), L('filename-height'),
                L('filename-colour'), L('filename-font-size'),
                background_visual=serge.blocks.visualblocks.Rectangle(
                    (L('filename-width') + 2 * L('filename-stroke-width'),
                     L('filename-height') + 2 * L('filename-stroke-width')),
                    L('filename-back-colour'),
                    L('filename-stroke-width'),
                    L('filename-stroke-colour'),
                ),
                background_layer='main',
                show_cursor=True,
                has_focus=True,
            ),
            layer_name='ui',
            center_position=L('filename-position'),
        )
        self.filename.setText('dungeon-1.png')
        self.filename.setCursorAtEnd()
        self.filename.linkEvent(serge.events.E_ACCEPT_ENTRY, self.doitClick)
        #
        # Do it button
        self.do_it = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'do-it',
            serge.blocks.visualblocks.RectangleText(
                'Do it', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('do-it-position'),
        )
        self.do_it.linkEvent(serge.events.E_LEFT_CLICK, self.doitClick)
        #
        # Cancel button
        self.cancel = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'cancel',
            serge.blocks.visualblocks.RectangleText(
                'Cancel', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('cancel-position'),
        )
        self.cancel.linkEvent(serge.events.E_LEFT_CLICK, self.cancelClick)
        self.world.linkEvent(serge.events.E_ACTIVATE_WORLD, self.onActivation)

    def onActivation(self, obj, arg):
        """World was activated"""
        self.filename.getFocus()

    def fileSelected(self, obj, arg):
        """A filename was selected"""
        self.log.debug('A filename (%s) was selected' % arg)
        self.do_it_callback(arg)
        self.engine.goBackToPreviousWorld()

    def updateActor(self, interval, world):
        """Update this actor"""
        super(FileSelectScreen, self).updateActor(interval, world)
        #
        if self.keyboard.isClicked(pygame.K_ESCAPE):
            self.cancelClick(None, None)

    def showAs(self, command, pattern, filename, callback):
        """Show the screen with a certain command and matching file pattern"""
        self.do_it.visual.text_visual.setText(command)
        self.filename.setText(filename)
        self.file_menu.setupMenu(common.getFilenames(pattern))
        self.engine.setCurrentWorld(self.world)
        self.do_it_callback = callback

    def doitClick(self, obj, arg):
        """User pressed the do it button"""
        self.log.debug('Command pressed')
        self.do_it_callback(self.filename.getText())
        self.engine.goBackToPreviousWorld()

    def cancelClick(self, obj, arg):
        """User pressed cancel"""
        self.log.debug('Cancel pressed')
        self.engine.goBackToPreviousWorld()


def main(options):
    """Create the main logic"""
    #
    # The screen actor
    common.FILE_SELECTION = s = FileSelectScreen(options)
    world = serge.engine.CurrentEngine().getWorld('file-select-screen')
    #
    # The behaviour manager
    manager = serge.blocks.behaviours.BehaviourManager('behaviours', 'behaviours')
    world.addActor(manager)
    world.addActor(s)
    #
    # Screenshots
    if options.screenshot:
        manager.assignBehaviour(None, 
            serge.blocks.behaviours.SnapshotOnKey(key=pygame.K_s, size=G('screenshot-size')
                , overwrite=False, location='screenshots'), 'screenshots')

