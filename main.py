import csv

with open("url_test.csv") as urlcsv:
    reader = csv.reader(urlcsv)
    for row in reader:
        print(row)