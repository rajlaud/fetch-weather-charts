"""Download latest weatherfax charts from list in csv file."""

import csv
import os
import requests

PREFIX = "https://tgftp.nws.noaa.gov/fax/"
SUFFIX = ".TIF"
CHART_LIST = "charts.csv"
CHART_DIR = "charts/"

with open(CHART_LIST, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        filename = row["filename"] + SUFFIX
        url = PREFIX + filename
        destination = CHART_DIR + row["type"] + "/"
        destination_file = destination + filename
        etag_file = destination + ".etag_" + filename

        os.makedirs(destination, exist_ok=True)

        etag = None

        if os.path.exists(destination_file) and os.path.exists(etag_file):
            with open(etag_file, "r") as efile:
                etag = efile.readline()

        try:
            r = requests.head(url)
            if etag is None or r.headers["etag"] != etag:
                print(f"Downloading chart {url}")
                file_request = requests.get(url)
                with open(destination_file, "wb") as download:
                    download.write(file_request.content)
                with open(etag_file, "w") as efile:
                    efile.write(r.headers["etag"])
            else:
                print(f"Skipping chart {filename} because it is unmodified.")
        except requests.HTTPError as error:
            print(f"Download of {url} failed with {error}")
