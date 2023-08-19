from fetchGS import get_authenticated_service, get_all_sheet_data

service = get_authenticated_service()
all_data = get_all_sheet_data(service)


def generate_player_list(sheet_name, data):
    header = data[0]
    player_data = data[1:]
    players = []

    for playerInfo in player_data:
        playerDict = {}
        for i, value in enumerate(playerInfo):
            header_name = header[i]
            playerDict[header_name] = value
        players.append(playerDict)

    return players


SHEETS_NAMES = ['Buts', 'Dividendes', 'Dividendes Dernière journée', 'PPF', 'Passe Dé', 'Penalty Reussi',
                'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ']

players_by_sheet = {}

for sheet_name in SHEETS_NAMES:
    players_by_sheet[sheet_name] = generate_player_list(sheet_name, all_data[sheet_name])

# For example, if you want to get the players data for "Buts" sheet:
print(players_by_sheet['Dividendes'])




