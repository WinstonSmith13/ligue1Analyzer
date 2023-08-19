from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1EHdPEQm9Suj9UZJd4n8vACkXLdzx4cQEun4Png__hTI'
SHEETS_NAMES = ['Buts', 'Dividendes', 'Dividendes Dernière journée', 'PPF', 'Passe Dé', 'Penalty Reussi',
                'CARTONS JAUNE', 'ARRETS GARDIEN', 'TITULARISATION', 'MATCH JOUÉ', 'PRIX']


def get_authenticated_service():
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

    return build('sheets', 'v4', credentials=creds)


def get_all_sheet_data(service):
    all_data = {}
    sheet = service.spreadsheets()

    for sheet_name in SHEETS_NAMES:
        range_name = f'{sheet_name}!A1:E500'  # Construct the range name
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            continue

        all_data[sheet_name] = values

    return all_data


def main():
    service = get_authenticated_service()
    all_data = get_all_sheet_data(service)

    for sheet_name, values in all_data.items():
        if not values:
            print(f'No data found for {sheet_name}.')
            continue

        print(f'\nData for {sheet_name}:')  # Print the sheet's name
        for row in values:
            print(', '.join(row))


if __name__ == '__main__':
    main()
