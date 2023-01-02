import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sunnyvale_golfcourse')

all_tee_times = SHEET.worksheet('Tee Times').get_values()


def get_tee_times():
    """
    Gets the available tee-times on a chosen day
    and lets user choose a tee time that the function then returns
    """
    print("Hi there golfer,\nto choose what day you would"
          + " like to book a tee time, enter a number between 0-6.")
    print("\n0 = Monday\n1 = Tuesday\n2 = Wednesday\n"
          + "3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday\n")
    user_day = int(input("What day would you like to tee off on? "))

    week_days = {0: 'Monday',
                 1: 'Tuesday',
                 2: 'Wednesday',
                 3: 'Thursday',
                 4: 'Friday',
                 5: 'Saturday',
                 6: 'Sunday'}

    print("Here are all the availble tee times on "
          + f"{week_days[user_day]}:")
  
    for i in range(len(all_tee_times)):
        print(all_tee_times[i][user_day])

    print('\nNow choose what time you would to tee off by'
          + 'typing out one of the tee times above!\n')
    user_time = input("What time would you like to tee off on " 
                      + f"{week_days[user_day]}? ")

    times_to_tee_off = {"8:15 AM": 0,
                        "8:30 AM": 1,
                        "8:45 AM": 2,
                        "9:00 AM": 3,
                        "9:15 AM": 4,
                        "9:30 AM": 5,
                        "9:45 AM": 6,
                        "10:00 AM": 7,
                        "10:15 AM": 8,
                        "10:30 AM": 9,
                        "10:45 AM": 10,
                        "11:00 AM": 11,
                        "11:15 AM": 12,
                        "11:30 AM": 13,
                        "11:45 AM": 14,
                        "12:00 PM": 15,
                        "12:15 PM": 16,
                        "12:30 PM": 17,
                        "12:45 PM": 18,
                        "1:00 PM": 19,
                        "1:15 PM": 20,
                        "1:30 PM": 21,
                        "1:45 PM": 22,
                        "2:00 PM": 23,
                        "2:15 PM": 24}
    print(f"You've chosen to tee off on {week_days[user_day]}"
          + f" {all_tee_times[times_to_tee_off[user_time]][user_day]}")


get_tee_times()

