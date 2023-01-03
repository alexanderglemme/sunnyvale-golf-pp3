import os
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
weather = SHEET.worksheet('Weather').get_values()

"""
Under here are key value pairs that correspond with
the expected user input. This is implemented because
of the .get_values() function, which presents the
worksheet values as a 2D list (indices starts at 0).
The user input is later manipulated in the update_worksheet
function to accurately fit the data format of the worksheet
(indices starts at 1, not 0).
"""
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
    clear()
   
    print("Hey there buddy,\nChoose what day you would"
          + " like to tee off.")
    print("\n0 = Monday\n1 = Tuesday\n2 = Wednesday\n"
          + "3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday\n")
    user_day = int(input("On what day would you like to tee off? "))

    clear()

    for i in range(len(all_tee_times)):
        if weather[i][user_day] != 'Thunder':
            print(all_tee_times[i][user_day])

    print("Above you'll find all the availble tee times on "
          + f"{week_days[user_day]}\n")

    print('\nNow choose what time you would like to tee off by'
          + ' typing out one of the tee times above!\n')
    user_time = input("What time would you like to tee off on "
                      + f"{week_days[user_day]}? ")

    chosen_tee_time = times_to_tee_off[user_time]

    clear()

    print("(The tee time you've chosen is:"
          + f"{week_days[user_day]} {user_time})")

    if all_tee_times[chosen_tee_time][user_day] == 'Booked':
        print("\nSorry bud! The tee time on "
              + f"{week_days[user_day]} at {user_time} is already booked,\n"
              + "and our lame golf course supervisor Mr.Lahey"
              + " only lets one group play per tee time.\n"
              + "Try choosing another one!\n")
        make_tee_times()

    elif weather[times_to_tee_off[user_time]][user_day] == 'Cloudy':
        print("All right bud, make sure to bring a sweater,\n"
              + "the weather's looking a bit cloudy on "
              + f"{week_days[user_day]} at {user_time}.\n")

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


def update_bookings(num_row, num_col):
    """
    Updates the 'Tee Times' and 'Names' worksheets, using the returned
    values from make_tee_times(), so that the program doesn't
    disclose any personal information to users when they're booking
    tee times.
    """
    print("We're almost set! All I need is your name.\n")
    user_name = input('Enter the name you want to book in: ')
    clear()
    SHEET.worksheet('Names').update_cell(num_row + 1, num_col + 1, user_name)
    SHEET.worksheet('Tee Times').update_cell(num_row + 1, num_col + 1, 'Booked')
    print("\nYour tee time has been booked!\n"
          + "We'll handle greenfees and eventual cartfees at your arrival\n"
          + "to Sunnyvale Golf Course (we take cash or hash-coins only)!\n"
          + "\nOh, and make sure to tell the course supervisor, Jim Lahey,"
          + " to frigg off if you see him!\nIt's Sunnyvale policy.\n"
          + "Anyhoo! Happy golfing bud!\n")
    print("\nIf you want, you can book more tee times. Do so by entering\n"
          + "2 down below. This will take you straight to bookings,\n"
          + "or just press Enter. This will take you back to the landing page.")

    user_choice = int(input("What will it be bud? "))
    
    if user_choice == 2:
        make_tee_times()
    else:
        clear()
        start_booking()


def start_booking():
    """
    Starts the session by printing out a greeting to the user
    and gives directions on how to start booking tee times
    """
    print("Welcome to the very official and fancy booking-system of:\n"
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


def clear():
    """
    Function that clears the terminal when called to reduce clutter.
    """
    os.system('cls')  # on Windows System
    os.system('clear')  # on Linux System


start_booking()
