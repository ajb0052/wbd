'''
Created on Sep 9, 2016

'''
import unittest
import Navigation.prod.Angle as A


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_Happy(self):
        angle = A.Angle()
        self.assertEqual(angle.degrees, 0)
        self.assertEqual(angle.minutes, 0.0)
    
    def test_setDegrees_Happy(self):
        angle = A.Angle()
        self.assertEqual(angle.setDegrees(30), 30)
        
    def test_setDegreesAndMinutes_Happy(self):
        angle = A.Angle()
        self.assertEqual(angle.setDegreesAndMinutes("23d32"), 23)
        
    def test_add_Happy(self):
        angle = A.Angle()
        bngle = A.Angle()
        angle.setDegreesAndMinutes("30d20")
        bngle.setDegreesAndMinutes("70d20")
        angle.add(bngle)
        self.assertEquals(angle.degrees, 100)
        self.assertEquals(angle.minutes, 40)
        self.assertEquals(bngle.degrees, 70)
        self.assertEquals(bngle.minutes, 20)
        
    def test_subtract_Happy(self):
        angle = A.Angle()
        bngle = A.Angle()
        angle.setDegreesAndMinutes("100d30")
        bngle.setDegreesAndMinutes("100d30")
        angle.subtract(bngle)
        self.assertEquals(angle.degrees, 0)
        self.assertEquals(angle.minutes, 0.0)
        self.assertEquals(bngle.degrees, 100)
        self.assertEquals(bngle.minutes, 30) 
        
    def test_compare_Happy(self):
        angle = A.Angle()
        bngle = A.Angle()
        self.assertEquals(angle.compare(bngle), 0)
        
        bngle.setDegreesAndMinutes("0d5")
        self.assertEquals(angle.compare(bngle), -1)
        
        angle.setDegreesAndMinutes("4d0")
        self.assertEquals(angle.compare(bngle), 1)
    
    def test_getString_Happy(self):
        angle = A.Angle()
        self.assertEquals(angle.getString(), "0d0.0")
    
    def test_getDegrees_Happy(self):
        angle = A.Angle()
        self.assertEquals(angle.getDegrees(), 0)

