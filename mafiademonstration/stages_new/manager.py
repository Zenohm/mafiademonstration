from kivy.uix.screenmanager import ScreenManager, NoTransition

try:
    import stages
except ModuleNotFoundError:
    import mafiademonstration.stages as stages


class Stages(ScreenManager):
    transition = NoTransition()

    def build(self):
        self.add_widget(stages.MainMenu(name='mainmenu'))
        self.add_widget(stages.Discussion(name='discussion'))
        self.add_widget(stages.TutorialMenu(name='tutorial'))
        self.add_widget(stages.PlayerTutorial(name='playerstatus'))
        self.add_widget(stages.StagesTutorial(name='stagestutorial'))
        self.add_widget(stages.Credits(name='credits'))
        self.add_widget(stages.Trial(name='trial'))
        self.add_widget(stages.Night(name='night'))
        self.add_widget(stages.Loading(name='loading'))
        self.add_widget(stages.GameOverMenu(name='gameovermenu'))
        return self

