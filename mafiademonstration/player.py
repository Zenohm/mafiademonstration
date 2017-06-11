from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
        BooleanProperty, BoundedNumericProperty, DictProperty,
        ObjectProperty, StringProperty, ListProperty, NumericProperty
)
from kivy.logger import Logger

try:
    from mafiademonstration.border_behavior import BorderBehavior
except ModuleNotFoundError:
    from border_behavior import BorderBehavior



Builder.load_string("""
#:import to_rgba kivy.utils.get_color_from_hex

<Player>:
    name: "player"
    number: 0
    icon: "./data/icons/player_alive.png"
    alive: True
    on_alive: root.ready_action("die")
    mafia: False
    strategic_value: 0
    current_action: "accuse"
    # on_current_action: self.borders = (2, "solid", to_rgba("05F5F5")); self.update_borders()
    actions: {"accuse": {"player": None, "reason": None}, "suspect": {"player": None, "reason": None}, "kill": None, "vote": "abstain"}
    borders: 2, "solid", to_rgba("F5F5F5")

    orientation: "vertical"
    canvas.before:
        Color:
            rgba: to_rgba("F5F5F5")
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size
    ImageButton:
        source: root.icon
        on_press: app.root.selected_player.act_on(root) if app.root.selected_player else None
    Spinner:
        text: "Action"
        color: to_rgba("F5F5F5")
        background_color: to_rgba("212121")
        values: "Accuse", "Suspect", "Clear"
        on_text: app.root.selected_player = root.ready_action(self.text)
""")

class Player(BoxLayout, BorderBehavior):
    name = StringProperty("")
    number = NumericProperty(0)
    alive = BooleanProperty(True)
    mafia = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    current_action = StringProperty()  # Holds a reference to the action that is to be taken on another player.
    actions = DictProperty()

    def ready_action(self, action):
        """ Designate the current player as the one who will be performing actions.
            This is done by setting the self player instance as the selected player.
        """
        self.current_action = action.lower()
        Logger.info("{name} is ready to {action}".format(name=self.name,
                                                         action=self.current_action))

        if self.current_action == "clear":
            self.actions = {"accuse": None, "suspect": None,
                            "kill": None, "vote": None}
            self.alive = False
        if self.current_action == "die":
            self.actions = {}
            self.alive = False
            self.icon = "/data/icons/player_dead.png"
        return self

    def act_on(self, player):
        assert isinstance(player, type(self))

        if self == player:
            # TODO: Figure out how I want to handle this.
            return

        self.actions[self.current_action] = player
        Logger.info("{self} {action} {other}".format(self=self.name, action=self.current_action, other=player.name))
        return self

