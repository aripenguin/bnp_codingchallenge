import csv
import sys
#import pandas as pan
import matplotlib.pyplot as plt
#import array as arr
from collections import OrderedDict
import datetime
import numpy as np

people = {}#hold person:[# send, # receive] for everyone (question 1)
top_send={}#holds person:[0*9], one for each of the top5 people. the array is for the 9 different timestamps for emails sent by person
top1={}#holds person:# for all unique people who contacts the top1 person (question2). the # represents the timestamp 0-8
top2={}#same as top1 but for top2
top3={}#same as top1 but for top3
top4={}#same as top1 but for top4
top5={}#same as top1 but for top5
    #top=[top1,top2,top3,top4,top5]
top=[[top1,''],[top2,''],[top3,''],[top4,''],[top5,'']]
    #top=[[top1,'',0],[top2,'',0],[top3,'',0],[top4,'',0],[top5,'',0]]
    

top_receive={}#holds person:[0*9] like top_send but holds the # of unique people who contacted the person over the timestamps 
unique_receive={}#holds person:[0*9] like top_received but only hold the # of unique people across the top5


def readCsv():
    # open csv
    with open('enron-event-history-all.csv', 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
            # send sender or receiver names to personArr
                singleName(2, row[2])
                singleName(3, row[3])
                #print(row[2],row[3])
    #print(people)
    #close the csv?

def singleName(num,per):
        #print(num,per)
    # check if per is a single name or has no '|'
    if '|' in per:
        # split and send all to personArr
        for p in per.split('|'):
            personArr(num, p)
            #print p
    else:
        personArr(num, per)

def personArr(num, per):
    #try to do [per, #,#], if failed append
    if per not in people.keys(): #expression for any integer is wrong
        #print("New person " + per)
        add(people,per,[0,0])
    if num == 2:
        #print (people[per][0])
        people[per][0] += 1
    elif num == 3:
        people[per][1] += 1

def add(self, key, value):
    self[key] = value

def writeCsv():
    #open csv
    with open('emails.csv','w') as writeFile:
        fieldnames = ['person', 'sent', 'received']
        writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        writer.writeheader()
        tmp=0
        for key,value in sorted(people.items(), key=lambda item:item[1],reverse=True):
            # write row by row
            writer.writerow({'person': key, 'sent': value[0], 'received': value[1]})
            if tmp < 5:
                #save the top 5 for png file
                print(key,value)
                add(top_send, key, [0,0,0,0,0,0,0,0,0])
                add(top_receive, key, [0,0,0,0,0,0,0,0,0])
                top[tmp][1]=key
                tmp += 1

def createTimestamp():
    print("createTimestamp")
    #top 10 -10 timestamps
    #print(top_send)
    with open('enron-event-history-all.csv', 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
            #call singlename for row[2] and row[3]
            #add to a timestamp by findTimestamp()
            if row[2] in top_send:
                findTimestamp(row[2],top_send, null, row[0])
            if row[3] in top_receive:    
                findTimestamp(row[3], top_receive, row[2], row[0])
                
                #for question 3 - have row[2]/sender row[3]/receiver
                #top -> top1, top2 - check if row[2] belongs to the top#-top_send
                for sender in top:
                    if row[2] == sender[1]:#fix the identifer
                        #needs to split them up
                        for name in row[3].split('|'):
                            if name not in sender[0]:
                                #list.append(row[3])
                                add(sender[0], name, 0)
    print(top_send)
    print(top)
    
def findTimestamp(name,dict_top,sender,time):
    #takes in name (row[2] or row[3]), dict_top (top_send or top_receive), sender (for receive)
    year=datetime.datetime.fromtimestamp(float(time) / 1000.0).strftime('%Y')
    month=datetime.datetime.fromtimestamp(float(time) / 1000.0).strftime('%m')
    count=0 #holds timestamp id
        #change these if to for loop?
    if year == '1998':
        dict_top[name][0]+=1
        count=0
    elif year == '1999':
        if 1<=float(month)<=6:
            dict_top[name][1]+=1
            count=1
        else:
            dict_top[name][2]+=1
            count=2
    elif year == '2000':
        if 1<=float(month)<=6: 
            dict_top[name][3]+=1
            count=3
        else:
            dict_top[name][4]+=1
            count=4
    elif year == '2001':
        if 1 <= float(month) <= 6:
            dict_top[name][5]+=1
            count=5
        else:
            dict_top[name][6]+=1
            count=6
    elif year == '2002':
        if 1 <= float(month) <= 6:
            dict_top[name][7]+=1
            count=7
        else:
            dict_top[name][8]+=1
            count=8
    #top_receive also has to send the person name to top#
    if dict_top=top_receive:
        for person in top:
            if name = person[1]: 
                add(person[0],sender,count)

    
def findUnique():
    print("In findUnique")
    #top_receive will be filled from create & findTimestamp -> set unique_receive = top_receive
    unique_receive=top_receive
    
    #go through below to subtract from timestamps if someone in top# is in another top#
    for list in top:#[top#,name]
        for value in list[0]:
            is_found=0
            for colist in top:
                if (value in colist[0]) and (is_found==0)and (colist[0] != list[0]):
                    #no changes to if statement - just nee to make should correct value in unique is subtracts
                    stamp=value.value 
                    unique_receive[list[1]][stamp] -= 1
                    #top[tmp2][2]-=1
                    print (top[list[1]],value) #check if the value is being deleted once
                    #if top[tmp2][0]=top1:test_num
                    is_found=1
                    
    test = 0
    print("test-unique against each other")
    fori in top:
        print(top[test][1], top[test][2])
        test += 1

def createPNG():
    print("createPNG")
    #create line graph for top 10
    stamp=['Jul-Dec\n1998','Jan-Jun\n1999','Jul-Dec\n1999',
           'Jan-Jun\n2000','Jul-Dec\n2000','Jan-Jun\n2001',
           'Jul-Dec\n2001','Jan-Jun\n2002','Jul-Dec\n2002']
    for key in top_send:
        print(key, top_send[key])#(2 * np.pi * np.random.rand(100))
        plt.plot(stamp,top_send[key], color=np.random.rand(3,),label=key)
    plt.ylabel('Number of emails sent')
    plt.xlabel('Time')
    plt.legend(loc='upper right')
    plt.title('Top 5 email senders over 5 year')
    #ax.grid(zorder=0)
    #plt.show()
    plt.savefig('sender_timeline.png')
    #send it as a png, change the specifics - y label & grid background

def createVisual():
    print("In createVisual")
    #create line graph for top 10
    stamp=['Jul-Dec\n1998','Jan-Jun\n1999','Jul-Dec\n1999',
           'Jan-Jun\n2000','Jul-Dec\n2000','Jan-Jun\n2001',
           'Jul-Dec\n2001','Jan-Jun\n2002','Jul-Dec\n2002']
    for key in top:
        color=np.random.rand(3,)
        #print(key, top_send[key])#(2 * np.pi * np.random.rand(100))
        plt.plot(stamp,top_receive[key], color=color,label=key)#straight
        plt.plot(stamp,unique_receive[key], color=color)#dashed - ,label=key
        
    plt.ylabel('Number of emails received')
    plt.xlabel('Time')
    plt.legend(loc='upper right')
    plt.title('Top 5 email senders over 5 year')
    #ax.grid(zorder=0)
    plt.show()
    #send it as a png, change the specifics - y label & grid background


def main():
    print('start')
    readCsv()
    writeCsv()
    createTimestamp()
    createPNG()
    findUnique()
    #createVisual()#not ready for testing
    print('end')


if __name__ == '__main__':
    main()
