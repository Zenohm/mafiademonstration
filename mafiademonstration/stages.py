from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

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
            text: 'Mafia Game Logo'

        BoxLayout:
            orientation: 'horizontal'
            cols: 3

            Label:

            GridLayout:
                rows: 4
                row_force_default: True
                row_default_height: 50
                spacing: [10, 10]

                Label:

                Button:
                    text: 'Start'
                    on_press: root.manager.current = 'loading'

                Button:
                    text: 'Settings'
                    on_press: root.manager.current = 'settings'

                Button:
                    text: 'Exit'
                    on_press: exit()

            Label:

# <SettingsItem>
#     text: ''
#
#     Label:
#         id: item_info
#         color: to_rgba("212121")
#         # size_hint_x: None
#         anchor_x: 'left'
#         text: root.text
#
#     Button:
#         id: item_input
#         size_hint_x: 0.3
#         anchor_x: 'right'
#         text: 'testing'
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
        orientation: 'vertical'
        padding: [20, 25]

        Label:
            size_hint_x: None
            size_hint_y: 0.1
            color: to_rgba("212121")
            halign: 'left'
            markup: True
            text: '[b]Settings[/b]'

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
                halign: 'left'
                text: 'testing'

            TextInput:
                size_hint_x: 2
                text: 'testing'

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: 'left'
                text: 'testing'

            TextInput:
                size_hint_x: 2
                text: 'testing'

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: 'left'
                text: 'testing'

            TextInput:
                size_hint_x: 2
                text: 'testing'

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: 'left'
                text: 'testing'

            TextInput:
                size_hint_x: 2
                text: 'testing'

            Label:
                size_hint_x: None
                color: to_rgba("212121")
                halign: 'left'
                text: 'testing'

            TextInput:
                size_hint_x: 2
                text: 'testing'

        Label:
            size_hint_y: 0.1

        Button:
            size_hint: (0.35, 0.15)
            pos_hint: {'center_x': 0.825}
            text: 'Return'
            on_press: root.manager.current = 'menu'


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
            text: 'Loading...'

""")


# class SettingsItem(AnchorLayout):
#     pass

class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class LoadingScreen(Screen):
    pass


class DiscussionScreen(Screen):
    pass


class TrialScreen(Screen):
    pass


class NightScreen(Screen):
    pass


class EndGameScreen(Screen):
    pass

sm = ScreenManager(transition=NoTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(LoadingScreen(name='loading'))
sm.add_widget(DiscussionScreen(name='discussion'))
sm.add_widget(TrialScreen(name='trial'))
sm.add_widget(NightScreen(name='night'))
sm.add_widget(EndGameScreen(name='endgame'))


class Stages(App):

    def build(self):
        return sm

if __name__ == '__main__':
   Stages().run()

