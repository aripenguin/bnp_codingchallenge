# bnp_codingchallenge
#BNPData Scientist Technical Exam
#Applicant - Ariann Chai

#Question 1: I used __ in readCSV() to go through the csv file given line by line. With singleName() (to split if there is more than one sender or receiver) and personArr(), to store all sender or receiver names in a dictionary/hash table called people. The person's name becomes a key and the value is a size two array [# of email sent by person, # of emails recieved by person]. This is done by testing if person name is a key in people and adding them with a value of [0,0] to start. It then takes the other value num which tells it if this person was the sender or reciever (2=sender, 3-receiver) and will add one to the array value of the person. THis is then send to writeCSV() to make the new .csv file by going through people in sorted (highest to lowest # of sends).

#question 2: In order to get the names of the people who are the top 5 senders, in the for loop in writeCSV(), I added a count variable that will store the first 5 people into a new dictionary?//// which because of the sort are the top 5 senders. In order to find out the progress of the amount of emails send for each, I made that array an array of array that held an int array of size nine to store the number of emails send from that person at each time stamps chosen. I choose to set my time stamps at 9 because the data given is from May 1998 - Dec?//// 2002 and semi-annually seems like a good count for now. (The first half of 1998 has one email and it was not one of the top 5 so I ignore that one)

#question 3:
