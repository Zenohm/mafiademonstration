import collections
import json
import math
import random

from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import (
    ObjectProperty
)
from kivy.uix.screenmanager import Screen

try:
    from border_behavior import BorderBehavior
    from player import (
        Player, PlayerIcon,
        DiscussionPlayer, DiscussionAgent,
        TrialPlayer, TrialAgent,
        NightSleepingPlayer, NightMafiaPlayer,
    )
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import (
        Player, PlayerIcon, DiscussionPlayer,
        NightSleepingPlayer, NightMafiaPlayer,
        TrialPlayer, TrialAgent
    )

Builder.load_string("""
#:import to_rgba kivy.utils.get_color_from_hex
#:import webbrowser webbrowser
#:import CircularLayout kivy.garden.circularlayout.CircularLayout
""")


class Stage(Screen):
    # Static variables
    players = list()
    player_count = 0
    agent_number = 0

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
                parent_instance=player,
                name=player.name,
                icon=player.icon,
                number=player.number,
                is_alive=player.is_alive,
                is_mafia=player.is_mafia,
                is_agent=player.is_agent,
                is_on_trial=player.is_on_trial,
                is_on_death_row=player.is_on_death_row,
                strategic_value=player.strategic_value,
                actions=player.actions
            )

            self.ids.circular_layout.add_widget(new_player)

    def load_stage(self, stage_name):
        """
        Acts as a helper function to transition between two screens while also
        passing through a loading screen in-between.
        The loading screen will send off data to the reasoner and set the game
        state using the response.
        :param stage_name: The name of the stage that will ultimately be transitioned to.
        :return: None
        """
        loading = self.manager.get_screen("loading")
        loading.next_stage = stage_name
        self.manager.current = "loading"

    def get_player_class(self, player):
        """
        Given a player, find the class that they are a member of
        during the current stage and return that class.
        :param player: A player that needs to be organized into a class.
        :return: The class that the given player belongs to in the current stage.
        """
        return self.__class__

    def on_enter(self, *args):
        """
        Called once the transition to a stage has been completed.
        :param args:
        :return: None
        """
        super().on_enter(*args)
        Logger.debug(f"Movement: Entered: {self.__class__.__name__}")

    def on_pre_leave(self, *args):
        """
        Called prior to beginning the transition between stages.
        :param args:
        :return: None
        """
        super().on_pre_leave(*args)
        Logger.debug(f"Movement: Exiting: {self.__class__.__name__}")

    @staticmethod
    def create_players(player_count, agent_number):
        """
        Create a list of players whose states will be used to instantiate
        specific types of players for each stage. Using the provided agent number,
        one of the players will be designated as an agent, who will be controlled
        autonomously by an outside reasoner.
        :param player_count: The number of players to create.
        :param agent_number: The index of the player which will become an autonomous agent.
        :return: A list of players with potentially one agent.
        """
        players = []

        for number in range(player_count):
            name = 'player {}'.format(number)
            icon_alive = "data/icons/player_alive.png"
            icon_dead = "data/icons/player_dead.png"
            icon = "data/icons/easter_egg.png" if random.random() < 0.01 else icon_alive
            agent = False

            players.append(Player(
                name=name,
                number=number,
                is_alive=True,
                is_mafia=False,
                is_agent=agent,
                is_on_death_row=False,
                icon=icon,
                icon_alive=icon_alive,
                icon_dead=icon_dead,
                strategic_value=0
            ))

        if 0 <= agent_number < player_count:
            new_agent = players[agent_number]
            Logger.debug("Player: Agent assuming the role of {}.".format(new_agent.name))

            # All values that need to be set for
            # the is_agent should be set here.
            new_agent.name = "agent"
            new_agent.icon_alive = "data/icons/agent_alive.png"
            new_agent.icon_dead = "data/icons/agent_dead.png"
            new_agent.icon = new_agent.icon_alive
            new_agent.is_agent = True

        number_of_mafia = math.floor(math.sqrt(player_count))
        mafia_members = random.sample(players, number_of_mafia)

        for player in mafia_members:
            player.is_mafia = True

        return players

    @staticmethod
    def check_for_winner(players):
        """
        Check the win conditions for both mafia and town.
        If either have met their win conditions, designate
        them as the winners!
        :param players: The list of players which hold the game state.
        :return: "Nobody" if nobody has won, else "Mafia" if the mafia has won and "Town" for the town.
        """

        winner = "Nobody"
        mafia_count = 0
        towny_count = 0

        for player in players:
            if player.is_alive:
                if player.is_mafia:
                    mafia_count += 1
                else:
                    towny_count += 1

        if mafia_count == 0:
            winner = "Town"

        if towny_count == 0:
            winner = "Mafia"

        return winner


class Menu(Stage):
    def ready_game(self):
        """
        Reads a configuration file and uses the values contained within
        to create a list of players. Uses that list of players to initialize
        the game state.
        :return: None
        """
        Config.read('mafiademonstration/mafiademonstration.ini')
        player_count = Config.getint('user_settings', 'player_count')
        agent_number = Config.getint('user_settings', 'agent_number')
        Stage.players = self.create_players(player_count, agent_number)


class MainMenu(Menu):
    Builder.load_string("""
<MainMenu>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            pos: self.pos
            size: self.size

    GridLayout:
        rows: 2

        BoxLayout:
            orientation: "vertical"
            Label:

            Image:
                source: "data/icons/logo.gif"

            Label:

        BoxLayout:
            orientation: "horizontal"
            cols: 3

            Label:

            GridLayout:
                rows: 5
                row_force_default: True
                row_default_height: 50
                spacing: [10, 10]

                Button:
                    text: "Start"
                    on_press:
                        root.ready_game()
                        root.manager.current = "discussion"

                Button:
                    text: "Settings"
                    on_press: app.open_settings()

                Button:
                    text: "Tutorial"
                    on_press: root.manager.current = "tutorial"

                Button:
                    text: "Credits"
                    on_press: root.manager.current = "credits"

                Button:
                    text: "Exit"
                    on_press: exit()

            Label:

    """)


class GameOverMenu(Menu):
    Builder.load_string("""
<GameOverMenu>:
    text: "[b]{} wins![/b]"
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: "vertical"

            Label:

            ImageButton:
                source: "data/icons/player_alive.png"
                on_press:
                    if self.source == "data/icons/player_alive.png": self.source = "data/icons/player_alive_old.png"
                    else: self.source = "data/icons/player_alive.png"
            Label:
                color: to_rgba("212121")
                text: root.text
                markup: True

        BoxLayout:
            orientation: "horizontal"
            cols: 3

            Label:

            GridLayout:
                rows: 4
                row_force_default: True
                row_default_height: 50
                spacing: [10, 10]

                Label:

                Button:
                    text: "Restart"
                    on_press:
                        root.ready_game()
                        root.manager.current = "discussion"

                Button:
                    text: "Main Menu"
                    on_press: root.manager.current = "mainmenu"

                Button:
                    text: "Exit"
                    on_press: exit()

            Label:

    """)


class TutorialMenu(Menu):
    Builder.load_string("""
<Tutorial>:
    GridLayout:
        rows: 8
        row_force_default: True
        row_default_height: 50
        spacing: [10, 10]

        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            color: to_rgba("212121")
            text: "[b]          Tutorials[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True

        Label:
            color: to_rgba("212121")
            text: "Please click one of the following categories for more information."
            text_size: self.size
            halign: 'center'
            valign: 'center'

        GridLayout:
            cols: 3
            Label:
            Button:
                text: "Player Status"
                text_size: self.size
                halign: 'center'
                valign: 'center'
                on_press: root.manager.current = "playerstatus"
            Label:

        GridLayout:
            cols: 3
            Label:
            Button:
                text: "Stages"
                text_size: self.size
                halign: 'center'
                valign: 'center'
                on_press: root.manager.current = "stagestutorial"
            Label:

        Label:
        Label:
        Label:

    FloatLayout:
        Button:
            text: "Main Menu"
            text_size: self.size
            halign: 'center'
            valign: 'center'
            size_hint: [0.3, 0.075]
            pos: (root.width-self.width-15, 25)
            on_press: root.manager.current = "mainmenu"

    """)


class PlayerTutorial(Menu):
    Builder.load_string("""
<PlayerStatus>:
    GridLayout:
        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        rows: 6
        cols: 4
        padding: [0, 0, 5, 0]

        Label:
            color: to_rgba("212121")
            text: "[b]     Player Status[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True

        Label:
        Label:
        Label:

        Image:
            source: "data/icons/player_alive.png"
            halign: 'center'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Player is alive in discussion and trial stages"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/player_dead.png"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Player is dead"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/player_alive_mafia.png"
            halign: 'center'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Mafia awakes in night stage"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/player_asleep.png"
            halign: 'left'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Player is asleep in night stage"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/player_on_trial.png"
            halign: 'left'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Player is on trial"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/agent_alive.png"
            halign: 'left'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Autonomous agent"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Image:
            source: "data/icons/easter_egg.png"
            halign: 'center'
            valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "Detective (Coming Soon...!)"
            text_size: self.size
            halign: 'left'
            valign: 'center'

        Label:
        Label:
        Label:
        Label:
        Label:

    FloatLayout:
        Button:
            text: "Return"
            text_size: self.size
            halign: 'center'
            valign: 'center'
            size_hint: [.3, .075]
            pos: (root.width-self.width-15, 25)
            on_press: root.manager.current = "tutorial"

    """)


class StagesTutorial(Menu):
    Builder.load_string("""
<StagesTutorial>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            color: to_rgba("212121")
            text: "[b]Stages Tutorial[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint: [.3, .075]
            pos_hint: {"center_x": .175, "center_y": .95}
            markup: True

        Label:
            color: to_rgba("212121")
            text: "[b]Discussion Stage[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint: [.3, .075]
            pos_hint: {"center_x": .2, "center_y": .9}
            markup: True

        Label:
            color: to_rgba("212121")
            text: "This stage involves the townspeople accusing and suspecting people with specified reasons. Each player has the option of not choosing any option, allowing them to abstain from accusing or suspecting anyone. The person who is accused the most will go on trial, if nobody is accused then the stage will advance immediately to the night stage. After a night stage and in the beginning of the discussion stage, if there is a player being 'murdered,' there would be a public announcement, as well as revealing the identity of the eliminated player."
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint_x: .875
            pos_hint: {"center_x": .5, "center_y": .78}

        Label:
            color: to_rgba("212121")
            text: "[b]Trial Stage[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint: [.3, .075]
            pos_hint: {"center_x": .2, "center_y": .65}
            markup: True

        Label:
            color: to_rgba("212121")
            text: "The player who is being accused the most would be placed on trial. If the majority of the players vote to eliminate that player, he will be eliminated from the game, and his identity would be revealed to the public once he has been eliminated."
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint_x: .875
            pos_hint: {"center_x": .5, "center_y": .58}

        Label:
            color: to_rgba("212121")
            text: "[b]Night Stage[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint: [.3, .075]
            pos_hint: {"center_x": .2, "center_y": .5}
            markup: True

        Label:
            color: to_rgba("212121")
            text: "The night stage is where the Mafia members deciding on which player to kill and proceed to killing."
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint_x: .875
            pos_hint: {"center_x": .5, "center_y": .46}

        Image:
            source: "data/icons/submit_complete.png"
            halign: 'left'
            valign: 'center'
            size_hint: [.325, .325]
            pos_hint: {"center_x": .125, "center_y": .3}

        Label:
            color: to_rgba("212121")
            text: "[b]Stage transition button[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint: [.3, .075]
            pos_hint: {"center_x": .34, "center_y": .34}
            markup: True

        Label:
            color: to_rgba("212121")
            text: "The button which finalizes all the decisions made by the players and proceeds to the next stage."
            text_size: self.size
            halign: 'left'
            valign: 'center'
            size_hint_x: .75
            pos_hint: {"center_x": .57, "center_y": .295}

        Button:
            text: "Return"
            text_size: self.size
            halign: 'center'
            valign: 'center'
            size_hint: [.3, .075]
            pos: (root.width-self.width-15, 25)
            on_press: root.manager.current = "tutorial"
    """)


class Credits(Menu):
    Builder.load_string("""
<Credits>:
    GridLayout:
        rows: 16
        row_force_default: True
        row_default_height: 45
        spacing: [10, 10]

        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            color: to_rgba("212121")
            text: "[b]     Credits[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True

        Label:
            color: to_rgba("212121")
            text: "[b]               Written by:[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True

        GridLayout:
            rows: 2
            cols: 2
            padding: [150, 0, 75, 0]

            Label:
                color: to_rgba("212121")
                text: "Isaac Smith"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "Hei Jing Tsang"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "smitil01@students.ipfw.edu"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "tsangh@purdue.edu"
                text_size: self.size
                halign: 'left'
                valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "[b]               Advisors:[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True
        GridLayout:
            rows: 2
            cols: 2
            padding: [150, 0, 75, 0]

            Label:
                color: to_rgba("212121")
                text: "Prof. John Licato"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "Prof. Max Fowler"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "John.Licato@gmail.com"
                text_size: self.size
                halign: 'left'
                valign: 'center'

            Label:
                color: to_rgba("212121")
                text: "maxfwlr@gmail.com"
                text_size: self.size
                halign: 'left'
                valign: 'center'

        Label:
            color: to_rgba("212121")
            text: "[b]               Beta-testers:[b]"
            text_size: self.size
            halign: 'left'
            valign: 'center'
            markup: True

        Label:
            color: to_rgba("212121")
            text: "Cole Duncan, Reese Crowell"
            text_size: self.size
            halign: 'center'
            valign: 'center'

        Label:

        ImageButton:
            source: "data/icons/GitHub-Mark-120px-plus.png"
            halign: 'center'
            valign: 'center'
            markup: True
            on_press: webbrowser.open("https://www.github.com/zenohm/mafiademonstration")


        Label:

        GridLayout:
            cols: 3
            Label:
            Button:
                text: "Return"
                on_press: root.manager.current = "mainmenu"
            Label:

        Label:
        Label:
    """)


class Loading(Stage):
    Builder.load_string("""
<Loading>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        Image:
            source: "data/icons/loading.gif"
    """)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_stage = ""

    def exit(self):
        self.manager.current = self.next_stage

    def on_enter(self):
        json_players = Loading.to_json(Stage.players)
        json_players_modified = Loading.call_reasoner(json_players)
        Stage.players = Loading.from_json(json_players_modified)
        self.exit()

    @staticmethod
    def call_reasoner(json_players):
        players = Loading.from_json(json_players)
        # Simulate a slow reasoner
        # import time
        # time.sleep(3)

        choices = []
        agent = None

        for player in players:
            if player.is_agent:
                agent = player
                break

        if agent.is_alive:
            for player in players:
                if player.is_agent:
                    continue

                if player.is_alive:
                    choices.append(player)

        if choices:
            poor_devil = random.choice(choices)
            agent.actions['accuse']['player'] = poor_devil
            agent.actions['vote']['decision'] = "guilty" if random.random() > 0.5 else "innocent"
        json_players_modified = Loading.to_json(players)
        return json_players_modified

    @staticmethod
    def to_json(player_list) -> str:
        """
        Convert player object to standard language for transmission
        between various outside reasoners.
        """
        return json.dumps(list(map(dict, player_list)))

    @staticmethod
    def from_json(json_players) -> list:
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


class Discussion(Stage):
    Builder.load_string("""
<Discussion>:
    action_text: ""
    mafia_text: ""
    FloatLayout:
        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        ImageButton:
            source: "data/icons/menu_button.png"
            pos_hint: {"center_x": 0.95, "center_y": 0.05}
            size_hint: (0.1, 0.1)
            on_press: root.manager.current = "mainmenu"

        Label:
            text: root.action_text
            text_size: self.size
            halign: 'left'
            valign: 'top'
            markup: True
            color: to_rgba("212121")
            pos: (0, root.height-self.height)
            size_hint: .2, 1

        Label:
            text: root.mafia_text
            text_size: self.size
            halign: 'right'
            valign: 'top'
            markup: True
            color: to_rgba("212121")
            pos: (root.width-self.width, root.height-self.height)
            size_hint: .2, .3

        ImageButton:
            id: submit_button
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            source: "data/icons/submit_complete.png"
            size_hint: None, None
            size: "135dp", "135dp"
            on_press: root.submit()

        CircularLayout:
            id: circular_layout
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_y: 0.7
            start_angle: -180/len(self.children)-90 if len(self.children) else 0
            inner_radius_hint: 0.65
            outer_radius_hint: 1.2
            direction: "cw"
    """)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action_text = ""
        self.mafia_text = ""

    def submit(self):
        """
        Event Handler for stage transition button in the Discussion Stage.
        :return: None
        """
        most_accused_player = Discussion.count_accusations(Stage.players)

        Logger.info(f"Discussion: Most accused player: {str(most_accused_player)}")
        if most_accused_player is not None:
            most_accused_player.is_on_trial = True
            self.load_stage("trial")
        else:
            self.load_stage("night")

    def write_to_mafia_log(self, *args):
        output = "[b]Mafia List:[/b]\n"
        for player in self.players:
            if player.is_mafia and player.is_alive:
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

    def get_player_class(self, player):
        if player.is_alive:
            if player.is_agent:
                new_player_class = DiscussionAgent
            else:
                new_player_class = DiscussionPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

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

        if dict(collections.Counter(accusations))[accusation_amount] > 1:
            Logger.debug("Discussion: Accusation Counts: {}".format(dict(collections.Counter(accusations))))
            Logger.info("Discussion: There was a tie amongst the accused.")
            return None

        return players[most_accused]


class Trial(Stage):
    Builder.load_string("""
<Trial>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: to_rgba("F44336")
            Rectangle:
                pos: self.pos
                size: self.size

        ImageButton:
            source: "data/icons/menu_button.png"
            pos_hint: {"center_x": 0.95, "center_y": 0.05}
            size_hint: (0.1, 0.1)
            on_press: root.manager.current = "mainmenu"

        ImageButton:
            id: submit_button
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: None, None
            size: "135dp", "135dp"
            source: "data/icons/submit_complete.png"
            on_press: root.submit()

        CircularLayout:
            id: circular_layout
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_y: 0.7
            start_angle: -180/len(self.children)-90 if len(self.children) else 0
            inner_radius_hint: 0.65
            outer_radius_hint: 1.1
            direction: "cw"
    """)

    player_on_trial = ObjectProperty()

    def submit(self):
        verdict = Trial.decide_verdict(Stage.players)
        self.player_on_trial.is_on_trial = False

        if verdict == "guilty":
            Logger.info("{} is guilty!".format(self.player_on_trial.name))
            self.player_on_trial.icon = self.player_on_trial.icon_dead
            self.player_on_trial.is_alive = False
        elif verdict == "innocent":
            Logger.info("{} is innocent!".format(self.player_on_trial.name))
            self.player_on_trial.icon = self.player_on_trial.icon_alive
        elif verdict == "tie":
            Logger.info("{} split the votes and will be released!".format(self.player_on_trial.name))
            # This could be changed so that the result is decided by a coin toss or something similar.
            self.player_on_trial.icon = self.player_on_trial.icon_alive

        winner = Stage.check_for_winner(Stage.players)
        if winner == "Nobody":
            self.load_stage("night")
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = "{} wins!".format(winner)
            self.manager.current = "gameovermenu"

    def get_player_class(self, player):
        if player.is_alive:
            if player.is_on_trial:
                new_player_class = PlayerIcon
            elif player.is_agent:
                new_player_class = TrialAgent
            else:
                new_player_class = TrialPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

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
    Builder.load_string("""
<Night>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: to_rgba("2196F3")
            Rectangle:
                pos: self.pos
                size: self.size

        ImageButton:
            source: "data/icons/menu_button.png"
            pos_hint: {"center_x": 0.95, "center_y": 0.05}
            size_hint: (0.1, 0.1)
            on_press: root.manager.current = "mainmenu"

        ImageButton:
            id: submit_button
            source: "data/icons/submit_complete.png"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint: None, None
            size: "135dp", "135dp"
            on_press: root.submit()

        CircularLayout:
            id: circular_layout
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_y: 0.7
            start_angle: -180/len(self.children)-90 if len(self.children) else 0
            inner_radius_hint: 0.7
            outer_radius_hint: 1.2
            direction: "cw"
    """)

    def submit(self):
        victim = Night.find_poor_unfortunate_soul(Stage.players)

        if victim is not None:
            victim.is_alive = False

        winner = Stage.check_for_winner(Stage.players)
        if winner == "Nobody":
            self.load_stage("discussion")
        else:
            game_over = self.manager.get_screen("gameovermenu")
            game_over.text = "{} wins!".format(winner)
            self.manager.current = "gameovermenu"

    def get_player_class(self, player):
        if player.is_alive:
            if player.is_mafia:
                new_player_class = NightMafiaPlayer
            else:
                new_player_class = NightSleepingPlayer
        else:
            new_player_class = PlayerIcon

        return new_player_class

    def on_enter(self):
        super().on_enter()
        self.add_players(Stage.players)

    def on_pre_leave(self):
        super().on_pre_leave()

        for player in self.players:
            player.actions["accuse"]["player"] = None
            player.actions["suspect"]["player"] = None
            player.actions["vote"]["decision"] = "abstain"

        self.ids.circular_layout.clear_widgets()

    @staticmethod
    def find_poor_unfortunate_soul(players):
        for player in players:
            if player.is_selected:
                return player

        return None

