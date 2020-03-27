"""The main screen for the game"""

import os
import threading
import pygame
import time
import glob

import serge.actor
import serge.visual
import serge.events
import serge.common
import serge.blocks.utils
import serge.blocks.layout
import serge.blocks.visualblocks
import serge.blocks.behaviours
import serge.blocks.actors

from theme import G, theme
import common 
import runningwindow
import dynamicparameters
import terrain


class MainScreen(serge.blocks.actors.ScreenActor):
    """The logic for the main screen"""
    
    def __init__(self, options):
        """Initialise the screen"""
        super(MainScreen, self).__init__('item', 'main-screen')
        self.options = options
        self.builder_thread = None
        self.generator = None

    def addedToWorld(self, world):
        """Added to the world"""
        super(MainScreen, self).addedToWorld(world)
        #
        the_theme = theme.getTheme('main-screen')
        L = the_theme.getProperty
        serge.blocks.utils.addTextItemsToWorld(
            world, [
                ('Builders', 'builders'),
                ('Renderers', 'renderers'),
            ],
            the_theme, 'foreground',
        )
        #
        # Run all button
        self.run_all = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'run-all',
            serge.blocks.visualblocks.RectangleText(
                'Run All', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('run-all-position'),
        )
        self.run_all.linkEvent(serge.events.E_LEFT_CLICK, self.runAllClick)
        #
        # Render button
        self.render = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'render',
            serge.blocks.visualblocks.RectangleText(
                'Render', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('render-position'),
        )
        self.render.linkEvent(serge.events.E_LEFT_CLICK, self.renderClick)
        #
        # Load button
        self.load = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'load',
            serge.blocks.visualblocks.RectangleText(
                'Load', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('load-position'),
        )
        self.load.linkEvent(serge.events.E_LEFT_CLICK, self.loadClick)
        #
        # Save button
        self.save = serge.blocks.utils.addVisualActorToWorld(
            world, 'button', 'save',
            serge.blocks.visualblocks.RectangleText(
                'Save', L('buttons-colour'), L('buttons-size'),
                L('buttons-rect-colour'), L('buttons-font-size'),
                stroke_colour=L('buttons-stroke-colour'),
                stroke_width=L('buttons-stroke-width'),
            ),
            layer_name='ui',
            center_position=L('save-position'),
        )
        self.save.linkEvent(serge.events.E_LEFT_CLICK, self.saveClick)
        #
        # Main output
        self.output = serge.blocks.utils.addVisualActorToWorld(
            world, 'output', 'output',
            serge.visual.SurfaceDrawing(
                L('output-width'), L('output-height'),
            ),
            layer_name='main',
            center_position=L('output-position'),
        )
        #
        # The running indicator
        self.status = serge.blocks.utils.addActorToWorld(
            world,
            runningwindow.RunningWindow('status', 'status'),
            layer_name='ui-back',
            center_position=L('status-position')
        )
        self.status.visible = False
        self.status.linkEvent(runningwindow.E_SHOULD_STOP, self.stopRequested)
        #
        # The list of dynamic parameters
        self.dynamic = serge.blocks.utils.addActorToWorld(
            world,
            dynamicparameters.DynamicParameterList('parameters', 'parameters'),
            layer_name='ui',
            center_position=L('dynamic-parameters-position'),
        )
        #
        # Filename entry or selection
        #
        world.linkEvent(serge.events.E_ACTIVATE_WORLD, self.updateViews)
        #
        # Thread to update current status
        self.status_updater = threading.Thread(target=self.updateCurrentStatus)
        self.status_updater.setDaemon(True)
        self.status_updater.start()
        #
        # Cheating
        if self.options.cheat:
            fps = serge.blocks.utils.addActorToWorld(world,
                serge.blocks.actors.FPSDisplay(G('fps-x'), G('fps-y'), G('fps-colour'), G('fps-size')))

    def updateActor(self, interval, world):
        """Update this actor"""
        super(MainScreen, self).updateActor(interval, world)

    def updateTerrainGenerator(self, update_dynamics=False):
        """Update the generator"""
        self.generator = terrain.generator.Generator()
        self.generator.setOptions(
            os.path.join('inputfiles', common.FILENAME),
            os.path.join('outputfiles', common.FILENAME),
            'main'
        )
        if update_dynamics:
            self.dynamic.updateConfiguration(self.generator.root)
        self.generator.createBuilders()
        self.generator.createRenderers()

    def updateViews(self, obj=None, arg=None):
        """Update the views of the generator"""
        #
        # Update terrain generator
        self.updateTerrainGenerator()
        #
        # Clear up old actors
        self.world.clearActorsWithTags(['transient'])
        self.status.visible = False
        self.output.visual.clearSurface()
        #
        the_theme = theme.getTheme('main-screen')
        L = the_theme.getProperty
        #
        # Builders menu
        self.builder_names = [builder.name for builder in self.generator.getSortedBuilders()]
        self.builder_menu = serge.blocks.utils.addActorToWorld(
            self.world,
            serge.blocks.actors.ToggledMenu(
                'transient', 'builder-menu',
                self.builder_names,
                serge.blocks.layout.VerticalBar(
                    'transient', 'builder-layout',
                    # height=L('menu-height'),
                    # width=L('menu-width'),
                    background_colour=L('menu-back-colour'),
                    background_layer='background',
                    item_width=L('menu-item-width'),
                    item_height=L('menu-item-height')
                ),
                self.builder_names[0],
                on_colour=L('menu-on-colour'),
                off_colour=L('menu-off-colour'),
                mouse_over_colour=L('menu-mouse-colour'),
                callback=self.builderMenuClick,
                font_colour=L('menu-font-colour'),
                font_size=L('menu-font-size'),
                width=L('menu-width'),
                height=L('menu-height'),
            ),
            center_position=L('builder-menu-position'),
            layer_name='ui',
        )
        #
        # Renderers menu
        self.renderer_names = [renderer.name for renderer in self.generator.getSortedRenderers()]
        self.renderer_menu = serge.blocks.utils.addActorToWorld(
            self.world,
            serge.blocks.actors.ToggledMenu(
                'transient', 'renderer-menu',
                self.renderer_names,
                serge.blocks.layout.VerticalBar(
                    'transient', 'renderer-layout',
                    # height=L('menu-height'),
                    # width=L('menu-width'),
                    background_colour=L('menu-back-colour'),
                    background_layer='background',
                    item_width=L('menu-item-width'),
                    item_height=L('menu-item-height')
                ),
                self.renderer_names[0],
                on_colour=L('menu-on-colour'),
                off_colour=L('menu-off-colour'),
                mouse_over_colour=L('menu-mouse-colour'),
                callback=self.rendererMenuClick,
                font_colour=L('menu-font-colour'),
                font_size=L('menu-font-size'),
                width=L('menu-width'),
                height=L('menu-height'),
            ),
            center_position=L('renderer-menu-position'),
            layer_name='ui',
        )
        #
        # The dynamic parameters list
        self.dynamic.updateFrom(self.generator)

    def runOneClick(self, obj, arg):
        """Run one was clicked"""
        builder_name = self.builder_menu.getSelection()
        self.log.info('Run one clicked with builder "%s"' % builder_name)
        if self.builder_thread:
            self.log.info('Builder thread already running')
            return
        self.log.info('Run all clicked')
        self.builder_thread = threading.Thread(target=lambda: self._runOnce(builder_name))
        self.builder_thread.setDaemon(True)
        self.builder_thread.start()

    def _runOnce(self, name):
        """Run one builder on a thread"""
        self.runBuilderByName(name)
        self.builder_thread = None

    def runBuilderByName(self, name):
        """Run a builder"""
        self.status.visible = True
        self.status.setText(title='RUNNING: %s' % name, status=runningwindow.S_IN_PROGRESS)
        try:
            self.generator.runBuilderNamed(name)
        except Exception, err:
            self.log.error('Error running builder: %s' % err)
            self.status.setText(title='FAILED: %s' % name, status=runningwindow.S_FAILED)
            return False
        else:
            self.renderClick(None, None)
            self.status.setText(title='FINISHED: %s' % name, status=runningwindow.S_OK)
            return True

    def runAllClick(self, obj, arg):
        """Run all was clicked"""
        if self.builder_thread:
            self.log.info('Builder thread already running')
            return
        self.log.info('Run all clicked')
        self.builder_thread = threading.Thread(target=self._doRunAll)
        self.builder_thread.setDaemon(True)
        self.builder_thread.start()

    def _doRunAll(self):
        """Run all builders on a thread"""
        self.updateTerrainGenerator(update_dynamics=True)
        for idx, name in enumerate(self.builder_names):
            self.runBuilderByName(name)
        self.builder_thread = None

    def builderMenuClick(self, obj, option):
        """Clicked on the builder menu"""
        self.log.info('Clicked on option "%s" on the builder menu' % option)

    def rendererMenuClick(self, obj, option):
        """Clicked on the renderer menu"""
        self.log.info('Clicked on option "%s" on the renderer menu' % option)

    def renderClick(self, obj, world=None):
        """Run the renderer"""
        renderer_name = self.renderer_menu.getSelection()
        result = None
        try:
            result = self.generator.renderOutput(renderer_name, world)
        except Exception, err:
            self.log.error('Rendering error: %s' % err)
            return
        try:
            image = pygame.image.load('%s.png' % os.path.splitext(self.generator.renderfile)[0])
        except Exception, err:
            self.log.error('Unable to load file')
            return
        #
        # Make the image into the current output display
        out_width, out_height = self.output.width, self.output.height
        scaled_image = pygame.transform.smoothscale(image, (out_width, out_height))
        self.output.visual.setSurface(scaled_image)
        #
        # Show message if there is one
        if result:
            self.status.setText(title=result, status=runningwindow.S_OK)

    def updateCurrentStatus(self):
        """Update the status from the currently running builder if we have one"""
        while True:
            if self.generator:
                status = self.generator.getProgress()
                if status:
                    percent, world = status
                    self.log.debug('Percent is %s' % percent)
                    self.status.setProgress(percent)
                    self.renderClick(None, world)
                else:
                    self.status.setProgress(None)
            else:
                self.status.setProgress(None)
            time.sleep(1.0)

    def stopRequested(self, obj, arg):
        """Request a stop"""
        if self.generator:
            self.generator.requestStop()

    def saveClick(self, obj, arg):
        """Save the parameters"""
        self.log.debug('Save clicked')

        def saveFile(filename):
            """Callback to save the file"""
            common.SPECIFIC_NAME = filename
            common.FILENAME = '%s-%s.xml' % (common.BASE_FILENAME, filename)
            self.dynamic.updateConfiguration(self.generator.root)
            self.dynamic.saveParameters(os.path.join('inputfiles', common.FILENAME), self.generator.root)

        name = os.path.splitext(common.FILENAME)[0]
        common.FILE_SELECTION.showAs('Save', '%s\-(.+)' % common.BASE_FILENAME, common.SPECIFIC_NAME, saveFile)

    def loadClick(self, obj, arg):
        """Load the parameters"""
        self.log.debug('Load clicked')

        def loadFile(filename):
            """Callback to load the file"""
            common.SPECIFIC_NAME = filename
            common.FILENAME = '%s-%s.xml' % (common.BASE_FILENAME, filename)
            self.updateViews(None, None)

        common.FILE_SELECTION.showAs('Load', '%s\-(.+)' % common.BASE_FILENAME, common.SPECIFIC_NAME, loadFile)


def main(options):
    """Create the main logic"""
    #
    world = serge.engine.CurrentEngine().getWorld('main-screen')
    #
    # The behaviour manager
    manager = serge.blocks.behaviours.BehaviourManager('behaviours', 'behaviours')
    world.addActor(manager)
    manager.assignBehaviour(None, serge.blocks.behaviours.KeyboardBackWorld(), 'keyboard-back')
    #
    # The screen actor
    s = MainScreen(options)
    world.addActor(s)
    #
    # Screenshots
    if options.screenshot:
        manager.assignBehaviour(None, 
            serge.blocks.behaviours.SnapshotOnKey(key=pygame.K_s, size=G('screenshot-size')
                , overwrite=False, location='screenshots'), 'screenshots')

