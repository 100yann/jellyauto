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
data = {'Hani Sinno': {'Ready to edit': {'num': 6, 'videos': {'Snap from FB - These Amazon Products Should Be ILLEGAL': 'https://core.jellysmack.com/#/productionTaskDetails/125234/brief', 'Snap from FB - Reacting To And Making Overpriced Art': 'https://core.jellysmack.com/#/productionTaskDetails/127404/brief', 'Snap from FB - The Trad Wife Epidemic Is Insane': 'https://core.jellysmack.com/#/productionTaskDetails/127697/brief', 'Snap from FB - Part 1 - I Bought DISCONTINUED Products From Our Childhood': 'https://core.jellysmack.com/#/productionTaskDetails/128606/brief', 'Snap from FB - Part 2 - I Bought DISCONTINUED Products From Our Childhood': 'https://core.jellysmack.com/#/productionTaskDetails/128607/brief', 'Snap from FB - I Bought Every VIRAL Wig Off Amazon': 'https://core.jellysmack.com/#/productionTaskDetails/129105/brief'}}, 'Ongoing edit': {'num': 3, 'videos': {'Driving Across America': 'https://core.jellysmack.com/#/productionTaskDetails/122613/brief', 'I Bought DISCONTINUED Products From Our Childhood': 'https://core.jellysmack.com/#/productionTaskDetails/128605/brief', 'I Bought Every VIRAL Wig Off Amazon': 'https://core.jellysmack.com/#/productionTaskDetails/129104/brief'}}, 'review/re-edit': {'num': 1, 'videos': {'Reacting To And Making Overpriced Art': 'https://core.jellysmack.com/#/productionTaskDetails/127402/brief'}}, 'AB Test': {'num': 0, 'videos': {}}, 'total_videos': {'num': 10}}, 
        'Patriot Bytyqi': {'Ready to edit': {'num': 3, 'videos': {'confessions that cancelled the wedding - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/128587/brief', 'Snap - 5 Minute Crafts that Make My Brain Hurt': 'https://core.jellysmack.com/#/productionTaskDetails/128608/brief', 'Snap from FB - that came out of nowhere ! - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/129231/brief'}}, 'Ongoing edit': {'num': 2, 'videos': {'petty divorce drama that made it to AITA - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/127393/brief', 'that came out of nowhere ! - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/129109/brief'}}, 'review/re-edit': {'num': 1, 'videos': {'FB to Snap - Part 1 - Bad honeymoons that got EXPOSED on TikTok - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/127782/brief'}}, 'AB Test': {'num': 0, 'videos': {}}, 'total_videos': {'num': 6}}, 
        'Betim Mehani': {'Ready to edit': {'num': 3, 'videos': {'RE-EDIT : Entitled Bridezillas And Their Insane Demands - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/128576/brief', "TikTok's that Need to Stay in 2021": 'https://core.jellysmack.com/#/productionTaskDetails/128610/brief', 'RE-EDIT : Bridezillas That Are On Another Level #entitled - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/129100/brief'}}, 'Ongoing edit': {'num': 2, 'videos': {'Dumb People That Need To Get Off Social Media - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/125995/brief', 'Snap from FB - This Show Needs To Be Cancelled…': 'https://core.jellysmack.com/#/productionTaskDetails/128083/brief'}}, 'review/re-edit': {'num': 3, 'videos': {"What You Didn’t Know About America's Most INFAMOUS Serial Killer": 'https://core.jellysmack.com/#/productionTaskDetails/127403/brief', 'This Show Needs To Be Cancelled…': 'https://core.jellysmack.com/#/productionTaskDetails/128082/brief', 'FB to Snap - call the whole wedding off right now! - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/128102/brief'}}, 'AB Test': {'num': 0, 'videos': {}}, 'total_videos': {'num': 8}}, 
        'Stoyan Kolev': {'Ready to edit': {'num': 1, 'videos': {'Snap from FB - Every video is a crazier Karen - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/129230/brief'}}, 'Ongoing edit': {'num': 2, 'videos': {'Every video is a crazier Karen - REACTION': 'https://core.jellysmack.com/#/productionTaskDetails/129097/brief', "Let's Go Down The Toxic Tik Tok Rabbit Hole - REACTION": 'https://core.jellysmack.com/#/productionTaskDetails/129099/brief'}}, 'review/re-edit': {'num': 0, 'videos': {}}, 'AB Test': {'num': 0, 'videos': {}}, 'total_videos': {'num': 3}}}


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
    curr_worksheet.batch_clear(['A3:T50'])

    for editor in data.keys():
        for status in data[editor]:
            if status == 'total_videos':
                column += 1
                continue
            num_videos = data[editor][status]['num']
            if num_videos == 0:
                column += 1
                continue
            videos = data[editor][status]['videos']
            column_cells = curr_worksheet.range(f'{chr(column)}3:{chr(column)}{num_videos + 2}')
            for index, video_name in enumerate(videos):
                video_url = videos[video_name]
                column_cells[index].value = f'=HYPERLINK("{video_url}", "{video_name}")'
            curr_worksheet.update_cells(column_cells, value_input_option='USER_ENTERED')
            column += 1


add_videos_to_sheet()
# update_tracker()