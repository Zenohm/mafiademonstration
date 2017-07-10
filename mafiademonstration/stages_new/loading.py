class LoadingScreen(Stage):
    def on_enter(self):
        super().on_enter()
        players = list(map(dict, Stage.players))
        json_players = LoadingScreen.to_json(players)
        json_players_modified = LoadingScreen.call_reasoner(json_players)
        Stage.players = LoadingScreen.from_json(json_players_modified)
        self.exit()

    def exit(self):
        pass

    @staticmethod
    def call_reasoner(json_players):
        players = LoadingScreen.from_json(json_players)
        # Simulate a slow reasoner
        # import time
        # time.sleep(3)

        choices = []
        agent = None

        for player in players:
            if player.agent:
                agent = player
                break

        if agent.alive:
            for player in players:
                if player.agent:
                    continue

                if player.alive:
                    choices.append(player)

        if choices:
            poor_devil = random.choice(choices)
            agent.actions['accuse']['player'] = poor_devil
            agent.actions['vote']['decision'] = "guilty" if random.random() > 0.5 else "innocent"
        players = list(map(dict, players))
        json_players_modified = LoadingScreen.to_json(players)
        return json_players_modified

    @staticmethod
    def to_json(player_list) -> str:
        """
        Convert player object to standard language for transmission
        between various outside reasoners.
        """
        return json.dumps(player_list)

    @staticmethod
    def from_json(json_players):
        """
        Read a list of players in a standard format and convert it
        into a list of Player objects.
        """
        json_data = json.loads(json_players)
        output_data = [0] * len(json_data)
        for person_data in json_data:
            player = Player(**person_data)
            player.number = int(player.number)
            output_data[player.number] = player

        # Change the player names in the dict to actual player references
        for player in output_data:
            for action, attributes in player.actions.items():
                for attribute, value in attributes.items():
                    if attribute == "player" and value is not None:
                        output_data[player.number].actions[action][attribute] = output_data[value]

        return output_data


class LoadingDT(LoadingScreen):
    def exit(self):
        self.manager.current = "trial"


class LoadingTN(LoadingScreen):
    def exit(self):
        self.manager.current = "night"


class LoadingND(LoadingScreen):
    def exit(self):
        self.manager.current = "discussion"

