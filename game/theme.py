"""Our main visual theme"""

import serge.blocks.themes

W, H = 1000, 600
B = 100

theme = serge.blocks.themes.Manager()
theme.load({
    'main': ('', {
    
    # Main properties
    'screen-height': H,
    'screen-width': W,
    'screen-title': 'Terrain Generator',
    'screen-icon-filename': 'icon.png',
    'screenshot-size': (0, 0, W, H),
    
    # Mute button
    'mute-button-alpha': 0.4,
    'mute-button-position': (30, 30),
    'pre-stop-pause': 0.5,
    
    # FPS display
    'fps-x': 50,
    'fps-y': H-30,
    'fps-colour': (255, 255, 0),
    'fps-size': 12,
    
    }),

    'main-screen': ('sub-screen', {
        # Builders text
        'builders-position': (B, 50),
        'builders-colour': (255, 255, 255),
        'builders-font-size': 24,
        # Renderers text
        'renderers-position': (B, 370),
        'renderers-colour': (255, 255, 255),
        'renderers-font-size': 24,
        # General menu properties
        'menu-width': 150,
        'menu-height': 30,
        'menu-back-colour': (0, 0, 0, 100),
        'menu-item-width': 150,
        'menu-item-height': 30,
        'menu-on-colour': (0, 255, 0, 100),
        'menu-mouse-colour': (0, 150, 0, 100),
        'menu-off-colour': (0, 0, 0, 100),
        'menu-font-colour': (255, 255, 0),
        'menu-font-size': 16,
        # Builder menu
        'builder-menu-position': (B, 80),
        # Renderer menu
        'renderer-menu-position': (B, 400),
        # Hide button
        'hide-button-colour': (255, 255, 255),
        'hide-button-size': (40, 30),
        'hide-button-rect-colour': (255, 0, 0, 100),
        'hide-button-font-size': 18,
        'hide-button-stroke-colour': (255, 255, 255),
        'hide-button-stroke-width': 3,
        # Button positions
        'run-one-position': (60, 250),
        'run-all-position': (B, 250),
        'render-position': (B, 550),
        'load-position': (860, 30),
        'save-position': (940, 30),
        # Output
        'output-width': 580,
        'output-height': 580,
        'output-position': (500, 300),
        # Running Status
        'status-position': (W/2, 580),
        'status-hide-position': (218, 0),
        # Status title
        'status-title-colour': (255, 255, 0),
        'status-title-size': (400, 30),
        'status-title-rect-colour': (0, 0, 0, 255),
        'status-title-font-size': 18,
        'status-title-stroke-colour': (255, 255, 255),
        'status-title-stroke-width': 3,
        'status-title-position': (0, 0),
        # Progress bar
        'progress-size': (400, 30),
        'progress-value-ranges': (
            (0, 100, (0, 255, 0)),
        ),
        'progress-position': (0, -5),
        # Status body
        'status-body-colour': (0, 255, 255),
        'status-body-font-size': 14,
        'status-body-font': 'CLEAR',
        'status-body-position': (0, 0),
        # Dynamic parameters
        'dynamic-parameters-position': (900, 70),
        'dynamic-title-position': (0, 0),
        'dynamic-title-colour': (255, 255, 255),
        'dynamic-title-font-size': 24,
        'parameter-position': (0, 40),
        'parameter-width': 150,
        'parameter-height': 30,
        # Dynamic text
        'dynamic-text-colour': (255, 255, 0),
        'dynamic-text-font-size': 16,
        'dynamic-entry-colour': (0, 255, 0),
        'dynamic-entry-font-size': 15,
        'dynamic-entry-back-colour': (0, 0, 0, 100),
        'dynamic-entry-stroke-colour': (0, 255, 0, 100),
        'dynamic-entry-stroke-width': 3,
        # Parameter page control
        'dynamic-page-count': 5,
        'page-menu-width': 50,
        'page-menu-height': 26,
        'page-menu-item-width': 50,
        'page-menu-item-height': 26,
        'page-menu-font-colour': (255, 255, 255),
        'page-menu-font-size': 12,
        'page-menu-position': (850, 95),
        'page-menu-on-colour': (0, 255, 0, 100),
        'page-menu-mouse-colour': (0, 150, 0, 100),
        'page-menu-off-colour': (0, 0, 0, 100),
        'page-menu-back-colour': (0, 0, 0, 0),
    }),

    'start-screen': ('main', {
        # Logo and title
        'bg-position': (W/2, H/2),
        'logo-position': (W/2, 80),
        'title': 'terrainui',
        'title-position': (W/2, 300),
        'title-colour': (255, 255, 255, 255),
        'title-font-size': 36,
        # Version text
        'version-position': (W/2, H-10),
        'version-colour': (50, 50, 50),
        'version-font-size': 12,
        # Start button
        'start-position': (W/2, H-120),
        'start-colour': (255, 255, 0, 255),
        'start-font-size': 48,
        # Help button
        'help-position': (W-100, H-40),
        'help-colour': (0, 255, 0, 255),
        'help-font-size': 24,
        # Credits button
        'credits-position': (100, H-40),
        'credits-colour': (0, 255, 0, 255),
        'credits-font-size': 24,    
        # Achievements button
        'achievements-position': (W/2, H-40),
        'achievements-colour': (0, 255, 0, 255),
        'achievements-font-size': 24,
        # Filename
        'filename-position': (450, 250),
        'filename-width': 500,
        'filename-height': 30,
        'filename-colour': (255, 255, 255),
        'filename-font-size': 30,
        'filename-back-colour': (0, 0, 0, 100),
        'filename-stroke-colour': (255, 255, 255),
        'filename-stroke-width': 3,
        # Filename label
        'filename-label-position': (W/2, 250),
        'filename-label-colour': (255, 255, 255),
        'filename-label-font-size': 30,
        # File menu properties
        'menu-width': 150,
        'menu-height': 30,
        'menu-back-colour': (0, 0, 0, 0),
        'menu-item-width': 150,
        'menu-item-height': 30,
        'menu-on-colour': (0, 255, 0, 100),
        'menu-off-colour': (0, 0, 0, 100),
        'menu-font-colour': (255, 255, 0),
        'menu-font-size': 16,
        'menu-position': (W/2, 300),
    }),

    'sub-screen': ('start-screen', {
        # Logo and title
        'logo-position': (W/2-50, 40),
        'title-position': (W/2+50, 40),
        'title-colour': (255, 255, 255, 255),
        'title-font-size': 36,
        # Back button
        'back-colour': (255, 255, 0, 255),
        'back-font-size': 24,
        # Buttons
        'buttons-colour': (255, 255, 255),
        'buttons-size': (70, 30),
        'buttons-rect-colour': (100, 150, 100),
        'buttons-font-size': 18,
        'buttons-stroke-colour': (255, 255, 255),
        'buttons-stroke-width': 3,
    }),
    'file-select-screen': ('sub-screen', {
        # Filename
        'filename-position': (W / 2, 50),
        'filename-width': 500,
        'filename-height': 30,
        'filename-colour': (255, 255, 255),
        'filename-font-size': 30,
        'filename-back-colour': (0, 0, 0, 100),
        'filename-stroke-colour': (255, 255, 255),
        'filename-stroke-width': 3,
        # Filename label
        'filename-label-position': (W/2, 250),
        'filename-label-colour': (255, 255, 255),
        'filename-label-font-size': 30,
        # File menu properties
        'file-menu-position': (W/2, 100),
        # Do it
        'do-it-position': (W/2 + 50, H - 50),
        # Cancel
        'cancel-position': (W/2 - 50, H - 50),
    }),
     'help-screen': ('sub-screen', {
        # Help text
        'text-position': (W/2, H/2),
    }),
    'credits-screen': ('sub-screen', {
        # Author
        'author-title-colour': (0, 220, 220),
        'author-title-font-size': 24,
        'author-title-position': (W/2, 110),
        'author-colour': (255, 255, 0),
        'author-font-size': 32,
        'author-position': (W/2, 150),
        'url-colour': (255, 0, 0),
        'url-font-size': 14,
        'url-position': (W/2, 170),
        # Music
        'music-title1-colour': (0, 220, 220),
        'music-title1-font-size': 20,
        'music-title1-position': (W/2, 220),
        'music-title2-colour': (0, 220, 220),
        'music-title2-font-size': 18,
        'music-title2-position': (W/2, 240),
        'music-colour': (255, 255, 0),
        'music-font-size': 16,
        'music-position': (W/2, 260),
        # Sound
        'sound-title1-colour': (0, 220, 220),
        'sound-title1-font-size': 20,
        'sound-title1-position': (W/2, 340),
        'sound-title2-colour': (0, 220, 220),
        'sound-title2-font-size': 18,
        'sound-title2-position': (W/2, 360),
        # Built using        
        'built-title-colour': (0, 220, 220),
        'built-title-font-size': 20,
        'built-title-position': (W/4, 420),
        'built-colour': (255, 255, 0),
        'built-font-size': 16,
        'built-position': (W/4, 440),
        # Engine
        'engine-title-colour': (0, 220, 220),
        'engine-title-font-size': 20,
        'engine-title-position': (W/4, 480),
        'engine-colour': (255, 255, 0),
        'engine-font-size': 16,
        'engine-position': (W/4, 500),
        # Engine version
        'engine-version-colour': (75, 75, 0),
        'engine-version-font-size': 10,
        'engine-version-position': (W/4, 520),
        # Fonts
        'font-title1-colour': (0, 220, 220),
        'font-title1-font-size': 20,
        'font-title1-position': (W*3/4, 420),
        'font-title2-colour': (0, 220, 220),
        'font-title2-font-size': 18,
        'font-title2-position': (W*3/4, 440),
        'font-colour': (255, 255, 0),
        'font-font-size': 16,
        'font-position': (W*3/4, 460),
        #
        'back-position': (100, H-40),

    }),
    
    'achievements': ('main', {
        # Properties of the achievements system
        'banner-duration': 5,
        'banner-position': (175, 525),
        'banner-size': (300, 50),
        'banner-backcolour': (0, 0, 0, 50),
        'banner-font-colour': (255, 255, 0, 255),
        'banner-name-size': 14,
        'banner-description-size': 8,
        'banner-name-position': (-100, -18),
        'banner-description-position': (-100, 0),
        'banner-font-name': 'DEFAULT',
        'banner-graphic-position': (-125, 0),
        
        'time-colour': (255, 255, 255, 100),
        'time-size': 10,
        'time-position': (-100, 24),
        
        'logo-position': (400, 50),
        'screen-background-sprite': None,
        'screen-background-position': (400, 300),
        'grid-size': (2, 5),
        'grid-width': 800,
        'grid-height': 400,
        'grid-position': (400, 320),
        
        'back-colour': (255, 255, 255, 255),
        'back-font-size': 20,
        'back-font-name': 'DEFAULT',
        'back-position': (400, 560),
        'back-sound': 'click',
    }),

    '__default__': 'main',

})

G = theme.getProperty
