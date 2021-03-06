"""Main module for the game"""

import os
import time

import serge.engine
import serge.world
import serge.actor
import serge.zone
import serge.render
import serge.sound 
import serge.events
import serge.blocks.achievements

import serge.visual
import serge.blocks.actors
import serge.blocks.utils
import serge.blocks.onlinescores

import common
import mainscreen
import startscreen
import helpscreen
import creditsscreen
import fileselectscreen

from theme import G, theme


def registerSounds():
    """Register the sounds to use"""
    serge.sound.Sounds.setPath('sound')
    r = serge.sound.Sounds.registerItem
    r('click', 'click.wav')


def registerMusic():
    """Register the music to use"""
    serge.sound.Music.setPath('music')
    r = serge.sound.Music.registerItem


def registerGraphics():
    """Register the graphics to use"""
    serge.visual.Sprites.setPath('graphics')
    r = serge.visual.Sprites.registerItem
    rf = serge.visual.Sprites.registerFromFiles
    rm = serge.visual.Sprites.registerMultipleItems
    rp = serge.visual.Sprites.registerItemsFromPattern
    r('map', 'map-graphic.png', zoom=1.15)
    r('icon', 'logo.png')
    r('logo', 'icon.png', zoom=0.2)
    r('small-icon', 'icon.png', zoom=0.2)
    r('help-text', 'help-text.png')
    rf('mute-button', 'music-%d.png', 2, zoom=0.5)
    rf('achievement', 'achievement-%d.png', 2)
    #
    # Fonts
    serge.visual.Fonts.setPath('fonts')
    serge.visual.Fonts.registerItem('DEFAULT', 'uptown.ttf')
    serge.visual.Fonts.registerItem('CLEAR', 'OpenSans-Light.ttf')


def registerEvents():
    """Register all the events"""
    broadcaster = serge.events.getEventBroadcaster()
    broadcaster.registerEventsFromModule(common)


def registerAchievements(options):
    """Register the achievements for the game"""
    r = serge.blocks.achievements.initManager('terrainui').safeRegisterAchievement
    a = serge.blocks.achievements.Achievement
    r(a('Played the game', 'You played the game at least once', 
        'badge', False, 'play', condition_string=': True'))
    serge.blocks.achievements.addAchievementsWorld(options, theme)
    

def startEngine(options):
    """Start the main engine"""
    engine = serge.engine.Engine(
        width=G('screen-width'), height=G('screen-height'),
        title=G('screen-title'), icon=os.path.join('graphics', G('screen-icon-filename')))
    serge.blocks.utils.createVirtualLayersForEngine(
        engine, ['background', 'foreground', 'main', 'ui-back', 'ui', 'ui-progress', 'ui-front', 'ui-over'])
    serge.blocks.utils.createWorldsForEngine(
        engine,
        ['start-screen', 'main-screen', 'credits-screen', 'help-screen', 'file-select-screen'])
    #
    engine.setCurrentWorldByName('start-screen' if not options.straight else 'main-screen')
    return engine


def stoppingNow(obj, arg):
    """We are about to stop"""
    #
    # Fade out music and wait for a bit before going away
    serge.sound.Music.fadeout(G('pre-stop-pause')*1000)
    time.sleep(G('pre-stop-pause'))
       

def createHighScores(options):
    """Create the high score table"""
    hs = serge.blocks.onlinescores.HighScoreSystem(
        G('app-url', 'high-score-screen'), secret_user=options.cheat)
    app_name = G('app-name', 'high-score-screen')
    if hs.gameExists(app_name):
        return
    #
    common.log.info('Creating high score table')
    hs.createGame(app_name)
    #
    # Create categories
    # hs.createGameCategory(
    #     app_name,
    #     'CATEGORY_NAME',
    #     'SCORE_NAME',
    #     LOWER_IS_BETTER,
    #     MAX_PLAYER_SCORES
    # )


def main(options, args):
    """Start the engine and the game"""
    #
    # Create the high scores
    if options.high_score:
        createHighScores(options)
    #
    # Create the engine
    engine = startEngine(options)
    engine.linkEvent(serge.events.E_BEFORE_STOP, stoppingNow)
    #
    registerSounds()
    registerMusic()
    registerGraphics()
    registerEvents()
    #
    # Record a movie
    if options.movie:
        serge.blocks.utils.RecordDesktop(options.movie)
    #
    # Change theme settings
    if options.theme:
        theme.updateFromString(options.theme)
    #
    # Muting
    mute = serge.blocks.actors.MuteButton('mute-button', 'ui', alpha=G('mute-button-alpha'))
    serge.blocks.utils.addMuteButtonToWorlds(mute, center_position=G('mute-button-position'))
    #
    if options.musicoff:
        mute.toggleSound()
    #
    # Initialise the main logic
    registerAchievements(options)
    mainscreen.main(options)
    startscreen.main(options)
    helpscreen.main(options)
    creditsscreen.main(options)
    fileselectscreen.main(options)
    #
    if options.debug:
        serge.builder.builder.main(engine, options.framerate)
    else:
        engine.run(options.framerate)
