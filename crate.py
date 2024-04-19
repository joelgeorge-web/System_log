#create a csv file name data.csv

# Import the necessary libraries
import csv
import os

#create the csv
def create_csv():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number"])
        print("CSV file created successfully")


#save the csv
def save_csv(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data])
        print("Data saved successfully")

