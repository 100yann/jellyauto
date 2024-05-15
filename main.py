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
data = {'Hani Sinno': {'Ready to edit': {'num': 6, 'videos': ['Snap from FB - These Amazon Products Should Be ILLEGAL', 'Snap from FB - Reacting To And Making Overpriced Art', 'Snap from FB - The Trad Wife Epidemic Is Insane', 'I Bought DISCONTINUED Products From Our Childhood', 'Snap from FB - Part 1 - I Bought DISCONTINUED Products From Our Childhood', 'Snap from FB - Part 2 - I Bought DISCONTINUED Products From Our Childhood']}, 'Ongoing edit': {'num': 2, 'videos': ['Driving Across America', 'Reacting To And Making Overpriced Art']}, 'review/re-edit': {'num': 2, 'videos': ['Giving Horrible Advice To Redditors', 'RE-EDIT : Entitled Karens That Were Called Out On Social Media - REACTION']}, 'AB Test': {'num': 5, 'videos': ['AB to relaunch_New Edit - Tiktok’s PSYCHO Ex Girlfriends', 'AB to relaunch_Couples Content Makes Me Cringe', "Reacting to My Old Tiktok's | Cringe", 'Drunk Drag!', 'The Trad Wife Epidemic Is Insane']}, 'Delivered': {'num': 0, 'videos': []}, 'total_videos': {'num': 15}},
        'Patriot Bytyqi': {'Ready to edit': {'num': 4, 'videos': ['petty divorce drama that made it to AITA - REACTION', 'confessions that cancelled the wedding - REACTION', 'Snap - 5 Minute Crafts that Make My Brain Hurt', 'Snap from FB - influencers that thought they were the main character - REACTION']}, 'Ongoing edit': {'num': 2, 'videos': ['FB to Snap - Bad honeymoons that got EXPOSED on TikTok - REACTION', 'FB to Snap - Watching TikToks until I find the world’s craziest Ex - REACTION']}, 'review/re-edit': {'num': 1, 'videos': ['influencers that thought they were the main character - REACTION']}, 'AB Test': {'num': 2, 'videos': ['Bad honeymoons that got EXPOSED on TikTok - REACTION', 'Watching TikToks until I find the world’s craziest Ex - REACTION']}, 'Delivered': {'num': 0, 'videos': []}, 'total_videos': {'num': 9}}, 
        'Betim Mehani': {'Ready to edit': {'num': 3, 'videos': ['Dumb People That Need To Get Off Social Media - REACTION', 'RE-EDIT : Entitled Bridezillas And Their Insane Demands - REACTION', "TikTok's that Need to Stay in 2021"]}, 'Ongoing edit': {'num': 3, 'videos': ["What You Didn’t Know About America's Most INFAMOUS Serial Killer", 'Snap from FB - This Show Needs To Be Cancelled…', 'FB to Snap - call the whole wedding off right now! - REACTION']}, 'review/re-edit': {'num': 3, 'videos': ['Reacting To Your INSANE Wedding Stories - REACTION', 'call the whole wedding off right now! - REACTION', 'This Show Needs To Be Cancelled…']}, 'AB Test': {'num': 3, 'videos': ['TIKtok Is Rotting My Brain…', "LOCKED INSIDE AMERICA'S MOST HAUNTED ASYLUM ft @CelinaSpookyBoo | PART ONE", 'WE DID A SEANCE IN THE MOST HAUNTED CITY IN AMERICA Ft @CelinaSpookyBoo | PART 1']}, 'Delivered': {'num': 0, 'videos': []}, 'total_videos': {'num': 12}}, 
        'Stoyan Kolev': {'Ready to edit': {'num': 1, 'videos': ['what did I just read?! judging your AITA stories']}, 'Ongoing edit': {'num': 0, 'videos': []}, 'review/re-edit': {'num': 0, 'videos': []}, 'AB Test': {'num': 1, 'videos': ['Craziest People That OBJECTED At Weddings - REACTION']}, 'Delivered': {'num': 0, 'videos': []}, 'total_videos': {'num': 2}}
        }

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


def add_videos_to_sheet():
    column = 65 # ascii for first column A
    for editor in data.keys():
        for status in data[editor]:
            if status == 'total_videos':
                continue
            num_videos = data[editor][status]['num']
            if num_videos == 0:
                column += 1
                continue
            videos = data[editor][status]['videos']
            column_cells = curr_worksheet.range(f'{chr(column)}3:{chr(column)}{num_videos + 2}')
            index = 0
            for cell in column_cells:
                cell.value = videos[index]
                index += 1
            curr_worksheet.update_cells(column_cells)
            column += 1


add_videos_to_sheet()
