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
        expected = ":\tD:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\testLog.txt\n" 
        Fix.Fix('testLog.txt')
        log = open('testLog.txt','r')
        for line in log:
            actualUnsplit = line
        actualSplit = actualUnsplit.split("Log file")
        if(len("Log file") == 1):
            self.assertEquals(True, False)
        actual = actualSplit[1]
            
        self.assertEquals(expected, actual)

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
        expected = ":\tD:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\f.xml\n"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('f.xml')
        log = open('testLog.txt', 'r')
        logLines = log.readlines()
        for line in logLines:
            actualUnsplit = line
        actualSplit = actualUnsplit.split("Sighting file")
        if(len(actualSplit) == 1):
            self.assertEquals(False, True)
        actual = actualSplit[1]
            
        self.assertEquals(expected, actual)
         
        
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
        expected = "\t2017-04-14\t23:50:14\t15d01.5\t27d59.1\t84d33.4\n"
        aFix = Fix.Fix('test300_Log.txt')
        aFix.setSightingFile('test300_SightingFile.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings()
        log = open('test300_Log.txt', 'r')
        logLines = log.readlines()
        containsData = False
        for line in logLines:
            actualUnsplit = line
            actualSplit = actualUnsplit.split('Pollux')
            if(len(actualSplit) == 2):
                actual = actualSplit[1]
                containsData = True
        self.assertEquals(containsData, True)
        self.assertEquals(actual, expected)
         

    def test300_020_ShouldOutputSightingErrorsInLogFile(self):
        #default lat and long = "0d0.0"
        expected = ":\t1\n"
        aFix = Fix.Fix('test300_Log.txt')
        aFix.setSightingFile('test300_SightingFile.xml')
        aFix.setStarFile("stars.txt")
        aFix.setAriesFile("aries.txt")
        aFix.getSightings()
        log = open('test300_log.txt', 'r')
        logLines = log.readlines()
        containsData = False
        for line in logLines:
            actualUnsplit = line
            actualSplit = actualUnsplit.split('Sighting errors')
            if(len(actualSplit) == 2):
                actual = actualSplit[1]
                containsData = True
        self.assertEquals(containsData, True)
        actual = actualSplit[1]
        self.assertEquals(actual, expected)
         
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
        expected = "D:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\aries.txt"
        aFix = Fix.Fix('testLog.txt')
        actual = aFix.setAriesFile("aries.txt")
        self.assertEquals(actual, expected)
    
    def test400_020_ShouldOutputEntryToLogFile(self):
        expected = ":\tD:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\aries.txt\n"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setAriesFile("aries.txt")
        log = open('testLog.txt', 'r')
        logLines = log.readlines()
        for line in logLines:
            actualUnsplit = line
        actualSplit = actualUnsplit.split('Aries file')
        if(len(actualSplit) == 1):
            self.assertEquals(True, False)
        actual = actualSplit[1]
        self.assertEquals(actual, expected)
        
    def test400_910_ShouldRaiseExceptionParameterViolation(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        with self.assertRaises(ValueError):
            aFix.setAriesFile(5432345)
            
#   Acceptance Test:500
#        Analysis - setStarsFile
#            inputs
#               starsFile
#            state change
#               Writes the following entry to the log file: "Stars file:\t" + abs filepath of stars file
#            Happy path
#                returns a string whose value is the abs filepath of the file specified
#            Sad path
#                Exception raised. no state change
#                raised when filename is invalid (violates parameter specification or cannot be open)
#      Happy path

    def test500_010_ShouldReturnAbsoluteFilePath(self):
        expected = "D:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\stars.txt"
        aFix = Fix.Fix('testLog.txt')
        actual = aFix.setStarFile("stars.txt")
        self.assertEquals(actual, expected)

    def test500_020_ShouldOutputEntryToLogFile(self):
        expected = ":\tD:\\6700_Process\\Git\\SoftwareProcess\\SoftwareProcess\\Navigation\\test\\stars.txt\n"
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        aFix.setStarFile("stars.txt")
        log = open('testLog.txt', 'r')
        logLines = log.readlines()
        for line in logLines:
            actualUnsplit = line
        actualSplit = actualUnsplit.split('Star file')
        if(len(actualSplit) == 1):
            self.assertEquals(True, False)
        actual = actualSplit[1]
        self.assertEquals(actual, expected)
        
    def test500_910_ShouldRaiseExceptionParameterViolation(self):
        aFix = Fix.Fix('testLog.txt')
        aFix.setSightingFile('test.xml')
        with self.assertRaises(ValueError):
            aFix.setStarFile(5432345)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()