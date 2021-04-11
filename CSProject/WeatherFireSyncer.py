# First function:
# input: station_id, time
# output: weather info (understand the features in the weather file)

# Second function:
# create table: station_id, county
# input: county
# output: stations

# Fire document: county, time, fire info
# Third function: used to create the dataset
# 1. scan all the fire data point --> county time size_of_fire (for loop)
#    find station_id using second function --> stations county time size_of_fire
#    find weather info using first function --> stations county time size_of_fire weather_info

# 2. Weather_info, size_of-fire → table num_rows num_fire_data_points, num_col weather_info + size_of_fire (numpy array)

import math
import pandas as pd
import numpy as np
import os
from os import path


class WeatherFireSyncer:

    def __init__(self, f_paths):
        self.df = self.read_fire_data(f_paths)

    fire_paths = ['CalFire2017.txt', 'CalFire2018.txt', 'CalFire2019.txt']
    county_paths = ['RAWS_Stations_CountiesCA.txt']

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

    # Reads in fire data from paths and creates dictionary with name, date, county, size, and % contained
    def read_fire_data(self, f_paths):

        init_data = {'name': [], 'date': [], 'county': [], 'size': [], '%_contained': [], 'high_temp': [],
                     'low_temp': [], 'high_humidity': [], 'low_humidity': [], 'wind_speed': [], 'wind_gust': [],
                     'fuel_temp': [], 'fuel_moisture': [], 'max_radiation': [], 'peak_wind_direction': []}

        for f_path in f_paths:
            file = open(f_path, 'r')

            count = 0
            while True:
                # get next line from file
                line = file.readline()

                if not line:
                    break

                if count % 5 == 0:
                    init_data['name'].append(line[0:-1])
                elif count % 5 == 1:
                    init_data['date'].append(line[0:-1])
                elif count % 5 == 2:
                    init_data['county'].append(line[0:-1])
                elif count % 5 == 3:
                    init_data['size'].append(self.str2int(line))
                else:
                    init_data['%_contained'].append(self.str2int(line))
                    init_data['high_temp'].append(None)
                    init_data['low_temp'].append(None)
                    init_data['high_humidity'].append(None)
                    init_data['low_humidity'].append(None)
                    init_data['wind_speed'].append(None)
                    # init_data['wind_direction'].append(None)
                    init_data['wind_gust'].append(None)
                    init_data['fuel_temp'].append(None)
                    init_data['fuel_moisture'].append(None)
                    init_data['max_radiation'].append(None)
                    init_data['peak_wind_direction'].append(None)

                count += 1
            file.close()

        return pd.DataFrame(data=init_data)  # self.data_frame()

    # for file in fire_paths:
    # read_fire_data(file)

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
                    counties.append(county[comma_indexes[placeholder_count-1]+2:index])
                placeholder_count += 1
            counties.append(county[comma_indexes[placeholder_count-1]+2:len(county)])
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

    # Re-formats start time from fire file to match that of weather file
    def find_start_time(self, fire_date):
        if len(fire_date) == 10:
            start_time = fire_date[6:10] + fire_date[0:2] + fire_date[3:5]
        elif len(fire_date) == 9 and fire_date[1] == "/":
            start_time = fire_date[5:9] + "0" + fire_date[0:1] + fire_date[2:4]
        elif len(fire_date) == 9:
            start_time = fire_date[5:9] + fire_date[0:2] + "0" + fire_date[3:4]
        else:
            start_time = fire_date[4:8] + "0" + fire_date[0:1] + "0" + fire_date[2:3]
        return start_time

    # Retrieve and add weather data for one particular station
    def read_weather_data(self, stn_id, fire_index):
        str_stn_id = str(stn_id)
        weather_file = open('ca/wx' + str_stn_id + '.fw13', 'r')

        fire_date = self.df.date[fire_index]
        # fire_date = self.init_data["date"][fire_index]
        time_counter = 0  # increments after every row (every day)

        start_time = self.find_start_time(fire_date)

        tot_high_temp = 0
        tot_low_temp = 0
        tot_high_humidity = 0
        tot_low_humidity = 0
        # tot_max_wind_speed = 0

        while True:
            # get next line from file
            line = weather_file.readline()

            if line[9:17] == start_time:  # or time_counter < tot_time:
                tot_high_temp += self.str2int(line[37:40])
                tot_low_temp += self.str2int(line[40:43])
                tot_high_humidity += self.str2int(line[43:46])
                tot_low_humidity += self.str2int(line[46:49])
                # tot_max_wind_speed += int(line[70:72])
                break

            if not line:
                break
            time_counter += 1

        weather_file.close()
        return [tot_high_temp, tot_low_temp, tot_high_humidity, tot_low_humidity]  # max_wind_speed

    # Adds averaged weather data across all stations in a county for each fire
    def avg_weather_data(self):
        fire_index = 0

        while True:
            weather_array = [0, 0, 0, 0]  # [high_temp, low_temp, high_humidity, low_humidity, max_wind_speed]

            # Break from loop condition (df rows are all traversed through)
            if fire_index >= len(self.df):
                break

            station_ids = self.stn_ids_in_county(self.df.county[fire_index], 'RAWS_Stations_CountiesCA.txt')
            for station in station_ids:
                init_weather_array = self.read_weather_data(station, fire_index)

                index = 0
                for _ in init_weather_array:
                    weather_array[index] += init_weather_array[index]
                    index += 1

            if len(station_ids) == 0:
                avg_high_temp = 0
                avg_low_temp = 0
                avg_high_humidity = 0
                avg_low_humidity = 0
            else:
                avg_high_temp = weather_array[0] / len(station_ids)
                avg_low_temp = weather_array[1] / len(station_ids)
                avg_high_humidity = weather_array[2] / len(station_ids)
                avg_low_humidity = weather_array[3] / len(station_ids)
                # avg_max_wind_speed = weather_array[4] / len(station_ids)

            # avg_high_temp = self.tot_high_temp / (len(self.stn_ids) * tot_time)
            # avg_low_temp = self.tot_low_temp / (len(self.stn_ids) * tot_time)
            # avg_high_humidity = self.tot_high_humidity / (len(self.stn_ids) * tot_time)
            # avg_low_humidity = self.tot_low_humidity / (len(self.stn_ids) * tot_time)
            # avg_max_wind_speed = self.tot_max_wind_speed / (len(self.stn_ids) * tot_time)
            self.df.at[fire_index, 'high_temp'] = avg_high_temp
            self.df.at[fire_index, 'low_temp'] = avg_low_temp
            self.df.at[fire_index, 'high_humidity'] = avg_high_humidity
            self.df.at[fire_index, 'low_humidity'] = avg_low_humidity
            # self.df.at[fire_index, 'max_wind'] = avg_max_wind_speed

            station_ids.clear()
            fire_index += 1

        return self.df

    # Maps counties to corresponding station names for MesoWest data
    def county_stn_mapper(self, counties, f_path):
        stn_county_file = open(f_path, 'r')
        stn_names = []

        county_list = counties.split(", ")
        county_list_new = []

        for _ in county_list:
            # Cases below are counties/states/countries outside of California
            # Remove these from counties list
            if _ in ["State of Nevada", "State of Oregon", "State of Arizona", "Mexico"]:
                pass
            # Cases below are counties without any RAWS stations (stn_ids will be empty)
            # Average values from stations in neighboring counties
            elif _ == "Sutter":
                county_list_new.append("Colusa")
                county_list_new.append("Yuba")
                county_list_new.append("Placer")
                county_list_new.append("Yolo")
            elif _ == "Solano":
                county_list_new.append("Napa")
                county_list_new.append("Yolo")
                county_list_new.append("Contra Costa")
            elif _ == "Sacramento":
                county_list_new.append("Yolo")
                county_list_new.append("Placer")
                county_list_new.append("El Dorado")
                county_list_new.append("Amador")
            elif _ == "San Francisco":
                county_list_new.append("Marin")
                county_list_new.append("San Mateo")
            elif _ == "San Joaquin":
                county_list_new.append("Stanislaus")
                county_list_new.append("Calaveras")
                county_list_new.append("Alameda")
                county_list_new.append("Contra Costa")
            else:
                county_list_new.append(_)

        county_list = list(set(county_list_new))

        for county in county_list:
            while True:
                line = stn_county_file.readline()

                if line[6:len(line)-1] == county:
                    stn_names.append(line[0:5])
                    break

                if not line:
                    break

        stn_county_file.close()
        return stn_names

    def find_start_time2(self, fire_date):
        if len(fire_date) == 10:
            start_time = fire_date[6:10] + "-" + fire_date[0:2] + "-" + fire_date[3:5]
        elif len(fire_date) == 9 and fire_date[1] == "/":
            start_time = fire_date[5:9] + "-0" + fire_date[0:1] + "-" + fire_date[2:4]
        elif len(fire_date) == 9:
            start_time = fire_date[5:9] + fire_date[0:2] + "-0" + fire_date[3:4]
        else:
            start_time = fire_date[4:8] + "-0" + fire_date[0:1] + "-0" + fire_date[2:3]
        return start_time

    def str2float(self, val):

        float_set = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        final_val = ""

        for _ in range(len(val)):
            item = val[_]
            if item in float_set:
                final_val += item
        # check if final_val is empty
        if final_val == "":
            return 0
        else:
            return float(final_val)

    # Adds wind speed, wind direction, wind gust, solar radiation, fuel temp, and fuel moisture features
    # FUNCTION NOT DONE YET
    def read_mesowest_data(self, stn_name, fire_index):
        file = open('MesoWest/' + stn_name + '.2020-01-01.csv', 'r')

        tot_wind_speed = 0
        # tot_wind_direction = 0
        tot_wind_gust = 0
        tot_fuel_temp = 0
        tot_fuel_moist = 0
        tot_max_radiation = 0
        tot_peak_wind = 0
        count = 0

        fire_date = self.df.date[fire_index]
        start_time = self.find_start_time2(fire_date)

        flag = False
        while True:
            line = file.readline()

            if count >= 100 or not line:
                break

            # If within 100 hours after the start time of fire
            if line[6:16] == start_time or flag:
                flag = True

                str_wind_speed = ""
                # str_wind_direction = ""
                str_wind_gust = ""
                str_max_radiation = ""
                str_solar_radiation = ""
                str_fuel_temp = ""
                str_fuel_moist = ""
                str_peak_wind = ""

                # Extract the data for features
                comma_count = 0
                for item in line:
                    if item == ",":
                        comma_count += 1

                    # Wind speed
                    if comma_count == 4 and item != ",":
                        str_wind_speed += item

                    # Wind direction
                    # if comma_count == 5 and item != ",":
                        # str_wind_direction += item

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

                tot_wind_speed += self.str2float(str_wind_speed)
                # tot_wind_direction += self.str2float(str_wind_direction)
                tot_wind_gust += self.str2float(str_wind_gust)
                tot_max_radiation += self.str2float(str_max_radiation)
                tot_fuel_temp += self.str2float(str_fuel_temp)
                tot_fuel_moist += self.str2float(str_fuel_moist)
                tot_peak_wind += self.str2float(str_peak_wind)

                count += 1

        file.close()
        return [tot_wind_speed, tot_wind_gust, tot_max_radiation, tot_fuel_temp, tot_fuel_moist, tot_peak_wind]

    def avg_mesowest_data(self):
        fire_index = 0

        while True:
            mw_array = [0, 0, 0, 0, 0, 0]

            # Break from loop condition (df rows are all traversed through)
            if fire_index == len(self.df):
                break

            station_names = self.county_stn_mapper(self.df.county[fire_index], 'Stn_Name_ID_Match.txt')
            # print(station_names)

            for station in station_names:
                init_mw_array = self.read_mesowest_data(station, fire_index)
                # print(init_mw_array)
                index = 0
                for _ in init_mw_array:
                    mw_array[index] += init_mw_array[index]
                    index += 1

            total_points = 100 * len(station_names)  # total number of data points for each feature
            if len(station_names) == 0:
                avg_wind_speed = 0
                # avg_wind_direction = 0
                avg_wind_gust = 0
                avg_max_radiation = 0
                avg_fuel_temp = 0
                avg_fuel_moist = 0
                avg_peak_wind = 0
            else:
                avg_wind_speed = mw_array[0] / total_points
                # avg_wind_direction = mw_array[1] / total_points
                avg_wind_gust = mw_array[1] / total_points
                avg_max_radiation = mw_array[2] / total_points
                avg_fuel_temp = mw_array[3] / total_points
                avg_fuel_moist = mw_array[4] / total_points
                avg_peak_wind = mw_array[5] / total_points

            self.df.at[fire_index, 'wind_speed'] = avg_wind_speed
            # self.df.at[fire_index, 'wind_direction'] = avg_wind_direction
            self.df.at[fire_index, 'wind_gust'] = avg_wind_gust
            self.df.at[fire_index, 'max_radiation'] = avg_max_radiation
            self.df.at[fire_index, 'fuel_temp'] = avg_fuel_temp
            self.df.at[fire_index, 'fuel_moisture'] = avg_fuel_moist
            self.df.at[fire_index, 'peak_wind_direction'] = avg_peak_wind

            fire_index += 1
            station_names.clear()

        return self.df

    # Creates DataFrame for inputting/extracting data
    def data_frame(self):
        df = pd.DataFrame(data=self.init_data)
        return df

    # Given a certain county retrieve which fires are within that county (defined as true if in county)
    def county_info(self, df, county):
        temp = df["county"].isin([county])
        idx = list(temp[temp == True].index)
        return df.loc[idx, :]


WFS = WeatherFireSyncer(['CalFire2017.txt', 'CalFire2018.txt', 'CalFire2019.txt'])
WFS.read_fire_data(['CalFire2017.txt', 'CalFire2018.txt', 'CalFire2019.txt'])
WFS.avg_weather_data()
WFS.avg_mesowest_data()