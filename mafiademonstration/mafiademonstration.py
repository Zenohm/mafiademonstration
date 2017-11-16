# -*- coding: utf-8 -*-

from os.path import join, dirname

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

kivy.require('1.9.1')


try:
    import stages
except ModuleNotFoundError:
    import mafiademonstration.stages


class MafiaDemonstrationApp(App):
    """

    Attributes:
      title (str): Window title of the application

    """

    title = 'Mafia Demonstration'

    def __init__(self, **kwargs):
        App.__init__(self)
        self.language = kwargs.get("language", "en")
        self.player_count = kwargs.get("player_count", 8)
        self.agent_number = kwargs.get("agent_number", 0)

    def build(self) -> ScreenManager:
        """Initialize the GUI using the screen manager.

        :rtype: ScreenManager
        :return: The screen manager which is to act as the root widget for the application.
        """
        manager = ScreenManager(transition=NoTransition())
        manager.add_widget(stages.MainMenu(name='main_menu'))
        manager.add_widget(stages.GameOverMenu(name='game_over_menu'))
        manager.add_widget(stages.TutorialMenu(name='tutorial'))
        manager.add_widget(stages.PlayerTutorial(name='player_status'))
        manager.add_widget(stages.StagesTutorial(name='stages_tutorial'))
        manager.add_widget(stages.Credits(name='credits'))
        manager.add_widget(stages.Loading(name='loading'))
        manager.add_widget(stages.Discussion(name='discussion'))
        manager.add_widget(stages.Trial(name='trial'))
        manager.add_widget(stages.Night(name='night'))

        return manager

    def build_config(self, config) -> None:
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

    def build_settings(self, settings) -> None:
        filename = join(dirname(__file__), 'user_settings.json')
        settings.add_json_panel(self.title, self.config, filename)

    def on_config_change(self, config, section, key, value) -> None:
        if config is self.config:
            token = (section, key)
            if token == ('user_settings', 'language'):
                self.language = value
            elif token == ('user_settings', 'player_count'):
                self.player_count = value
            elif token == ('user_settings', 'agent_number'):
                self.agent_number = value

    def on_pause(self) -> bool:
        return True

    def on_resume(self) -> None:
        pass
