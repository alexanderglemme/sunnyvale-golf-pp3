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
worksheet values as a 2D list (indices start at 0).
The user input is later manipulated in the update_worksheet()
function to accurately fit the data format of the worksheet
(indices start at 1, not 0).
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
    and lets user choose a tee time that the function then returns.
    If user enters empty of incorrect input it prints a message to the user
    and lets the user try again to avoid error.
    """

    print("- Hey there buddy!\nWhat day would"
          + " you like to tee off?")
    print("\n0 = Monday\n1 = Tuesday\n2 = Wednesday\n"
          + "3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday\n")
    user_day_str = input("Enter number of day here: \n")

    clear()

    if user_day_str == "":
        print('*You entered empty input, try again.*\n')
        make_tee_times()
    elif int(user_day_str) > 6:
        print("*You entered a number that was too big, try again*")
        make_tee_times()
    else:
        user_day_int = int(user_day_str)
        for i in range(len(all_tee_times)):
            if weather[i][user_day_int] != 'Thunder':
                print(all_tee_times[i][user_day_int])

    print("Above you'll find all the availble tee times on "
          + f"{week_days[user_day_int]}\n")

    print(f"-What time would you like to tee off on {week_days[user_day_int]}?"
          + "\nType out one of the times in the same exact format as above.\n")
    user_time = input("Enter time here: \n")

    if user_time not in times_to_tee_off:
        clear()
        print("*You entered incorrect or empty input, try again.*\n")
        make_tee_times()
    else:
        chosen_tee_time = times_to_tee_off[user_time]

    clear()

    print("(The tee time you've chosen is:"
          + f" {week_days[user_day_int]} {user_time})")

    if all_tee_times[chosen_tee_time][user_day_int] == 'Booked':
        print("\n- Sorry bud! The tee time on "
              + f"{week_days[user_day_int]} at {user_time} is already booked\n"
              + "and our lame golf course supervisor Mr.Lahey"
              + " only lets one group play per tee time.\n"
              + "Try choosing another one!\n")
        make_tee_times()

    elif weather[times_to_tee_off[user_time]][user_day_int] == 'Cloudy':
        print("- All right bud, make sure to bring a sweater,\n"
              + "the weather's looking a bit cloudy on "
              + f"{week_days[user_day_int]} at {user_time}.\n")

    elif weather[times_to_tee_off[user_time]][user_day_int] == 'Rain':
        print("- Okay bud, bring your rain gear, "
              + "looks like the weather's a bit rainy on "
              + f"{week_days[user_day_int]} at {user_time}.")

    else:
        print(f"- It's looking sunny on {week_days[user_day_int]}"
              + f" at {user_time}.\n"
              + "Make sure to bring at least 2"
              + " or 3 extra cases of beer bud.\n")

    if weather[chosen_tee_time][user_day_int] != 'Thunder':
        uppdate_worksheets(chosen_tee_time, user_day_int)


def uppdate_worksheets(num_row, num_col):
    """
    Updates the 'Tee Times' and 'Names' worksheets, using the returned
    values from make_tee_times(), so that the program doesn't
    disclose any personal information while looking for tee times
    """
    print("\n- We're almost set! All I need now is your name.\n")
    user_name = input("Enter name here: \n")
    clear()
    SHEET.worksheet('Names').update_cell(num_row + 1, num_col + 1, user_name)
    SHEET.worksheet('Tee Times').update_cell(num_row + 1,
                                             num_col + 1,
                                             'Booked')

    print("- Your tee time has been booked!\n"
          + "We'll handle greenfees and eventual cartfees at your arrival\n"
          + "to Sunnyvale Golf Course. We only take cash or hash-coins.\n"
          + "\n- Oh, and make sure to tell the course supervisor,\n"
          + "Jim Lahey, to frigg off if you see him!\n"
          + "It's Sunnyvale policy.\n"
          + "Anyhoo! Happy golfing bud!\n"
          + "_______________________________________________________________")

    print("\n- Would you like to book more tee times?\n"
          + "Do so by entering 2 down below.\n"
          + "This will take you straight to bookings.\n"
          + "Or just press Enter."
          + " This will take you back to the landing page.")

    user_choice = input("Press Enter, or 2 then Enter: ")

    if user_choice == "2":
        clear()
        make_tee_times()
    else:
        clear()
        start_booking()


def start_booking():
    """
    Starts the session by printing out a greeting to the receptionist
    at Sunnyvale Golf Course and gives directions on how to start
    booking tee times and what to say to the guest requesting a tee time
    """
    print("- Welcome to:\n"
          + "  __                                _\n"
          + "/ __> _ _ ._ _ ._ _  _ _  _ _  ___ | | ___\n"
          + "\__ \| | || ' || ' || | || | |<_> || |/ ._>\n"
          + "<___/`___||_|_||_|_|`_. ||__/ <___||_|\___.\n"
          + "                    <___'\n"
          + " ___        _  ___   ___\n"
          + "/  _>  ___ | || | ' |  _> ___  _ _  _ _  ___ ___ \n"
          + "| <_/\/ . \| || |-  | <__/ . \| | || '_><_-</ ._>\n"
          + "`____/\___/|_||_|   `___/\___/`___||_|  /__/\___.\n")
    print("- My name is Trevor and I'll be helping you book your tee time.\n")

    print(input('Press Enter to book a tee time\n'))
    clear()
    make_tee_times()


def clear():
    """
    Function that clears the terminal when called to reduce clutter.
    """
    os.system('cls')  # on Windows System
    os.system('clear')  # on Linux System


start_booking()
