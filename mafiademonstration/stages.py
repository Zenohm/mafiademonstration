from collections import Counter
import json
import math
import random
from kivy.clock import Clock
from kivy.garden.circularlayout import CircularLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.config import Config


try:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import (
        Player, DeadPlayer, DiscussionPlayer,
        PlayerIcon, NightSleepingPlayer, TrialPlayer
    )
except ModuleNotFoundError:
    from border_behavior import BorderBehavior
    from player import (
        Player, DeadPlayer, DiscussionPlayer,
        PlayerIcon, NightSleepingPlayer, TrialPlayer
    )

try:
    Builder.load_file('mafiademonstration/stages.kv')
except FileNotFoundError:
    Builder.load_file('../mafiademonstration/stages.kv')


class Stage(Screen):
    # Kivy Properties
    # This will be used to keep track of who is acting against whom.
    selected_player = ObjectProperty(None, allownone=True)

    # Static variables
    players = dict()
    player_count = 0
    agent_number = 0
    player_to_be_tried = None
    winner = "Nobody"
    player_log = "Output text goes here"

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)
        self.config = Config

    def add_players(self, default_new_player_class):
        """
        Goes through every player, and, depending on the state of the player,
        adds that player to the current stage.
        :param default_new_player_class: The Class of the player to be created and added to the stage.
        :return: None
        """
        for player in self.players.values():
            if player.alive:
                new_player_class = default_new_player_class
            else:
                new_player_class = DeadPlayer

            # Here there be shallow copied dragons.
            new_player = new_player_class(
                name=player.name,
                number=player.number,
                alive=player.alive,
                mafia=player.mafia,
                icon=player.icon,
                strategic_value=player.strategic_value,
                actions=player.actions
            )

            self.ids.circular_layout.add_widget(new_player)

    def initialize_settings(self):
        Config.read('mafiademonstration/mafiademonstration.ini')
        Stage.player_count = self.config.getint('user_settings', 'player_count')
        Stage.agent_number = self.config.getint('user_settings', 'agent_number')
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

    def initialize_players(self):
        for player_number in range(1, Stage.player_count + 1):
            if player_number == self.agent_number:
                # All values that need to be set for
                # the agent should be set here.
                player_icon = './data/icons/agent_alive.png'
                player_name = "agent"
                Logger.debug("Player: Agent found: {}".format(player_name))
            else:
                player_name = 'player {}'.format(player_number)
                player_icon = './data/icons/player_alive.png'
            player = Player(name=player_name, icon=player_icon)
            player.number = player_number
            Stage.players[player_name] = player

        number_of_mafia = math.floor(math.sqrt(Stage.player_count))
        mafia_members = random.sample(list(Stage.players), number_of_mafia)

        for player in mafia_members:
            Stage.players[player].mafia = True

    def on_pre_enter(self, *args):
        super(Stage, self).on_pre_enter(*args)
        Logger.debug("Movement: Entering: {stage}".format(stage=self.__class__.__name__))

    def on_enter(self, *args):
        super(Stage, self).on_enter(*args)
        Logger.debug("Movement: Entered: {stage}".format(stage=self.__class__.__name__))

    def on_pre_leave(self, *args):
        super(Stage, self).on_pre_leave(*args)
        Logger.debug("Movement: Exiting: {stage}".format(stage=self.__class__.__name__))

    def on_leave(self, *args):
        super(Stage, self).on_leave(*args)
        Logger.debug("Movement: Exited: {stage}".format(stage=self.__class__.__name__))

    @staticmethod
    def check_for_winner():

        mafia_count = 0
        towny_count = 0

        for name, player in Stage.players.items():
            if player.alive:
                if player.mafia:
                    mafia_count += 1
                else:
                    towny_count += 1

        if mafia_count == 0:
            Stage.winner = "Town"

        if towny_count == 0:
            Stage.winner = "Mafia"

        return Stage.winner


class MainMenu(Stage):
    def on_pre_leave(self, *args):
        super(MainMenu, self).on_pre_leave(*args)
        self.initialize_settings()
        self.initialize_players()


class Discussion(Stage):
    def submit(self):
        most_accused = Discussion.count_accusations()

        if most_accused is None:
            self.manager.current = "loadingTN"
        else:
            Logger.info("Discussion: Most accused player: {}".format(most_accused.name))
            Stage.player_to_be_tried = most_accused
            self.manager.current = "loadingDT"

    def write_to_action_log(self, *args):
        output = ""
        for name, player in self.players.items():
            if player.actions['accuse']['player'] is not None:
                output += f"{player.number} accuses  {player.actions['accuse']['player'].number}\n"
            if player.actions['suspect']['player'] is not None:
                output += f"{player.number} suspects {player.actions['suspect']['player'].number}\n"
        self.text = output

    def on_enter(self):
        super(Discussion, self).on_enter()
        Clock.schedule_interval(self.write_to_action_log, 0.5)
        self.add_players(DiscussionPlayer)

    def on_pre_leave(self):
        super(Discussion, self).on_pre_leave()
        self.ids.circular_layout.clear_widgets()

    @staticmethod
    def count_accusations():
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
        accusation_amount = accusations[most_accused]

        if dict(Counter(accusations.values()))[accusation_amount] > 1:
            Logger.debug("Discussion: Accusation Counts: {}".format(dict(Counter(accusations.values()))))
            Logger.info("Discussion: There was a tie amongst the accused.")
            # most_accused = max(suspicions, key=suspicions.get)
            # accusation_amount = max(suspicions.values())
            return None

            # if dict(Counter(suspicions.values()))[accusation_amount] > 1:
            #     Logger.info("Tie amongst the players, no one goes on trial.")
            #     return None

        return Stage.players[most_accused]


class Trial(Stage):
    def add_players(self, default_new_player_class):
        for player in self.players.values():
            if player.alive:
                if Stage.players[Stage.player_to_be_tried.name] == player:
                    new_player_class = PlayerIcon
                else:
                    new_player_class = default_new_player_class
            else:
                new_player_class = DeadPlayer

            # Here there be shallow copied dragons.
            new_player = new_player_class(
                name=player.name,
                number=player.number,
                alive=player.alive,
                mafia=player.mafia,
                icon=player.icon,
                strategic_value=player.strategic_value,
                actions=player.actions
            )

            self.ids.circular_layout.add_widget(new_player)

    def submit(self):
        verdict = Trial.decide_verdict()

        player = Stage.players[Stage.player_to_be_tried.name]

        if verdict == "guilty":
            Logger.info("{} is guilty!".format(Stage.player_to_be_tried.name))
            player.icon = "data/icons/player_dead.png"
            player.alive = False
        elif verdict == "innocent":
            Logger.info("{} is innocent!".format(player.name))
            player.icon = "data/icons/player_alive.png"
            Stage.player_to_be_tried = None
        elif verdict == "tie":
            Logger.info("{} split the votes and will be released!".format(player.name))
            # This could be changed so that the result is decided by a coin toss or something similar.
            player.icon = "data/icons/player_alive.png"
            Stage.player_to_be_tried = None

        winner = Stage.check_for_winner()
        print(winner)
        if winner == "Nobody":
            self.manager.current = "loadingTN"
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = game_over.text.format(winner)
            self.manager.current = "gameovermenu"

    def on_enter(self, *args):
        super(Trial, self).on_enter(*args)
        player = Stage.players[Stage.player_to_be_tried.name]
        player.icon = "data/icons/player.png"
        self.add_players(TrialPlayer)

    def on_pre_leave(self, *args):
        super(Trial, self).on_pre_leave(*args)
        self.ids.circular_layout.clear_widgets()

    @staticmethod
    def decide_verdict() -> str:
        """
        Step through the players, count their votes, and decide on a verdict.
        :return: A string with the value of guilty, innocent, or tie.
        """
        vote = {'guilty': 0, 'innocent': 0}

        for player in Stage.players.values():
            decision = player.actions['vote']['decision']

            if decision is None:
                Logger.warning("{} had None in their vote:decision field!".format(player.name))
                continue

            if decision == "abstain":
                Logger.debug("{} decided to abstain.".format(player.name))
                continue

            Logger.debug("{} voted {}".format(player.name, decision))
            vote[decision] += 1

        if vote['guilty'] == vote['innocent']:
            verdict = "tie"
            Logger.debug("The vote was a tie.")
        else:
            verdict = max(vote, key=vote.get)
            Logger.debug("The verdict was {}.".format(verdict))

        return verdict


class Night(Stage):
    def add_players(self, default_new_player_class):
        for player in self.players.values():
            if player.alive:
                if player.mafia:
                    new_player_class = PlayerIcon
                else:
                    new_player_class = default_new_player_class
            else:
                new_player_class = DeadPlayer

            # Here there be shallow copied dragons.
            new_player = new_player_class(
                name=player.name,
                number=player.number,
                alive=player.alive,
                mafia=player.mafia,
                icon=player.icon,
                strategic_value=player.strategic_value,
                actions=player.actions
            )

            self.ids.circular_layout.add_widget(new_player)

    def submit(self):
        if self.selected_player:
            Stage.players[self.selected_player.name].die()

        winner = Stage.check_for_winner()
        print(winner)
        if winner == "Nobody":
            self.manager.current = "loadingND"
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = game_over.text.format(winner)
            self.manager.current = "gameovermenu"

    def on_enter(self):
        super(Night, self).on_enter()
        for name, player in self.players.items():
            # TODO: Move all the add_players methods into each stage's on_enter method.
            if player.alive:
                if player.mafia:
                    player.icon = "data/icons/player_alive_mafia.png"
                else:
                    player.icon = "data/icons/player_asleep.png"

        self.add_players(NightSleepingPlayer)

    def on_pre_leave(self):
        super(Night, self).on_pre_leave()

        for name, player in self.players.items():
            if player.alive:
                if player.number == self.agent_number:
                    player.icon = "data/icons/agent_alive.png"
                else:
                    player.icon = "data/icons/player_alive.png"

        self.ids.circular_layout.clear_widgets()


class GameOverMenu(Stage):
    def on_pre_leave(self):
        super(GameOverMenu, self).on_pre_leave()
        Stage.winner = "Nobody"
        self.initialize_settings()
        self.initialize_players()


class LoadingScreen(Stage):
    def on_enter(self):
        super(LoadingScreen, self).on_enter()
        players = [dict(player) for player in Stage.players.values()]
        json_players = LoadingScreen.to_json(players)
        json_players_modified = LoadingScreen.call_reasoner(json_players)
        Stage.players = LoadingScreen.from_json(json_players_modified)
        self.exit()

    def exit(self):
        pass

    @staticmethod
    def call_reasoner(json_players):
        players = LoadingScreen.from_json(json_players)
        # Simulate a slow reasoner
        # import time
        # time.sleep(3)

        choices = []

        if players['agent'].alive:
            for name, player in players.items():
                if name == 'agent':
                    continue

                if player.alive:
                    choices.append(player)

        if choices:
            poor_devil = random.choice(choices)
            players['agent'].actions['accuse']['player'] = poor_devil
            players['agent'].actions['vote']['decision'] = "guilty" if random.random() > 0.5 else "innocent"
        players = [dict(player) for player in players.values()]
        json_players_modified = LoadingScreen.to_json(players)
        return json_players_modified

    @staticmethod
    def to_json(player_list) -> str:
        """
        Convert player object to standard language for transmission
        between various outside reasoners.
        """
        return json.dumps(player_list)

    @staticmethod
    def from_json(json_players):
        """
        Read a list of players in a standard format and convert it
        into a list of Player objects.
        """
        output_data = {}
        json_data = json.loads(json_players)
        for person_data in json_data:
            player = Player(**person_data)
            output_data[player.name] = player

        # Change the player names in the dict to actual player references
        for name, player in output_data.items():
            for action, attributes in player.actions.items():
                for attribute, value in attributes.items():
                    if attribute == "player" and value is not None:
                        output_data[name].actions[action][attribute] = output_data[value]

        return output_data


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

