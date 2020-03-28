import valve.source.a2s


class ServerInfo:

    def __init__(self, server_address):
        self.heartbeat(server_address)

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return vars(self)

    def heartbeat(self, server_address):
        """
        Queries the server to update the class with latest data.

        :param server_address: The server to query from.
        :return: None
        """
        self.SERVER_PORT = 27015

        # Allow only IP address to be entered instead of (IP, PORT) tuple
        if type(server_address) is not tuple:
            server_address = (server_address, self.SERVER_PORT)

        # Store information from the server query
        self.data = valve.source.a2s.ServerQuerier(server_address).info()

        # Populate remaining server attributes for easy access
        self.server_address = server_address
        self.response_type = self.data["response_type"]
        self.server_name = self.data["server_name"]
        self.server_map = self.data["map"]
        self.folder = self.data["folder"]
        self.game = self.data["game"]
        self.app_id = self.data["app_id"]
        self.player_count = self.data["player_count"]
        self.max_players = self.data["max_players"]
        self.bot_count = self.data["bot_count"]
        self.server_type = self.data["server_type"]
        self.platform = self.data["platform"]
        self.password_protected = self.data["password_protected"]
        self.vac_enabled = self.data["vac_enabled"]
        self.version = self.data["version"]
        return None

    def print(self):
        """
        Display all class attributes from latest query.

        :return: None
        """
        attrs = self.__repr__()
        print(''.join("%s: %s\n" % item for item in attrs.items()))

    def get_player_info(self):
        """
        Fetches the number of and list of active players on the server.

        :return: (int player_count, list[] player_list)
        """
        player_list = []

        with valve.source.a2s.ServerQuerier(self.server_address) as data:
            info = data.info()
            players = data.players()

        for player in sorted(players["players"], key=lambda p: p["score"], reverse=True):
            player_list.append("{name}".format(**player))

        return self.player_count, player_list

    def ping(self):
        # https://python-valve.readthedocs.io/en/latest/source.html?highlight=ping#valve.source.a2s.ServerQuerier.ping
        # https://developer.valvesoftware.com/wiki/Server_queries

        # Doesn't work currently
        return valve.source.a2s.ServerQuerier(self.server_address).ping()