import mcstatus


class Status:

    def __init__(self):
        self.server_ip = None
        self.server_status = None
        self.server = None
        self.server_status_data = {
            "player_count": 0,
            "max_players": 0,
            "player_names": [],
            "version": None,
            "motd": None,
            "ip": None,
            "update_flag": False
        }

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip
        self.server = mcstatus.MinecraftServer.lookup(server_ip)

    def get_server_ip(self):
        return self.server_ip

    def get_server_status(self):
        server_data = dict.copy(self.server_status_data)
        if self.server_status_data["update_flag"]:
            self.server_status_data["update_flag"] = False

        return server_data

    def poll_server_status(self):
        if self.server_ip is not None and self.server is not None:
            new_server_status = self.server.query()

            if self.server_status is None or self.server_status.raw != new_server_status.raw:
                self.server_status_data["update_flag"] = True

            self.server_status = new_server_status
            self.server_status_data["player_count"] = self.server_status.raw["numplayers"]
            self.server_status_data["max_players"] = self.server_status.raw["maxplayers"]
            self.server_status_data["player_names"] = self.server_status.players.names
            self.server_status_data["version"] = self.server_status.raw["version"]
            self.server_status_data["motd"] = self.server_status.raw["hostname"]
            self.server_status_data["ip"] = self.server_ip
