import sys
import csv
from collections import OrderedDict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy

people = {}  # hold person:[# send, # receive] for everyone
top_send = {}  # holds person:[0*9], one for each of the top5 people. the array is for the 9 different timestamps for emails sent by person
top1 = {}  # holds person:# for all unique people who contacts the top1 person # = a timestamp 0-8
top2 = {}  # same as top1
top3 = {}  
top4 = {}  
top5 = {}  
top=[[top1,''],[top2,''],[top3,''],[top4,''],[top5,'']]
top_receive={}#holds person:[0*9] like top_send but holds the # of unique people who contacted the person over the timestamps 
unique_receive={}#holds person:[0*9] like top_received but only hold the # of unique people across the top5


def readCsv(csv_input):
    #read given csv file
    with open(csv_input, 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
                for name in singleName(row[2]):
                    personArr(2, name)
                for name in singleName(row[3]):
                    personArr(3, name)

def singleName(per):
    # check if per is a single name or has multiple names '|'
    if '|' in per:
        # split and send all back
        return per.split('|')
    else:
        return [per,]
                          
def personArr(num, per):
    #add to person's send or receive count
    #if person is not in people: add them first
    if per not in people.keys(): 
        add(people,per,[0,0])
    if num == 2:
        people[per][0] += 1
    elif num == 3:
        people[per][1] += 1

def add(self, key, value):
    #used to add to dictionaries
    self[key] = value

def writeCsv():
    #start new csv file
    with open('enron-email-summary.csv','w') as writeFile:
        fieldnames = ['person', 'sent', 'received']
        writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        writer.writeheader()
        tmp=0
        for key,value in sorted(people.items(), key=lambda item:item[1],reverse=True):
            # write key by key sorted by # of emails sent (Highest to Lowest) 
            writer.writerow({'person': key, 'sent': value[0], 'received': value[1]})
            if tmp < 5:
                #save the top 5 sender for question 2 & 3
                add(top_send, key, [0,0,0,0,0,0,0,0,0])
                add(top_receive, key, [0,0,0,0,0,0,0,0,0])
                top[tmp][1]=key
                tmp += 1

def createTimestamp(csv_input):
    #opens the csv file again this time for question 2 & 3
    with open(csv_input, 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
            #call singlename for row[2] and row[3]
            for name in singleName(row[2]):
                    if name in top_send:
                        changeTimestamp(name,top_send, '', row[0])
                    for name2 in singleName(row[3]):
                        if name2 in top_receive:
                            changeTimestamp(name2, top_receive, name, row[0])
                            
def changeTimestamp(name,dict_top,sender,time):
    #takes in name (row[2] or row[3]), dict_top (top_send or top_receive), sender (for receive)
    #adds to top_send, top_receive timestamps for that top 5 person
    year=datetime.datetime.fromtimestamp(float(time) / 1000.0).strftime('%Y')
    month=datetime.datetime.fromtimestamp(float(time) / 1000.0).strftime('%m')
    count=findTimeStamp(year, month) #holds timestamp id
    dict_top[name][count]+=1
    #top_receive has extra criteria
    if dict_top==top_receive:
        for person in top:
            if name == person[1]: 
                #top_receive has to keep uniqueness for a person so it has to test if sender is already in top# dict
                if sender in person[0]:
                    #if it is, needs to subtract from 2 timestamps, delete sender from person[0]
                    dict_top[name][person[0][sender]]-=1 
                    dict_top[name][count]-=1
                    del person[0][sender]
                else:
                    #top_receive sends the sender name amd timestamp to top# for more uniqueness testing
                    add(person[0],sender,count)
                    
                    
def findTimeStamp(year, month):
    #returns timestamp to changeTimestamp
    years=['1998','1999','2000','2001','2002']#holds the years in the timeline
    count=0
    for time in years:
        if year == time:
            if 1<=float(month)<=6:
                count-=1
                return count
            else: 
                return count
        else:
            count+=2                         
    
def findUnique():
    # top_receive will be filled from create & findTimestamp -> set unique_receive = top_receive
    unique_receive=copy.deepcopy(top_receive)
    # go through below to subtract from timestamps if someone in top# is in another top#
    for list in top:
        for value in list[0]:
            is_found = 0
            for colist in top:
                # additional conditions to make sure a value is only tested once and not againist the same top#
                if (value in colist[0]) and (is_found == 0) and (colist[0] != list[0]):
                    stamp = list[0][value]
                    unique_receive[list[1]][stamp] -= 1
                    is_found = 1
    createVisual(unique_receive)

def createPNG():
    # create line graph for top 5 people' emails sent over the timeline
    stamp = ['Jul-Dec\n1998', 'Jan-Jun\n1999', 'Jul-Dec\n1999',
             'Jan-Jun\n2000', 'Jul-Dec\n2000', 'Jan-Jun\n2001',
             'Jul-Dec\n2001', 'Jan-Jun\n2002', 'Jul-Dec\n2002']

    plt.grid(b=True,which='major',color='#666666')
    for key in top_send:
        plt.plot(stamp, top_send[key], color=np.random.rand(3, ), label=key)
    
    plt.ylabel('Number of emails sent')
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('Top five email senders over five years')
    plt.yticks(np.arange(0, 2500 + 1, 250))
    plt.savefig('enron-send-timeline.png')
    plt.clf()

def createVisual(unique_receive):
    # create line graph for top 5 people' unique receivers over the timeline
    stamp = ['Jul-Dec\n1998', 'Jan-Jun\n1999', 'Jul-Dec\n1999',
             'Jan-Jun\n2000', 'Jul-Dec\n2000', 'Jan-Jun\n2001',
             'Jul-Dec\n2001', 'Jan-Jun\n2002', 'Jul-Dec\n2002']

    plt.grid(b=True,which='major',color='#666666')
    for key in top_receive:
        #group by color keys in top_receive and unique_receive (unique = dashed line
        color = np.random.rand(3, )
        plt.plot(stamp, top_receive[key], color=color, label=key)
        plt.plot(stamp, unique_receive[key], color=color, linestyle='--')

    plt.ylabel('Unique number of receivers')
    plt.xlabel('Time')
    plt.legend(loc='upper left',title="dashed = relative unique")
    plt.title('Top five email senders\' unique receivers over five year')
    plt.yticks(np.arange(0, 120 + 1, 10))
    plt.show()


def main():
    # get csv file for command line argument
    csv_input=sys.argv[1]

    readCsv(csv_input) 
    writeCsv()
    createTimestamp(csv_input) 
    createPNG()
    findUnique()


if __name__ == '__main__':
    main()
