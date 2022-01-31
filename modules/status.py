def build_player_list(num_players: int, player_names: str):
    if int(num_players) > 0:
        num = 1
        player_nicknames = "\n"
        for player in player_names:
            player_nicknames += str(num) + ". " + player + "\n"
            num += 1
        player_nicknames += ""
    else:
        player_nicknames = "Никого нет на сервере..."
    return player_nicknames


def build_motd(server_status):
    if isinstance(server_status.raw["description"], dict):
        num = len(server_status.raw["description"]["extra"])
        x = 0
        y = 0
        all_strings = []
        while True:
            if x != num:
                motd_final = server_status.raw["description"]["extra"][x]
                all_strings.append(motd_final["text"])
                x += 1
                y += 1
            else:
                motd = "".join(all_strings)
                break
    else:
        motd = server_status.raw["description"]
    return motd
