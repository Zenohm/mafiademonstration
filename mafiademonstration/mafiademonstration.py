# -*- coding: utf-8 -*-

import json
import kivy
from kivy.app import App
from kivy.properties import (
        ListProperty,
)
from kivy.uix.screenmanager import ScreenManager, NoTransition

from os.path import join, dirname

kivy.require('1.9.1')


try:
    import mafiademonstration.stages as stages
except ModuleNotFoundError:
    import stages


class MafiaDemonstrationApp(App):
    """Simple Slideshow App with a user defined title.

    Attributes:
      title (str): Window title of the application

    """

    title = 'Mafia Demonstration'

    def build(self):
        """Initialize the GUI based on the kv file and set up events.

        Returns:
          (:class:`kivy.uix.screenmanager.ScreenManager`):
            Root widget specified in the kv file of the app
        """
        # cycle = NumericProperty(0)
        sm = ScreenManager(transition=NoTransition())
        sm.selected_player = None
        sm.players = ListProperty()
        sm.add_widget(stages.MainMenu(name='mainmenu'))
        sm.add_widget(stages.LoadingDT(name='loadingDT'))
        sm.add_widget(stages.LoadingTN(name='loadingTN'))
        sm.add_widget(stages.LoadingND(name='loadingND'))
        sm.add_widget(stages.Discussion(name='discussion'))
        sm.add_widget(stages.Trial(name='trial'))
        sm.add_widget(stages.Night(name='night'))
        sm.add_widget(stages.GameOverMenu(name='gameovermenu'))

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

        config.setdefaults(
            'debug', {
                'stage_jump': 'discussion',
            }
        )

    def build_settings(self, settings):
        """Read the user settings and create a panel from it."""
        filename = join(dirname(__file__), 'user_settings.json')
        settings.add_json_panel(self.title, self.config, filename)

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
