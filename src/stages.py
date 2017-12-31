from collections import Counter
import json
import math
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.config import Config


try:
    from border_behavior import BorderBehavior
    from player import (
        Player, PlayerIcon, DiscussionPlayer,
        NightSleepingPlayer, NightMafiaPlayer,
        TrialPlayer, TrialAgent
    )
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import (
        Player, PlayerIcon, DiscussionPlayer,
        NightSleepingPlayer, NightMafiaPlayer,
        TrialPlayer, TrialAgent
    )

try:
    Builder.load_file('src/stages.kv')
except FileNotFoundError:
    Builder.load_file('../src/stages.kv')


class Stage(Screen):
    # Kivy Properties
    # This will be used to keep track of who is acting against whom.
    selected_player = ObjectProperty(None, allownone=True)

    # Static variables
    players = list()
    player_count = 0
    agent_number = 0
    # player_log = "Output text goes here"

    def get_player_class(self, player):
        return self.__class__

    def add_players(self, players):
        """
        Goes through every player, and, depending on the state of the player,
        adds that player to the current stage.
        :return: None
        """
        for player in players:
            new_player_class = self.get_player_class(player)

            # Here there be shallow copy dragons.
            new_player = new_player_class(
                name=player.name,
                number=player.number,
                alive=player.alive,
                mafia=player.mafia,
                agent=player.agent,
                icon=player.icon,
                is_on_trial=player.is_on_trial,
                strategic_value=player.strategic_value,
                actions=player.actions
            )

            self.ids.circular_layout.add_widget(new_player)

    @staticmethod
    def initialize_settings():
        Config.read('config.ini')
        Stage.player_count = Config.getint('user_settings', 'player_count')
        Stage.agent_number = Config.getint('user_settings', 'agent_number')

    @staticmethod
    def create_players(player_count, agent_number):
        players = []

        for number in range(player_count):
            name = 'player {}'.format(number)
            icon = "data/icons/easter_egg.png" if random.random() < 0.01 else "data/icons/player_alive.png"
            agent = False

            players.append(Player(
                name=name,
                number=number,
                alive=True,
                mafia=False,
                agent=agent,
                icon=icon,
                strategic_value=0
            ))

        if 0 <= agent_number < player_count:
            new_agent = players[agent_number]
            Logger.debug("Player: Agent assuming the role of {}.".format(new_agent.name))
            # All values that need to be set for
            # the agent should be set here.

            new_agent.name = "agent"
            new_agent.icon = './data/icons/agent_alive.png'
            new_agent.agent = True

        number_of_mafia = math.floor(math.sqrt(player_count))
        mafia_members = random.sample(players, number_of_mafia)

        for player in mafia_members:
            player.mafia = True

        return players

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        Logger.debug("Movement: Entering: {stage}".format(stage=self.__class__.__name__))

    def on_enter(self, *args):
        super().on_enter(*args)
        Logger.debug("Movement: Entered: {stage}".format(stage=self.__class__.__name__))

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        Logger.debug("Movement: Exiting: {stage}".format(stage=self.__class__.__name__))

    def on_leave(self, *args):
        super().on_leave(*args)
        Logger.debug("Movement: Exited: {stage}".format(stage=self.__class__.__name__))

    @staticmethod
    def check_for_winner(players):

        winner = "Nobody"
        mafia_count = 0
        towny_count = 0

        for player in players:
            if player.alive:
                if player.mafia:
                    mafia_count += 1
                else:
                    towny_count += 1

        if mafia_count == 0:
            winner = "Town"

        if towny_count == 0:
            winner = "Mafia"

        return winner


class MainMenu(Stage):
    def ready_game(self):
        self.initialize_settings()
        Stage.players = self.create_players(Stage.player_count, Stage.agent_number)


class Tutorial(Stage):
    pass


class PlayerStatus(Stage):
    pass


class StagesTutorial(Stage):
    pass


class Credits(Stage):
    pass


class Discussion(Stage):

    def submit(self):
        most_accused = Discussion.count_accusations(Stage.players)

        if most_accused is None:
            self.manager.current = "loadingTN"
        else:
            Logger.info("Discussion: Most accused player: {}".format(most_accused.name))
            Stage.players[most_accused.number].is_on_trial = True
            self.manager.current = "loadingDT"

    def get_player_class(self, player):
        if player.alive:
            if player.agent:
                new_player_class = PlayerIcon
            else:
                new_player_class = DiscussionPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

    def write_to_mafia_log(self, *args):
        output = "[b]Mafia List:[/b]\n"
        for player in self.players:
            if player.mafia and player.alive:
                output += f"{player.name}\n"
        self.mafia_text = output

    def write_to_action_log(self, *args):
        output = "[b]Action List:[/b]\n"
        for player in self.players:
            if player.actions['accuse']['player'] is not None:
                output += f"{player.number} accuses  {player.actions['accuse']['player'].number}\n"
            if player.actions['suspect']['player'] is not None:
                output += f"{player.number} suspects {player.actions['suspect']['player'].number}\n"
        self.action_text = output

    def on_enter(self):
        super().on_enter()
        Clock.schedule_interval(self.write_to_action_log, 0.5)
        Clock.schedule_interval(self.write_to_mafia_log, 0.5)
        self.add_players(Stage.players)

    def on_pre_leave(self):
        super().on_pre_leave()
        self.ids.circular_layout.clear_widgets()

    @staticmethod
    def count_accusations(players):
        """

        :return: A reference to the player to be put on trial, or None
        """
        accusations = [0] * len(players)
        suspicions = [0] * len(players)

        for player in players:
            if player.actions['accuse']['player'] is not None:
                accusations[player.actions['accuse']['player'].number] += 1
            if player.actions['suspect']['player'] is not None:
                suspicions[player.actions['suspect']['player'].number] += 1

        most_accused, accusation_amount = max(enumerate(accusations), key=lambda p: p[1])

        if dict(Counter(accusations))[accusation_amount] > 1:
            Logger.debug("Discussion: Accusation Counts: {}".format(dict(Counter(accusations))))
            Logger.info("Discussion: There was a tie amongst the accused.")
            # most_accused = max(suspicions, key=suspicions.get)
            # accusation_amount = max(suspicions.values())
            return None

            # if dict(Counter(suspicions.values()))[accusation_amount] > 1:
            #     Logger.info("Tie amongst the players, no one goes on trial.")
            #     return None

        return players[most_accused]


class Trial(Stage):
    player_on_trial = ObjectProperty()

    def get_player_class(self, player):
        if player.alive:
            if player.is_on_trial:
                new_player_class = PlayerIcon
            elif player.agent:
                new_player_class = TrialAgent
            else:
                new_player_class = TrialPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

    def submit(self):
        verdict = Trial.decide_verdict(Stage.players)
        self.player_on_trial.is_on_trial = False

        if verdict == "guilty":
            Logger.info("{} is guilty!".format(self.player_on_trial.name))
            self.player_on_trial.icon = "data/icons/player_dead.png"
            self.player_on_trial.alive = False
        elif verdict == "innocent":
            Logger.info("{} is innocent!".format(self.player_on_trial.name))
            self.player_on_trial.icon = "data/icons/player_alive.png"
        elif verdict == "tie":
            Logger.info("{} split the votes and will be released!".format(self.player_on_trial.name))
            # This could be changed so that the result is decided by a coin toss or something similar.
            self.player_on_trial.icon = "data/icons/player_alive.png"

        winner = Stage.check_for_winner(Stage.players)
        if winner == "Nobody":
            self.manager.current = "loadingTN"
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = "{} wins!".format(winner)
            self.manager.current = "gameovermenu"

    def on_enter(self, *args):
        super().on_enter(*args)

        if not any(player.is_on_trial for player in Stage.players):
            Logger.error("Trial: No player has the is_on_trial variable set to true in the trial stage!")

        for player in Stage.players:
            if player.is_on_trial:
                self.player_on_trial = player
                break

        if self.player_on_trial is None:
            Logger.error("Trial: No player was put on trial despite having entered the trial stage!")

        self.player_on_trial.icon = "data/icons/player_on_trial.png"
        self.add_players(Stage.players)

    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        self.ids.circular_layout.clear_widgets()

    @staticmethod
    def decide_verdict(players) -> str:
        """
        Step through the players, count their votes, and decide on a verdict.
        :return: A string with the value of guilty, innocent, or tie.
        """
        vote = {'guilty': 0, 'innocent': 0}

        for player in players:
            decision = player.actions['vote']['decision']

            if decision is None:
                Logger.warning("{} had None in their vote:decision field!".format(player.name))
                continue

            if decision == "abstain":
                Logger.info("{} decided to abstain.".format(player.name))
                continue

            Logger.info("{} voted {}".format(player.name, decision))
            vote[decision] += 1

        if vote['guilty'] == vote['innocent']:
            verdict = "tie"
            Logger.info("The vote was a tie.")
        else:
            verdict = max(vote, key=vote.get)
            Logger.info("The verdict was {}.".format(verdict))

        return verdict


class Night(Stage):

    def get_player_class(self, player):
        if player.alive:
            if player.mafia:
                new_player_class = NightMafiaPlayer
            else:
                new_player_class = NightSleepingPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

    def submit(self):
        if self.selected_player:
            Stage.players[self.selected_player.number].die()

        winner = Stage.check_for_winner(Stage.players)
        if winner == "Nobody":
            self.manager.current = "loadingND"
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = "{} wins!".format(winner)
            self.manager.current = "gameovermenu"

    def on_enter(self):
        super().on_enter()
        # for player in self.players:
        #     # TODO: Move all the add_players methods into each stage's on_enter method.
        #     if player.alive:
        #         if player.mafia:
        #             player.icon = "data/icons/player_alive_mafia.png"
        #         else:
        #             player.icon = "data/icons/player_asleep.png"

        self.add_players(Stage.players)

    def on_pre_leave(self):
        super().on_pre_leave()

        for player in self.players:
            # if player.alive:
            #     if player.agent:
            #         player.icon = "data/icons/agent_alive.png"
            #     else:
            #         player.icon = "data/icons/player_alive.png"
            player.actions = {"accuse": {"player": None}, "suspect": {"player": None}, "vote": {"decision": "abstain"}}

        self.ids.circular_layout.clear_widgets()


class GameOverMenu(Stage):
    def ready_game(self):
        self.initialize_settings()
        Stage.players = self.create_players(Stage.player_count, Stage.agent_number)


class LoadingScreen(Stage):
    def on_enter(self):
        super().on_enter()
        players = list(map(dict, Stage.players))
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
        agent = None

        for player in players:
            if player.agent:
                agent = player
                break

        if agent.alive:
            for player in players:
                if player.agent:
                    continue

                if player.alive:
                    choices.append(player)

        if choices:
            poor_devil = random.choice(choices)
            agent.actions['accuse']['player'] = poor_devil
            agent.actions['vote']['decision'] = "guilty" if random.random() > 0.5 else "innocent"
        players = list(map(dict, players))
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
        json_data = json.loads(json_players)
        output_data = [0] * len(json_data)
        for person_data in json_data:
            player = Player(**person_data)
            player.number = int(player.number)
            output_data[player.number] = player

        # Change the player names in the dict to actual player references
        for player in output_data:
            for action, attributes in player.actions.items():
                for attribute, value in attributes.items():
                    if attribute == "player" and value is not None:
                        output_data[player.number].actions[action][attribute] = output_data[value]

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


