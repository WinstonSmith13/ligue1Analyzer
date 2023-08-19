from fetchGS import get_authenticated_service, get_all_sheet_data

service = get_authenticated_service()
all_data = get_all_sheet_data(service)

def generate_player_list(sheet_name, data):
    header = data[0]
    player_data = data[1:]
    return [{header[i]: value for i, value in enumerate(playerInfo)} for playerInfo in player_data]

SHEETS_NAMES = ['Buts', 'Dividendes', 'Dividendes Dernière journée', 'PPF', 'PRIX', 'Passe Dé', 'Penalty Reussi',
                'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ']

players_by_sheet = {sheet_name: generate_player_list(sheet_name, all_data[sheet_name]) for sheet_name in SHEETS_NAMES}

def find_next_purchase(data_dividendes, data_PPF, data_valeurs, poste, max_price=5000000, min_price=4000000):
    potential_players = []

    for player in data_dividendes:
        if player['POSTE'] != poste:
            continue

        dividendes = int(player['DIVIDENDE'])
        matched_value = next((item for item in data_valeurs if item['NOM'] == player['NOM']), None)
        matched_ppf = next((item for item in data_PPF if item['NOM'] == player['NOM']), None)

        if not matched_value or not matched_ppf:
            continue

        price = int(matched_value['PRIX'])
        player_ppf = int(matched_ppf['PPF'])

        if max_price >= price >= min_price and dividendes > 0 and player_ppf < 80:
            potential_players.append(player)

    return sorted(potential_players, key=lambda x: int(x['DIVIDENDE']), reverse=True)

POSTES = ['Gardien', 'Défenseur', 'Milieu', 'Attaquant']

for poste in POSTES:
    best_purchase = find_next_purchase(players_by_sheet['Dividendes'], players_by_sheet['PPF'], players_by_sheet['PRIX'], poste)

    if best_purchase:
        print(f"Meilleur achat potentiel pour le poste de {poste}:")
        print("Nom:", best_purchase[0]['NOM'])
        print("Prix:", best_purchase[0]['PRIX'])
        print("Dividendes:", best_purchase[0]['DIVIDENDE'])
    else:
        print(f"Aucun joueur pour le poste de {poste} ne correspond aux critères.")
