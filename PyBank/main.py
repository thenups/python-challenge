# In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company.
# You will be given two sets of revenue data (budget_data_1.csv and budget_data_2.csv).
# Each dataset is composed of two columns: Date and Revenue. (Thankfully, your company has rather lax standards for accounting so the records are simple.)

# Your task is to create a Python script that analyzes the records to calculate each of the following:
    # The total number of months included in the dataset
    # The total amount of revenue gained over the entire period
    # The average change in revenue between months over the entire period
    # The greatest increase in revenue (date and amount) over the entire period
    # The greatest decrease in revenue (date and amount) over the entire period

# Import modules
import os, csv, datetime

# Set path for current files
bankDataCvsPath1 = os.path.join("raw_data","budget_data_1.csv")
bankDataCvsPath2 = os.path.join("raw_data","budget_data_2.csv")

# Create list of current files to be combined
allFiles = [bankDataCvsPath1,bankDataCvsPath2]

# Declare list variables
month = []
revenue = []

# Declare output varibales
nMonths = 0 #total number of months included in the dataset
totalRev = 0 #total amount of revenue gained over the entire period
revDeltAvg = 0 #average change in revenue between months over the entire period

# Function to figure out is value is an actual number
def isNumber(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

# Function to combine data files
def combineFiles (dataFile):
    with open(dataFile, 'r', newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        # Define date formats in the cvs to iterate through
        dateFormats = ["%b-%y","%b-%Y"]

        # For each row in the reader
        for row in csvreader:

            # Skips the header - looks at value in second column and searches for number
            if isNumber(row[1]):

                # Tries different date formats
                for formats in dateFormats:

                    # Convert all dates into date format so it's easy to compare them
                    try:
                        dateObject = datetime.datetime.strptime(row[0],formats)

                    # If the date format is not accounted for print an error
                    except ValueError:
                        pass

                # Append values to respective lists
                month.append(dateObject)
                revenue.append(int(row[1]))

# Find out which files to analyze
userInput = input("Would you like to use the (c)urrent files or (n)ew files? ")
newFiles = []
response = True

# Figure out what data user wants the use
while response:

    # If user wants the current given data
    if userInput == "c":

        # Combine data files
        for item in allFiles:
            combineFiles(item)

        response = False

    # If the user wants to input new data
    elif userInput == "n":
        nFiles = int(input("How many files would you like to analyze? ")) #how many files to account for

        print("Please put your files in the PyBank/raw_data folder")

        for f in range(0,nFiles): #for each file a user wants
            fileName = input("What is your file name (make sure to include the extension e.g. .csv): ")
            combineFiles(os.path.join("raw_data",fileName)) #add data to lists

        response = False

    # If neither c or n is entered, ask again
    else:
        print("Sorry, that was not a valid choice")
        userInput = input("Would you like to use the (c)urrent files or (n)ew files? ")

# Zip and Sort Date / Revenue lists
sortedValues = sorted(zip(month,revenue))

# Length of sorted data list
l = len(sortedValues)
i = 0
monthTotal = 0

# While the index is less than the length of the list
while i < l:

    duplicateValues = True #assume there are duplicate values
    monthTotal = sortedValues[i][1] #rev value for that month

    # If there are duplicate values...
    if duplicateValues:

        # If the date is the same is the following date
        if sortedValues[i][0] == sortedValues[i+1][0]:

            # Calculate total for the month
            monthTotal = monthTotal + sortedValues[i+1][1]

            # Go to next item
            i += 1

            if i+1 < l: #make sure there isn't an index error

                # If the date isn't the same as the followin value
                if sortedValues[i][0] != sortedValues[i+1][0]:

                    # Replace value with combined value
                    sortedValues[i] = (sortedValues[i][0],monthTotal)

                    # Delete previous item
                    del(sortedValues[i-1])

                    # Account for the fewer items in list
                    i -= 1
                    l -= 1

            # If the following month is a duplicate value
            else:

                # Store the new combined value
                sortedValues[i] = (sortedValues[i][0],monthTotal)

                # Delete the previous list item
                del(sortedValues[i-1])

        # What to do if the next value is NOT a duplicate
        else:
            # Don't loop to add rev values
            duplicateValues = False

    # Move to the next list item
    i += 1

# Calculate total number of months included in the dataset
nMonths = len(sortedValues)

# Create variables for final output
revDeltTot = 0

# Set counters
n = 0
revIncDate = 0 #greatest increase in revenue over the entire period
revDecDate = 0 #greatest decrease in revenue over the entire period
current_max = sortedValues[n][1] - sortedValues[n-1][1]
current_min = sortedValues[n][1] - sortedValues[n-1][1]

# Make all final calculations
while n < nMonths:

    # Calculate total amount of revenue gained over the entire period
    totalRev = totalRev + sortedValues[n][1]



    # Calculate change MoM and add to a total variable
    if n > 0:
        delt = sortedValues[n][1] - sortedValues[n-1][1]
        revDeltTot = revDeltTot + delt

        # Calculate greatest revenue incerase
        if delt > current_max:
            current_max = delt
            revIncDate = sortedValues[n][0]

        # Calculate greatest revenue decrease
        elif delt < current_min:
            current_min = delt
            revDecDate = sortedValues[n][0]
    n += 1

# The average change in revenue between months over the entire period
revDeltAvg = revDeltTot / (nMonths-1) #account for 1 less divisor

# Print Results
print("--------------------------")
print("Financial Results")
print("--------------------------")
print("Total Months: " + str(nMonths))
print("Total Revenue: $" + str(totalRev))
print("Average Revenue Change: $" + str(int(revDeltAvg)))
print("Greatest Increase in Revenue: " + revIncDate.strftime("%b-%y ") + "($" + str(current_max) + ")")
print("Greatest Decrease in Revenue: " + revDecDate.strftime("%b-%y ") + "($" + str(current_min) + ")")

# Save file with results
f = open("Financial Results.txt","w")
f.write("Financial Results"
"\n--------------------------"
"\nTotal Months: " + str(nMonths) +
"\nTotal Revenue: $" + str(totalRev) +
"\nAverage Revenue Change: $" + str(int(revDeltAvg)) +
"\nGreatest Increase in Revenue: " + revIncDate.strftime("%b-%y ") + "($" + str(current_max) + ")" +
"\nGreatest Decrease in Revenue: " + revDecDate.strftime("%b-%y ") + "($" + str(current_min) + ")"
)
f.close()
