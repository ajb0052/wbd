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
    def __init__(self, logFile="log.txt"):
        if(isinstance(logFile, str) == False):
            raise ValueError('Fix.fix:  could not open or append to file')
        else:
            try:
                if(logFile == ""):
                    raise ValueError('Fix.fix:  could not open or append to file')
                self.logFile = logFile
                currentUTC = time.gmtime()
                currentHour = time.localtime().tm_hour
                self.UTCoffset = (currentUTC.tm_hour - currentHour)%12
                self.UTCoffset = str(self.UTCoffset + 1) + ":00"
                HrMinSec = str(currentUTC.tm_hour) + ":" + str(currentUTC.tm_min) + ":" + str(currentUTC.tm_sec) + " "
                self.logmsg = "LOG: " + str(date.today()) + " " + HrMinSec + "-" + self.UTCoffset + " "
                log = open(logFile, 'a')
                log.write(self.logmsg + 'Start of log\n')
                log.close()
                self.sightingFile = None
            except ValueError:
                raise ValueError('Fix.fix:  could not open or append to file')
    
    def setSightingFile(self, sightingFile=None):
        if(sightingFile==None):
            raise ValueError("Fix.setSightingFile:  ValueError Raised")
        try:
            filename = str(sightingFile).split(".")
            if (isinstance(sightingFile, str) == False):
                raise ValueError("Fix.setSightingFile:  ValueError Raised")
            if (len(filename) != 2):
                raise ValueError
            if (filename[1] != 'xml'):
                raise ValueError
            if (filename[0] == ''):
                raise ValueError
            #CREATE FILE IF IT DOESNT ALREADY EXIST
            sFile = open(sightingFile, 'a')
            sFile.close()
            
            #SET FILE
            self.sightingFile = sightingFile
            
            #WRITE TO LOG
            logmsgStart = 'Start of sighting file: ' + sightingFile
            log = open(self.logFile, 'a')
            log.write(self.logmsg + logmsgStart + '\n')
            log.close()
            return self.sightingFile
        except ValueError:
            raise ValueError("Fix.setSightingFile:  ValueError Raised")
            print("Fix.setSightingFile:  ValueError Raised")
            
    def getSightings(self):
        try:
            if(self.sightingFile == None):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            approximateLatitude = "0d0.0"
            approximateLongitude = "0d0.0"
            #retrieve data
            fix = parse(self.sightingFile)
            
            if(fix.documentElement.tagName != "fix"):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            sightings = fix.getElementsByTagName("sighting")
            self.bodies = []
            for sighting in sightings:
                body = sighting.getElementsByTagName("body")[0]
                bodySplit = str(body.childNodes).split("'")
                if (len(bodySplit) <= 2):
                    raise ValueError
                body = bodySplit[1]
                self.bodies.append(body)
            
            self.observations = []
            for sighting in sightings:
                observation = sighting.getElementsByTagName("observation")[0]
                observationSplit = str(observation.childNodes).split("'")
                if (len(observationSplit) <= 2):
                    raise ValueError
                observation = observationSplit[1]
                dm = observation.split('d')
                if(len(dm) == 1):
                    raise ValueError('invalid observation')
                self.observations.append(observation)
                
            #see if valid
            self.dates = []
            for sighting in sightings:
                date = sighting.getElementsByTagName("date")[0]
                dateSplit = str(date.childNodes).split("'")
                if (len(dateSplit) <= 2):
                    raise ValueError
                date = dateSplit[1]
                ymd = date.split('-')
                if(len(ymd) == 1):
                    raise ValueError
                if(int(ymd[0]) > 2016):
                    raise ValueError("Invalid year")
                if(int(ymd[1]) > 12):
                    raise ValueError("Invalid month")
                if(int(ymd[2]) > 31):
                    raise ValueError("Invalid day")
                self.dates.append(date)
            
            #see if valid
            self.times = []
            for sighting in sightings:
                time = sighting.getElementsByTagName("time")[0]
                timeSplit = str(time.childNodes).split("'")
                if (len(timeSplit) <= 2):
                    raise ValueError
                time = timeSplit[1]
                hms = time.split(':')
                if(len(hms) == 1):
                    raise ValueError('invalid time')
                if(int(hms[0]) > 24):
                    raise ValueError("Invalid hour")
                if(int(hms[1]) > 59):
                    raise ValueError("Invalid minute")
                if(int(hms[2]) > 59):
                    raise ValueError("Invalid second")
                self.times.append(time)
            
            #find the dip
            self.heights = []
            for sighting in sightings:
                height = sighting.getElementsByTagName("height")[0]
                heightSplit = str(height.childNodes).split("'")
                if (len(heightSplit) <= 2):
                    raise ValueError
                height = heightSplit[1]
                decCheck = height.split('.')
                if(len(decCheck) == 1):
                    raise ValueError("Invalid height")
                self.heights.append(height)
                
            self.horizons = []
            self.dips = []
            location = 0
            for sighting in sightings:
                horizon = sighting.getElementsByTagName("horizon")[0]
                horizonSplit = str(horizon.childNodes).split("'")
                if (len(horizonSplit) <= 2):
                    raise ValueError
                horizon = horizonSplit[1]
                if ((horizon.lower() != "natural")  and (horizon.lower() != "artificial")):
                    raise ValueError("Invalid Horizon")
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
                if (len(pressureSplit) <= 0):
                    raise ValueError
                pressure = pressureSplit[1]
                if((int(pressure) < 100)  or (int(pressure) > 1100)):
                    raise ValueError("Invalid Pressure")
                self.pressures.append(float(pressure))
            
            self.temperaturesInC = []
            self.refractions = []
            self.adjAltitudes = []
            location = 0
            for sighting in sightings:
                temperature = sighting.getElementsByTagName("temperature")[0]
                temperatureSplit = str(temperature.childNodes).split("'")
                if (len(temperatureSplit) <= 0):
                    raise ValueError
                temperature = float(temperatureSplit[1])
                if((int(temperature)) < -20  or  (int(temperature) > 120)):
                    raise ValueError("Temperature not in range")
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
                log.write(self.logmsg + logmsgBody + '\n')
            logmsgEnd = 'End of sighting file: ' + self.sightingFile + '\n'
            log.write(self.logmsg + logmsgEnd + '\n')
            log.close()
            return (approximateLatitude, approximateLongitude)
        except ValueError:
            raise ValueError("Fix.getSightings:  ValueError Raised")
            print("Fix.getSightings:  ValueError Raised")
            
            
            