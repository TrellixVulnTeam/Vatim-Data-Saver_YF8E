import requests
import time
import datetime
import os
from random import randint
import ClientsParse


def savevatdata(saveperiod, savepath):
    """
    -savevatdata(): Takes all of the raw vatsim data and saves it to a text file in the default directory
    -Params:
        saveperiod - The frequency (in seconds) a new file will be created with the updated vatsim data must
        be greater than 120 seconds
        savepath - The path the vatsim raw data files will be saved in
    """
    while saveperiod > 119 & os.path.isdir(savepath) is True:
        currenttime = datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
        pagecontents = requests.get(returnvalidlink())

        newsavefile = open(os.path.join(savepath, currenttime + '.txt'), 'w')
        newsavefile.write(pagecontents.text)
        newsavefile.close()
        print('File: "' + newsavefile.name + '" saved!')
        time.sleep(saveperiod)


def savelocalvatdata():
    pagecontents = requests.get(returnvalidlink()).text
    with open('data.vatsim.txt', 'w') as f:
        f.write(pagecontents)
    print("data.vatsim.txt updated at: " + datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S"))


def savevatstatusdata():
    """
    -savevatstatusdata(): Saves the status.vatsim.net file to directory as status.vatsim.txt.
     Only to be done once on initial startup
    """
    pagecontents = requests.get('http://status.vatsim.net/')
    newsavefile = open('status.vatsim.txt', 'w')
    for line in pagecontents.text:
        newsavefile.write(line.strip('\n'))
    print("status.vatsim.txt updated at: " + datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S"))


def saveclientdata():
    currenttime = datetime.datetime.utcnow().strftime("%Y-%m-%d, %H:%M:%S")
    connectedclients = ClientsParse.returnconnectedclients()
    atc = str(len(ClientsParse.returnatc()))
    pilots = str(len(ClientsParse.returnpilots()))
    with open('ClientSaves.txt', 'a') as f:
        f.write('\n' + connectedclients + ', ' + atc + ', ' + pilots + ', ' + currenttime)
    print(f.name + ' saved at: ' + datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S"))


def returnvalidlink():
    """
    -returnvalidlink(): Returns a random link from the status.vatsim.txt file with the header url=0
    """
    validlinks = []
    savefile = open('status.vatsim.txt', 'r')
    sub = 'url0='
    for line in savefile:
        if sub in line:
            validlinks.append(line.strip(sub + '\n'))
    savefile.close()
    return validlinks[randint(0, 2)]

