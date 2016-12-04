'''
Created on Oct 11, 2016

@author: Amanda Bailey
'''
from xml.dom.minidom import parse
from datetime import date, timedelta
import time
import math
import os
import Navigation.prod.Angle as Angle

class Fix():
    def __init__(self, logFile="log.txt"):
        self.starFile = None
        self.ariesFile = None
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
                log.write(self.logmsg + "Log file:\t" + os.path.abspath(logFile) + "\n")
                log.close()
                self.sightingFile = None
            except ValueError:
                raise ValueError('Fix.fix:  could not open or append to file')
    
    def setAriesFile(self, ariesFile=None):
        if(ariesFile==None):
            raise ValueError("Fix.setAriesFile:  ValueError Raised")
        try:
            filename = str(ariesFile).split(".")
            if (isinstance(ariesFile, str) == False):
                raise ValueError("Fix.setAriesFile:  ValueError Raised")
            if (len(filename) != 2):
                raise ValueError
            if (filename[1] != 'txt'):
                raise ValueError
            if (filename[0] == ''):
                raise ValueError
            #CREATE FILE IF IT DOESNT ALREADY EXIST
            aFile = open(ariesFile, 'a')
            aFile.close()
            
            #SET FILE
            self.ariesFile = ariesFile
            
            #WRITE TO LOG
            logmsgStart = 'Aries file:\t' + os.path.abspath(ariesFile)
            log = open(self.logFile, 'a')
            log.write(self.logmsg + logmsgStart + '\n')
            log.close()
            return os.path.abspath(ariesFile)
        except ValueError:
            raise ValueError("Fix.setAriesFile:  ValueError Raised")

    def setStarFile(self, starFile=None):
        if(starFile==None):
            raise ValueError("Fix.setStarFile:  ValueError Raised")
        try:
            filename = str(starFile).split(".")
            if (isinstance(starFile, str) == False):
                raise ValueError("Fix.setStarFile:  ValueError Raised")
            if (len(filename) != 2):
                raise ValueError
            if (filename[1] != 'txt'):
                raise ValueError
            if (filename[0] == ''):
                raise ValueError
            #CREATE FILE IF IT DOESNT ALREADY EXIST
            aFile = open(starFile, 'a')
            aFile.close()
            
            #SET FILE
            self.starFile = starFile
            
            #WRITE TO LOG
            logmsgStart = 'Star file:\t' + os.path.abspath(starFile)
            log = open(self.logFile, 'a')
            log.write(self.logmsg + logmsgStart + '\n')
            log.close()
            return os.path.abspath(starFile)
        except ValueError:
            raise ValueError("Fix.setStarFile:  ValueError Raised")
            
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
            logmsgStart = 'Sighting file:\t' + os.path.abspath(sightingFile)
            log = open(self.logFile, 'a')
            log.write(self.logmsg + logmsgStart + '\n')
            log.close()
            return os.path.abspath(sightingFile)
        except ValueError:
            raise ValueError("Fix.setSightingFile:  ValueError Raised")
            print("Fix.setSightingFile:  ValueError Raised")
            
    def getSightings(self):
        try:
            if(self.sightingFile == None):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            if(self.ariesFile == None):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            if(self.starFile == None):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            approximateLatitude = "0d0.0"
            approximateLongitude = "0d0.0"
            #retrieve data
            fix = parse(self.sightingFile)
            
            if(fix.documentElement.tagName != "fix"):
                raise ValueError("Fix.getSightings:  ValueError Raised")
            sightings = fix.getElementsByTagName("sighting")
            sightingErrorPos = []
            bodyPos = 0
            self.bodies = []
            for sighting in sightings:
                body = sighting.getElementsByTagName("body")[0]
                bodySplit = str(body.childNodes).split("'")
                if (len(bodySplit) <= 2):
                    body = "Unknown"
                    sightingErrorPos.append(bodyPos) 
                else:
                    body = bodySplit[1]
                self.bodies.append(body)
                bodyPos = bodyPos + 1
            
            obsCount = 0
            self.observations = []
            for sighting in sightings:
                observation = sighting.getElementsByTagName("observation")[0]
                observationSplit = str(observation.childNodes).split("'")
                if (len(observationSplit) <= 2):
                    observation = 'error'
                    sightingErrorPos.append(obsCount)
                else:
                    observation = observationSplit[1]
                    dm = observation.split('d')
                    if(len(dm) == 1):
                        observation = 'error'
                        sightingErrorPos.append(obsCount)
                self.observations.append(observation)
                obsCount = obsCount + 1
                
           
            
            #see if valid
            self.times = []
            position = 0
            for sighting in sightings:
                time = sighting.getElementsByTagName("time")[0]
                timeSplit = str(time.childNodes).split("'")
                if (len(timeSplit) <= 2):
                    raise ValueError
                time = timeSplit[1]
                hms = time.split(':')
                if(len(hms) != 3):
                    time = 'error'
                    sightingErrorPos.append(position)
                else:
                    if(len(hms) == 1):
                        time = 'error'
                        sightingErrorPos.append(position)
                    if(int(hms[0]) > 24):
                        time = 'error'
                        sightingErrorPos.append(position)
                    if(int(hms[1]) > 59):
                        time = 'error'
                        sightingErrorPos.append(position)
                    if(int(hms[2]) > 59):
                        time = 'error'
                        sightingErrorPos.append(position)
                self.times.append(time)
                position = position + 1
            
            self.heights = []
            heightCount = 0
            for sighting in sightings:
                found = False
                alternate = 0
                for node in sighting.childNodes:
                    if(alternate == 18):
                        break
                    if(alternate%2 == 0):
                        candidate = node.nextSibling
                        candidate = candidate.tagName
                        alternate = alternate + 1
                    else:
                        alternate = alternate +1
                    if(candidate == "height"):
                        found = True
                        break
                    
                if(found):
                    height = sighting.getElementsByTagName("height")[0]
                    heightSplit = str(height.childNodes).split("'")
                    if (len(heightSplit) <= 2):
                        height = 'error'
                        sightingErrorPos.append(heightCount)
                    else:
                        height = heightSplit[1]
                        decCheck = height.split('.')
                        if(len(decCheck) == 1):
                            height = 'error'
                            sightingErrorPos.append(heightCount)
                else:
                    height = 0
                self.heights.append(height)
                heightCount = heightCount + 1
            #HORIZON
            self.horizons = []
            self.dips = []
            location = 0
            for sighting in sightings:
                if(self.heights[location] == 'error'):
                    self.horizons.append('error')
                    self.dips.append('error')
                    continue
                
                found = False
                alternate = 0
                for node in sighting.childNodes:
                    if(alternate == 18):
                        break
                    if(alternate%2 == 0):
                        candidate = node.nextSibling
                        candidate = candidate.tagName
                        alternate = alternate + 1
                    else:
                        alternate = alternate +1
                    if(candidate == "horizon"):
                        found = True
                        break
                
                if(found):
                    horizon = sighting.getElementsByTagName("horizon")[0]
                    horizonSplit = str(horizon.childNodes).split("'")
                    if (len(horizonSplit) <= 2):
                        horizon = 'error'
                        sightingErrorPos.append(location)
                    horizon = horizonSplit[1]
                    if ((horizon.lower() != "natural")  and (horizon.lower() != "artificial")):
                        horizon = 'error'
                        sightingErrorPos.append(location)
                else:
                    horizon = "natural"
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
            pressureCount = 0
            for sighting in sightings:
                found = False
                alternate = 0
                for node in sighting.childNodes:
                    if(alternate == 18):
                        break
                    if(alternate%2 == 0):
                        candidate = node.nextSibling
                        candidate = candidate.tagName
                        alternate = alternate + 1
                    else:
                        alternate = alternate +1
                    if(candidate == "pressure"):
                        found = True
                        break
                if(found):
                    pressure = sighting.getElementsByTagName("pressure")[0]
                    pressureSplit = str(pressure.childNodes).split("'")
                    if(len(pressureSplit) <= 2):
                        pressure = 'error'
                        sightingErrorPos.append(pressureCount)
                        self.pressures.append(pressure)
                    else:
                        #check if float
                        pressure = pressureSplit[1]
                        isFloat = pressureSplit[1]
                        if '.' in isFloat:
                            pressure = 'error'
                            sightingErrorPos.append(pressureCount)
                            self.pressures.append(pressure)
                        else:
                            pressure = int(isFloat)
                            if((pressure < 100)  or (pressure > 1100)):
                                pressure = 'error'
                                sightingErrorPos.append(pressureCount)
                                self.pressures.append(pressure)
                            self.pressures.append(int(pressure))
                else:
                    pressure = 1010
                    self.pressures.append(pressure)
                pressureCount = pressureCount + 1
                
            #Calculating adjustedAltitudes
            self.temperaturesInC = []
            self.refractions = []
            self.adjAltitudes = []
            location = 0
            found = False
            for sighting in sightings:
                if(self.observations[location] == 'error' or
                   self.heights[location] == 'error' or
                   self.pressures[location] == 'error'):
                    continue
                alternate = 0
                for node in sighting.childNodes:
                    if(alternate == 18):
                        break
                    if(alternate%2 == 0):
                        candidate = node.nextSibling
                        candidate = candidate.tagName
                        alternate = alternate + 1
                    else:
                        alternate = alternate +1
                    if(candidate == "temperature"):
                        found = True
                        break
                if(found):
                    temperature = sighting.getElementsByTagName("temperature")[0]
                    temperatureSplit = str(temperature.childNodes).split("'")
                    if (len(temperatureSplit) <= 0):
                        temperature = 'error'
                        sightingErrorPos.append(location)
                        continue
                    temperature = float(temperatureSplit[1])
                    if((int(temperature)) < -20  or  (int(temperature) > 120)):
                        temperature = 'error'
                        sightingErrorPos.append(location)
                        continue
                else:
                    temperature = 72
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
           
            #retrieve DATES   
            self.dates = []
            self.deltaDates = []
            for sighting in sightings:
                date = sighting.getElementsByTagName("date")[0]
                dateStr = str(date.childNodes).split("'")
                
                #see if valid
                if (len(dateStr) <= 2):
                    sightingErrorPos.append(sighting)
                    date = 'error'
                date = dateStr[1]
                ymd = date.split('-')
                if(len(ymd) == 1):
                    sightingErrorPos.append(sighting)
                    date = 'error'
                if(int(ymd[0]) > 9999):
                    sightingErrorPos.append(sighting)
                    date = 'error'
                if(int(ymd[1]) > 12):
                    sightingErrorPos.append(sighting)
                    date = 'error'
                if(int(ymd[2]) > 31):
                    sightingErrorPos.append(sighting)
                    date = 'error'
                self.dates.append(date)
                
                if(date == 'error'):
                    delta = 'error'
                else:
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
                if(time != 'error' and len(timeSplit) == 3):
                    delta = timedelta(hours=int(timeSplit[0]), minutes=int(timeSplit[1]), seconds=int(timeSplit[2]))
                else:
                    delta = 0
                self.deltaTimes.append(delta)
            #merge deltaTimes which is timedelta and deltaDates
            self.givenDeltaDateTimes = []
            location = 0
            for deltaTime in self.deltaTimes:
                #days and minutes were converted into seconds in deltaTimes
                if(self.deltaDates[location] == 'error'):
                    deltaDateTime = 'error'
                else:
                    deltaDateTime = timedelta(seconds = deltaTime.seconds,
                                              days = self.deltaDates[location].days)
                self.givenDeltaDateTimes.append(deltaDateTime)
                location = location + 1
                
            #get lat long
            star = open(self.starFile)
            starLines = star.readlines()
            aries = open(self.ariesFile)
            ariesLines = aries.readlines()
            bodyCount = 0
            dateLineSplit = []
            self.lats = []
            self.longs = []
            self.SHAstars = []
            for body in self.bodies:
                #star File data
                if(body == "Unknown"):
                    self.lats.append(approximateLatitude)
                    self.longs.append(approximateLongitude)
                    bodyCount = bodyCount+1  
                    continue
                if(self.times[bodyCount] == 'error' or
                   self.dates[bodyCount] == 'error' or
                   self.deltaTimes[bodyCount] == 'error' or
                   self.deltaDates[bodyCount] == 'error' or
                   self.givenDeltaDateTimes == 'error'):
                    self.lats.append(approximateLatitude)
                    self.longs.append(approximateLongitude)
                    bodyCount = bodyCount+1 
                    continue
                for line in starLines:
                    lineSplit = line.split("\t")
                    if(len(lineSplit) == 1):
                        raise ValueError
                    if((lineSplit[0] == body)):
                        bodyYMD = self.dates[bodyCount].split("-")
                        starLineMDY = lineSplit[1].split("/")
                        if(bodyYMD[1] == starLineMDY[0]):
                            if(bodyYMD[2] <= starLineMDY[1]):
                                dateLineSplit = lineSplit
                if(len(dateLineSplit) == 4):
                    SHAstar = dateLineSplit[2].split("d")
                    self.lats.append(dateLineSplit[3])
                #aries file data
                ariesLine1 = []
                ariesLine2 = []
                for line in ariesLines:
                    lineSplit = line.split("\t")
                    if(len(lineSplit) == 1):
                        raise ValueError
                    if(len(ariesLine1) > 0):
                        ariesLine2 = lineSplit
                    if(True):
                        bodyYMD = self.dates[bodyCount].split("-")
                        bodyHMS = self.times[bodyCount].split(":")
                        bodyH = 0
                        if(int(bodyHMS[0]) != 0):
                            bodyH = int(bodyHMS[0].lstrip("0"))
                        s = (int(bodyHMS[1])*60) + bodyH #5
                        ariesLineMDY = lineSplit[0].split("/")
                        if(bodyYMD[1] == ariesLineMDY[0]):
                            if(bodyYMD[2] == ariesLineMDY[1]):
                                if(bodyH == int(lineSplit[1])):
                                    ariesLine1 = lineSplit
                if((len(ariesLine1) == 3) and (len(ariesLine2) == 3)):
                    GHA1 = []
                    ariesLine1Split = ariesLine1[2].split("d") #1 and 2
                    GHA1degree = float(ariesLine1Split[0])
                    GHA1minuteSplit = ariesLine1Split[1].split("\n")
                    GHA1minute = GHA1minuteSplit[0]
                    GHA1.append(GHA1degree)
                    GHA1.append(GHA1minute)
                    
                    GHA2 = []
                    ariesLine2Split = ariesLine2[2].split("d") #3 and 4
                    GHA2degree = float(ariesLine2Split[0])
                    GHA2minuteSplit = ariesLine2Split[1].split("\n")
                    GHA2minute = GHA2minuteSplit[0]
                    GHA2.append(GHA2degree)
                    GHA2.append(GHA2minute)
                    degreeDiff = abs(GHA2[0] - GHA1[0])#6
                    minuteDiff = abs(float(GHA2[1]) - float(GHA1[0]))
                    GHA = []
                    GHA.append((degreeDiff*s/3600.0) + float(GHA1[0]))
                    GHA.append(((minuteDiff*s/3600.0) + float(GHA1[1]))%60)
                    GHAo = []
                    GHAo.append((GHA[0] + float(SHAstar[0]))%360)#C1 and 2
                    GHAo.append(GHA[1] + float(SHAstar[1]))
                    self.longs.append(str(GHAo[0]) + "d" + str(GHAo[1]))
                else:
                    self.longs.append(approximateLongitude)
                bodyCount = bodyCount+1  
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
            #write
            log = open(self.logFile, 'a')
            for orderPos in order:
                body = self.bodies[orderPos]
                date = self.dates[orderPos]
                time = self.times[orderPos]
                obser = self.observations[orderPos]
                lat = self.lats[orderPos]
                glong = self.longs[orderPos]
                logmsgBody = body + "\t" + date  + "\t" + time  + "\t" + obser + "\t" + lat + "\t" + glong
                log.write(self.logmsg + logmsgBody + '\n')
            numOfErrors = 0
            #for i in range(0, len(sightings)):
            #    if(sightingErrorPos.count(i) > 0):
            #        numOfErrors = numOfErrors+1
            numOfErrors = len(sightingErrorPos)
            logmsgEnd = 'Sighting errors:\t' + str(numOfErrors)
            log.write(self.logmsg + logmsgEnd + '\n')
            log.close()
            return (approximateLatitude, approximateLongitude)
        except ValueError:
            raise ValueError("Fix.getSightings:  ValueError Raised")
            print("Fix.getSightings:  ValueError Raised")
        