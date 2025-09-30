import pandas as pd
from unidecode import unidecode
from calendar import monthrange, weekday
from datetime import datetime
from math import ceil
from os import environ
import dotenv


# Get directory name from the .env file located in this directory (untracked by version control)
dotenv.load_dotenv()
STAVROI_LOCATION = environ["STAVROI_LOCATION"]
stavroi = pd.read_excel(STAVROI_LOCATION)

# Filters to keep only the soldier entries
stavroi = stavroi.set_index("ΟΝΟΜΑ ΟΠΛΙΤΗ")
stavroi = stavroi.dropna(subset=['ΥΠΗΡΕΣΙΕΣ']).dropna(subset=['ΓΚΡΟΥΠ'])

# Creating a dictionary which will match a given surname to a full name
# Soldiers are stored as "{RANK} {SURNAME} {NAME}"
# We split the string and keep only the surname
# keys are surnames, values are ranks and full names
full_names = stavroi.index.values
unicode_surname_dict = {unidecode(sldr.split()[1]): sldr for sldr in full_names}

# Duties dictionary creation (to match codenames with explanation)
# For GitHub reviewers: This function is not included as it reveals sensitive information
import get_duties
DUTIES_DICT = get_duties.get_duties_dict()


# For calendar.datetime.weekday
DAYS_DICT = dict(enumerate(['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή']))


def map_name_input(surname: str, mapping_dict: dict) -> str:
    surname = unidecode(surname.upper())
    soldier_full_name = mapping_dict[surname]
    return soldier_full_name


def scan_duties(soldier_full_name: str, stavroi_excel: pd.DataFrame, duties_dict: dict, days_dict: dict) -> None:
    # Calendar stuff to get month, year and the amount of days in the current month
    cur_month = datetime.now().month
    cur_year = datetime.now().year
    _, month_range = monthrange(year=cur_year, month=cur_month)

    curr_day = datetime.today().day
    # We get a pd.Series with just the duties per day for simplicity reasons
    duties = stavroi_excel.loc[soldier_full_name][3+curr_day-1:3+month_range]

    scheduled_duty = False
    day_counter = curr_day
    for duty in duties:
        duty = str(duty).upper().strip()
        # IMPORTANT: When Python comes across an empty cell it's value is: nan of type float
        # Since you can't .upper() and .strip() a float, I am converting duty to a string always to catch that case
        if duty not in ('Ε', 'ΥΠΗΡ', 'NAN'):
            scheduled_duty = True
            day_name = days_dict[weekday(cur_year, cur_month, day_counter)]
            try:
                if duty == 'ΤΙΜ':
                    print(f'Την ημέρα {day_name} {day_counter}/{cur_month}/{cur_year} είσαι αδειούχος!🎉')
                elif duty == 'ΟΡΓ':
                    print(f'Την ημέρα {day_name} {day_counter}/{cur_month}/{cur_year} είσαι Όργανο.')
                elif duty == 'ΒΑΥΔΜ':
                    print(f'Την ημέρα {day_name} {day_counter}/{cur_month}/{cur_year} είσαι ΒΑΥΔΜ.')
                elif duty == 'ΚΑ':
                    print(f'Την ημέρα {day_name} {day_counter}/{cur_month}/{cur_year} έχεις ζητήσει κάτι.')
                else:
                    print(f'Την ημέρα {day_name} {day_counter}/{cur_month}/{cur_year} έχεις υπηρεσία: {duties_dict[duty]}.')
            except KeyError:
                # print(f'ΣΦΑΛΜΑ: ο κωδικός "{duty}", δεν αντιστοιχεί σε όνομα υπηρεσίας ({day_counter}/{cur_month}/{cur_year})')
                pass
        day_counter +=1  # we move on to the next day
    if scheduled_duty == False:
        print(f'Δεν υπάρχουν μελοντικά καταχωρημένες υπηρεσίες για εσένα (μέχρι στιγμής)...')
    return


if __name__ == "__main__":
    soldier_surname = input('Αλτ, τις ει;\n(επώνυμο): ')

    try:
        soldier_full_name = map_name_input(soldier_surname, unicode_surname_dict)
    except KeyError:
        print(f'Σφάλμα: Ο στρατιώτης με επώνυμο "{soldier_surname}" δε βρέθηκε.')
        # print(f"Σφάλμα: Το όνομα σου δε βρέθηκε στο Excel.\nΒεβαιώσου ότι το username σου στο Discord είναι σωστό και της μορφής '[Επώνυμο]<ΚΕΝΟ>[κινητό τηλέφωνο]' (πχ Παντόφλας 6912345678).")
    else:
        scan_duties(soldier_full_name=soldier_full_name,
                    stavroi_excel=stavroi,
                    duties_dict=DUTIES_DICT,
                    days_dict=DAYS_DICT)
