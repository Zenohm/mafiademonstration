class MainMenu(Stage):
    def ready_game(self):
        self.initialize_settings()
        Stage.players = self.create_players(Stage.player_count, Stage.agent_number)


class GameOverMenu(Stage):
    def ready_game(self):
        self.initialize_settings()
        Stage.players = self.create_players(Stage.player_count, Stage.agent_number)


class Tutorial(Stage):
    pass


class PlayerStatus(Stage):
    pass


class StagesTutorial(Stage):
    pass


class Credits(Stage):
    pass


