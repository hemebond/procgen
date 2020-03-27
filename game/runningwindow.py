"""A window to show what is running"""

import logging

import serge.actor
import serge.events
import serge.blocks.utils
import serge.blocks.actors
import serge.blocks.visualblocks

from theme import G, theme
import terrain.common
import terrain.loggable


# Status for window
S_OK = (0, 150, 0)
S_FAILED = (150, 0, 0)
S_IN_PROGRESS = (0, 0, 0)
S_INFO = (0, 0, 255, 50)

E_SHOULD_STOP = 'should-stop'


class RunningWindow(serge.actor.MountableActor):
    """Shows running status"""

    def addedToWorld(self, world):
        """Added the actor to the world"""
        super(RunningWindow, self).addedToWorld(world)
        #
        the_theme = theme.getTheme('main-screen')
        L = the_theme.getProperty
        #
        # Hide button
        self.hide = serge.actor.Actor('button', 'hide')
        self.hide.visual = serge.blocks.visualblocks.RectangleText(
            'X', L('hide-button-colour'), L('hide-button-size'),
            L('hide-button-rect-colour'), L('hide-button-font-size'),
            stroke_colour=L('hide-button-stroke-colour'),
            stroke_width=L('hide-button-stroke-width'),
        )
        self.hide.setLayerName('ui-front')
        self.mountActor(self.hide, L('status-hide-position'))
        self.hide.linkEvent(serge.events.E_LEFT_CLICK, self.hideClick)
        #
        # Main title
        self.title = serge.actor.Actor('text', 'title')
        self.title.visual = serge.blocks.visualblocks.RectangleText(
            'Title of running window', L('status-title-colour'), L('status-title-size'),
            L('status-title-rect-colour'), L('status-title-font-size'),
            stroke_colour=L('status-title-stroke-colour'),
            stroke_width=L('status-title-stroke-width'),
        )
        self.title.setLayerName('ui-front')
        self.mountActor(self.title, L('status-title-position'))
        #
        # Progress indicator
        self.progress_indicator = serge.actor.Actor('progress', 'progress')
        self.progress_indicator.visual = serge.blocks.visualblocks.ProgressBar(
            L('progress-size'),
            L('progress-value-ranges')
        )
        self.progress_indicator.setLayerName('ui-progress')
        self.progress_indicator.visual.value = 0
        self.mountActor(self.progress_indicator, L('progress-position'))

    def hideClick(self, obj, arg):
        """Hide this window"""
        self.visible = False
        self.processEvent((E_SHOULD_STOP, self))

    def setText(self, title=None, status=None):
        """Set the text for the window"""
        if title is not None:
            self.title.visual.text_visual.setText(title)
        if status is not None:
            self.title.visual.rect_visual.colour = status

    def setProgress(self, value):
        """Set the progress percent"""
        if value is not None:
            self.progress_indicator.visual.value = value
            self.progress_indicator.visible = True and self.visible
        else:
            self.progress_indicator.visible = False