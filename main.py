import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1V9cRH7Oq-rF0pa2ADtHAKNvOImAMzTwt-vRRt7tvn1U'
sheet = client.open_by_key(sheet_id)

MONTHS = ['May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
EDITORS = {'Hani': 'A', 'Patriot': 'C', 'Betim': 'E', 'Stoyan': 'G'}

for month in MONTHS:
    worksheet_name = f'{month} 2024'
    try:
        curr_worksheet = sheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title=worksheet_name, rows=50, cols=10)
        curr_worksheet = sheet.worksheet(worksheet_name)
        for editor, row in EDITORS.items():
            curr_worksheet.update_acell(f'{row}1', f'{editor} total videos')