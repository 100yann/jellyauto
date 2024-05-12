import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from scraper import scrape_data    


scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1V9cRH7Oq-rF0pa2ADtHAKNvOImAMzTwt-vRRt7tvn1U'
sheet = client.open_by_key(sheet_id)

MONTHS = ['May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
EDITORS = {'Hani Sinno': 'A', 'Patriot Bytyqi': 'D', 'Betim Mehani': 'G', 'Stoyan Kolev': 'J'}
PRODUCTIVITY_HEADERS = ['Ready to edit', 'Ongoing edit', 'review/re-edit', 'AB Test', 'total_videos']


curr_month = datetime.now().date().strftime('%B')
curr_year = datetime.now().date().strftime('%Y')


def create_worksheets():
    for month in MONTHS:
        worksheet_name = f'{month} {curr_year}'
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            sheet.add_worksheet(title=worksheet_name, rows=50, cols=12)


curr_worksheet = sheet.worksheet(f'{curr_month} {curr_year}')
# data = scrape_data()
data = {'Hani Sinno': {'review/re-edit': {'num': 3, 'videos': "Giving Horrible Advice To Redditors, Reacting to My Old Tiktok's | Cringe, Drunk Drag!, "}, 'total_videos': {'num': 10}, 'Ongoing edit': {'num': 4, 'videos': 'READ BRIEF_These Amazon Products Should Be ILLEGAL, Reacting To And Making Overpriced Art, The Trad Wife Epidemic Is Insane, RE-EDIT : Entitled Karens That Were Called Out On Social Media - REACTION, '}, 'Ready to edit': {'num': 3, 'videos': 'Snap from FB - These Amazon Products Should Be ILLEGAL, Snap from FB - Reacting To And Making Overpriced Art, Snap from FB - The Trad Wife Epidemic Is Insane, '}, 'AB Test': {'num': 0}}, 
               'Patriot Bytyqi': {'Ready to edit': {'num': 3, 'videos': 'petty divorce drama that made it to AITA - REACTION, FB to Snap - Bad honeymoons that got EXPOSED on TikTok - REACTION, FB to Snap - Watching TikToks until I find the world’s craziest Ex - REACTION, '}, 'total_videos': {'num': 9}, 'Ongoing edit': {'num': 4, 'videos': 'Bad honeymoons that got EXPOSED on TikTok - REACTION, Watching TikToks until I find the world’s craziest Ex - REACTION, FB to Snap - Part 1 - petty beef that turned SAVAGE - REACTION, FB to Snap - Part 2 - petty beef that turned SAVAGE - REACTION, '}, 'review/re-edit': {'num': 1, 'videos': 'petty beef that turned SAVAGE - REACTION, '}, 'AB Test': {'num': 1, 'videos': 'Vertical - from BFF to BACKSTABBER - REACTION, '}}, 
               'Betim Mehani': {'Ongoing edit': {'num': 4, 'videos': "Reacting To Your INSANE Wedding Stories - REACTION, What You Didn’t Know About America's Most INFAMOUS Serial Killer, call the whole wedding off right now! - REACTION, This Show Needs To Be Cancelled…, "}, 'total_videos': {'num': 11}, 'review/re-edit': {'num': 1, 'videos': 'Cheaters ruining their marriages in 10 seconds or less - REACor less - REACTION, '}, 'Ready to edit': {'num': 2, 'videos': 'Snap from FB - This Show Needs To Be Cancelled…, FB to Snap - call the whole wedding off right now! - REACTION, '}, 'AB Test': {'num': 4, 'videos': "married couple drama that lit up AITA - REACTION, TIKtok Is Rotting My Brain…, LOCKED INSIDE AMERICA'S MOST HAUNTED ASYLUM ft @CelinaSpookyBoo | PART ONE, WE DID A SEANCE IN THE MOST HAUNTED CITY IN AMERICA Ft @CelinaSpookyBoo | PART 1, "}}, 
               'Stoyan Kolev': {'Ready to edit': {'num': 1, 'videos': 'Craziest People That OBJECTED At Weddings - REACTION, '}, 'total_videos': {'num': 5}, 'review/re-edit': {'num': 3, 'videos': 'Part 1 -\xa0FB to Snap\xa0- serving up heaping slices of humble pie - REACTION, Part 2 -\xa0FB to Snap\xa0- serving up heaping slices of humble pie - REACTION, Part 3 - FB to Snap - serving up heaping slices of humble pie - REACTION, '}, 'AB Test': {'num': 1, 'videos': 'serving up heaping slices of humble pie - REACTION, '}, 'Ongoing edit': {'num': 0}}}

def update_tracker():
    tracker_worksheet = sheet.worksheet('Tracker')
    cells = tracker_worksheet.range('A2:F5')

    cells_data = [] 

    for editor in EDITORS:
        cells_data.append(editor)
        for col in PRODUCTIVITY_HEADERS:
            cells_data.append(data[editor][col]['num'])

    index = 0
    for cell in cells:
        cell.value = cells_data[index]
        index += 1

    tracker_worksheet.update_cells(cells)

def display_total_videos():
    row = 1
    header_cells = curr_worksheet.range('A1:L1')
    headers_data = []

    for editor, column in EDITORS.items():
        headers_data.append(f'{editor} total videos')
        headers_data.append(data[editor]['total_videos']['num'])
        headers_data.append('') # leaves an empty cell inbetween editors

    index = 0
    for cell in header_cells:
        cell.value = headers_data[index]
        index += 1

    curr_worksheet.update_cells(header_cells)


update_tracker()
# display_total_videos()