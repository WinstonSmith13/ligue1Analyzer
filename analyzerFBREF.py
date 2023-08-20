from fetchGS import get_authenticated_service, get_all_sheet_data

# Initialisation et récupération des données
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
                'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ', 'FBREF']

players_by_sheet = {}
for sheet_name in SHEETS_NAMES:
    players_by_sheet[sheet_name] = generate_player_list(sheet_name, all_data[sheet_name])

# Utilisation de data_FBREF pour les analyses
data_FBREF = players_by_sheet['FBREF']
data_PPF_dict = {player['NOM']: player['PPF'] for player in players_by_sheet['PPF']}

# Évaluation Globale des Joueurs
def evaluate_player_performance(player):
    ppf = float(data_PPF_dict.get(player['NOM'], 0))
    score = (float(player['Buts/90']) + float(player['PD/90']) + float(player['xG/90']) + float(player['xAG/90'])) - (float(player['CJ']) * 0.1 + float(player['CR']) * 0.5)
    return score, ppf

# Analyse des Opportunités d'Investissement
def identify_investment_opportunities(players, seuil, limite_PPF):
    for player in players:
        score, ppf = evaluate_player_performance(player)
        if score > seuil and ppf < limite_PPF:
            print("Opportunité d'investissement:", player['NOM'])

# Analyse des Risques
def identify_high_risks(players, seuil2, limite_PPF_haut):
    for player in players:
        score, ppf = evaluate_player_performance(player)
        if score < seuil2 and ppf > limite_PPF_haut:
            print("Risque élevé:", player['NOM'])

# Seuils
seuil = 5.0
limite_PPF = 50
seuil2 = 3.0
limite_PPF_haut = 100

# Exécution
identify_investment_opportunities(data_FBREF, seuil, limite_PPF)
identify_high_risks(data_FBREF, seuil2, limite_PPF_haut)
