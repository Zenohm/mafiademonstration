from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
        BooleanProperty, DictProperty,
        StringProperty, NumericProperty
)
from kivy.logger import Logger

try:
    from mafiademonstration.border_behavior import BorderBehavior
except ModuleNotFoundError:
    from border_behavior import BorderBehavior


try:
    Builder.load_file('mafiademonstration/player.kv')
except FileNotFoundError:
    Builder.load_file('player.kv')


class Player(BoxLayout, BorderBehavior):
    name = StringProperty("")
    number = NumericProperty(0)
    alive = BooleanProperty(True)
    mafia = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    # Holds a reference to the action that is to be taken on another player.
    current_action = StringProperty()
    actions = DictProperty()

    def ready_action(self, action):
        """
        Designate the current player as the one who will be performing actions.
        This is done by setting the player instance as the selected player.
        """
        self.current_action = action.lower()
        Logger.info("{name} is ready to {action}".format(
            name=self.name,
            action=self.current_action
        ))

        if self.current_action == "clear":
            self.actions = {"accuse": None, "suspect": None,
                            "kill": None, "vote": None}
            self.alive = False
        if self.current_action == "die":
            self.actions = {}
            self.alive = False
            self.icon = "data/icons/player_dead.png"
        return self

    def act_on(self, player):
        print(player)
        assert issubclass(type(self), Player)

        if self == player:
            # TODO: Figure out how I want to handle this.
            return

        self.actions[self.current_action] = player
        Logger.info("{self} {action} {other}".format(self=self.name,
                    action=self.current_action, other=player.name))
        return self


class DiscussionPlayer(Player):
    pass


class NightPlayer(Player):
    pass


class TrialPlayer(Player):
    pass
