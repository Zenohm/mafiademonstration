# -*- coding: utf-8 -*-

# import webbrowser
import copy  # Going to be used to create deep copy of players for records.

import kivy
kivy.require('1.9.1')

# from kivy.animation import Animation
from kivy.app import App
# from kivy.clock import Clock
from kivy.garden.circularlayout import CircularLayout
from kivy.garden.modernmenu import ModernMenu
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty, BoundedNumericProperty, DictProperty,
    ObjectProperty, StringProperty, ListProperty, NumericProperty
)
# from kivy.uix.carousel import Carousel
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.label import Label
# from kivy.uix.progressbar import ProgressBar
from os.path import join, dirname

try:
    from mafiademonstration.border_behavior import BorderBehavior
except ModuleNotFoundError:
    from border_behavior import BorderBehavior

# TIMER_OPTIONS = {
#     '1/60 sec': 1 / 60.0,
#     '1/30 sec': 1 / 30.0,
#     '1/15 sec': 1 / 15.0,
# }


def _(text):
    """This is just so we can use the default gettext format."""
    return text


class ImageButton(BorderBehavior, ButtonBehavior, Image):
    pass


class ActionList(DropDown):
    pass


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
                            "kill": None,   "vote": None}
            self.alive = False
        if self.current_action == "die":
            self.actions = {}
            self.alive = False
            self.icon = "./data/icons/player_dead.png"
        return self

    def act_on(self, player):
        assert isinstance(player, type(self))

        if self == player:
            # TODO: Figure out how I want to handle this.
            return

        self.actions[self.current_action] = player
        Logger.info("{self} {action} {other}".format(self=self.name, action=self.current_action, other=player.name))
        return self


# class I18NLabel(Label):
    # """Label that supports internationlization."""
    # source_text = StringProperty('')


# class RefLabel(Label):
    # """Simple that opens a contained url in the webbrowser."""

    # def on_ref_press(self, url):
        # """Callback which is being run when the user clicks on a ref in the
        # label.

        # :param str url: URL to be opened in the webbrowser
        # """
        # Logger.info("Opening '{url}' in webbrowser.".format(url=url))
        # webbrowser.open(url)


# class TransitionProgress(ProgressBar):
    # """ProgressBar with pre-defined animations for fading in and out."""

    # _in = Animation(opacity=1.0, duration=0.4)
    # _out = Animation(opacity=0.0, duration=0.1)

    # def fade_in(self):
        # """Play the animation for changing the ProgressBar to be opaque."""
        # self._in.start(self)

    # def fade_out(self):
        # """Play the animation to hide the ProgressBar."""
        # self._out.start(self)


class MafiaDemonstrationApp(App):
    """Simple Slideshow App with a user defined title.

    Attributes:
      title (str): Window title of the application

      timer (:class:`kivy.properties.BoundedNumericProperty`):
        Helper for the slide transition of `carousel`

    """

    title = 'Mafia Demonstration'
    stages = ListProperty(['Discussion', 'Vote', 'Mafia'])
    stage = StringProperty('Discussion')
    cycle = NumericProperty(0)
    ready_to_submit = BooleanProperty(False)

    # language = StringProperty('en')
    # translation = ObjectProperty(None, allownone=True)

    # timer = BoundedNumericProperty(0, min=0, max=400)
    # carousel = ObjectProperty(Carousel)

    def __init__(self, language, **kwargs):
        # self.language = language
        # self.switch_lang(self.language)
        super(MafiaDemonstrationApp, self).__init__(**kwargs)

    def submit_conditions_met(self):
        """
        Used to check and see if all the conditions for pressing the submit
        button have been met.
        This includes all living players having selected someone to both accuse
        and suspect.
        """

        if self.cycle == 0:
            return True
        if all(player.alive for player in self.root.players.values()):
            Logger.debug("All players are alive.")
        # TODO: Perform all sorts of checks here.
        return True

    def submit(self):
        """
        Submits information to whatever backend we have communicating
        the individual player accusations and suspicions as well as
        who has been voted off or killed or anything else.
        """
        if self.submit_conditions_met():
            players = self.root.players
            players['player 2'].alive = False
            Logger.info("Submit button pressed")
            ready_to_submit = True
        else:
            # TODO: Figure out how to handle this.
            pass

    # def start_timer(self, *args, **kwargs):
        # """Schedule the timer update routine and fade in the progress bar."""
        # Logger.debug("Starting timer")
        # Clock.schedule_interval(self._update_timer, self.timer_interval)
        # self.progress_bar.fade_in()

    # def stop_timer(self, *args, **kwargs):
        # """Reset the timer and unschedule the update routine."""
        # Logger.debug("Stopping timer")
        # Clock.unschedule(self._update_timer)
        # self.progress_bar.fade_out()
        # self.timer = 0

    # def delay_timer(self, *args, **kwargs):
        # """Stop the timer but re-schedule it based on `anim_move_duration` of
        # :attr:`MafiaDemonstrationApp.carousel`.
        # """
        # self.stop_timer()
        # Clock.schedule_once(
            # self.start_timer,
            # self.carousel.anim_move_duration
        # )

    def build(self):
        """Initialize the GUI based on the kv file and set up events.

        Returns:
          (:class:`kivy.uix.anchorlayout.AnchorLayout`): Root widget specified
            in the kv file of the app
        """
        self.player_count = int(self.config.get('user_settings', 'player_count'))
        self.agent_number = int(self.config.get('user_settings', 'agent_number'))
        # self.language = self.config.get('user_settings', 'language')

        # user_interval = self.config.get('user_settings', 'timer_interval')
        # self.timer_interval = TIMER_OPTIONS[user_interval]

        players = dict()
        for player_number in range(1, self.player_count+1):
            player_name = 'player {}'.format(player_number)
            player = Player(name=player_name)
            player.number = player_number
            # player.borders = (2, "solid",(0,2,3,4))

            if player_number == self.agent_number:
                # All values that need to be set for the agent
                # should be set here.
                player.icon = './data/icons/agent.png'

            players[player_name] = player
            self.root.ids.circular_layout.add_widget(player)

        self.root.players = players
        # This will be used to keep track of who is acting against whom.
        self.root.selected_player = None

        # self.carousel = self.root.ids.carousel
        # self.progress_bar = self.root.ids.progress_bar
        # self.progress_bar.max = self.property('timer').get_max(self)

        # self.start_timer()
        # self.carousel.bind(on_touch_down=self.stop_timer)
        # self.carousel.bind(current_slide=self.delay_timer)

        # Allow the kivy-style access of the root widget.
        global app
        app = self

        return self.root

    def build_config(self, config):
        """Create a config file on disk and assign the ConfigParser object to
        `self.config`.
        """
        config.setdefaults(
            'user_settings', {
                'timer_interval': '1/60 sec',
                'language': 'en',
                'player_count': 6,
                'agent_number': 1,
            }
        )

    def build_settings(self, settings):
        """Read the user settings and create a panel from it."""
        settings_file =  join(dirname(__file__), 'user_settings.json')
        settings.add_json_panel(self.title, self.config, settings_file)

    def on_config_change(self, config, section, key, value):
        """Called when the user changes the config values via the settings
        panel. If `timer_interval` is being changed update the instance
        variable of the same name accordingly.
        """
        if config is self.config:
            token = (section, key)
            if token == ('user_settings', 'timer_interval'):
                pass
                # self.timer_interval = TIMER_OPTIONS[value]
            elif token == ('user_settings', 'language'):
                self.language = value
            elif token == ('user_settings', 'player_count'):
                self.player_count = value
            elif token == ('user_settings', 'agent_number'):
                self.agent_number = value

    def on_pause(self):
        """Enables the user to switch to another application causing
        :class:`MafiaDemonstrationApp` to wait until the user
        switches back to it eventually.
        """
        return True

    def on_resume(self):
        """Called when the app is resumed. Used to restore data that has been
        stored in :meth:`MafiaDemonstrationApp.on_pause`.
        """
        pass

    # def _update_timer(self, dt):
        # try:
            # self.timer += 1
        # except ValueError:
            # self.stop_timer()
            # self.carousel.load_next()
            # Logger.debug("Automatically loading next slide")

    # def on_language(self, instance, language):
        # self.switch_lang(language)

    # def switch_lang(self, language):
        # locale_dir = join(dirname(dirname(__file__)), 'data', 'locales')
        # locales = gettext.translation(
            # 'mafiademonstration', locale_dir, languages=[self.language]
        # )

        # if sys.version_info.major >= 3:
            # self.translation = locales.gettext
        # else:
            # self.translation = locales.ugettext
