# -*- coding: utf-8 -*-

# import webbrowser
import copy  # Going to be used to create deep copy of players for records.

import kivy

kivy.require('1.9.1')

# from kivy.animation import Animation
from kivy.app import App
# from kivy.clock import Clock
from kivy.garden.circularlayout import CircularLayout
from kivy.garden.modernmenu import ModernMenu
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty, BoundedNumericProperty, DictProperty,
    ObjectProperty, StringProperty, ListProperty, NumericProperty
)
# from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
# from kivy.uix.progressbar import ProgressBar
from os.path import join, dirname

try:
    import mafiademonstration.stages as stages
except ModuleNotFoundError:
    import stages


# TIMER_OPTIONS = {
#     '1/60 sec': 1 / 60.0,
#     '1/30 sec': 1 / 30.0,
#     '1/15 sec': 1 / 15.0,
# }



class MafiaDemonstrationApp(App):
    """Simple Slideshow App with a user defined title.

    Attributes:
      title (str): Window title of the application

      timer (:class:`kivy.properties.BoundedNumericProperty`):
        Helper for the slide transition of `carousel`

    """

    title = 'Mafia Demonstration'
    cycle = NumericProperty(0)
    ready_to_submit = BooleanProperty(False)

    def build(self):
        """Initialize the GUI based on the kv file and set up events.

        Returns:
          (:class:`kivy.uix.anchorlayout.AnchorLayout`): Root widget specified
            in the kv file of the app
        """
        # self.player_count = int(self.config.get('user_settings', 'player_count'))
        # self.agent_number = int(self.config.get('user_settings', 'agent_number'))
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(stages.MenuScreen(name='menu'))
        sm.add_widget(stages.SettingsScreen(name='settings'))
        sm.add_widget(stages.LoadingScreen(name='loading'))
        sm.add_widget(stages.DiscussionScreen(name='discussion'))
        sm.add_widget(stages.TrialScreen(name='trial'))
        sm.add_widget(stages.NightScreen(name='night'))
        sm.add_widget(stages.EndGameScreen(name='endgame'))


        return sm

    def build_config(self, config):
        """Create a config file on disk and assign the ConfigParser object to
        `self.config`.
        """
        config.setdefaults(
            'user_settings', {
                'timer_interval': '1/60 sec',
                'language': 'en',
                'player_count': 6,
                'agent_number': 1,
            }
        )

    def build_settings(self, settings):
        """Read the user settings and create a panel from it."""
        settings_file = join(dirname(__file__), 'user_settings.json')
        settings.add_json_panel(self.title, self.config, settings_file)

    def on_config_change(self, config, section, key, value):
        """Called when the user changes the config values via the settings
        panel. If `timer_interval` is being changed update the instance
        variable of the same name accordingly.
        """
        if config is self.config:
            token = (section, key)
            if token == ('user_settings', 'timer_interval'):
                pass
                # self.timer_interval = TIMER_OPTIONS[value]
            elif token == ('user_settings', 'language'):
                self.language = value
            elif token == ('user_settings', 'player_count'):
                self.player_count = value
            elif token == ('user_settings', 'agent_number'):
                self.agent_number = value

    def on_pause(self):
        """Enables the user to switch to another application causing
        :class:`MafiaDemonstrationApp` to wait until the user
        switches back to it eventually.
        """
        return True

    def on_resume(self):
        """Called when the app is resumed. Used to restore data that has been
        stored in :meth:`MafiaDemonstrationApp.on_pause`.
        """
        pass
