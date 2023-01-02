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
weather = SHEET.worksheet('Wheather').get_values()

week_days = {0: 'Monday',
             1: 'Tuesday',
             2: 'Wednesday',
             3: 'Thursday',
             4: 'Friday',
             5: 'Saturday',
             6: 'Sunday'}

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


def make_tee_times():
    """
    Gets the available tee-times on a chosen day
    and lets user choose a tee time that the function then returns
    """
    print("Hi there buddy,\nto choose what day you would"
          + " like to book a tee time, enter a number between 0-6.")
    print("\n0 = Monday\n1 = Tuesday\n2 = Wednesday\n"
          + "3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday\n")
    user_day = int(input("What day would you like to tee off on? "))

    print("Here are all the availble tee times on "
          + f"{week_days[user_day]}:")

    for i in range(len(all_tee_times)):
        print(all_tee_times[i][user_day])

    print('\nNow choose what time you would like to tee off by'
          + ' typing out one of the tee times above!\n')
    user_time = input("What time would you like to tee off on "
                      + f"{week_days[user_day]}? ")

    print(f"You've chosen tee time: {week_days[user_day]} {user_time}")

    if weather[times_to_tee_off[user_time]][user_day] == 'Thunder':
        print("Sorry bud, the weather's looking a bit electrifying on "
              + f"{week_days[user_day]},\n"
              + "our lame golf course supervisor Mr.Lahey "
              + "won't let our guests play during thunder.\n"
              + "Try choosing another tee time!\n")
        make_tee_times()

    elif weather[times_to_tee_off[user_time]][user_day] == 'Cloudy':
        print("All right bud, make sure to bring a sweater, "
              + "the weather's looking a bit cloudy on "
              + week_days[user_day], user_time)

    elif weather[times_to_tee_off[user_time]][user_day] == 'Rain':
        print("Okay bud, bring your rain gear, "
              + "looks like the weather's a bit rainy on "
              + week_days[user_day], user_time)

    else:
        print("Looking sunny in Sunnyvale on "
              + week_days[user_day], user_time)

    chosen_tee_time = times_to_tee_off[user_time]
    update_bookings(chosen_tee_time, user_day)

    return chosen_tee_time, user_day


def update_bookings(num_1, num_2):
    """
    Updates the 'Tee Times' spreadsheet, using the returned
    values from make_tee_times()
    """
    SHEET.worksheet('Tee Times').update_cell(num_1 + 1, num_2, "Booked")
    print("Your tee time has been booked!"
          + "Make sure to tell the course supervisor, Jim Lahey,"
          + " to frigg off if you see him!"
          + " Happy golfing bud!")


make_tee_times()

