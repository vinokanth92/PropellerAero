#This Python script is part of PropellerAero coding challenge
#V Vinokanth
#Last modified 9/10/17
#This script will extract data from FTP servers of NGS

import sys
from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from ftplib import FTP
from ftplib import all_errors as ERROR_FTP
import os
import math
from argparse import ArgumentParser
import logging 
import gzip

def getArgs():
    """Parses terminal arguments"""

    parser = ArgumentParser()
    parser.add_argument("base", help = "Enter base station")
    parser.add_argument("start", help = "Enter start time period. Format: YYYY-MM-DD:T:H:M::SZ")
    parser.add_argument("end", help = "Enter end time period. Format: YYYY-MM-DD:T:H:M::SZ")  
    
    args = parser.parse_args()
    return args

def getDateTime(dateTime):
    """This function splits the input date-timestamp string into date and time"""

    indexT = dateTime.find("T", 0, len(dateTime))
    dateStr = dateTime[0:indexT]
    timeStr = dateTime[indexT+1:len(dateTime)-1] #len(dateTime)-1 to strip off 'Z' denoting UTC time
    return dateStr, timeStr

def getYearMonthDay(dateStr):
    """Returns year month day from the input date string"""
    
    #Split the dateStr into year, month and day
    split = dateStr.split("-")
    year = int(split[0])
    month = int(split[1])
    day = int(split[2])
    
    #Create a dateobj and compute day of the year
    dateObj = date(year, month, day)
    return year, month, day

def getHourMinSec(timeStr):
    """Returns hour minute seconds as a list from the input string denoting time"""

    split = timeStr.split(":")
    hours = int(split[0])
    minutes = int(split[1])
    seconds = int(split[2])
    return hours, minutes, seconds

def getHourBlocksFileInfo(baseStationID, startDate, startHour, numDays, numHours):
    """Composes a list of tuples contaning information to search for files from the FTP server"""

    #Dictionary object to map ints to alphabets
    hourToAlphaDict = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h", 8:"i", 9:"j", 10:"k",
                       11:"l", 12:"m", 13:"n", 14:"o", 15:"p", 16:"q", 17:"r", 18:"s", 19:"t", 20:"u",
                       21:"v", 22:"w", 23:"x"}

    outputList = [] #output list of filenames

    for day in range(0,numDays):
        for hour in range(1,23):
            nextEntry = startDate +  timedelta(hours = hour)
            dayOfYear = nextEntry.strftime("%j") #the %j directive of datetime.strftime() returns day of the year
            year = nextEntry.year
            yearShort = str(year)[2:len(str(year))] #extract the last to digits of year
            
            #Compose tuple
            fileName = baseStationID + dayOfYear + hourToAlphaDict[nextEntry.hour] + "." + yearShort + "o.gz"
            outputTuple = (str(year), dayOfYear, baseStationID, fileName)
            outputList.append(outputTuple)

        #Update startDate by adding a day 
        startDate = startDate + timedelta(days = 1)

    #Now append numHours
    for hour in range(0,numHours):
        nextEntry = startDate + timedelta(hours = hour)
        dayOfYear = nextEntry.strftime("%j") #the %j directive of datetime.strftime() returns day of the year
        year = nextEntry.year
        yearShort = str(year)[2:len(str(year))] #extract the last to digits of year
        
        #Compose tuple
        fileName = baseStationID + dayOfYear + hourToAlphaDict[nextEntry.hour] + "." + yearShort + "o.gz"
        outputTuple = (str(year), dayOfYear, baseStationID, fileName)
        outputList.append(outputTuple)

    return outputList

def getFile(fileInfoList, baseStationID, startDate, endDate):
    """Retreives files from the FTP server"""
    
    #Initialize ftp parameters
    ftp = FTP("www.ngs.noaa.gov")
    ftpDirectory = "/cors/rinex/" 
    ftp.login() 
    logging.info("Successfully opened FTP connection with the server.")

    #Change current directory to ./Downloads in order to download files at the said location
    os.chdir("./Downloads")
    deleteFilesCount = 0 #counter to track the number of empty files to be deleted

    try:
        for item in fileInfoList:
            
            #Chage directory based on each tuple info in order to reflect year, dayOfYear info
            try:
                ftp.cwd(ftpDirectory + item[0] + "/" + item[1] + "/" + item[2] + "/")
            
            except ERROR_FTP:
                logging.critical('Failed to change directory {0}'.format(ftpDirectory + item[0] + "/" + item[1] + "/" + item[2] + "/"))
            
            fileName = item[3]
            localFile = open(fileName, 'wb')
            
            try:
                ftp.retrbinary('RETR ' + fileName, localFile.write)
            
            except ERROR_FTP:
                logging.warning("File not found: {0}".format(fileName))
                os.remove(fileName)
                deleteFilesCount = deleteFilesCount + 1 
            
            else:
                logging.info("Downloaded file: {0}".format(fileName))

            finally:
                localFile.close()


        if deleteFilesCount == len(fileInfoList):

            logging.info("Time block files not found. Checking for day entries.")
            dayOfYear = fileInfoList[0][1] #get day of year from fileInfoList
            
            while startDate != (endDate + timedelta(days = 1)): 
                fileName = baseStationID + str(dayOfYear) +  "0." + str(item[0])[2:len(str(item[0]))] + "o.gz"                
                localFile = open(fileName, 'wb')
                
                try:
                    ftp.retrbinary("RETR " + fileName, localFile.write)
                    
                except ERROR_FTP:
                    logging.warning("File not found: {0}".format(fileName))
                    os.remove(fileName)

                else:
                    logging.info("Downloaded file: {0}".format(fileName))

                finally:
                    localFile.close()
                    startDate = startDate + timedelta(days = 1)
                    dayOfYear = int(dayOfYear) + 1

    except ERROR_FTP as e:
        logging.critical("Error occured during file download. Exception: {0}".format(e))

    else:
        if not os.listdir(os.getcwd()):
            logging.warning("Day entry files not found. Please try again with different parameters.")

        else:
            logging.info("Successfully downloaded all files from FTP server")

    finally:
        ftp.quit()
        logging.info("FTP connection successfully closed.")

def unZipFiles():
    """Unzips .gz files using gzip module"""

    #Get list of files in the dir to iterate and unzip
    filesList = os.listdir(os.getcwd())
    fileCounter = 0 #file counter to append to filename

    #for each file in $PWD, extract them using gunzip
    for file in filesList:

        fileCounter = fileCounter + 1 

        try:
            inputFile = gzip.open(file, 'rb')
        
        except Exception:
            logging.warning("Unable to open .gz file: {0}".format(inputFile))

        outputFile = open("file_" + str(fileCounter) + '.o', 'wb') #open .o file to write read file info

        try:
            outputFile.write(inputFile.read())
        
        except Exception:
            logging.warning("Unable to write to output file: {0}".format(outputFile))
        
        finally:
            inputFile.close()
            outputFile.close()

#script entry point
def main():  
    """Entry point of the script"""

    #Get arguments from CLI
    args = getArgs();
    baseStationID = args.base
    startTime = args.start
    endTime = args.end

    #Setup logging     
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    #Strip date and time
    dateStart, timeStart = getDateTime(startTime)
    dateEnd, timeEnd = getDateTime(endTime)

    #Extract year, month, day components of date
    startYear, startMonth, startDay = getYearMonthDay(dateStart)
    endYear, endMonth, endDay = getYearMonthDay(dateEnd)

    #Extract hour, minute, seconds components of time
    startHour, startMinute, startSeconds = getHourMinSec(timeStart)
    endHour, endMinute, endSeconds = getHourMinSec(timeEnd)

    #Construct datetime object with above extracted components
    startDateTimeObj = datetime(year = startYear, month = startMonth, day = startDay, 
                                                hour = startHour, minute = 0, second = 0)
    endDateTimeObj = datetime(year = endYear, month = endMonth, day = endDay, 
                                                hour = endHour, minute = 0, second = 0)

    #Compute day and hour difference between the start and end date using datetime.timedelta
    timeDelta = endDateTimeObj - startDateTimeObj
    deltaDays = timeDelta.days
    deltaHours = int(math.ceil(timeDelta.seconds/3600))
    deltaMins = timeDelta.seconds//60

    #Increament if deltaMin is greated than 0. This is to consider the consecutive hour block when min or sec > 0
    if(endMinute > 0 or endSeconds > 0):
        deltaHours = deltaHours + 1

    #Compose a datetime object with start date and start hour of the command line input START_DATE
    #This will initialize the datetime object to the start hour of the start date 
    startDateTime = datetime(startYear, startMonth, startDay, startHour)
    fileInfoList = getHourBlocksFileInfo(baseStationID, startDateTime, time(hour = startHour), deltaDays, deltaHours)

    #Retrieve files and unzip files
    getFile(fileInfoList = fileInfoList, baseStationID = baseStationID, 
                                    startDate = startDateTimeObj.date(), endDate = endDateTimeObj.date())
    unZipFiles()

#Defining entry point of the script
if __name__ == "__main__":
   main()

