'''
Created on Oct 29, 2016

@author: ajb0052
'''
import unittest
import Navigation.prod.Fix as Fix
import os


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

#      NOTE: CHECK THAT THE ABSOLUTE PATH IS CORRECT ON YOUR MACHINE
    def test100_010_ShouldOutputLogStringInLogFile(self):
        expected = "Log file:\tD:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\testLog.txt" 
        Fix.Fix('testLog.txt')
        log = open('testLog.txt','r')
        for line in log:
            actual = line
        self.assertEquals(expected, actual)
        os.remove('testLog.txt')

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
    def test200_010_ShouldOutputSightingStringInLogFile(self):
        expected = "Sighting file:\tD:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\testLog.txt"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('f.xml')
        log = open('testLog.txt', 'r')
        logLines = log.split('\n')
        for line in logLines:
            actual = line
        self.assertEquals(expected, actual)
        os.remove('testLog.txt')
        
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

    def test300_010_ShouldOutputSightingDataInLogFile(self):
        #default lat and long = "0d0.0"
        expected = "Pollux      2017-04-14     23:50:14     15d01.5     27d59.1     84d33.4"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        log = open('testLog.txt', 'r')
        logLines = log.split('\n')
        actualLine = logLines[2]
        actualSplit = actualLine.split(' ')
        actual = actualSplit[3] + actualSplit[4]
        aFix.getSightings()
        self.assertEquals(actual, expected)
        os.remove('testLog.txt')

    def test300_020_ShouldOutputSightingErrorsInLogFile(self):
        #default lat and long = "0d0.0"
        expected = "Sighting errors:      1"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.getSightings()
        log = open('testLog.txt', 'r')
        logLines = log.split('\n')
        for line in logLines:
            actualLine = line
        actualSplit = actualLine.split(' ')
        actual = actualSplit[3] + actualSplit[4]
        aFix.getSightings()
        self.assertEquals(actual, expected)
        os.remove('testLog.txt')
    #sadness
    def test300_910_ShouldReturnValueErrorExceptionForAriesFile(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setStarFile('star.txt')
        with self.assertRaises(ValueError):
            aFix.getSightings()
    def test300_920_ShouldReturnValueErrorExceptionForStarFile(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setAriesFile('aries.txt')
        with self.assertRaises(ValueError):
            aFix.getSightings()
#   Acceptance Test:400
#        Analysis - setAriesFile
#            inputs
#               ariesFile
#            state change
#               Writes the following entry to the log file: "Aries file:\t" + abs filepath of aries file
#            Happy path
#                returns a string whose value is the abs filepath of the file specified
#            Sad path
#                Exception raised. no state change
#                raised when filename is invalid (violates parameter specification or cannot be open)
#      Happy path

    def test400_010_ShouldReturnAbsoluteFilePath(self):
        expected = "D:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\aries.txt"
        aFix = Fix.Fix('testLog.txt')
        actual = aFix.setAriesFile("aries.txt")
        self.assertEquals(actual, expected)
    
    def test400_020_ShouldOutputEntryToLogFile(self):
        expected = "Aries file:    D:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\aries.txt"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setAriesFile("aries.txt")
        aFix.setStarile("stars.txt")
        aFix.getSightings()
        log = open('testLog.txt', 'r')
        logLines = log.split('\n')
        for line in logLines:
            actualLine = line
        actualSplit = actualLine.split(' ')#split the prefix date/time written from info
        actual = actualSplit[3] + actualSplit[4]#out back together the "Aries file:" and abs filepath of file
        aFix.getSightings()
        self.assertEquals(actual, expected)
        os.remove('testLog.txt')
        
    def test400_910_ShouldRaiseExceptionParameterViolation(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        with self.assertRaises(ValueError):
            aFix.setAriesFile(5432345)
            
#   Acceptance Test:500
#        Analysis - setAriesFile
#            inputs
#               ariesFile
#            state change
#               Writes the following entry to the log file: "Aries file:\t" + abs filepath of aries file
#            Happy path
#                returns a string whose value is the abs filepath of the file specified
#            Sad path
#                Exception raised. no state change
#                raised when filename is invalid (violates parameter specification or cannot be open)
#      Happy path

    def test500_010_ShouldReturnAbsoluteFilePath(self):
        expected = "D:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\stars.txt"
        aFix = Fix.Fix('testLog.txt')
        actual = aFix.setStarFile("stars.txt")
        self.assertEquals(actual, expected)
    
    def test500_020_ShouldOutputEntryToLogFile(self):
        expected = "Star file:    D:\6700_Process\Git\SoftwareProcess\SoftwareProcess\Navigation\test\stars.txt"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setAriesFile("aries.txt")
        aFix.setStarile("stars.txt")
        aFix.getSightings()
        log = open('testLog.txt', 'r')
        logLines = log.split('\n')
        for line in logLines:
            actualLine = line
        actualSplit = actualLine.split(' ')#split the prefix date/time written from info
        actual = actualSplit[3] + actualSplit[4]#out back together the "Star file:" and abs filepath of file
        aFix.getSightings()
        self.assertEquals(actual, expected)
        os.remove('testLog.txt')
        
    def test500_910_ShouldRaiseExceptionParameterViolation(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        with self.assertRaises(ValueError):
            aFix.setStarFile(5432345)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()