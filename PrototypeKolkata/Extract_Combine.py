import csv

import requests
import sys
import pandas as pd
import os
from bs4 import BeautifulSoup


def met_data(month, year):
    file_html = open('Data/Html_Data/{}/{}.html'.format(year, month), 'rb')
    plain_text = file_html.read()

    tempD = []
    finalD = []

    soup = BeautifulSoup(plain_text, "lxml")

    # single or multiple tables
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempD.append(a)  # 1-D list of temporary data

    rows = round(len(tempD) / 15)

    for times in range(rows):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD.pop(0))

        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length - 1)
    finalD.pop(0)

    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD


def data_combine(year, cs):
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":

    aqi = pd.read_csv('Data/AQI/July2018Sept2022.csv', delimiter=",")
    pm = aqi.iloc[:, 2].values.tolist()
    pm_index = 0

    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2018, 2023):
        start_month = 7 if year == 2018 else 1
        end_month = 10 if year == 2022 else 13

        final_data = []
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(start_month, end_month):
            temp = met_data(month, year)
            final_data = final_data + temp

        for i in range(len(final_data)):
            # final_data[i].insert(8, p,[i])
            final_data[i].insert(8, pm[i+pm_index])

        pm_index += len(final_data)

        with open('Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            # writing the row in the file if every data cell in the row is filled otherwise dropped.
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-" or elem == "None":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)

    data_2018 = data_combine(2018, 1000)
    data_2019 = data_combine(2019, 1000)
    data_2020 = data_combine(2020, 1000)
    data_2021 = data_combine(2021, 1000)
    data_2022 = data_combine(2022, 1000)
    total = data_2018 + data_2019 + data_2020 + data_2021 + data_2022

    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)

