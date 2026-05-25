import soccerdata as sd
import pandas as pd
from pathlib import Path

def fetch_players(season="2425") -> pd.DataFrame:
    print(f"Fetching Ligue 1 player stats — season {season}...")
    fbref = sd.FBref(leagues="FRA-Ligue 1", seasons=season)
    df = fbref.read_player_season_stats(stat_type="standard")
    df.columns = [" ".join(col).strip() if col[0] != col[1] else col[1] for col in df.columns]
    df = df.reset_index()
    return df

def save_raw(df: pd.DataFrame, season="2425"):
    path = Path("src/data/raw")
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / f"ligue1_players_{season}.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath} ({len(df)} players)")
    return filepath

if __name__ == "__main__":
    df = fetch_players()
    filepath = save_raw(df)
    print(f"\n{len(df)} joueurs récupérés")
    print(df[["player", "team", "pos", "Performance Gls", "Performance Ast"]].head(10))