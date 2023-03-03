import csv

with open("C:/StoreSales/Data/test.csv", "r") as f:
        reader = csv.reader(f)
        print(reader[-1])