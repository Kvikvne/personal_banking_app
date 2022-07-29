import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

CATEGORY_LIST = ["Rent", "Groceries", "Restaurants", "Transportation", "Entertainment", "Online Shopping", "Clothes",
                 "Utilities", "Investments", "Insurance", "Snacks/Nicotine/beer", "Weed", "Income", "misc.", "Fitness"]

DATE_RANGE_START = '2022-07-14'
DATE_RANGE_END = '2022-07-18'

data = pd.read_csv('your_csv_file_here.csv')
# Rename columns
data.rename(columns={'Posted': 'Date', 'Memo': 'Item'}, inplace=True)

# Get rid of unneeded columns
data.drop(["Account Number", "Type", "Effective Date", "Transfer ID", "Description", "Ending Balance"]
          , axis=1, inplace=True)

# Convert dates to datetime
data['Date'] = pd.to_datetime(data.Date, infer_datetime_format=True)

# Sort data by date
data_range = (data['Date'] >= DATE_RANGE_START) & (data['Date'] <= DATE_RANGE_END)
data_range = data.loc[data_range]

# New csv file
new_csv = data_range.to_csv("new_csv.csv")
data_2 = pd.read_csv("new_csv.csv")
data_2.drop(data_2.columns[data_2.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
data_2.reset_index(drop=True)

# Separating columns into lists
dates = []
items = []
amounts = []
finale_list = []
cat = ""

for i in range(int(len(data_2.index))):
        dates.append(data_2["Date"][i])
        items.append(data_2["Item"][i])
        amounts.append(data_2["Amount"][i])

# new formatted list
for i in range(len(dates)):
    if "TRANSFER FR" in str(items[i]):
        pass
    else:
        finale_list.append({"date": dates[i], "item": items[i], "amount": amounts[i], "cat": cat})

for item in finale_list:
    if str(item['item']) == "nan":
        item['item'] = str(item['item'])

    if "-" in str(item['amount']):
        item['amount'] = str(item['amount']).replace('-', '')

# Categorizing
for item in range(0, len(finale_list)- 1):
    if "LIQUOR0" in finale_list[item]['item'] or "7-ELEVEN" in finale_list[item]['item'] or "CIRCLE H" \
            in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[10]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "AMAZON" in finale_list[item]['item'] or "Amazon" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[5]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "RESTAURANT" in finale_list[item]['item'] or "KITCHEN" in finale_list[item]['item'] or "STARBUCKS" in \
            finale_list[item]['item'] or "CHIPOTLE" in finale_list[item]['item'] or "WENDY'S" in \
            finale_list[item]['item'] or "EATS" in finale_list[item]['item'] or "BURGER KING" in \
            finale_list[item]['item'] or "SQUARE PURCHASE" in finale_list[item]['item'] or "GELATO" in finale_list[item]['item'] or \
            "PITA PARADISE" in finale_list[item]['item'] or "COFFEE" in finale_list[item]['item'] or "MCDONALD'S" in\
            finale_list[item]['item'] or "TACOS" in finale_list[item]['item'] or "SNACK" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[2]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "CHEVRON" in finale_list[item]['item'] or "NEX FUEL" in finale_list[item]['item'] or \
            "UNITED" in finale_list[item]['item'] or "HAWAIIAN AIRLI" in finale_list[item]['item'] or "SHELL" \
            in finale_list[item]['item'] or "AIRLINE" in finale_list[item]['item'] or "PENDING.UBER.COM"in \
            finale_list[item]['item']:
        new_cat = CATEGORY_LIST[3]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "VONS" in finale_list[item]['item'] or "99 RANCH" in finale_list[item]['item'] or "SPROUTS" in \
            finale_list[item]['item'] or "FOODLAND" in finale_list[item]['item'] or "SAFEWAY" in \
            finale_list[item]['item']:
        new_cat = CATEGORY_LIST[1]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "STEAMGAMES" in finale_list[item]['item'] or "KNOTTS" in finale_list[item]['item'] or "Steam" in \
            finale_list[item]['item'] or "AMC" in finale_list[item]['item'] or "Photo" in finale_list[item]['item'] \
            or "ZOO" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[4]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "SUPPLEMENT" in finale_list[item]['item'] or "FITNESS" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[14]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "VENMO" in finale_list[item]['item'] and "598.00" in finale_list[item]['amount']:
        new_cat = CATEGORY_LIST[0]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "ATT*BILL" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[7]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "CALVIN KLEIN" in finale_list[item]['item'] or "ROSS" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[6]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "Anderson Kaikane New York" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[12]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    elif "ROBINHOOD" in finale_list[item]['item']:
        new_cat = CATEGORY_LIST[8]
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)

    else:
        new_cat = "misc."
        finale_list[item]['cat'] = finale_list[item]['cat'].replace(finale_list[item]['cat'], new_cat)


# Google api
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = 'your sheet id'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

for item in finale_list:
    body_data = [[str(item["date"]), str(item['item']), str(item['amount']), str(item['cat'])]]
    print(body_data)
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='enterdata!c3:f1',
                                    valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS",
                                    body={"values": body_data}).execute()

    print(request)
    time.sleep(3)
