import csv
#import pandas as pan
import matplotlib.pyplot as plt
#import array as arr
from collections import OrderedDict
import datetime
import numpy as np

people = {}
top_send={}
top1={}
top2={}
top3={}
top4={}
top5={}
#top=[top1,top2,top3,top4,top5]
top=[[top1,''],[top2,''],[top3,''],[top4,''],[top5,'']]
#top=[[top1,'',0],[top2,'',0],[top3,'',0],[top4,'',0],[top5,'',0]]
    #top[#][2]=len(top#)-non-unique



def readCsv():
    # open csv
    with open('enron-event-history-all.csv', 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
            # send sender or receiver names to personArr
                singleName(2, row[2])
                singleName(3, row[3])
                print(row[2],row[3])
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
                top[tmp][1]=key
                tmp += 1

def createTimestamp():
    print("createTimestamp")
    #top 10 -10 timestamps
    #print(top_send)
    with open('enron-event-history-all.csv', 'r') as readFile:
        read = csv.reader(readFile, delimiter=',')
        for row in read:
            if row[2] in top_send:
                #add to a timestamp
                year=datetime.datetime.fromtimestamp(float(row[0]) / 1000.0).strftime('%Y')
                month=datetime.datetime.fromtimestamp(float(row[0]) / 1000.0).strftime('%m')
                if year == '1998':
                    top_send[row[2]][0] += 1
                elif year == '1999':
                    if 1<=float(month)<=6:
                        top_send[row[2]][1] += 1
                    else:
                        top_send[row[2]][2] += 1
                elif year == '2000':
                    if 1<=float(month)<=6:
                        top_send[row[2]][3] += 1
                    else:
                        top_send[row[2]][4] += 1
                elif year == '2001':
                    if 1 <= float(month) <= 6:
                        top_send[row[2]][5] += 1
                    else:
                        top_send[row[2]][6] += 1
                elif year == '2002':
                    if 1 <= float(month) <= 6:
                        top_send[row[2]][7] += 1
                    else:
                        top_send[row[2]][8] += 1
                #for question 3 - have row[2]/sender row[3]/receiver
                #top -> top1, top2 - check if row[2] belongs to the top#-top_send
                for list,key in top:
                    if row[2] == key:#fix the identifer
                        #needs to split them up
                        for name in row[3].split('|'):
                            if name not in list:
                                #list.append(row[3])
                                add(list, name, 0)
    print(top_send)
    print(top)
    # close the csv?

def findUnique():
    print("In findUnique")
    #set top[#][3]s
    tmp1=0
    for list in top:
        print(list)
        print(len(list))
        #top[tmp1][2]=len(list)
        print(tmp1)
        tmp1+=1
    print top
    test=0
    for i in top:
        print(top[test][2])
        test+=1
    #go through top - for each top1 value - check if in any another top# list
    tmp2=0
    for list in top:
        for value in list[0]:
            #top1 - going through keys.
            for colist in top:
                if value in colist[0]:
                    top[tmp2][2]-=1
                    continue
        tmp2+=1
    test = 0
    for i in top:
        print(top[i][2])
        test+=1

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
    bars=[[1,0],[4,0],[2,0],[3,0],[3,0]]
    X= np.arange(3)
    #for key in top:
        #set bar lengths and name
        #plt.bar(X + 0.00, bars[0][0], color='b', width=0.25)
        #plt.bar(X + 0.00, bars[0][1], color='b', width=0.25)

    plt.bar(X + 0.00, bars[0][0], color='b', width=0.25)
    plt.bar(X + 0.00, bars[0][1], color='g', width=0.25)
    plt.show()


def main():
    print('start')
    a=['tee','gee','dee']
    b = ['qee', 'see', 'fee']
    if 'tee' in a:
        print("yes")
    abc=[a,b]
    for t in abc:
        print(t)#works


    readCsv()
    writeCsv()
    createTimestamp()
    createPNG()
    #findUnique()
    #createVisual()
    #question3()
    print('end')


if __name__ == '__main__':
    main()
