import sys
import csv

# list of important keywords associated with the candidate names
KEYWORD_IDENTIFIERS = ["said", "Dr.", "Ph.D.", "PE", "president", "CEO", "by", "sen.", "senate", "officer", "attorney",
                       "quoted", "spokeswoman", "spokesman", "reporter", "actress", "father", "son", "mother",
                       "daughter", "Sheriff", "Justice", "chief"]


def check_suffix_salutations():
    """checks if the candidate name has any suffix salutations"""
    check_suffix_salutation = 0
    names = name.lower().split()
    suffix_salutations = ["Jr.", "Sr.", "I", "II", "III", "IV"]
    for salutation in suffix_salutations:

        if salutation.lower() in names:
            check_suffix_salutation = 1
    return check_suffix_salutation


def minimum_distance_to_eol():
    """finds the minimum distance to end of line for the candidate name"""
    eol_locations = []
    eol_location = -1

    # populate the eol locations array.
    while True:
        eol_location = file_contents.find("\n", eol_location + 1)
        if eol_location == -1:
            break

        eol_locations.extend([eol_location])

    # find the location of the closet eol char from the start or end position
    min_location_of_eol = -1
    for eol in eol_locations:
        if min_location_of_eol == -1 or abs(start_position - eol) < min_location_of_eol:
            min_location_of_eol = abs(start_position - eol)
        if min_location_of_eol == -1 or abs(end_position - eol) < min_location_of_eol:
            min_location_of_eol = abs(end_position - eol)

    #print('s', start_position, 'e', end_position, 'm', min_location_of_eol, 'eol', eol_locations)
    return min_location_of_eol


def minimum_distance_to_period():
    """finds the minimum distance to period for the candidate name"""
    period_locations = []
    period_location = -1

    # populate the period locations array
    while True:
        period_location = file_contents.find(".", period_location + 1)
        if period_location == -1:
            break

        period_locations.extend([period_location])

    # find the location of the closet period from the start or end position
    min_location_of_period = -1
    for p in period_locations:
        if min_location_of_period == -1 or abs(start_position - p) < min_location_of_period:
            min_location_of_period = abs(start_position - p)
        if min_location_of_period == -1 or abs(end_position - p) < min_location_of_period:
            min_location_of_period = abs(end_position - p)

    return min_location_of_period


def minimum_distance_to_keywords():
    """finds the minimum distance to important keywords for the candidate name"""
    location_of_closed_keyword = -1

    # find the location of the closest keyword from the start or end position
    for keyword in KEYWORD_IDENTIFIERS:
        keyword_location = -1
        while True:
            keyword_location = file_contents.lower().find(keyword.lower(), keyword_location + 1)
            if keyword_location == -1:
                break
            if location_of_closed_keyword == -1 or abs(start_position - keyword_location) < location_of_closed_keyword:
                location_of_closed_keyword = abs(start_position - keyword_location)
            if location_of_closed_keyword == -1 or abs(end_position - keyword_location) < location_of_closed_keyword:
                location_of_closed_keyword = abs(end_position - keyword_location)

    return location_of_closed_keyword


with open("../../Output/" + sys.argv[1], "r") as intermediateFeaturesFile:
    intermediateFeatureReader = csv.DictReader(intermediateFeaturesFile)
    fieldnames = ['id', 'name', 'some_capitalized', 'atleast_one_capitalized', 'first_letter_capitalized',
                  'has_suffix_salutation', 'start_position', 'distance_to_period', 'distance_to_closest_keyword',
                  'frequency', 'contains_period', 'contains_keywords', 'name_length', 'number_of_capitals', 'distance_to_closest_eol', 'label']

    output = csv.DictWriter(open("../../Output/" + sys.argv[2], "w"), fieldnames=fieldnames)
    output.writeheader()

    for row in intermediateFeatureReader:
        identifier = row['id']
        name = row['name']
        number_of_capitals = sum(1 for c in name if c.isupper())
        contains_period = 0 if name.find(".") == -1 else 1
        name_length = len(name)
        some_capitalized = 1 if number_of_capitals >= 2 else 0
        atleast_one_capitalized = 1 if number_of_capitals >= 1 else 0
        first_letter_capitalized = 1 if name[0].isupper() else 0
        has_suffix_salutations = check_suffix_salutations()
        start_position = int(row['start_position'])
        end_position = int(row['end_position'])
        label = row['label']
        frequency = row['frequency']

        file_name = row['file_name'];
        reference_file = open("../../data/" + sys.argv[3] + "/" + file_name, 'r')
        file_contents = reference_file.read()

        min_distance_to_period = minimum_distance_to_period()
        min_distance_to_key_words = minimum_distance_to_keywords()
        min_distance_to_eol = minimum_distance_to_eol()

        contains_keywords = 0
        for keyword in KEYWORD_IDENTIFIERS:
            if name.lower().find(keyword.lower()) != -1:
                contains_keywords = 1
                break

        output.writerow({'id': identifier,
                         'name': name,
                         'some_capitalized': some_capitalized,
                         'atleast_one_capitalized': atleast_one_capitalized,
                         'first_letter_capitalized': first_letter_capitalized,
                         'has_suffix_salutation': has_suffix_salutations,
                         'start_position': start_position,
                         'distance_to_period': min_distance_to_period,
                         'distance_to_closest_keyword': min_distance_to_key_words,
                         'frequency': frequency,
                         'contains_period': contains_period,
                         'contains_keywords': contains_keywords,
                         'name_length': name_length,
                         'number_of_capitals': number_of_capitals,
                         'distance_to_closest_eol': min_distance_to_eol,
                         'label': label})
