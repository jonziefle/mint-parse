import os
import sys
import csv
import argparse
from decimal import Decimal

# global variables
categories = {
    "Auto & Transport" : {
        "sumTotal": [],
        "subcategories": {
            "Auto & Transport" : [],
            "Auto Insurance" : [],
            "Auto Insurance" : [],
            "Auto Payment" : [],
            "Gas & Fuel" : [],
            "Parking" : [],
            "Public Transportation" : [],
            "Service & Parts" : [],
        }
    },
    "Misc Expenses" : {
        "sumTotal": [],
        "subcategories": {}
    }
}

dateList = ["1/2017","2/2017","3/2017","4/2017","5/2017","6/2017","7/2017","8/2017","9/2017","10/2017","11/2017","12/2017"]

def main(inputFile, outputFile):
    # data object
    data = {}

    # initialize categories
    for category in categories:
        categories[category]["sumTotal"] = [0] * 12
        for subcategory in categories[category]["subcategories"]:
            categories[category]["subcategories"][subcategory] = [0] * 12

    # open and process csv file
    with open(inputFile, newline='') as csvfile:
        print("Processing: " + inputFile)
        csvreader = csv.reader(csvfile)

        # skip first row
        next(csvreader)

        # read csv rows
        for row in csvreader:
            csvDate = row[0].split("/")[0] + "/" + row[0].split("/")[2]
            csvSubcategory = row[5]

            csvAmount = round(Decimal(row[3]), 2)
            if (row[4] == "credit"):
                csvAmount *= -1

            if csvDate in dateList:
                index = dateList.index(csvDate)

                # set default category
                csvCategory = ""
                for category in categories:
                    if csvSubcategory in categories[category]["subcategories"]:
                        csvCategory = category
                        break

                # check to see if this is a new category
                if csvCategory == "":
                    csvCategory = "Misc Expenses"
                    categories[csvCategory]["subcategories"][csvSubcategory] = [0] * 12

                # add amount
                categories[csvCategory]["sumTotal"][index] += csvAmount
                categories[csvCategory]["subcategories"][csvSubcategory][index] += csvAmount

    # write csv data
    with open(outputFile, 'w', newline='') as csvfile:
        print("Writing: " + outputFile)
        csvwriter = csv.writer(csvfile)

        # write categories
        csvwriter.writerow(["Category"] + dateList)
        for category in categories:
            csvwriter.writerow([category] + categories[category]["sumTotal"])

        csvwriter.writerow([])

        # write subcategories
        csvwriter.writerow(["Subcategory"] + dateList)
        for category in categories:
            for subcategory in categories[category]["subcategories"]:
                csvwriter.writerow([subcategory] + categories[category]["subcategories"][subcategory])

if __name__ == "__main__":
    # parses command line for input file and output path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='<Required> Input File', required=True)
    parser.add_argument('--output', help='<Required> Output File', required=True)
    args = parser.parse_args()

    #print(args)

    # execute only if run as a script
    main(args.input, args.output)
