import os
import sys
import csv
import argparse
from decimal import Decimal

# global variables
categories = {
    "Income" : {
        "sumTotal": [],
        "subcategories": {
            "Income" : [],
            "Bonus" : [],
            "Interest Income" : [],
            "Paycheck" : [],
            "Reimbursement" : [],
            "Rental Income" : [],
            "Returned Purchase" : []
        }
    },
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
            "Service & Parts" : []
        }
    },
    "Bills & Utilities" : {
        "sumTotal": [],
        "subcategories": {
            "Bills & Utilities" : [],
            "Home Phone" : [],
            "Internet" : [],
            "Mobile Phone" : [],
            "Television" : [],
            "Utilities" : []
        }
    },
    "Business Services" : {
        "sumTotal": [],
        "subcategories": {
            "Business Services" : [],
            "Advertising" : [],
            "Legal" : [],
            "Office Supplies" : [],
            "Printing" : [],
            "Shipping" : []
        }
    },
    "Education" : {
        "sumTotal": [],
        "subcategories": {
            "Education" : [],
            "Books & Supplies" : [],
            "Student Loan" : [],
            "Tuition" : []
        }
    },
    "Entertainment" : {
        "sumTotal": [],
        "subcategories": {
            "Entertainment" : [],
            "Amusement" : [],
            "Arts" : [],
            "Movies & DVDs" : [],
            "Music" : [],
            "Newspapers & Magazines" : []
        }
    },
    "Fees & Charges" : {
        "sumTotal": [],
        "subcategories": {
            "Fees & Charges" : [],
            "ATM Fee" : [],
            "Bank Fee" : [],
            "Finance Charge" : [],
            "Late Fee" : [],
            "Service Fee" : [],
            "Trade Commissions" : []
        }
    },
    "Financial" : {
        "sumTotal": [],
        "subcategories": {
            "Financial" : [],
            "Financial Advisor" : [],
            "Life Insurance" : []
        }
    },
    "Food & Dining" : {
        "sumTotal": [],
        "subcategories": {
            "Food & Dining" : [],
            "Alcohol & Bars" : [],
            "Coffee Shops" : [],
            "Fast Food" : [],
            "Groceries" : [],
            "Restaurants" : []
        }
    },
    "Gifts & Donations" : {
        "sumTotal": [],
        "subcategories": {
            "Gifts & Donations" : [],
            "Charity" : [],
            "Gift" : []
        }
    },
    "Health & Fitness" : {
        "sumTotal": [],
        "subcategories": {
            "Health & Fitness" : [],
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
        "sumTotal": [],
        "subcategories": {
            "Home" : [],
            "Furnishings" : [],
            "Home Improvement" : [],
            "Home Insurance" : [],
            "Home Services" : [],
            "Home Supplies" : [],
            "Lawn & Garden" : [],
            "Mortgage & Rent" : []
        }
    },
    "Investments" : {
        "sumTotal": [],
        "subcategories": {
            "Investments" : []
        }
    },
    "Kids" : {
        "sumTotal": [],
        "subcategories": {
            "Kids" : [],
            "Allowance" : [],
            "Baby Supplies" : [],
            "Babysitter & Daycare" : [],
            "Child Support" : [],
            "Kids Activities" : [],
            "Toys" : []
        }
    },
    "Loans" : {
        "sumTotal": [],
        "subcategories": {
            "Loans" : [],
            "Loan Fees and Charges" : [],
            "Loan Insurance" : [],
            "Loan Interest" : [],
            "Loan Payment" : [],
            "Loan Principal" : []
        }
    },
    "Misc Expenses" : {
        "sumTotal": [],
        "subcategories": {
            "Misc Expenses" : []
        }
    },
    "Personal Care" : {
        "sumTotal": [],
        "subcategories": {
            "Personal Care" : [],
            "Hair" : [],
            "Laundry" : [],
            "Spa & Massage" : []
        }
    },
    "Pets" : {
        "sumTotal": [],
        "subcategories": {
            "Pets" : [],
            "Pet Food & Supplies" : [],
            "Pet Grooming" : [],
            "Veterinary" : []
        }
    },
    "Shopping" : {
        "sumTotal": [],
        "subcategories": {
            "Shopping" : [],
            "Books" : [],
            "Clothing" : [],
            "Electronics & Software" : [],
            "Hobbies" : [],
            "Sporting Goods" : []
        }
    },
    "Taxes" : {
        "sumTotal": [],
        "subcategories": {
            "Taxes" : [],
            "Federal Tax" : [],
            "Local Tax" : [],
            "Property Tax" : [],
            "Sales Tax" : [],
            "State Tax" : []
        }
    },
    "Transfer" : {
        "sumTotal": [],
        "subcategories": {
            "Transfer" : [],
            "Credit Card Payment" : [],
            "Transfer for Cash Spending" : []
        }
    },
    "Travel" : {
        "sumTotal": [],
        "subcategories": {
            "Travel" : [],
            "Air Travel" : [],
            "Hotel" : [],
            "Rental Car & Taxi" : [],
            "Vacation" : []
        }
    },
    "Uncategorized" : {
        "sumTotal": [],
        "subcategories": {
            "Uncategorized" : [],
            "Cash & ATM" : [],
            "Check" : []
        }
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

        # write income
        csvwriter.writerow(["Income"] + dateList)
        category = "Income"
        csvwriter.writerow([category] + categories[category]["sumTotal"])
        csvwriter.writerow([])

        # write expense
        csvwriter.writerow(["Expenses"] + dateList)
        for category in categories:
            if category != "Income":
                csvwriter.writerow([category] + categories[category]["sumTotal"])
        csvwriter.writerow([])

        # write income details
        csvwriter.writerow(["Income Details"] + dateList)
        category = "Income"
        for subcategory in categories[category]["subcategories"]:
            csvwriter.writerow([subcategory] + categories[category]["subcategories"][subcategory])
        csvwriter.writerow([])

        # write expense details
        csvwriter.writerow(["Expense Details"] + dateList)
        for category in categories:
            if category != "Income":
                for subcategory in categories[category]["subcategories"]:
                    csvwriter.writerow([subcategory] + categories[category]["subcategories"][subcategory])
                csvwriter.writerow([])

if __name__ == "__main__":
    # parses command line for input file and output path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='<Required> Input File', required=True)
    parser.add_argument('--output', help='<Required> Output File', required=True)
    args = parser.parse_args()

    #print(args)

    # execute only if run as a script
    main(args.input, args.output)
