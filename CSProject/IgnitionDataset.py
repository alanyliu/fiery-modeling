import pandas as pd
import numpy as np
import os
from os import path
import random


class IgnitionDataSyncer:

    def __init__(self, f_paths, county_list):
        self.df = self.read_fire_data(f_paths, county_list)
        self.df_updated = pd.DataFrame()

    fire_paths = ['CalFire2017.txt', 'CalFire2018.txt', 'CalFire2019.txt']

    # Converts string to integer (removes extraneous symbols like , and %)
    @staticmethod
    def str2int(val):
        number_set = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        final_val = ""

        for _ in range(len(val)):
            item = val[_]
            if item in number_set:
                final_val += item
        # check if final_val is empty
        if final_val == "":
            return 0
        else:
            return int(final_val)

    def format_start_time(self, date):
        if len(date) == 11:
            time = date[6:10] + "-" + date[0:2] + "-" + date[3:5]
        elif len(date) == 10 and date[1] == "/":
            time = date[5:9] + "-0" + date[0:1] + "-" + date[2:4]
        elif len(date) == 10:
            time = date[5:9] + "-" + date[0:2] + "-0" + date[3:4]
        else:
            time = date[4:8] + "-0" + date[0:1] + "-0" + date[2:3]
        return time

    def start_time_no_hyphens(self, date):
        time = ""
        for item in date:
            if item == "-":
                pass
            else:
                time += item
        return time

    # Reads in fire data from paths and creates dictionary with name, date, county, size, and % contained
    def read_fire_data(self, f_paths, county_list):

        init_data = {'yes_no_fire': [], 'date': [], 'fire_index': [], 'fire_county': [], 'temp1': [], 'hum1': [],
                     'wind_spd1': [], 'wind_gust1': [], 'fuel_temp1': [], 'fuel_moist1': [], 'max_rad1': [],
                     'pk_wind_dir1': [], 'temp2': [], 'hum2': [], 'wind_spd2': [], 'wind_gust2': [], 'fuel_temp2': [],
                     'fuel_moist2': [], 'max_rad2': [], 'pk_wind_dir2': [], 'temp3': [], 'hum3': [], 'wind_spd3': [],
                     'wind_gust3': [], 'fuel_temp3': [], 'fuel_moist3': [], 'max_rad3': [], 'pk_wind_dir3': [],
                     'temp4': [], 'hum4': [], 'wind_spd4': [], 'wind_gust4': [], 'fuel_temp4': [], 'fuel_moist4': [],
                     'max_rad4': [], 'pk_wind_dir4': [], 'temp5': [], 'hum5': [], 'wind_spd5': [], 'wind_gust5': [],
                     'fuel_temp5': [], 'fuel_moist5': [], 'max_rad5': [], 'pk_wind_dir5': []}

        for f_path in f_paths:
            file = open(f_path, 'r')

            day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                   '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']
            month = day[0:12]
            year = f_path[7:11]

            for m in month:
                for d in day:
                    init_data['yes_no_fire'].append("No")
                    init_data['date'].append(year + "-" + m + "-" + d)
                    init_data['fire_index'].append(-1)
                    init_data['fire_county'].append(None)

                    count1to5 = 1
                    while True:
                        str_count = str(count1to5)
                        init_data['temp' + str_count].append(None)
                        init_data['hum' + str_count].append(None)
                        init_data['wind_spd' + str_count].append(None)
                        init_data['wind_gust' + str_count].append(None)
                        init_data['fuel_temp' + str_count].append(None)
                        init_data['fuel_moist' + str_count].append(None)
                        init_data['max_rad' + str_count].append(None)
                        init_data['pk_wind_dir' + str_count].append(None)

                        count1to5 += 1
                        if count1to5 == 6:
                            break

                if m == '02':
                    pass
                else:
                    simple_count = 0
                    while True:
                        init_data['yes_no_fire'].append("No")
                        init_data['fire_index'].append(-1)
                        init_data['fire_county'].append(None)

                        count1to5 = 1
                        while True:
                            str_count = str(count1to5)
                            init_data['temp' + str_count].append(None)
                            init_data['hum' + str_count].append(None)
                            init_data['wind_spd' + str_count].append(None)
                            init_data['wind_gust' + str_count].append(None)
                            init_data['fuel_temp' + str_count].append(None)
                            init_data['fuel_moist' + str_count].append(None)
                            init_data['max_rad' + str_count].append(None)
                            init_data['pk_wind_dir' + str_count].append(None)

                            count1to5 += 1
                            if count1to5 == 6:
                                break

                        if simple_count == 0:
                            init_data['date'].append(year + "-" + m + "-" + "29")
                        else:
                            init_data['date'].append(year + "-" + m + "-" + "30")
                            break

                        simple_count += 1

                    if m in ['01', '03', '05', '07', '08', '10', '12']:
                        init_data['yes_no_fire'].append("No")
                        init_data['date'].append(year + "-" + m + "-" + "31")
                        init_data['fire_index'].append(-1)
                        init_data['fire_county'].append(None)

                        count1to5 = 1
                        while True:
                            str_count = str(count1to5)
                            init_data['temp' + str_count].append(None)
                            init_data['hum' + str_count].append(None)
                            init_data['wind_spd' + str_count].append(None)
                            init_data['wind_gust' + str_count].append(None)
                            init_data['fuel_temp' + str_count].append(None)
                            init_data['fuel_moist' + str_count].append(None)
                            init_data['max_rad' + str_count].append(None)
                            init_data['pk_wind_dir' + str_count].append(None)

                            count1to5 += 1
                            if count1to5 == 6:
                                break

            count = 0  # line in file counter
            temp_index = 0  # temporary placeholder for date_index
            flag = False  # set to True when date matches line in file, set back to False after df updated
            while True:
                # get next line from file
                line = file.readline()

                if not line:
                    break

                date_index = 0
                if "/" in line:
                    for date in init_data["date"]:
                        if self.format_start_time(line) == date:
                            flag = True
                            temp_index = date_index
                            break
                        date_index += 1
                if flag and count % 5 == 2:
                    flag = False
                    county_index = 1
                    
                    for _ in county_list:
                        if line[:-1] == _:
                            init_data["yes_no_fire"][temp_index] = "Yes"
                            init_data["fire_index"][temp_index] = county_index - 1
                            # init_data["fire" + str(county_index)][temp_index] = 1
                            init_data['fire_county'][temp_index] = line[:-1]

                        county_index += 1

                count += 1

            file.close()

        self.df = pd.DataFrame(data=init_data)
        print(self.df)
        return self.df

    # Output all station IDs within given county/counties
    def stn_ids_in_county(self, county, f_path):
        stn_ids = []
        county_file = open(f_path, 'r')

        # Find the county "ID"
        count = 1
        county_id = 0  # If no county in county_file matches, then default set to 00

        # Checks if there are multiple counties the fire spans, appends indexes of comma locations to list
        comma_indexes = []
        comma_index = 0
        for item in county:
            if item == ",":
                comma_indexes.append(comma_index)
            comma_index += 1

        # Adds separate county names into list (if there are more than one counties covered)
        counties = []
        if len(comma_indexes) > 0:
            placeholder_count = 0
            for index in comma_indexes:
                if placeholder_count == 0:
                    counties.append(county[0:index])
                else:
                    counties.append(county[comma_indexes[placeholder_count - 1] + 2:index])
                placeholder_count += 1
            counties.append(county[comma_indexes[placeholder_count - 1] + 2:len(county)])
        else:
            counties.append(county)

        # Anomaly cases below
        counties_new = []
        for _ in counties:
            # Cases below are counties/states/countries outside of California
            # Remove these from counties list
            if _ in ["State of Nevada", "State of Oregon", "State of Arizona", "Mexico"]:
                pass
            # Cases below are counties without any RAWS stations (stn_ids will be empty)
            # Average values from stations in neighboring counties
            elif _ == "Sutter":
                counties_new.append("Colusa")
                counties_new.append("Yuba")
                counties_new.append("Placer")
                counties_new.append("Yolo")
            elif _ == "Solano":
                counties_new.append("Napa")
                counties_new.append("Yolo")
                counties_new.append("Contra Costa")
            elif _ == "Sacramento":
                counties_new.append("Yolo")
                counties_new.append("Placer")
                counties_new.append("El Dorado")
                counties_new.append("Amador")
            elif _ == "San Francisco":
                counties_new.append("Marin")
                counties_new.append("San Mateo")
            elif _ == "San Joaquin":
                counties_new.append("Stanislaus")
                counties_new.append("Calaveras")
                counties_new.append("Alameda")
                counties_new.append("Contra Costa")
            else:
                counties_new.append(_)

        counties = list(set(counties_new))

        # Determine county/counties' IDs and find all station IDs within those county/counties
        for a_county in counties:
            while True:
                line = county_file.readline()

                if line[0:-1] == a_county:
                    county_id = count
                count += 1

                if count > 58:
                    break

            # Convert county ID into string format
            if county_id < 10:
                str_county_id = "0" + str(county_id)
            else:
                str_county_id = str(county_id)

            # Add all station IDs within a county to stn_ids
            id_count = 1
            while True:
                if id_count < 10:
                    if path.exists('ca/wx04' + str_county_id + '0' + str(id_count) + '.fw13'):
                        stn_ids.append("04" + str_county_id + '0' + str(id_count))
                else:
                    if path.exists('ca/wx04' + str_county_id + str(id_count) + '.fw13'):
                        stn_ids.append("04" + str_county_id + str(id_count))

                id_count += 1
                if id_count >= 100:
                    break

        county_file.close()
        return stn_ids

    # Converts string to float
    def str2float(self, val):
        float_set = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        final_val = ""

        count = 0
        negate = False
        for _ in range(len(val)):
            item = val[_]
            if item in float_set:
                final_val += item

            if count == 0 and item == "-":
                negate = True
            count += 1

        # check if final_val is empty
        if final_val == "":
            return 0
        elif negate:
            return -float(final_val)
        else:
            return float(final_val)

    # Returns station abbreviation within a specified county
    def cty_stn_mapper(self, county):
        cty_stn_file = open('Stn_Name_ID_Match.txt', 'r')
        stn_abv = ""
        while True:
            line = cty_stn_file.readline()

            if line[6:-1] == county:
                stn_abv = line[0:5]
                break

            if not line:
                break

        return stn_abv

    # Given a set of counties, enter weather data into DataFrame from 2017-19
    # r_paths = RAWS, m_paths = MesoWest, county_list: counties for consideration
    def read_weather_data(self, county_list):

        # Adding weather data by opening MesoWest file
        county_count = 1  # county number from 1 to 5
        for county in county_list:
            stn = self.cty_stn_mapper(county)
            m_file = open('MesoWest/' + stn + '.2020-01-01.csv')

            tot_air_temp = 0
            tot_humidity = 0
            tot_wind_speed = 0
            tot_wind_gust = 0
            tot_fuel_temp = 0
            tot_fuel_moist = 0
            tot_max_radiation = 0
            tot_peak_wind = 0

            hour_count = 0
            date_index = 0
            while True:
                line = m_file.readline()

                if not line:
                    break

                str_air_temp = ""
                str_humidity = ""
                str_wind_speed = ""
                str_wind_gust = ""
                str_max_radiation = ""
                str_solar_radiation = ""
                str_fuel_temp = ""
                str_fuel_moist = ""
                str_peak_wind = ""

                comma_count = 0
                for item in line:
                    if item == ",":
                        comma_count += 1

                    # Air temperature
                    if comma_count == 2 and item != ",":
                        str_air_temp += item

                    # Wind speed
                    if comma_count == 3 and item != ",":
                        str_humidity += item

                    # Wind speed
                    if comma_count == 4 and item != ",":
                        str_wind_speed += item

                    # Wind gust
                    if comma_count == 6 and item != ",":
                        str_wind_gust += item

                    # Solar radiation
                    if comma_count == 8 and item != ",":
                        str_solar_radiation += item
                    elif comma_count == 9 and item == ",":
                        # Set max radiation of that day if new solar radiation value is greater than current max
                        if self.str2float(str_solar_radiation) > self.str2float(str_max_radiation):
                            str_max_radiation = str_solar_radiation

                    # Fuel temperature
                    if comma_count == 11 and item != ",":
                        str_fuel_temp += item

                    # Fuel moisture
                    if comma_count == 12 and item != ",":
                        str_fuel_moist += item

                    # Peak wind direction
                    if comma_count == 13 and item != ",":
                        str_peak_wind += item

                tot_air_temp += 1.8 * self.str2float(str_air_temp) + 32
                tot_humidity += self.str2float(str_humidity)
                tot_wind_speed += self.str2float(str_wind_speed)
                tot_wind_gust += self.str2float(str_wind_gust)
                tot_max_radiation += self.str2float(str_max_radiation)
                tot_fuel_temp += self.str2float(str_fuel_temp)
                tot_fuel_moist += self.str2float(str_fuel_moist)
                tot_peak_wind += self.str2float(str_peak_wind)

                hour_count += 1
                # Add values to DataFrame every 24 hours (for each day) for a station
                if hour_count == 24:
                    hour_count = 0
                    str_county_count = str(county_count)
                    self.df.at[date_index, 'temp' + str_county_count] = tot_air_temp / 24
                    self.df.at[date_index, 'hum' + str_county_count] = tot_humidity / 24
                    self.df.at[date_index, 'wind_spd' + str_county_count] = tot_wind_speed / 24
                    self.df.at[date_index, 'wind_gust' + str_county_count] = tot_wind_gust / 24
                    self.df.at[date_index, 'fuel_temp' + str_county_count] = tot_fuel_temp / 24
                    self.df.at[date_index, 'fuel_moist' + str_county_count] = tot_fuel_moist / 24
                    self.df.at[date_index, 'max_rad' + str_county_count] = tot_max_radiation / 24
                    self.df.at[date_index, 'pk_wind_dir' + str_county_count] = tot_peak_wind / 24
                    tot_air_temp = 0
                    tot_humidity = 0
                    tot_wind_speed = 0
                    tot_wind_gust = 0
                    tot_fuel_temp = 0
                    tot_fuel_moist = 0
                    tot_max_radiation = 0
                    tot_peak_wind = 0
                    date_index += 1

            county_count += 1
            m_file.close()

        print(self.df)
        return self.df

    # Tracks indices of rows without a fire (can be removed from final data set)
    def remove_zero(self):
        zero_rows = []  # contains all indices of rows without a fire
        count = 0
        while True:
            if self.df.fire_index[count] == -1:
                zero_rows.append(count)
            count += 1
            if count >= len(self.df):
                break

        return zero_rows

    def fill_csv(self):
        zeroes = self.remove_zero()
        zeroes.append(1087)
        zeroes.append(1088)
        zeroes.append(1089)
        zeroes.append(1090)
        zeroes.append(1091)
        zeroes.append(1092)
        zeroes.append(1093)
        zeroes.append(1094)
        self.df_updated = self.df.drop(zeroes)
        # self.df_updated = self.df.drop([1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094])
        self.df_updated.to_csv('Dataset_ignition.csv')


select_counties = ['Monterey', 'Butte', 'Riverside', 'Tehama', 'San Diego']

IDS = IgnitionDataSyncer(['CalFire2017.txt', 'CalFire2018.txt', 'CalFire2019.txt'], select_counties)
IDS.read_weather_data(select_counties)
IDS.fill_csv()
