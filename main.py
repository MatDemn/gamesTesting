# script variables (MIGHT BE EDITED BY USER)
MIN_YEAR = 1800 # bounds: [1800;2299]
MAX_YEAR = 2299 # bounds: [1800;2299]
DEFAULT_OUTPUT_ROW_COUNT = 20 # bounds: [1;10000]
WRITE_HEADER = True # Header in result file: Name,Last Name,City,Pesel number
MAX_TRIES = 3 # Number of tries before random module turns off 
#             # (infinite loop protection, should be keeped low)

# necessary imports
import sys
import random
import datetime
import csv

# custom imports
from libs.pesel import Pesel
from libs.gender import Gender

def prevalidate_input():
    '''
    Normalize input variables
    '''
    global MIN_YEAR, MAX_YEAR, DEFAULT_OUTPUT_ROW_COUNT, WRITE_HEADER, MAX_TRIES
    if(MIN_YEAR < 1800):
        MIN_YEAR = 1800
    if(MIN_YEAR > 2299):
        MIN_YEAR = 2299
    if(MAX_YEAR < 1800):
        MAX_YEAR = 1800
    if(MAX_YEAR > 2299):
        MAX_YEAR = 2299
    if(MIN_YEAR>MAX_YEAR):
        temp = MIN_YEAR
        MIN_YEAR = MAX_YEAR
        MAX_YEAR = temp
    if(DEFAULT_OUTPUT_ROW_COUNT > 10000):
        DEFAULT_OUTPUT_ROW_COUNT = 10000
    if(DEFAULT_OUTPUT_ROW_COUNT < 0):
        DEFAULT_OUTPUT_ROW_COUNT = 1
    WRITE_HEADER = bool(WRITE_HEADER)
    if(MAX_TRIES > 42):
        MAX_TRIES = 42

def gen_random_date():
    '''
        Generate random date in datetime format
        Source: https://www.adamsmith.haus/python/answers/how-to-generate-a-random-date-between-two-dates-in-python
    '''
    global MIN_YEAR, MAX_YEAR
    min_date = datetime.datetime(MIN_YEAR, 1, 1)
    max_date = datetime.datetime(MAX_YEAR, 12, 31)

    days_between_dates = (max_date - min_date).days
    random_number_of_days = random.randrange(days_between_dates)
    return min_date + datetime.timedelta(days=random_number_of_days)

def correct_gender_input(gender):
    '''
        Set gender to correct enum
    '''
    return Gender.Female if gender == "K" else Gender.Male

def main():
    '''
        Main function running whole program
    '''
    global DEFAULT_OUTPUT_ROW_COUNT, MAX_TRIES
    # Setting bound for output data
    if(len(sys.argv) >= 2):
        # case for one-argument setup
        DEFAULT_OUTPUT_ROW_COUNT = int(sys.argv[1])

    # Prevalidate constants and other stuff
    prevalidate_input()

    names_list, last_names_list, cities_list = ([],[],[])
    # Open input files
    try: 
        with open("./input/names.txt", mode="r", encoding="utf-8") as names_file, \
        open("./input/last_names.txt", mode="r", encoding="utf-8") as last_names_file, \
        open("./input/cities.txt", mode="r", encoding="utf-8") as cities_file:
            # Load input data
            names_list = names_file.read().splitlines()
            last_names_list = last_names_file.read().splitlines()
            cities_list = cities_file.read().splitlines()
    except IOError as e:
        print(f"Opening input files failed {e.strerror}")
        sys.exit()

    if(len(names_list) == 0):
        print("ERROR: names.txt file is empty...")
        sys.exit()
    if(len(last_names_list) == 0):
        print("ERROR: last_names.txt file is empty...")
        sys.exit()
    if(len(cities_list) == 0):
        print("ERROR: cities.txt file is empty...")
        sys.exit()

    # Generate data
    result_data = set()
    try:
        with open("./output/result.csv", mode="w", encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if(WRITE_HEADER):
                csv_writer.writerow(["Name", "Last Name", "City", "Pesel number"])
            tries = 0
            while(len(result_data) != DEFAULT_OUTPUT_ROW_COUNT):
                name_part = random.choice(names_list)
                gender = correct_gender_input(name_part[-1])
                name_part = name_part[:-2]
                last_name_part = random.choice(last_names_list)
                city_part = random.choice(cities_list)
                pesel_part = str(Pesel(gen_random_date(), gender))
                to_add_data = [name_part,last_name_part,city_part,pesel_part]
                to_add_data_str = ",".join(to_add_data)
                if(to_add_data_str in result_data):
                    if(tries > MAX_TRIES):
                        break
                    tries += 1
                else:
                    tries = 0
                    result_data.add(to_add_data_str)
                    csv_writer.writerow(to_add_data)
        csv_file.close()    
        print(f"Generating data finished succesfully! Saved {len(result_data)} entries.")  

    except IOError as e:
        print(f"Opening input files failed {e.strerror}")
        sys.exit()
    
if __name__ == "__main__":
    main()

    




