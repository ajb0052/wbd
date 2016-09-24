'''
    Angle.py
    Created on 9 September 2016

    @author: Amanda Bailey
    An abstraction the represents an amount of rotation from a fixed point. 
    When used for navigation, angles are expressed in degrees and minutes, 
    where 1 degree = 60 minutes
'''
class Angle():
    '''
    Purpose: Creates an instance of Angle
     Parameters: No parameters
     Returns: An instance of Angle
     State change: The instance is set to 0 degrees, 0miniutes.
     Exceptions: No exceptions are raised
    '''
    def __init__(self):
        self.degrees = 0
        self.minutes = 0.0
    
    '''
    Purpose:
    
    Parameters: "degrees" num of degrees (and portions of). 
        It is a numeric value (integer or float). Optional,  defaults to zero 
        if missing. Arrives invalidated, if present.
    Returns: The resulting angle as degrees and portions of degrees as a 
        single floating point number, modulo 360
    State change: The instance is set to the specified value
    Exceptions: Type: ValueError
    Raised when: "degrees" violates the parameter specifications
    Exit conditions: The instance remains in the state it was in before the
    method was invoked. No new instance is produced '''
    def setDegrees(self, degrees):
        try:
            self.degrees = degrees
            return self.degrees%360
        except ValueError:
            print("Exceptions Raised: invalid")
            
    '''
    Purpose: Sets the value of the instance based on a string that contains
    degrees and minutes
    Parameters:
    Returns: The resulting angle as degrees and portions of degrees as a 
        single floating point number.
    State change: The instance is set to the specified value.
    Exceptions: Type: ValueError
    Raised when: "angleString" violates the parameter 
    specifications
    Exit conditions: No instance is created
    '''
    def setDegreesAndMinutes(self, angleString):
        try:
            degreesAndMinutes = angleString.split('d')
            if(len(degreesAndMinutes) == 2):
                self.degrees = float(degreesAndMinutes[0])
                self.minutes = float(degreesAndMinutes[1])
                return self.degrees%360
        except ValueError:
            print("Exception Raised: invalid")
    '''
    Purpose: adds the value of the parameterized value from the instance
    Parameter: "angle" is an instance of Angle whose value is to be added to
        current instance. Mandated Arrives invalidated.
    Returns: The resulting angle as degrees and portions of degrees as a 
        single floating point number, modulo 360
    State change: The instance retains the added value
    Exceptions: Type: ValueError   
    Raised when: "angle" is not a valid instance of Angle
    Exit conditions: The instance remains in the state it was 
        in before the method was invoked
                                         '''
    def add(self, angle):
        try:
            self.degrees = self.degrees + angle.degrees
            self.minutes = self.minutes + angle.minutes
            return self.degrees%360
        except ValueError:
            print("Exception Raised: invalid")
    '''
    Purpose:Subtracts the value of the parameterized value from the current
        instance.
    Parameters: "angle" is an instance of Angle whose value is to be 
    subtracted from the current instance
    Returns: The resulting angle as degrees and portions of degrees as a 
        single  floating point number, modulo 360
    State change: The instance retains the subtracted value.
    Exceptions: Type: ValueError
    Raised when: "angle" is not valid instance of Angle
    Exit Conditions: The instance remains in the state it 
        was in before the method was invoked.
    '''
    def subtract(self, angle):
        try:
            self.degrees = self.degrees - angle.degrees
            self.minutes = self.minutes - angle.minutes
            return self.degrees%360
        except ValueError:
            print("Exception Raised: invalid")
    
    '''
    Purpose: Compares parameterized value to the current instance.
    Parameters: "angle" is an instance of Angle whose value is to be added 
        to current instance. Mandatory. Arrives invalidated.
    Returns: An integer having the value: 
        -1 if the instance is less than the value passed as a parameter
            0 if the instance is equal to the value passed as a parameter
            1 if the instance is greater than the value passed as a parameter
    state change: No state change
    Exceptions: Type: ValueError
    Raised when: "angle" is not a valid instance of Angle
    Exit conditions: The instance remains in the state it was in
    before the method was invoked.
    '''
    def compare(self, angle):
        try:
            if (self.degrees == angle.degrees):
                if (self.minutes == angle.minutes):
                    return 0
                elif (self.minutes < angle.minutes):
                    return -1
                elif (self.minutes > angle.minutes):
                    return 1
            elif (self.degrees < angle.degrees):
                    return -1
            elif (self.degrees > angle.degrees):
                    return 1
        except ValueError:
            print("Exception Raised: invalid")
    
    '''
    Purpose: Returns a string value of the angle
    Parameters: No parameter
    Returns: A string in the form xdy.y where x is the number of degrees 
        (modulo 360, no leading zeros), "d" is a literal separator,
        and y.y is the number of minutes (modulo 60, no leading zeros), 
        rounded to one decimal point
    State change:No state change
    Exceptions: No expectations
    '''
    def getString(self):
        return '{0:0.0f}d{1:0.1f}'.format(self.degrees%360, self.minutes%60)
    
    '''
    Purpose: Returns the angle as degrees (and portions of degrees)
    Parameters: No parameter
    Returns: A floating point number representing the degrees and minutes 
    modulo 360, rounded to the nearest 1/10 minute.
    State change: No state change
    Exceptions: No exceptions are raised.
    '''
    def getDegrees(self):
        return self.degrees%360
    
    
    
    