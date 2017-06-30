from functools import partial
import inspect
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

try:
    from border_behavior import BorderBehavior
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior


try:
    Builder.load_file('mafiademonstration/player.kv')
except FileNotFoundError:
    Builder.load_file('../mafiademonstration/player.kv')


class Player(BoxLayout, BorderBehavior):
    name = StringProperty("player")
    number = NumericProperty(0)
    icon = StringProperty()
    alive = BooleanProperty(True)
    mafia = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    # Holds a reference to the action that is to be taken on another player.
    current_action = StringProperty()
    actions = DictProperty()

    def __iter__(self):
        flattened_actions = self.actions.copy()
        for action, decision in self.actions.items():
            flattened_actions[action] = decision.copy()
            for key, value in decision.items():
                if hasattr(value, "name"):
                    flattened_actions[action][key] = value.name
        return iter([('name', self.name),
                     ('number', self.number),
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
        stage.players[self.name].alive = self.alive = False
        stage.players[self.name].icon = self.icon = "data/icons/player_dead.png"

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
        Logger.debug("Method Call: {}".format(inspect.currentframe().f_code.co_name))

        self.current_action = action.lower()
        Logger.info("Player: {name} is ready to {action}".format(name=self.name, action=self.current_action))
        Logger.debug("Player: {}.current_action: {}".format(self.name, self.current_action))

        if self.current_action == "die":
            self.die()

        if self.current_action == "guilty" or self.current_action == "innocent":
            stage.players[self.name].actions["vote"]["decision"] = self.current_action

        Logger.debug("Method Exit: {}".format(inspect.currentframe().f_code.co_name))
        stage.selected_player = self

    def act_on(self, player) -> None:
        assert self.actions is not None
        assert player is not None
        assert issubclass(type(self), Player)
        assert self.actions != {}
        Logger.debug("Method Call: {}".format(inspect.currentframe().f_code.co_name))

        Logger.debug("Player: {}.actions: {}".format(self.name, self.actions))
        Logger.debug("Player: {}.actions: {}".format(player.name, player.actions))
        if self == player:
            Logger.debug("Player: {} tried to act on themselves.".format(type(self.name)))
            # TODO: Figure out how I want to handle this.
            Logger.debug("Method Exit: {}".format(inspect.currentframe().f_code.co_name))
            return

        if self.current_action.lower() != 'abstain':
            self.actions[self.current_action]['player'] = player
        Logger.info("Player: {self} {action} {other}".format(self=self.name,
                                                             action=self.current_action,
                                                             other=player.name))
        Logger.debug("Method Exit: {}".format(inspect.currentframe().f_code.co_name))

    def show_bubble(self) -> None:
        Logger.debug("Method Call: {}".format(inspect.currentframe().f_code.co_name))
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
        Logger.debug("Method Exit: {}".format(inspect.currentframe().f_code.co_name))

    def hide_bubble(self, instance, *args):
        Logger.debug("Method Call: {}".format(inspect.currentframe().f_code.co_name))
        self.ids.empty.remove_widget(self.bubb)
        Logger.debug("Method Exit: {}".format(inspect.currentframe().f_code.co_name))


class DiscussionPlayer(Player):
    pass


class NightSleepingPlayer(Player):
    pass


class TrialPlayer(Player):
    pass


class PlayerIcon(Player):
    pass


class DeadPlayer(Player):
    pass
