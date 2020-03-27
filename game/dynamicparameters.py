"""Display widget for dynamic parameters"""

import re
import xml.etree.ElementTree

import serge.actor
import serge.events
import serge.blocks.utils
import serge.blocks.actors
import serge.blocks.layout
import serge.blocks.visualblocks

from theme import theme, G
import runningwindow
import terrain.common


class DynamicParameterList(serge.actor.MountableActor):
    """Displays a list of dynamic parameters"""

    def addedToWorld(self, world):
        """The widget was added to the world"""
        super(DynamicParameterList, self).addedToWorld(world)
        #
        self.world = world
        self.status = world.findActorByName('main-screen').status
        the_theme = theme.getTheme('main-screen')
        L = the_theme.getProperty
        #
        title = self.mountActor(
            serge.blocks.actors.StringText(
                'text', 'text', 'Parameters', colour=L('dynamic-title-colour'),
                font_size=L('dynamic-title-font-size'),
            ),
            L('dynamic-title-position')
        )
        title.setLayerName('ui')
        #
        # Page layout
        self.page_menu = serge.blocks.utils.addActorToWorld(
            self.world,
            serge.blocks.actors.ToggledMenu(
                'menu', 'file-menu', [''],
                serge.blocks.layout.HorizontalBar(
                    'hbar', 'page-menu-bar',
                    background_colour=L('page-menu-back-colour'),
                    background_layer='main',
                    item_width=L('page-menu-item-width'),
                    item_height=L('page-menu-item-height'),
                ),
                default=None,
                on_colour=L('page-menu-on-colour'),
                off_colour=L('page-menu-off-colour'),
                mouse_over_colour=L('page-menu-on-colour'),
                font_colour=L('page-menu-font-colour'),
                font_size=L('page-menu-font-size'),
                width=L('page-menu-width'),
                height=L('page-menu-height'),
                callback=self.pageSelected,
            ),
            layer_name='ui-over',
            center_position=L('page-menu-position'),
        )
        #
        # The layout of parameters - we make a number of pages
        self.parameter_layouts = []
        for _ in range(L('dynamic-page-count')):
            parameter_layout = self.mountActor(
                serge.blocks.layout.VerticalBar(
                    'vbar', 'vbar', item_width=L('parameter-width'), item_height=L('parameter-height')
                ),
                L('parameter-position'),
            )
            parameter_layout.setLayerName('ui-over')
            self.parameter_layouts.append(parameter_layout)
        #
        # Focus manager
        self.focus_manager = serge.blocks.utils.addActorToWorld(
            world,
            serge.blocks.actors.FocusManager(
                'entry', 'focus-manager'
            )
        )
        self.focus_manager.linkEvent(serge.events.E_GOT_FOCUS, self.getFocus)
        #
        self.setParameters([])

    def setParameters(self, parameters):
        """Set the parameters to display"""
        #
        the_theme = theme.getTheme('main-screen')
        L = the_theme.getProperty
        self.world.clearActorsWithTags(['transient-text'])
        self.parameters = []
        #
        # Create page lookup
        self.parameter_pages = {}
        page_names = []
        for _, _, _, page in parameters:
            if not page in self.parameter_pages:
                self.parameter_pages[page] = len(self.parameter_pages)
                page_names.append(page)
        self.log.debug('Found %d parameter pages' % len(self.parameter_pages))
        #
        # Update the page control
        self.page_menu.setupMenu(page_names)
        #
        for idx, (name, value, description, page) in enumerate(parameters):
            #
            # The name
            layout = self.parameter_layouts[self.parameter_pages[page]]
            text = layout.addActor(
                serge.blocks.actors.StringText(
                    'transient-text', 'transient-%s' % name, name,
                    colour=L('dynamic-text-colour'),
                    font_size=L('dynamic-text-font-size'),
                ),
            )
            text.setLayerName('ui-over')
            #
            # The entry
            item = layout.addActor(
                serge.blocks.actors.TextEntryWidget(
                    'transient-text', 'transient-entry-%s' % name,
                    L('parameter-width'), L('parameter-height'),
                    L('dynamic-entry-colour'), L('dynamic-entry-font-size'),
                    background_visual=serge.blocks.visualblocks.Rectangle(
                        (L('parameter-width'), L('parameter-height')),
                        L('dynamic-entry-stroke-colour'), L('dynamic-entry-stroke-width'),
                    ),
                    show_cursor=True,
                    background_layer='ui-back',
                    has_focus=idx == 0
                )
            )
            item.setLayerName('ui-over')
            item.setText(value)
            item.description = description
            self.parameters.append(item)
            #
            self.focus_manager.addChild(item)
        #
        # Set the first parameter page as active
        if page_names:
            self.page_menu.selectItem(page_names[0])
        #
        # Don't bother to show the page control if there is only one page
        self.page_menu.active = len(page_names) > 1

    def pageSelected(self, obj, arg):
        """A page was clicked on"""
        self.activateParameterPage(self.parameter_pages[arg])

    def activateParameterPage(self, index):
        """Activate one of the parameter pages"""
        for i, parameter_layout in enumerate(self.parameter_layouts):
            parameter_layout.active = i == index
        self.focus_manager.resetFocus()

    def updateFrom(self, generator):
        """Update the list of parameters"""
        parameters = []
        items = generator.root.findall('.//*[@editable="True"]')
        for item in items:
            self.log.debug('Dynamic item "%s"' % item.tag)
            parameters.append((
                self._makeName(item.tag),
                item.text,
                terrain.common.getStrAttr(item, 'description', ''),
                terrain.common.getStrAttr(item, 'page', 'Main')
            ))
        self.setParameters(parameters)

    def _makeName(self, text):
        """Return a name with spaces where the case changes"""
        name = text[0].upper() + text[1:]
        return ' '.join(re.findall('[A-Z][a-z]*', name))

    def updateConfiguration(self, configuration):
        """Update a configuration from the user's entry"""
        for entry, tag in zip(self.parameters, configuration.findall('.//*[@editable="True"]')):
            self.log.debug('Dynamic item "%s"' % tag.tag)
            tag.text = entry.getText()

    def getFocus(self, obj, arg):
        """Got focus for editing"""
        if obj.description:
            self.status.visible = True
            self.status.setProgress(None)
            self.status.setText(title=obj.description, status=runningwindow.S_INFO)
        else:
            self.status.visible = False

    def saveParameters(self, filename, configuration):
        """Save all the parameters to a named file"""
        self.log.debug('Saving configuration to "%s"' % filename)
        #
        # Generate text and save it to a file
        text = xml.etree.ElementTree.tostring(configuration)
        file(filename, 'w').write(text)