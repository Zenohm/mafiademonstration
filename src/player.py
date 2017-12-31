from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex as to_rgba
from kivy.properties import (
        BooleanProperty, DictProperty,
        StringProperty, NumericProperty
)
from kivy.logger import Logger
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

try:
    from border_behavior import BorderBehavior
    from hover_behavior import HoverBehavior
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.hover_behavior import HoverBehavior


try:
    Builder.load_file('src/player.kv')
except FileNotFoundError:
    Builder.load_file('../src/player.kv')


class Player(BoxLayout, BorderBehavior):
    name = StringProperty("player")
    number = NumericProperty(0)
    icon = StringProperty()
    alive = BooleanProperty(True)
    mafia = BooleanProperty(False)
    agent = BooleanProperty(False)
    is_on_trial = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    # Holds a reference to the action that is to be taken on another player.
    current_action = StringProperty()
    actions = DictProperty()

    def __iter__(self):
        flattened_actions = self.actions.copy()
        for action, decision in self.actions.items():
            flattened_actions[action] = decision.copy()
            for key, value in decision.items():
                if hasattr(value, "number"):
                    flattened_actions[action][key] = value.number

        return iter([('name', self.name),
                     ('agent', self.agent),
                     ('number', self.number),
                     ('is_on_trial', self.is_on_trial),
                     ('icon', self.icon),
                     ('mafia', self.mafia),
                     ('alive', self.alive),
                     ('strategic_value', self.strategic_value),
                     ('current_action', self.current_action),
                     ('actions', flattened_actions)])

    def suspect(self, other):
        pass

    def accuse(self, other):
        pass

    def kill(self, other):
        pass

    def die(self):
        stage = App.get_running_app().root.current_screen
        stage.players[self.number].alive = self.alive = False
        stage.players[self.number].icon = self.icon = "data/icons/player_dead.png"

    def set_strategic_value(self, strategic_value):
        tolerance = 1.5

        if strategic_value > tolerance:
            self.borders = (2, "solid", to_rgba("05F5F5"))
        elif strategic_value < tolerance:
            self.borders = (2, "solid", to_rgba("05F5F5"))
        else:
            self.borders = (2, "solid", to_rgba("05F5F5"))

        self.update_borders()

    def ready_action(self, action) -> None:
        """
        Designate the current player as the one who will be performing actions.
        This is done by setting the player instance as the selected player.
        """
        stage = App.get_running_app().root.current_screen
        self.current_action = action.lower()
        stage.selected_player = self
        Logger.info(f"Player: {self.name} readies {self.current_action}")

        if self.current_action == "die":
            self.die()

        if self.current_action == "guilty" or self.current_action == "innocent":
            stage.players[self.number].actions["vote"]["decision"] = self.current_action

        if self.current_action == "abstain":
            # Fix Issue #17
            stage.players[self.number].actions["accuse"]["player"] = None
            stage.players[self.number].actions["suspect"]["player"] = None
            stage.selected_player = None

    def act_on(self, player) -> None:
        assert self.actions is not None
        assert player is not None
        assert issubclass(type(self), Player)
        assert self.actions != {}

        self.current_action = self.current_action.lower()

        if self == player:
            Logger.warning(f"Player: {self.name} tried to act on themselves.")
            return

        if self.current_action == 'suspect' and self.actions["accuse"]["player"] != player:
            self.actions["suspect"]['player'] = player
        elif self.current_action == 'accuse' and self.actions["suspect"]["player"] != player:
            self.actions["accuse"]['player'] = player

        Logger.info(f"Player: {self.name} {self.current_action} {player.name}")

    def show_bubble(self) -> None:
        self.bubb = Bubble(size_hint=(None, None),
                           size=(160, 30),
                           pos_hint={'center_x': .5, 'y': .6})
        accuse = BubbleButton(text='Accuse')
        suspect = BubbleButton(text='Suspect')
        accuse.bind(on_press=partial(self.hide_bubble, accuse))
        suspect.bind(on_press=partial(self.hide_bubble, suspect))
        self.bubb.add_widget(accuse)
        self.bubb.add_widget(suspect)
        self.ids.empty.add_widget(self.bubb)

    def hide_bubble(self, instance, *args):
        self.ids.empty.remove_widget(self.bubb)


class PlayerIcon(Player):
    """
    Used for dead players and other unclickable player icons.
    """
    pass


class DiscussionPlayer(Player):
    pass


class NightMafiaPlayer(Player):
    pass


class NightSleepingPlayer(Player):
    pass


class TrialPlayer(Player):
    pass


class TrialAgent(Player):
    pass


class ImageButton(BorderBehavior, ButtonBehavior, Image, HoverBehavior):
    pass

