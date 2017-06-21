from functools import partial
import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
        BooleanProperty, DictProperty,
        StringProperty, NumericProperty
)
from kivy.logger import Logger
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton

try:
    from mafiademonstration.border_behavior import BorderBehavior
except ModuleNotFoundError:
    from border_behavior import BorderBehavior


try:
    Builder.load_file('mafiademonstration/player.kv')
except FileNotFoundError:
    Builder.load_file('../mafiademonstration/player.kv')


class Player(BoxLayout, BorderBehavior):
    name = StringProperty()
    number = NumericProperty()
    icon = StringProperty()
    alive = BooleanProperty(True)
    mafia = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    # Holds a reference to the action that is to be taken on another player.
    current_action = StringProperty()
    actions = DictProperty()

    def ready_action(self, action) -> object:
        """
        Designate the current player as the one who will be performing actions.
        This is done by setting the player instance as the selected player.
        """
        self.current_action = action.lower()
        Logger.info("{name} is ready to {action}".format(
            name=self.name,
            action=self.current_action
        ))
        Logger.debug("{} said by the ready_action method".format(type(self.actions)))

        if self.current_action == "clear":
            self.alive = False
        if self.current_action == "die":
            self.alive = False
            self.icon = "data/icons/player_dead.png"
        return self

    def act_on(self, player) -> None:
        assert self.actions is not None
        assert player is not None
        assert issubclass(type(self), Player)
        assert self.actions != {}

        Logger.debug("{} said by the act_on method".format(type(self.actions)))
        if self == player:
            # TODO: Figure out how I want to handle this.
            return

        Logger.debug("ID in Player:act_on: {}".format(id(self.actions)))
        if self.current_action.lower() != 'abstain':
            self.actions[self.current_action]['player'] = player
        Logger.info("{self} {action} {other}".format(self=self.name,
                    action=self.current_action, other=player.name))

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

    def to_json(self) -> str:
        """
        Convert player object to standard language for transmission
        between various outside reasoners.
        """
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_players):
        """
        Read a list of players in a standard format and convert it
        into a list of Player objects.
        """
        output_data = list()
        json_data = json.loads(json_players)
        for person_data in json_data:
            output_data.append(Player(**person_data))
        App.get_running_app().root.Stage.players = output_data


class DiscussionPlayer(Player):
    pass


class NightPlayer(Player):
    pass


class TrialPlayer(Player):
    pass
