from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image

# from kivy.logger import Logger
from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty
)


try:
    from border_behavior import BorderBehavior
    from player import (
        DiscussionPlayer, NightPlayer, TrialPlayer
    )
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import (
        DiscussionPlayer, NightPlayer, TrialPlayer
    )

try:
    Builder.load_file('mafiademonstration/stages.kv')
except FileNotFoundError:
    Builder.load_file('stages.kv')


class Stage(Screen):
    player_count = NumericProperty()
    agent_number = NumericProperty()
    selected_player = ObjectProperty()
    players = ListProperty()

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)
        self.player_count = 6  # self.config.get('settings', 'player_count')
        self.agent_number = 0  # self.config.get('settings', 'agent_number')
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

    def enter(self, **kwargs):
        print("entering {stage}".format(stage=self.__class__.__name__))

    def exit(self, **kwargs):
        print("exiting {stage}".format(stage=self.__class__.__name__))


class MainMenu(Stage):
    pass


class Discussion(Stage):
    def __init__(self, **kwargs):
        super(Discussion, self).__init__(**kwargs)
        players = dict()
        for player_number in range(1, self.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = DiscussionPlayer(name=player_name)
            player.number = player_number
            # player.borders = (2, "solid",(0,2,3,4))

            if player_number == self.agent_number:
                # All values that need to be set for the agent
                # should be set here.
                player.icon = './data/icons/agent.png'

            players[player_name] = player
            self.ids.circular_layout.add_widget(player)

        Stage.players = players
        # This will be used to keep track of who is acting against whom.
        Stage.selected_player = None


class Trial(Stage):
    def __init__(self, **kwargs):
        super(Trial, self).__init__(**kwargs)
        players = dict()
        for player_number in range(1, self.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = TrialPlayer(name=player_name)
            player.number = player_number
            # player.borders = (2, "solid",(0,2,3,4))

            if player_number == self.agent_number:
                # All values that need to be set for the agent
                # should be set here.
                player.icon = './data/icons/agent.png'

            players[player_name] = player
            self.ids.circular_layout.add_widget(player)

        Stage.players = players
        # This will be used to keep track of who is acting against whom.
        Stage.selected_player = None

    def submit(self, **kwargs):
        print(kwargs)
        return True


class Night(Stage):
    def __init__(self, **kwargs):
        super(Night, self).__init__(**kwargs)
        players = dict()
        for player_number in range(1, self.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = NightPlayer(name=player_name)
            player.number = player_number
            if player_number % 2:
                player.mafia = True
            else:
                player.icon = "data/icons/player_asleep.png"
            # player.borders = (2, "solid",(0,2,3,4))

            if player_number == self.agent_number:
                # All values that need to be set for the agent
                # should be set here.
                player.icon = './data/icons/agent.png'

            players[player_name] = player
            self.ids.circular_layout.add_widget(player)

        Stage.players = players
        # This will be used to keep track of who is acting against whom.
        Stage.selected_player = None

    def submit(self, **kwargs):
        print(kwargs)
        return True


class GameOverMenu(Stage):
    pass


class LoadingScreen(Stage):
    def enter(self, **kwargs):
        super(LoadingScreen, self).enter(**kwargs)
        print("entered load phase called {stage}".format(
            stage=self.__class__.__name__)
        )
        print("We call the reasoner here")
        self.exit()

    def exit(self, **kwargs):
        super(LoadingScreen, self).exit(**kwargs)
        print("exited load phase called {stage}".format(
            stage=self.__class__.__name__)
        )
        self.manager.current = None


class LoadingDT(LoadingScreen):

    def exit(self, **kwargs):
        super(LoadingDT, self).exit(**kwargs)
        self.manager.current = "trial"


class LoadingTN(LoadingScreen):

    def exit(self, **kwargs):
        super(LoadingTN, self).exit(**kwargs)
        self.manager.current = "night"


class LoadingND(LoadingScreen):

    def exit(self, **kwargs):
        super(LoadingND, self).exit(**kwargs)
        self.manager.current = "discussion"


class ImageButton(BorderBehavior, ButtonBehavior, Image):
    pass


class ActionList(DropDown):
    pass
