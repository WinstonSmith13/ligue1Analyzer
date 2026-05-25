import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv
import os
import time

load_dotenv()

TYPES = {
    0: "dividendes",
    1: "valeur_reelle",
    2: "buts",
    3: "passes_decisives",
    4: "cartons_jaunes",
    5: "titularisations",
    6: "matches_joues",
    7: "presence_portefeuille",
    10: "penalties_reussis",
    11: "penalties_manques",
    12: "arrets_tirs",
}

def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
    session.post("https://www.idemfoot.com/", data={
        "login": os.getenv("IDEMFOOT_LOGIN"),
        "pass": os.getenv("IDEMFOOT_PASS")
    })
    return session

def scrape_type(session, type_id) -> dict:
    url = f"https://idemfoot.com/player/all.php?page=&popup=&compId=33&type={type_id}&poste=&team=&valeur=&afficher=Afficher"
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) > 5:
            headers = [th.get_text(strip=True) for th in rows[0].find_all(["td", "th"])]
            if "Joueur" not in headers:
                continue
            stat_col = headers[3]
            results = {}
            seen = set()
            for row in rows[1:]:
                cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
                if len(cols) >= 4:
                    name = cols[1]
                    if name and name not in seen:
                        seen.add(name)
                        val = cols[3].replace("€", "").replace("\xa0", "").replace(" ", "").strip()
                        try:
                            results[name] = float(val)
                        except:
                            results[name] = val
            print(f"  type={type_id} ({stat_col}): {len(results)} joueurs")
            return results
    return {}

def fetch_all() -> pd.DataFrame:
    print("Connecting to idemfoot...")
    session = get_session()

    all_data = {}
    for type_id, col_name in TYPES.items():
        data = scrape_type(session, type_id)
        for player, value in data.items():
            if player not in all_data:
                all_data[player] = {"player": player}
            all_data[player][col_name] = value
        time.sleep(0.5)

    # Récupérer poste et équipe depuis type=0
    url = f"https://idemfoot.com/player/all.php?page=&popup=&compId=33&type=0&poste=&team=&valeur=&afficher=Afficher"
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) > 5:
            headers = [th.get_text(strip=True) for th in rows[0].find_all(["td", "th"])]
            if "Joueur" in headers:
                seen = set()
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
                    if len(cols) >= 6:
                        name = cols[1]
                        if name and name not in seen:
                            seen.add(name)
                            if name in all_data:
                                all_data[name]["poste"] = cols[4]
                                all_data[name]["valeur"] = cols[2].replace("€", "").replace("\xa0", "").replace(" ", "").strip()

    df = pd.DataFrame(list(all_data.values()))
    df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
    return df.sort_values("dividendes", ascending=False)

def save_raw(df: pd.DataFrame):
    path = Path("src/data/raw")
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / "idemfoot_players_2526_full.csv"
    df.to_csv(filepath, index=False)
    print(f"\nSaved: {filepath} ({len(df)} players)")
    return filepath

if __name__ == "__main__":
    df = fetch_all()
    save_raw(df)
    print(df.head(10).to_string(index=False))