# In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process.
# (Up until now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it used to be.)

# You will be given two sets of poll data (election_data_1.csv and election_data_2.csv).
# Each dataset is composed of three columns: Voter ID, County, and Candidate.
# Your task is to create a Python script that analyzes the votes and calculates each of the following:
    # The total number of votes cast
    # A complete list of candidates who received votes
    # The percentage of votes each candidate won
    # The total number of votes each candidate won
    # The winner of the election based on popular vote.

# Import modules
import os, csv

# Set path for file
pollDataCvsPath1 = os.path.join("raw_data","election_data_1.csv")
pollDataCvsPath2 = os.path.join("raw_data","election_data_2.csv")

# Create list of files to be combined
allFiles = [pollDataCvsPath1,pollDataCvsPath2]

# Declare list variables
voterId = []
county = []
voteFor = []

# Declare output varibales
voteTot = 0 #total number of votes cast
candidates = [] #list of candidates
votesPerCandidate = [] #list of how many votes each candidate got
percPerCandidate = []

# Function to figure out is value is an actual number
def isNumber(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

# Function to save file data in lists
def combineFiles (dataFile):
    with open(dataFile, 'r', newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        # For each row in the reader
        for row in csvreader:

            # Skips the header - looks at value in second column and searches for number
            if isNumber(row[0]):

                voterId.append(int(row[0]))
                county.append(row[1])
                voteFor.append(row[2])

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

        print("Please wait while we calculate the results...\n.............................................")

        response = False

    # If the user wants to input new data
    elif userInput == "n":
        nFiles = int(input("How many files would you like to analyze? "))
        print("Please put your files in the PyPoll/raw_data folder")

        for f in range(0,nFiles): #for each file a user wants
            fileName = input("What is your file name (make sure to include the extension e.g. .csv): ")
            print("Please wait...")
            combineFiles(os.path.join("raw_data",fileName)) #add data to lists

        response = False

    # If neither c or n is entered, ask again
    else:
        print("Sorry, that was not a valid choice")
        userInput = input("Would you like to use the (c)urrent files or (n)ew files? ")

# Zip lists
allData = zip(voterId,county,voteFor)
# Make sure there are no duplicate values
noDuplicateData = set(allData)

# Calculate total number of votes cast
voteTot = len(noDuplicateData)

# Compile a complete list of candidates who received votes
candidates = set(voteFor)

# Calculate the total number of votes each candidate won
for c in candidates:
    n = 0  #counter

    # Look at each tuple in the non duplicate votes list
    for votes in noDuplicateData:

        # If the candidate name is the same as the voted candidate, add 1 to the counter
        if c == votes[2]:
            n += 1

    # Append the total number of votes to its list
    votesPerCandidate.append(n)

# Calculate the percentage of votes each candidate won
for c in votesPerCandidate:
    percent = (c / voteTot)* 100
    percPerCandidate.append(round(percent,2))

# Zip final results so candidates are tied to their result
finalResults = list(zip(candidates,percPerCandidate,votesPerCandidate))

# Find the winner of the election based on popular vote
winningIndex = votesPerCandidate.index(max(votesPerCandidate))
winner = finalResults[winningIndex][0]

# Print values
print("Election Results")
print("-------------------------")
print("Total Votes: " + str(voteTot))
print("-------------------------")
for result in finalResults:
    print(result[0] + ": " + str(result[1]) + "% (" + str(result[2]) + ")")
print("-------------------------")
print("Winner: " + winner)
print("-------------------------")


# Save file with results
f = open("Election Results.txt","w")
f.write(
"Election Results"
+ "\n" + "-------------------------"
+ "\n" + "Total Votes: " + str(voteTot)
+ "\n" + "-------------------------" + "\n")

for result in finalResults:
    f.write(result[0] + ": " + str(result[1]) + "% (" + str(result[2]) + ")" + "\n")

f.write(
"-------------------------"
+ "\n" + "Winner: " + winner
+ "\n" + "-------------------------")

f.close()
