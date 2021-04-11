# Alan Liu
# Dr. Bhattacharya
# Capstone CS Final Project
# 2-1-2021

# This .py file contains both the ImportCSVData and Client classes.


import pandas
#import matplotlib.pyplot as plt

class ImportCSVData:

    # This class will read the two data sets of csv files and print only the essential columns.

    # printFile1 is for the Current_Wildfire_Perimeters data set (2020 US data)
    def printFile1(self):
        file1 = pandas.read_csv(r"/Users/alanliu/PycharmProjects/CSProject/Current_Wildfire_Perimeters.csv")
        name = file1.IncidentName
        size = file1.GISAcres
        date = file1.DateCurrent
        unit = file1.UnitID

        # Stores incident name, size, date, and unit ID in list
        data1 = [name, size, date, unit]

        print("Size(acres)      Date               Unit  Incident Name")

        # Loops through rows of data in csv file and only prints size, data, unit ID, and incident name
        count = 0
        for data in file1:
            print(size[count]),
            print(date[count]),
            print(unit[count]),
            print(name[count])
            count += 1

        print

        #plt.scatter(x='SHAPE_Length', y='GISAcres', c='DarkBlue')
        g1 = file1.plot.scatter(x='SHAPE_Length',
                                y='GISAcres',
                                c='DarkBlue')

        # Prints csv file for reference
        # print(file1)
        return

    # printFile2 is for the Historic_GeoMAC_Perimeters_2019 data set (2019 US data)
    def printFile2(self):
        # file2 is a DataFrame containing 2019 US data points
        file2 = pandas.read_csv(r"/Users/alanliu/PycharmProjects/CSProject/Historic_GeoMAC_Perimeters_2019.csv")
        agency = file2.agency
        datetime = file2.perimeterdatetime
        size = file2.gisacres
        state = file2.state

        # Stores agency, size, and date/time in list
        data2 = [agency, state, datetime, size]

        print("Agency/State Date          Size(acres)")

        # Loops through rows in csv file and only prints agency, state, date/time, and size
        count = 0
        for data in file2:
            print(agency[count]),
            print(state[count]),
            print(datetime[count]),
            print(size[count])
            count += 1

        print

        # Prints csv file for reference
        # print(file2)
        return


class Client:

    # This class is meant for the convenience of client use.

    # Get an instance of ImportCSVData to be able to access printFile1() and printFile2() from Client class
    pFile1 = ImportCSVData()
    pFile2 = ImportCSVData()

    # Call printFile1() and printFile2() from Client
    pFile1.printFile1()
    pFile2.printFile2()