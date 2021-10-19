"""Download latest weatherfax charts from list in csv file."""

import csv
import os
import urllib.request
import urllib.error

PREFIX = "https://tgftp.nws.noaa.gov/fax/"
SUFFIX = ".TIF"
CHART_LIST = "charts.csv"
CHART_DIR = "charts/"

with open(CHART_LIST, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        available = [
            int(x) for x in row["available"].split(",")
        ]  # not doing anything yet
        filename = row["filename"] + SUFFIX
        url = PREFIX + filename
        destination = CHART_DIR + row["type"] + "/"
        os.makedirs(destination, exist_ok=True)
        print(f"Downloading chart {url}")
        try:
            urllib.request.urlretrieve(url, destination + filename)
        except urllib.error.HTTPError as error:
            print(f"Download of {url} failed with {error}")
