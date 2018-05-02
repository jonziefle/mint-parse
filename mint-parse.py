import os
import sys
import csv
import argparse
from decimal import Decimal

# global variables
categories = {
    "Income" : {
        "subcategories": {
            "Interest Income" : [],
            "Investments": []
        }
    },
    "Auto & Transport" : {
        "subcategories": {
            "Auto Insurance" : [],
            "Auto Payment" : [],
            "Gas & Fuel" : [],
            "Parking" : [],
            "Public Transportation" : [],
            "Service & Parts" : []
        }
    },
    "Bills & Utilities" : {
        "subcategories": {
            "Internet" : [],
            "Mobile Phone" : [],
            "Television" : [],
            "Utilities" : []
        }
    },
    "Business Services" : {
        "subcategories": {
            "Office Supplies" : [],
            "Printing" : [],
            "Shipping" : []
        }
    },
    "Education" : {
        "subcategories": {
            "Student Loan" : [],
            "Tuition" : []
        }
    },
    "Entertainment" : {
        "subcategories": {
            "Amusement" : [],
            "Arts" : [],
            "Movies & DVDs" : [],
            "Music" : [],
            "Newspapers & Magazines" : []
        }
    },
    "Fees & Charges" : {
        "subcategories": {
            "ATM Fee" : [],
            "Bank Fee" : [],
            "Service Fee" : []
        }
    },
    "Financial" : {
        "subcategories": {
			"College Savings" : [],
            "Financial Advisor" : [],
            "Life Insurance" : [],
			"Retirement" : [],
        }
    },
    "Food & Dining" : {
        "subcategories": {
            "Alcohol & Bars" : [],
            "Coffee Shops" : [],
            "Fast Food" : [],
            "Groceries" : [],
            "Restaurants" : []
        }
    },
    "Gifts & Donations" : {
        "subcategories": {
            "Charity" : [],
            "Gift" : []
        }
    },
    "Health & Fitness" : {
        "subcategories": {
            "Dentist" : [],
            "Doctor" : [],
            "Eyecare" : [],
            "Gym": [],
            "Health Insurance" : [],
            "Pharmacy" : [],
            "Sports" : []
        }
    },
    "Home" : {
        "subcategories": {
            "Furnishings" : [],
            "Home Improvement" : [],
            "Home Insurance" : [],
            "Home Services" : [],
            "Home Supplies" : [],
            "Lawn & Garden" : [],
            "Mortgage & Rent" : []
        }
    },
    "Kids" : {
        "subcategories": {
            "Allowance" : [],
            "Baby Supplies" : [],
            "Babysitter & Daycare" : [],
            "Child Support" : [],
            "Kids Activities" : [],
            "Toys" : []
        }
    },
    "Misc Expenses" : {
        "subcategories": {}
    },
    "Personal Care" : {
        "subcategories": {
            "Hair" : [],
            "Laundry" : [],
            "Spa & Massage" : []
        }
    },
    "Pets" : {
        "subcategories": {
            "Pet Food & Supplies" : [],
            "Pet Grooming" : [],
            "Veterinary" : []
        }
    },
    "Shopping" : {
        "subcategories": {
            "Books" : [],
            "Clothing" : [],
            "Electronics & Software" : [],
            "Hobbies" : [],
            "Sporting Goods" : []
        }
    },
    "Taxes" : {
        "subcategories": {
            "Federal Tax" : [],
            "Local Tax" : [],
            "State Tax" : []
        }
    },
    "Travel" : {
        "subcategories": {
            "Air Travel" : [],
            "Hotel" : [],
            "Rental Car & Taxi" : [],
            "Vacation" : []
        }
    },
    "Transfer for Cash Spending" : {
        "subcategories": {}
    },
    "Excluded" : {
        "subcategories": {
            "Transfer": [],
            "Credit Card Payment" : []
        }
    }
}

def main(inputFile, dataRange):
    # initialize dates
    dateList = []
    dateRange = dataRange.split('-')
    if (len(dateRange) == 2 and dateRange[1] > dateRange[0]):
        startDate = dateRange[0]
        endDate = dateRange[1]
    else:
        startDate = dateRange[0]
        endDate = dateRange[0]

    for year in range(int(startDate), int(endDate) + 1):
        for month in range(1, 13):
            date = str(month) + "/" + str(year)
            dateList.append(date)

    # initialize categories
    for category in categories:
        categories[category]["general"] = [0] * len(dateList)
        categories[category]["sumTotal"] = [0] * len(dateList)
        for subcategory in categories[category]["subcategories"]:
            categories[category]["subcategories"][subcategory] = [0] * len(dateList)

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

            if csvDate in dateList:
                index = dateList.index(csvDate)

                # set default category
                csvCategory = ""
                for category in categories:
                    if csvSubcategory in categories[category]["subcategories"]:
                        csvCategory = category
                        break
                    elif csvSubcategory == category:
                        csvCategory = csvSubcategory
                        break

                # check to see if this is a new category
                if csvCategory == "":
                    csvCategory = "Misc Expenses"
                    categories[csvCategory]["subcategories"][csvSubcategory] = [0] * len(dateList)

                # add credit/debit factor
                if (row[4] == "credit" and csvCategory != "Income"):
                    csvAmount *= -1

                # add amount
                if csvCategory == csvSubcategory:
                    categories[csvCategory]["general"][index] += csvAmount
                else:
                    categories[csvCategory]["subcategories"][csvSubcategory][index] += csvAmount

                categories[csvCategory]["sumTotal"][index] += csvAmount

    # write csv data
    outputFile = os.path.splitext(inputFile)[0] + "_output" + os.path.splitext(inputFile)[1]
    with open(outputFile, 'w', newline='') as csvfile:
        print("Writing: " + outputFile)
        csvwriter = csv.writer(csvfile)

        # write income
        csvwriter.writerow(["Income Details"] + dateList)
        category = "Income"
        csvwriter.writerow(["General"] + categories[category]["general"])
        for subcategory in categories[category]["subcategories"]:
            csvwriter.writerow([subcategory] + categories[category]["subcategories"][subcategory])
        csvwriter.writerow([])

        # write expense
        csvwriter.writerow(["Expense Summary"] + dateList)
        for category in categories:
            if category not in ["Income", "Excluded"]:
                csvwriter.writerow([category] + categories[category]["sumTotal"])

        csvwriter.writerow([])

        # write expense details
        csvwriter.writerow(["Expense Details"] + dateList)
        for category in categories:
            if category not in ["Income", "Excluded"]:
                csvwriter.writerow([category + ": " + "General"] + categories[category]["general"])
                for subcategory in categories[category]["subcategories"]:
                    csvwriter.writerow([category + ": " + subcategory] + categories[category]["subcategories"][subcategory])

if __name__ == "__main__":
    # parses command line for input file and output path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='<Required> Input File', required=True)
    parser.add_argument('--range', help='<Required> Single year (2018) or Multiyear (2015-2018)', required=True)
    args = parser.parse_args()

    #print(args)

    # execute only if run as a script
    main(args.input, args.range)
