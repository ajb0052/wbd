'''
Created on Nov 28, 2016

@author: ajb0052
'''
import unittest
import Navigation.prod.Fix as Fix

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

#################################################
# Parameter changes
    def test100_010_LatitudeShouldReturnValidStringWhereHIsN(self):
        expected = "N27d59.5"#hxdy.y
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "0d0.0" )
        actual = aFix.assumedLat
        self.assertEquals(expected, actual)

    def test100_020_LatitudeShouldReturnValidStringWhereHIsS(self):
        expected = "S27d59.5"#hxdy.y
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("S27d59.5", "0d0.0")
        actual = aFix.assumedLat
        self.assertEquals(expected, actual)
        
    def test100_030_LatitudeShouldReturnDefaultWithoutParameter(self):
        expectedLat = "0d0.0"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings()
        actualLat = aFix.assumedLat
        self.assertEquals(expectedLat, actualLat)
    
    def test100_040_LatitudeShouldReturnDefaultWithoutH(self):
        expected = "0d0.0"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("0d0.0", "0d0.0")
        actual = aFix.assumedLat
        self.assertEquals(expected, actual)
    
    def test100_050_LongitudetShouldReturnDefaultWithoutParameter(self):
        expected = "0d0.0"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings()
        actual = aFix.assumedLong
        self.assertEquals(expected, actual)
    
    def test100_060_LongitudeShouldReturnValidString(self):
        expected = "85d33.4"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "85d33.4")
        actual = aFix.assumedLong
        self.assertEquals(expected, actual)

    def test100_070_LongitudeShouldReturnDefault(self):
        expected = "0d0.0"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("0d0.0", "0d0.0")
        actual = aFix.assumedLong
        self.assertEquals(expected, actual)
    
    def test100_910_LatitudeShouldRaiseExceptionWithHAndDefaultAngle(self):
        expected = "0d0.0"
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("0d0.0", "0d0.0")
        actual = aFix.assumedLong
        self.assertEquals(expected, actual)
    
    def test100_920_LatitudeShouldRaiseExceptionWithoutHButNotDefaultAngle(self):
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        with self.assertRaises(ValueError):
            aFix.getSightings("27d59.5", "0d0.0")
    
    def test100_930_latitudeShouldRaiseExceptionWhenInvalidH(self):
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        with self.assertRaises(ValueError):
            aFix.getSightings("F27d59.5", "0d0.0")
    
    def test100_940_latitudeShoudRaiseExceptionWhenInvalidAngle(self):
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        with self.assertRaises(ValueError):
            aFix.getSightings("dsfg34523", "0d0.0")
    
    def test100_950_longitudeShouldRaiseExceptionWhenInvalidAngle(self):
        aFix = Fix.Fix('testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        with self.assertRaises(ValueError):
            aFix.getSightings("N27d59.5", "sdfgfdh23452")
    
#################################################
# Logfile Output Changes: For a sighting
    def test200_010_AssumedLatitudeShouldBeInLog(self):
        found = False
        aFix = Fix.Fix('200_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("0d0.0", "0d0.0")
        logfile = open('200_testLogCA05.txt', 'r')
        expected = "0d0.0"
        
        for line in logfile.readlines():
            isPollux = line.find('Pollux')
            if(isPollux != -1):
                splitLine = line.split("\t")
                if(splitLine[6] == expected):
                    found = True
        self.assertEquals(True, found)
    
    def test200_020_AssumedLongitudeShouldBeInLog(self):
        found = False
        aFix = Fix.Fix('200_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("0d0.0", "0d0.0")
        logfile = open('200_testLogCA05.txt', 'r')
        expected = "0d0.0"
        
        for line in logfile.readlines():
            isPollux = line.find('Pollux')
            if(isPollux != -1):
                splitLine = line.split("\t")
                if(splitLine[7] == expected):
                    found = True
        self.assertEquals(True, found)
    
    def test200_030_AzimuthAdjustmentShouldBeInLog(self):
        
        aFix = Fix.Fix('200_030_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "85d33.4")
        logfile = open('200_030_testLogCA05.txt', 'r')
        expected = "292d44.6"
        actual = 0
        
        for line in logfile.readlines():
            isPollux = line.find('Pollux')
            if(isPollux != -1):
                splitLine = line.split("\t")
                actual = splitLine[8]
        self.assertEquals(expected, actual)
    
    def test200_040_DistanceAdjustmentShouldBeInLog(self):
        aFix = Fix.Fix('200_030_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "85d33.4")
        logfile = open('200_030_testLogCA05.txt', 'r')
        expected = "174"
        actual = 0
        
        for line in logfile.readlines():
            isPollux = line.find('Pollux')
            if(isPollux != -1):
                splitLine = line.split("\t")
                actual = splitLine[9].strip('\n')
        self.assertEquals(expected, actual)
    
#################################################
# Logfile Output Changes: After listing the # of sightings that had an error
    def test300_010_approxLatShouldBeInLog(self):
        aFix = Fix.Fix('200_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "85d33.4")
        logfile = open('200_testLogCA05.txt', 'r')
        expected = "N29d68"
        actual = 0
        
        for line in logfile.readlines():
            hasAppLat = line.find('Approximate latitude:\tN29d68')
            if(hasAppLat != -1):
                splitLine = line.split("\t")
                actual = splitLine[9].strip('\n')
        self.assertEquals(expected, actual)
        
    def test300_020_approxLongSHouldBeInLog(self):
        aFix = Fix.Fix('200_testLogCA05.txt')
        aFix.setSightingFile('sightingFileCA05.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings("N27d59.5", "85d33.4")
        logfile = open('200_030_testLogCA05.txt', 'r')
        expected = "82d52.9"
        actual = 0
        
        for line in logfile.readlines():
            hasAppLong = line.find('Approximate longitude:\t82529')
            if(hasAppLong != -1):
                splitLine = line.split("\t")
                actual = splitLine[9].strip('\n')
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()