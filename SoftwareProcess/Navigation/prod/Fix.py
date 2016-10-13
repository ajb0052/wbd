'''
Created on Oct 11, 2016

@author: Amanda Bailey
'''
from xml.dom.minidom import parse
from datetime import date
class Fix():
    def __init__(self, logFile="logFile.txt"):
        if(isinstance(logFile, str) == False):
            raise ValueError
        else:
            try:
                self.logFile = logFile
                self.logmsg = "\nLOG: " + str(date.today()) + " "
                log = open(logFile, 'a')
                log.write(self.logmsg + 'Start of log')
                log.close()
            except ValueError:
                print('Fix.fix:  could not open or append to file')
    
    def setSightingFile(self, sightingFile):
        try:
            filename = str(sightingFile).split("'")
            self.sightingFile = filename[0]
            if (self.sightingFile.endswith('.xml') == False):
                raise ValueError
            if (sightingFile == ''):
                raise ValueError
            #CREATE FILE IF IT DOESNT ALREADY EXIST
            sFile = open(sightingFile, 'a')
            sFile.close()
            
            #SET FILE
            self.sightingFile = sightingFile
            
            #WRITE TO LOG
            logmsgStart = 'Start of sighting file: ' + sightingFile
            log = open(self.logFile, 'a')
            log.write(self.logmsg + logmsgStart)
            log.close()
            return self.sightingFile
        except ValueError:
            print("Fix.setSightingFile:  ValueError Raised")
            
    def getSightings(self):
        try:
            approximateLatitude = "0d0.0"
            approximateLongitude = "0d0.0"
            #Sort through data
            fix = parse(self.sightingFile)
            
            if(fix.documentElement.tagName != "fix"):
                raise ValueError
            sightings = fix.getElementsByTagName("sighting")
            self.bodies = []
            for sighting in sightings:
                body = sighting.getElementsByTagName("body")[0]
                bodySplit = str(body.childNodes).split("'")
                body = bodySplit[1]
                self.bodies.append(body)
            
            self.dates = []
            for sighting in sightings:
                date = sighting.getElementsByTagName("date")[0]
                dateStr = str(date.childNodes).split("'")
                date = dateStr[1]
                self.dates.append(date)
            
            self.times = []
            for sighting in sightings:
                time = sighting.getElementsByTagName("time")[0]
                timeSplit = str(time.childNodes).split("'")
                time = timeSplit[1]
                self.times.append(time)
                
            self.times = []
            for sighting in sightings:
                time = sighting.getElementsByTagName("time")[0]
                timeSplit = str(time.childNodes).split("'")
                time = timeSplit[1]
                self.times.append(time)
                
            self.observations = []
            for sighting in sightings:
                observation = sighting.getElementsByTagName("observation")[0]
                observationSplit = str(observation.childNodes).split("'")
                observation = observationSplit[1]
                self.observations.append(observation)
            #Write to log
            log = open(self.logFile, 'a')
            position = 0
            for body in self.bodies:
                logmsgBody = body + " " + self.dates[position]  + " " + self.times[position]  + " " + self.observations[position]
                log.write(self.logmsg + logmsgBody)
            logmsgEnd = 'End of sighting file: ' + self.sightingFile
            log.write(self.logmsg + logmsgEnd)
            log.close()
            return (approximateLatitude, approximateLongitude)
        except ValueError:
            print("Fix.getSightings:  ValueError Raised")
            
            
            