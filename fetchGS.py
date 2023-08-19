from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Spreadsheet ID
SAMPLE_SPREADSHEET_ID = '1EHdPEQm9Suj9UZJd4n8vACkXLdzx4cQEun4Png__hTI'

# Sheet names
SHEETS = ['Buts', 'Dividendes', 'Dividendes Dernière journée', 'PPF', 'Passe Dé', 'Penalty Reussi', 'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ']

def main():
    """Shows basic usage of the Sheets API."""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        for sheet_name in SHEETS:
            range_name = f'{sheet_name}!A1:E500'
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
            values = result.get('values', [])

            if not values:
                print(f'No data found for {sheet_name}.')
                continue

            print(f'Data for {sheet_name}:')
            for row in values:
                print(', '.join(row))

    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
