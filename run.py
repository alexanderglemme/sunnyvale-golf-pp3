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
    print("Hey there buddy,\nChoose what day you would"
          + " like to tee off.")
    print("\n0 = Monday\n1 = Tuesday\n2 = Wednesday\n"
          + "3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday\n")
    user_day = int(input("On what day would you like to tee off? "))

    for i in range(len(all_tee_times)):
        if weather[i][user_day] != 'Thunder':
            print(all_tee_times[i][user_day])

    print("Above you'll find all the availble tee times on "
          + f"{week_days[user_day]}:")

    print('\nNow choose what time you would like to tee off by'
          + ' typing out one of the tee times above!\n')
    user_time = input("What time would you like to tee off on "
                      + f"{week_days[user_day]}? ")

    chosen_tee_time = times_to_tee_off[user_time]  

    print(f"The tee time you've chosen is: {week_days[user_day]} {user_time}")

    if all_tee_times[chosen_tee_time][user_day] == 'Booked':
        print("\nSorry bud! The tee time on "
              + f"{week_days[user_day]} at {user_time} is already booked,\n"
              + "and our lame golf course supervisor Mr.Lahey"
              + " only lets one group play per tee time.\n"
              + "Try choosing another one!\n")
        make_tee_times()

    elif weather[times_to_tee_off[user_time]][user_day] == 'Cloudy':
        print("All right bud, make sure to bring a sweater, "
              + "the weather's looking a bit cloudy on "
              + f"{week_days[user_day]} at {user_time}.")

    elif weather[times_to_tee_off[user_time]][user_day] == 'Rain':
        print("Okay bud, bring your rain gear, "
              + "looks like the weather's a bit rainy on "
              + f"{week_days[user_day]} at {user_time}.")

    else:
        print(f"It's looking sunny on {week_days[user_day]} at {user_time}."
              + " Make sure to bring at least 2 or 3 extra cases of beer bud.")

    if weather[chosen_tee_time][user_day] != 'Thunder':
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
          + " to frigg off if you see him!\nIt's Sunnyvale policy.\n"
          + "Anyhoo! Happy golfing bud!")


print("Welcome To\n"
      + "  __                                _\n"
      + "/ __> _ _ ._ _ ._ _  _ _  _ _  ___ | | ___\n"
      + "\__ \| | || ' || ' || | || | |<_> || |/ ._>\n"
      + "<___/`___||_|_||_|_|`_. ||__/ <___||_|\___.\n"
      + "                    <___'\n"
      + " ___        _  ___   ___\n"
      + "/  _>  ___ | || | ' |  _> ___  _ _  _ _  ___ ___ \n"
      + "| <_/\/ . \| || |-  | <__/ . \| | || '_><_-</ ._>\n"
      + "`____/\___/|_||_|   `___/\___/`___||_|  /__/\___.\n")


print(input('Press Enter to book a tee time'))
make_tee_times()
