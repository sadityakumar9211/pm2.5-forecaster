"""
Author: Aditya Kumar Singh
Created on: 2022-10-14
"""

import os
from datetime import datetime
import requests
import sys


def retrieve_html():
    """retrieves the meteorological data from July 2018 to September 2022"""
    for year in range(2018, 2023):
        start_month = 7 if year == 2018 else 1
        end_month = 10 if year == 2022 else 13
        for month in range(start_month, end_month):
            if year == 2022 and month == 10:
                break

            if month <= 9:
                url = "https://en.tutiempo.net/climate/{}-0{}/ws-428070.html".format(month, year)
            else:
                url = "https://en.tutiempo.net/climate/{}-{}/ws-428070.html".format(month, year)

            # retrieves the entire html from the specified url
            texts = requests.get(url)
            text_utf = texts.text.encode('utf-8')

            if os.path.exists("Data/Html_Data/{}".format(year)) is False:
                os.makedirs("Data/Html_Data/{}".format(year))

            with open("Data/Html_Data/{}/{}.html".format(year, month), "wb") as output:
                output.write(text_utf)

        sys.stdout.flush()


if __name__ == "__main__":
    start_time = datetime.now()
    retrieve_html()
    end_time = datetime.now()
    print("Time taken: {} seconds".format((end_time - start_time).total_seconds()))
