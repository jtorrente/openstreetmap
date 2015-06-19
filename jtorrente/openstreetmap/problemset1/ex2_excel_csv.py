# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
"""
example.csv:

Station|Year|Month|Day|Hour|Max Load
COAST|2013|01|01|10|12345.6
EAST|2013|01|01|10|12345.6
FAR_WEST|2013|01|01|10|12345.6
NORTH|2013|01|01|10|12345.6
NORTH_C|2013|01|01|10|12345.6
SOUTHERN|2013|01|01|10|12345.6
SOUTH_C|2013|01|01|10|12345.6
WEST|2013|01|01|10|12345.6
"""

import xlrd
import os
import csv
from zipfile import ZipFile

directory = "../../../data/"
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    data = [['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']]
    for i in range(1,9):
        data.append(process_region(sheet, i))

    return data

def process_region(sheet, region_col_index):
    region_name = sheet.cell_value(0, region_col_index)
    region_load_values = sheet.col_values(region_col_index, 1)
    max_load = max(region_load_values)
    max_load_row = region_load_values.index(max_load) + 1
    time = sheet.cell_value(max_load_row, 0)
    time_tuple = xlrd.xldate_as_tuple(time, 0)
    return [region_name, time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], max_load]

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'wb') as output_csv_file:
        writer = csv.writer(output_csv_file, delimiter='|')
        for row in data:
            writer.writerow(row)

    
def test():
    saved_path = os.getcwd()
    os.chdir(directory)

    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)
    os.chdir(saved_path)
        
if __name__ == "__main__":
    test()
