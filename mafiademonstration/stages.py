from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.garden.circularlayout import CircularLayout
from kivy.garden.modernmenu import ModernMenu
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty, BoundedNumericProperty, DictProperty,
    ObjectProperty, StringProperty, ListProperty, NumericProperty
)


try:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.player import Player
except ModuleNotFoundError:
    from border_behavior import BorderBehavior
    from player import Player


Builder.load_string("""
#:import to_rgba kivy.utils.get_color_from_hex

<MenuScreen>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size

    GridLayout:
        rows: 2

        Label:
            color: to_rgba("212121")
            text: "Mafia Game Logo"

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
                    text: "Start"
                    on_press: root.manager.current = "loading"

                Button:
                    text: "Settings"
                    on_press: root.manager.current = "settings"

                Button:
                    text: "Exit"
                    on_press: exit()

            Label:

# <SettingsItem>
#     text: ""
#
#     Label:
#         id: item_info
#         color: to_rgba("212121")
#         # size_hint_x: None
#         anchor_x: "left"
#         text: root.text
#
#     Button:
#         id: item_input
#         size_hint_x: 0.3
#         anchor_x: "right"
#         text: "testing"
#


<SettingsScreen>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: [20, 25]

        Label:
            size_hint_x: None
            size_hint_y: 0.1
            color: to_rgba("212121")
            halign: "left"
            markup: True
            text: "[b]Settings[/b]"

        GridLayout:
            cols: 2
            rows: 6
            row_default_height: 10
            spacing: [10, 10]

            Label:
                size_hint: (6, 0.2)

            Label:
                size_hint: (2, 0.2)

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: "left"
                text: "Number of Players"

            TextInput:
                id: player_count
                size_hint_x: 2
                text: "6"

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: "left"
                text: "Number of Autonomous Agents"

            TextInput:
                id: agent_number
                size_hint_x: 2
                text: "0"

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: "left"
                text: "testing"

            TextInput:
                size_hint_x: 2
                text: "testing"

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: "left"
                text: "testing"

            TextInput:
                size_hint_x: 2
                text: "testing"

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: "left"
                text: "testing"

            TextInput:
                size_hint_x: 2
                text: "testing"

        Label:
            size_hint_y: 0.1

        Button:
            size_hint: (0.35, 0.15)
            pos_hint: {"center_x": 0.825}
            text: "Return"
            on_press: root.manager.current = "menu"


<LoadingScreen>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size

    BoxLayout:
        Label:
            color: to_rgba("212121")
            text: "Loading..."
        Button:
            text: "Next Screen"
            on_press: root.manager.current = "discussion"

<DiscussionScreen>:
    AnchorLayout:
        players: {}
        selected_player: None
        ready_to_submit: False
        on_ready_to_submit: submit_button = "./data/icons/submit_complete.png" if ready_to_submit else "./data/icons/submit_incomplete.png"
        canvas.before:
            Color:
                rgba: to_rgba("F5F5F5")
            Rectangle:
                pos: self.pos
                size: self.size

        ImageButton:
            id: submit_button
            source: "./data/icons/submit_incomplete.png"
            color: to_rgba("05F5F5")
            on_press: root.submit(); root.manager.current = 'trial'
            size_hint: .2, .2
            borders: 2, "solid", (1,1,1,1.)

        CircularLayout:
            id: circular_layout
            direction: "ccw"
            inner_radius_hint: 1
            outer_radius_hint: 1.5
            size_hint_x: 0.6
            size_hint_y: 0.5
            start_angle: 60

<TrialScreen>:
    Button:
        text: 'press me'
        on_press: root.manager.current = 'night'


<NightScreen>:
    AnchorLayout:
        players: {}
        selected_player: None
        ready_to_submit: False
        on_ready_to_submit: submit_button = "./data/icons/submit_complete.png" if ready_to_submit else "./data/icons/submit_incomplete.png"
        canvas.before:
            Color:
                rgba: to_rgba("0D47A1")
            Rectangle:
                pos: self.pos
                size: self.size

        ImageButton:
            id: submit_button
            source: "./data/icons/submit_incomplete.png"
            color: to_rgba("05F5F5")
            on_press: root.submit(); root.manager.current = 'discussion'
            size_hint: .2, .2
            borders: 2, "solid", (1,1,1,1.)

        CircularLayout:
            id: circular_layout
            direction: "ccw"
            inner_radius_hint: 1
            outer_radius_hint: 1.5
            size_hint_x: 0.6
            size_hint_y: 0.5
            start_angle: 60

<EndGameScreen>:
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size

    GridLayout:
        rows: 2

        Label:
            color: to_rgba("212121")
            text: "End Game!"

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
                    on_press: root.manager.current = "loading"

                Button:
                    text: "Main Menu"
                    on_press: root.manager.current = "settings"

                Button:
                    text: "Exit"
                    on_press: exit()

            Label:

""")

class Stage(Screen):
    selected_player = ObjectProperty()
    players = ListProperty()
    next_stage = StringProperty()

    def __init__(self, **kwargs):
        super(Stage, self).__init__(**kwargs)

    def enter(self, **kwargs):
        pass

    def exit(self, **kwargs):
        pass

# class SettingsItem(AnchorLayout):
#     pass

class MenuScreen(Stage):
    pass


class SettingsScreen(Stage):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.player_count = 6



class LoadingScreen(Stage):
    pass


class DiscussionScreen(Stage):
    def __init__(self, **kwargs):
        super(DiscussionScreen, self).__init__(**kwargs)
        self.player_count = 6 #int(self.config.get('settings', 'player_count'))
        self.agent_number = 0 #int(self.config.get('settings', 'agent_number'))
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

        players = dict()
        for player_number in range(1, self.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = Player(name=player_name)
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

class TrialScreen(Stage):
    pass


class NightScreen(Stage):
    def __init__(self, **kwargs):
        super(NightScreen, self).__init__(**kwargs)
        self.player_count = 6 #int(self.config.get('settings', 'player_count'))
        self.agent_number = 0 #int(self.config.get('settings', 'agent_number'))
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

        players = dict()
        for player_number in range(1, self.player_count + 1):
            player_name = 'player {}'.format(player_number)
            player = Player(name=player_name)
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



class EndGameScreen(Stage):
    pass


class ImageButton(BorderBehavior, ButtonBehavior, Image):
    pass


class ActionList(DropDown):
    pass
