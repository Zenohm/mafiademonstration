from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty, DictProperty,
    StringProperty, NumericProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex as to_rgba

try:
    from border_behavior import BorderBehavior
    from hover_behavior import HoverBehavior
except ModuleNotFoundError:
    from mafiademonstration.border_behavior import BorderBehavior
    from mafiademonstration.hover_behavior import HoverBehavior

Builder.load_string("""
#:import to_rgba kivy.utils.get_color_from_hex
#:import Logger kivy.logger.Logger
""")


class Player(BoxLayout, BorderBehavior):
    Builder.load_string("""
<Player>:
    orientation: "vertical"
    on_is_alive: self.icon = self.icon_dead
    # The second layer in this dictionary is REQUIRED.
    # Shallow copy dragons will get angry if you flatten this dict. Hiss.
    actions: {"accuse": {"player": None}, "suspect": {"player": None}, "vote": {"decision": "abstain"}}

    Label:
        text: root.name
        size_hint_y: 0.2
        color: to_rgba("212121")
    """)

    name = StringProperty("player")
    number = NumericProperty(0)
    icon = StringProperty()
    icon_alive = StringProperty("data/icons/player_alive.png")
    icon_dead = StringProperty("data/icons/player_dead.png")
    is_alive = BooleanProperty(True)
    is_agent = BooleanProperty(False)
    is_mafia = BooleanProperty(False)
    is_on_trial = BooleanProperty(False)
    is_on_death_row = BooleanProperty(False)
    is_selected = BooleanProperty(False)
    strategic_value = NumericProperty(0)
    # Holds a reference to the action that is to be taken on another player.
    current_action = StringProperty("abstain")
    actions = DictProperty()

    selected_player = None

    def __init__(self, parent_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_instance = parent_instance

    def __iter__(self):
        flattened_actions = self.actions.copy()
        for action, decision in self.actions.items():
            flattened_actions[action] = decision.copy()
            for key, value in decision.items():
                if hasattr(value, "number"):
                    flattened_actions[action][key] = value.number

        return iter([('name', self.name),
                     ('icon', self.icon),
                     ('number', self.number),
                     ('is_alive', self.is_alive),
                     ('is_agent', self.is_agent),
                     ('is_mafia', self.is_mafia),
                     ('is_on_trial', self.is_on_trial),
                     ('strategic_value', self.strategic_value),
                     ('current_action', self.current_action),
                     ('actions', flattened_actions)])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Player(name={self.name}, number={self.number}, is_alive={self.is_alive}, is_agent={self.is_agent}, is_selected={self.is_selected})"

    def set_strategic_value(self, strategic_value):
        tolerance = 1.5

        if strategic_value > tolerance:
            self.borders = (2, "solid", to_rgba("05F5F5"))
        elif strategic_value < tolerance:
            self.borders = (2, "solid", to_rgba("05F5F5"))
        else:
            self.borders = (2, "solid", to_rgba("05F5F5"))

        self.update_borders()

    def ready_action(self, action) -> object:
        """
        Designate the current player as the one who will be performing actions.
        This is done by setting the player instance as the selected player.
        """
        self.current_action = action.lower()
        selected_player = self
        Logger.info(f"Player: {self.name} readies {self.current_action}")

        if self.current_action == "guilty" or self.current_action == "innocent":
            self.actions["vote"]["decision"] = self.current_action

        if self.current_action == "abstain":
            selected_player = None

        return selected_player

    def act_on(self, other_player) -> None:
        assert self.actions is not None
        assert self.actions != {}
        assert issubclass(type(self), Player)

        if other_player is None:
            Logger.warning("Player: There was an attempt to act on a non-existent player!")
            return

        if self == other_player:
            Logger.warning(f"Player: {self.name} tried to act on themselves.")
            return

        if self.current_action == "suspect" and self.actions["accuse"]["player"] != other_player:
            self.actions["suspect"]["player"] = other_player
        elif self.current_action == "accuse" and self.actions["suspect"]["player"] != other_player:
            self.actions["accuse"]["player"] = other_player

        Logger.info(f"Player: {self.name} {self.current_action} {other_player.name}")

    @staticmethod
    def change_selected_player(player):
        """
        There's something strange going on with Kivy and setting things based
        on instances. This is probably a result of having multiple instances of
        the singletons. Fuck Singletons.
        :param player:
        :return:
        """
        if Player.selected_player is not None:
            Player.selected_player.is_selected = False

        if player:
            if player.parent_instance:
                Player.selected_player = player.parent_instance
            else:
                Player.selected_player = player
            Player.selected_player.is_selected = True
        else:
            Player.selected_player = None


class PlayerIcon(Player):
    """
    Used for dead players and other unclickable player icons.
    """
    Builder.load_string("""
<PlayerIcon>:
    Image:
        source: root.icon
    """)


class DiscussionPlayer(Player):
    Builder.load_string("""
<DiscussionPlayer>:
    drop_widget: drop_down.__self__

    ImageButton:
        source: root.icon
        on_release:
            if root.selected_player: root.selected_player.act_on(root); root.change_selected_player(None)
            else: drop_down.open(self)

    DropDown:
        id: drop_down
        drop_down: drop_down.__self__
        on_select:
            Logger.info("{}".format(args[1]))

        Button:
            text: "Accuse"
            size_hint_y: None
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            height: "38dp"
            on_release:
                root.parent_instance.current_action = "accuse"
                root.change_selected_player(root)
                drop_down.select("Ready to accuse another player")

        Button:
            text: "Suspect"
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            size_hint_y: None
            height: "38dp"
            on_release:
                root.parent_instance.current_action = "suspect"
                root.change_selected_player(root)
                drop_down.select("Ready to suspect another player")

        Button:
            text: "Abstain"
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            size_hint_y: None
            height: "38dp"
            on_release:
                # Fix Issue #17
                root.parent_instance.current_action = "abstain"
                root._reset_actions()
                root.change_selected_player(None)
                drop_down.select("Abstaining from the vote")
    
    """)

    def _reset_actions(self):
        self.actions["accuse"]["player"] = None
        self.actions["suspect"]["player"] = None


class DiscussionAgent(Player):
    Builder.load_string("""
<DiscussionAgent>:
    ImageButton:
        source: root.icon
        on_release:
            if root.selected_player: root.selected_player.act_on(root); root.change_selected_player(None)
    """)


class NightMafiaPlayer(Player):
    Builder.load_string("""
<NightMafiaPlayer>:
    Image:
        source: "data/icons/player_alive_mafia.png"
    """)


class NightSleepingPlayer(Player):
    Builder.load_string("""
<NightSleepingPlayer>:
    Image:
        source: "data/icons/player_asleep.png"

    Button:
        text: "Kill"
        size_hint_y: 0.5
        color: to_rgba("F5F5F5")
        background_color: to_rgba("212121")
        on_press:
            root.change_selected_player(root)

    """)


class TrialPlayer(Player):
    Builder.load_string("""
<TrialPlayer>:
    drop_widget: drop_down.__self__

    Image:
        source: root.icon

    Button:
        text: drop_down.text
        size_hint_y: 0.4
        color: to_rgba("F5F5F5")
        background_color: to_rgba("212121")
        on_release: drop_down.open(self)

    DropDown:
        id: drop_down
        text: "Vote"
        drop_down: drop_down.__self__
        on_select:
            self.text = args[1]

        Button:
            text: "Guilty"
            size_hint_y: None
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            height: "38dp"
            on_release:
                root.actions["vote"]["decision"] = "guilty"
                Logger.info("Voted guilty.")
                drop_down.select(self.text)

        Button:
            text: "Innocent"
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            size_hint_y: None
            height: "38dp"
            on_release:
                root.actions["vote"]["decision"] = "innocent"
                Logger.info("Voted innocent.")
                drop_down.select(self.text)

        Button:
            text: "Abstain"
            color: to_rgba("F5F5F5")
            background_color: to_rgba("607D8B")
            size_hint_y: None
            height: "38dp"
            on_release:
                root.actions["vote"]["decision"] = "abstain"
                Logger.info("Abstained from the vote.")
                drop_down.select(self.text)
    """)


class TrialAgent(Player):
    Builder.load_string("""
<TrialAgent>:
    Image:
        source: root.icon

    Label:
        canvas.before:
            Color:
                rgba: to_rgba("212121")
            Rectangle:
                pos: self.pos
                size: self.size
        text: root.actions["vote"]["decision"].title()
        size_hint_y: 0.4
        color: to_rgba("F5F5F5")
    """)


class ImageButton(Image, ButtonBehavior, BorderBehavior):
    pass

