from collections import Counter
from kivy.garden.circularlayout import CircularLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image

from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.config import Config


try:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import (
        Player, DiscussionPlayer, NightPlayer, TrialPlayer
    )
except ModuleNotFoundError:
    from border_behavior import BorderBehavior
    from player import (
        Player, DiscussionPlayer, NightPlayer, TrialPlayer
    )

try:
    Builder.load_file('mafiademonstration/stages.kv')
except FileNotFoundError:
    Builder.load_file('../mafiademonstration/stages.kv')


class Stage(Screen):
    # Kivy Properties
    # This will be used to keep track of who is acting against whom.
    selected_player = ObjectProperty(None)

    # Static variables
    players = dict()
    player_count = 0
    agent_number = 0
    player_to_be_tried = None

    def add_players(self, NewPlayerClass):
        for player in self.players.values():
            # Here there be shallow copied dragons.
            new_player = NewPlayerClass(
                name=player.name,
                number=player.number,
                alive=player.alive,
                mafia=player.mafia,
                strategic_value=player.strategic_value,
                actions=player.actions
            )
            self.ids.circular_layout.add_widget(new_player)

    def initialize_settings(self):
        Config.read('mafiademonstration/mafiademonstration.ini')
        self.config = Config
        Stage.player_count = self.config.getint('user_settings', 'player_count')
        Stage.agent_number = self.config.getint('user_settings', 'agent_number')
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

    def initialize_players(self):
        for player_number in range(1, Stage.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = Player(name=player_name)
            player.number = player_number
            # player.borders = (2, "solid",(0,2,3,4))

            if player_number == self.agent_number:
                Logger.debug("Agent found: {}".format(player.name))
                # All values that need to be set for
                # the agent should be set here.
                player.icon = './data/icons/agent.png'

            Stage.players[player_name] = player

    def on_enter(self):
        Logger.debug("Entering: {stage}".format(stage=self.__class__.__name__))

    def on_pre_leave(self):
        Logger.debug("Exiting: {stage}".format(stage=self.__class__.__name__))


class MainMenu(Stage):
    def on_pre_leave(self):
        super(MainMenu, self).on_pre_leave()
        self.initialize_settings()
        self.initialize_players()


class Discussion(Stage):
    def count_votes(self):
        """

        :return: A reference to the player to be put on trial, or None
        """
        accusations = dict.fromkeys(Stage.players.keys(), 0)
        suspicions = dict.fromkeys(Stage.players.keys(), 0)

        for player in Stage.players.values():
            if player.actions['accuse']['player'] is not None:
                accusations[player.actions['accuse']['player'].name] += 1
            if player.actions['suspect']['player'] is not None:
                suspicions[player.actions['suspect']['player'].name] += 1

        most_accused = max(accusations, key=accusations.get)
        accusation_amount = max(accusations.values())

        if dict(Counter(accusations.values()))[accusation_amount] > 1:
            Logger.debug("Accusation Counts: {}".format(dict(Counter(accusations.values()))))
            Logger.info("There was a tie amongst the accused.")
            # most_accused = max(suspicions, key=suspicions.get)
            # accusation_amount = max(suspicions.values())
            return None

            # if dict(Counter(suspicions.values()))[accusation_amount] > 1:
            #     Logger.info("Tie amongst the players, no one goes on trial.")
            #     return None

        return Stage.players[most_accused]

    def on_enter(self):
        super(Discussion, self).on_enter()
        self.add_players(DiscussionPlayer)

    def on_pre_leave(self):
        super(Discussion, self).on_pre_leave()
        self.ids.circular_layout.clear_widgets()

    def submit(self):
        most_accused = self.count_votes()

        if most_accused is None:
            self.manager.current = "loadingTN"
        else:
            Logger.info("Most accused player: {}".format(most_accused.name))
            Stage.player_to_be_tried = most_accused
            self.manager.current = "loadingDT"


class Trial(Stage):
    def on_enter(self):
        super(Trial, self).on_enter()
        self.add_players(TrialPlayer)

    def on_pre_leave(self):
        super(Trial, self).on_pre_leave()
        self.ids.circular_layout.clear_widgets()

    def submit(self):
        self.manager.current = "loadingTN"


class Night(Stage):
    def on_enter(self):
        super(Night, self).on_enter()
        self.add_players(NightPlayer)

    def on_pre_leave(self):
        super(Night, self).on_pre_leave()
        self.ids.circular_layout.clear_widgets()

    def submit(self):
        if not any(player.alive for player in Stage.players.values()):
            self.manager.current = "gameovermenu"
        else:
            self.manager.current = "loadingND"


class GameOverMenu(Stage):
    pass


class LoadingScreen(Stage):
    def on_enter(self):
        super(LoadingScreen, self).on_enter()
        print("We call the reasoner here")
        self.exit()

    def exit(self):
        pass


class LoadingDT(LoadingScreen):
    def exit(self):
        self.manager.current = "trial"


class LoadingTN(LoadingScreen):
    def exit(self):
        self.manager.current = "night"


class LoadingND(LoadingScreen):
    def exit(self):
        self.manager.current = "discussion"


class ImageButton(BorderBehavior, ButtonBehavior, Image):
    pass


class ActionList(DropDown):
    pass
