import os
import sys
import csv
import argparse

# global variables
categoryObject = {}
dateArray = ["1/2017","2/2017","3/2017","4/2017","5/2017","6/2017","7/2017","8/2017","9/2017","10/2017","11/2017","12/2017"]

def main(inputFile, outputFile):
    # data object
    data = {}

    # open and process csv file
    with open(inputFile, newline='') as csvfile:
        print("Processing: " + inputFile)
        csvreader = csv.reader(csvfile)

        # skip first row
        next(csvreader)

        # read csv rows
        for row in csvreader:
            date = row[0].split("/")[0] + "/" + row[0].split("/")[2]
            amount = row[3]
            category = row[5]

            if category not in categoryObject:
                categoryObject[category] = [0] * 12

            if date in dateArray:
                index = dateArray.index(date)
                categoryObject[category][index] += float(amount)

    # sort arrays
    dateArray.sort()

    # print csv data

    # write csv data
    with open(outputFile, 'w', newline='') as csvfile:
        print("Writing: " + outputFile)
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(["Category"] + dateArray)

        for key, value in categoryObject.items():
            csvwriter.writerow([key] + value)

if __name__ == "__main__":
    # parses command line for input file and output path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='<Required> Input File', required=True)
    parser.add_argument('--output', help='<Required> Output File', required=True)
    args = parser.parse_args()

    #print(args)

    # execute only if run as a script
    main(args.input, args.output)
