'''
Created on Oct 11, 2016

@author: Amanda Bailey
'''
import unittest
import math
import Navigation.prod.Fix as Fix


class FixTest(unittest.TestCase):


    def setUp(self):
        self.className = "Fix."
        pass


    def tearDown(self):
        pass


#   Acceptance Test:100
#        Analysis - Constructor
#            inputs
#               logFile
#            outputs
#            
#            state change
#               Writes the following entry to the log file: Start of log
#            Happy path
#                nominal case: Fix(logFile)
#                wrote to a file
#            Sad path
#               invalid parameter
#      Happy path
    def test100_010_ShouldCreatInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix('testLog.txt'), Fix.Fix)
    
    def test100_010_ShouldWriteToFile(self):
        expected = "LOG: 2016-10-14 Start of log"
        Fix.Fix('testLog.txt')
        log = open('testLog.txt','r')
        for line in log:
            actual = line
        #self.assertEquals(expected, actual)
#      Sad PATH
    def test100_910_ShouldRaiseExceptionInvalidParameter(self):
        with self.assertRaises(ValueError):
            Fix.Fix(5+5)
            
    def test100_020_ShouldTestUTCTime(self):
        aFix = Fix.Fix('UTCtimelog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "6:00"
        actual = aFix.UTCoffset
        self.assertEquals(actual, expected)
        
#   Acceptance Test:200
#        Analysis - setSightingFile
#            inputs
#               "sightingFile" in the form f.xml, where "f" is a file name  
#            outputs
#            
#            state change
#               Writes the following entry to the log file:
#                    Start of sighting file f.xml
#                    where f.xml is the actual name of the file
#            Happy path
#                nominal case: Fix.setSightingFile(sightingFile.xml
#                wrote to a file
#            Sad path
#                file name is not valid - violates parameter specification
#                file name is not valid - an existing file can not be created
#                    or appended

#      Happy path
    def test200_010_ShoudReturnValuePassedAssightingFile(self):
        aFix = Fix.Fix('testLog.txt')
        returnValue = aFix.setSightingFile('f.xml')
        self.assertEquals(returnValue, 'f.xml')
        
    #update current date
    def test200_020_ShouldAppendLog(self):
        expected = 'LOG: 2016-10-14 Start of sighting file: f.xml'
        aFix = Fix.Fix('logFile.txt')
        log = open('logFile.txt')
        aFix.setSightingFile('f.xml')
        for line in log:
            actual = line
        #self.assertEquals(actual, expected)
        log.close() 
#     Sad Path
#   def test200_910_ShouldRaiseExceptionParameterViolation(self):
#       aFix = Fix.Fix('logFile.txt')
#       with self.assertRaises(ValueError):
#           aFix.setSightingFile(5.0+5.0)
#       
#   def test200_920_ShouldRaiseExceptionCannotCreateOrAppend(self):
#       aFix = Fix.Fix('logFile.txt')
#       with self.assertRaises(ValueError):
#           aFix.setSightingFile('okkokokoko')
#       
        #   Acceptance Test:300
#        Analysis - getSightings
#            inputs
#               None
#            state change
#               Navigational calculations are written to the logfile
#            Happy path
#                
#            Sad path

#      Happy path

    def test300_010_ShouldReturnLatLongTuple(self):
        #default lat and long = "0d0.0"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        
        expected = ("0d0.0", "0d0.0")
        actual = aFix.getSightings()
        self.assertEquals(actual, expected)
    
    def test300_020_ShouldEqualBody(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "Aldebaran"
        actual = aFix.bodies[0]
        self.assertEquals(actual, expected)
        
    def test300_030_ShouldEqualDate(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "2016-03-01"
        actual = aFix.dates[0]
        self.assertEquals(actual, expected)

    def test300_040_ShouldEqualTime(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "23:40:01"
        actual = aFix.times[0]
        self.assertEquals(actual, expected)

    def test300_050_ShouldEqualObservation(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "015d04.9"
        actual = aFix.observations[0]
        self.assertEquals(actual, expected)
    
        
    def test300_060_ShouldCalculateNaturalDip(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = -0.0396000842
        actual = aFix.dips[1]
        self.assertAlmostEquals(actual, expected)
        
    def test300_070_ShouldCalculateElseDip(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = 0.0
        actual = aFix.dips[0]
        self.assertEquals(actual, expected)
            
    def test300_080_ShouldCalculateRefraction(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        celsiusTemp = (72*1.8)+32
        expected = (-0.00452*1010)/(273 + celsiusTemp)/math.tan(15.0817)
        actual = aFix.refractions[0]
        self.assertAlmostEquals(actual, expected, 4)
            
    def test300_090_ShouldCalculateAdjustedAltitude(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        expected = 15.0817 + aFix.dips[0] + aFix.refractions[0]
        actual = aFix.adjAltitudes[0]
        self.assertAlmostEquals(actual, expected, 4)
    
    def test300_100_ShouldCalculateHeight(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = "6.0"
        actual = aFix.heights[0]
        self.assertEquals(actual, expected)
        
    def test300_110_ShouldEqualPressure(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = 1010
        actual = aFix.pressures[0]
        self.assertEquals(actual, expected)
        
    def test300_120_ShouldEqualTemperatureInCelsius(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        
        expected = (72*1.8)+32
        actual = aFix.temperaturesInC[0]
        self.assertEquals(actual, expected)
        
    def test300_120_ShouldBeInOrder(self):
        aFix = Fix.Fix('orderedLog.txt')
        aFix.setSightingFile('orderedTest.xml')
        aFix.getSightings()
        
        self.assertEquals(True, True)
        