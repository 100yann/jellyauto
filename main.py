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
EDITORS = {'Hani': 'A', 'Patriot': 'D', 'Betim': 'G', 'Stoyan': 'J'}

SAMPLE_DATA = {'Betim': {'AB Test': 4, 'Ongoing edit': 2, 'review/re-edit': 1, 'Ready to edit': 4, 'TOTAL': 11}, 
               'Patriot': {'AB Test': 1, 'Ready to edit': 3, 'Ongoing edit': 4, 'review/re-edit': 1, 'TOTAL': 9}, 
               'Hani': {'review/re-edit': 3, 'Ongoing edit': 4, 'Ready to edit': 3, 'TOTAL': 10, 'AB Test': 0},
               'Stoyan': {'TOTAL': 1}
               }


for month in MONTHS:
    worksheet_name = f'{month} 2024'
    try:
        curr_worksheet = sheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title=worksheet_name, rows=50, cols=12)
        curr_worksheet = sheet.worksheet(worksheet_name)

curr_worksheet = sheet.worksheet('May 2024')

tracker_worksheet = sheet.worksheet('Tracker')
row = 2

for editor, column in EDITORS.items():
    tracker_worksheet.update(range_name=f'A{row}:F{row}', values=[[editor, *SAMPLE_DATA[editor].values()]], raw=True,)
    row += 1


def display_total_videos():
    for editor, column in EDITORS.items():
        curr_worksheet.update_acell(f'{column}1', f'{editor} total videos')
        curr_worksheet.update_acell(f'{chr(ord(column)+1)}1', SAMPLE_DATA[editor]['TOTAL'])


