from fetchGS import get_authenticated_service, get_all_sheet_data

service = get_authenticated_service()
all_data = get_all_sheet_data(service)

# Par exemple, pour obtenir les données du sheet 'Buts':
data_buts = all_data['Buts']
data_dividendes = all_data['Dividendes Dernière journée']

header_buts = data_buts[0]
player_data_but = data_buts[1:]

header_ddj = data_dividendes[0]
player_data_ddj = data_dividendes[1:]

players = []

for playerInfo in player_data_ddj:
    playerArray = {}
    for i, value in enumerate(playerInfo):
        header_name = header_ddj[i]
        playerArray[header_name] = value
    players.append(playerArray)

print(players)
