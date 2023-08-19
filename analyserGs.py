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


SHEETS_NAMES = ['Buts', 'Dividendes', 'Dividendes Dernière journée', 'PPF', 'PRIX', 'Passe Dé', 'Penalty Reussi',
                'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ']

players_by_sheet = {}

for sheet_name in SHEETS_NAMES:
    players_by_sheet[sheet_name] = generate_player_list(sheet_name, all_data[sheet_name])


data_buts = players_by_sheet['Buts']
data_dividendes = players_by_sheet['Dividendes']
data_DDJ = players_by_sheet['Dividendes Dernière journée']
data_PPF = players_by_sheet['PPF']
data_passes_dec = players_by_sheet['Passe Dé']
data_penalty_reussi = players_by_sheet['Penalty Reussi']
data_cj = players_by_sheet['CARTONS JAUNE']
data_arrets = players_by_sheet['ARRETS GARDIEN']
data_titu = players_by_sheet['TITULARISATION']
data_match_j = players_by_sheet['MATCH JOUÉ']
data_valeurs = players_by_sheet['PRIX']

print(data_valeurs)

# for player in data_arrets:
#     player['RATIO'] = int(player['ARRETS']) / int(player['PRIX'])
#
# # Trier les gardiens par ratio
# sorted_data = sorted(data_arrets, key=lambda x: x['RATIO'], reverse=True)

# Afficher les données triées
# for player in sorted_data:
#     print(player['NOM'], player['RATIO'])


# print(data_arrets)

# def find_next_purchase(data_dividendes, data_PPF, max_price=4000000, min_dividendes=100000):
#     potential_players = []
#
#     # Filtrer les joueurs selon les critères
#     for player in data_dividendes:
#         # Convertir les valeurs en entiers
#         price = int(player['PRIX'])
#         dividendes = int(player['DIVIDENDE'])
#         matched_player = next((item for item in data_PPF if item['NOM'] == player['NOM']), None)
#         if matched_player:
#             player_ppf = int(matched_player['PPF'])
#         else:
#             print(f"Le joueur {player['NOM']} n'a pas été trouvé dans data_PPF.")
#             continue
#
#         # Vérifier les critères
#         if price < max_price and dividendes > min_dividendes and player_ppf < 80:  # PPF faible (< 5 par exemple)
#             potential_players.append(player)
#
#     # Trier les joueurs potentiels par dividendes décroissants pour trouver le joueur avec les dividendes les plus élevés
#     sorted_players = sorted(potential_players, key=lambda x: int(x['DIVIDENDE']), reverse=True)
#
#     return sorted_players
#
# # Chercher le meilleur achat
# best_purchase = find_next_purchase(data_dividendes, data_PPF)
#
# # Afficher le meilleur joueur à acheter
# if best_purchase:
#     print("Meilleur achat potentiel :")
#     print("Nom:", best_purchase[0]['NOM'])
#     print("Prix:", best_purchase[0]['PRIX'])
#     print("Dividendes:", best_purchase[0]['DIVIDENDE'])
# else:
#     print("Aucun joueur ne correspond aux critères.")






