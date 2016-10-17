'''
Created on Oct 11, 2016

@author: Amanda Bailey
'''
from xml.dom.minidom import parse
from datetime import date, timedelta
import time
import math
import Navigation.prod.Angle as Angle
class Fix():
    def __init__(self, logFile="logFile.txt"):
        if(isinstance(logFile, str) == False):
            raise ValueError
        else:
            try:
                self.logFile = logFile
                currentUTC = time.gmtime()
                currentHour = time.localtime().tm_hour
                self.UTCoffset = (currentUTC.tm_hour - currentHour)%12
                self.UTCoffset = str(self.UTCoffset + 1) + ":00"
                HrMinSec = str(currentUTC.tm_hour) + ":" + str(currentUTC.tm_min) + ":" + str(currentUTC.tm_sec) + " "
                self.logmsg = "\nLOG: " + str(date.today()) + " " + HrMinSec + "-" + self.UTCoffset + " "
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
            #retrieve data
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
            
            self.observations = []
            for sighting in sightings:
                observation = sighting.getElementsByTagName("observation")[0]
                observationSplit = str(observation.childNodes).split("'")
                observation = observationSplit[1]
                self.observations.append(observation)
            
            #find the dip
            self.heights = []
            for sighting in sightings:
                height = sighting.getElementsByTagName("height")[0]
                heightSplit = str(height.childNodes).split("'")
                height = heightSplit[1]
                self.heights.append(height)
                
            self.horizons = []
            self.dips = []
            location = 0
            for sighting in sightings:
                horizon = sighting.getElementsByTagName("horizon")[0]
                horizonSplit = str(horizon.childNodes).split("'")
                horizon = horizonSplit[1]
                self.horizons.append(horizon)
                if (str.capitalize(horizon) == "Natural"):
                    height = float(self.heights[location])
                    dip = (-0.97 * math.sqrt(height))/60
                    self.dips.append(dip)
                else:
                    dip = 0.0
                    self.dips.append(dip)
                location = location + 1
                
            # retrieve more date and find the refraction and adjusted altitude
            self.pressures = []
            for sighting in sightings:
                pressure = sighting.getElementsByTagName("pressure")[0]
                pressureSplit = str(pressure.childNodes).split("'")
                pressure = pressureSplit[1]
                self.pressures.append(float(pressure))
            
            self.temperaturesInC = []
            self.refractions = []
            self.adjAltitudes = []
            location = 0
            for sighting in sightings:
                temperature = sighting.getElementsByTagName("temperature")[0]
                temperatureSplit = str(temperature.childNodes).split("'")
                temperature = float(temperatureSplit[1])
                tempInC = (temperature*1.8)+32
                self.temperaturesInC.append(tempInC)
                
                obsAltitude = Angle.Angle()
                obsAltitude.setDegreesAndMinutes(self.observations[location])
                obsAlt = obsAltitude.getDegrees()
                
                refraction = (-0.00452*self.pressures[location])/(273 + tempInC)/math.tan(obsAlt)
                self.refractions.append(refraction)
                
                adjAlt = obsAlt + self.dips[location] + refraction
                self.adjAltitudes.append(adjAlt)
                location = location + 1
            
            #retrieve more data    
            self.dates = []
            self.deltaDates = []
            for sighting in sightings:
                date = sighting.getElementsByTagName("date")[0]
                dateStr = str(date.childNodes).split("'")
                date = dateStr[1]
                self.dates.append(date)
                dateSplit = date.split("-")
                yearToDays = 0
                yearToDays = int(dateSplit[0])*365
                monthToDays = 0
                if (int(dateSplit[2]) == 2):
                    monthToDays = 31
                elif (int(dateSplit[2]) == 3):
                    monthToDays = 60
                elif (int(dateSplit[2]) == 4):
                    monthToDays = 91
                elif (int(dateSplit[2]) == 5):
                    monthToDays = 121
                elif (int(dateSplit[2]) == 6):
                    monthToDays = 152
                elif (int(dateSplit[2]) == 7):
                    monthToDays = 182
                elif (int(dateSplit[2]) == 8):
                    monthToDays = 213
                elif (int(dateSplit[2]) == 9):
                    monthToDays = 243
                elif (int(dateSplit[2]) == 10):
                    monthToDays = 274
                elif (int(dateSplit[2]) == 11):
                    monthToDays = 304
                elif (int(dateSplit[2]) == 12):
                    monthToDays = 335
                totalDays = yearToDays + monthToDays + int(dateSplit[2])
                delta = timedelta(days=totalDays)
                self.deltaDates.append(delta)
                
            self.times = []
            self.deltaTimes = []
            for sighting in sightings:
                time = sighting.getElementsByTagName("time")[0]
                timeSplit = str(time.childNodes).split("'")
                time = timeSplit[1]
                self.times.append(time)
                
                timeSplit = time.split(":")
                delta = timedelta(hours=int(timeSplit[0]), minutes=int(timeSplit[1]), seconds=int(timeSplit[2]))
                self.deltaTimes.append(delta)
            
            #merge deltaTimes and deltaDates
            self.givenDeltaDateTimes = []
            location = 0
            for deltaTime in self.deltaTimes:
                self.givenDeltaDateTimes.append(deltaTime + self.deltaDates[location])
                location = location + 1
                
            #find order
            order = [] # each element represents an element in deltaDateTime the number is the order
            actualDeltaDateTimes = []
            for given in self.givenDeltaDateTimes:
                actualDeltaDateTimes.append(given)
            actualDeltaDateTimes.sort()
            for given in self.givenDeltaDateTimes:
                position = 0 #order to be printed
                for actual in actualDeltaDateTimes:
                    if(given == actual):
                            order.append(position)
                    position = position + 1
                    
            #Write to log
            log = open(self.logFile, 'a')
            for orderPos in order:
                body = self.bodies[orderPos]
                date = self.dates[orderPos]
                time = self.times[orderPos]
                obser = self.observations[orderPos]
                logmsgBody = body + " " + date  + " " + time  + " " + obser
                log.write(self.logmsg + logmsgBody)
            logmsgEnd = 'End of sighting file: ' + self.sightingFile
            log.write(self.logmsg + logmsgEnd)
            log.close()
            return (approximateLatitude, approximateLongitude)
        except ValueError:
            print("Fix.getSightings:  ValueError Raised")
            
            
            