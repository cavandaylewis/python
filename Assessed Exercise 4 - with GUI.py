# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:08:26 2017

@author: Cavan Day-Lewis
"""
from tkinter import * # importing tkinter which is the module that generates the GUI
#here I import modules used in the code
import math
import numpy as np
import matplotlib.pyplot as plt # matplotlib is used to produce the graphs
import time as timer # the timer module is used to calculate the time taken to complete the orbit

#declaration of glabal variables
G = 6.67*10**-11 #m^3 kg^-1 s^-2
massEarth =  5.972*10**24 #kg
massMoon = 7.342*10**22 #kg
earthRadius = 6371000 #m
moonRadius = 1737100 #m
earthMoonDistance = 384402000 #m # approximately 2 semi major axis of an eliptical orbit around Earth and moon.

def accelerationCalcX(x,y): 
    """
    This function calculates and returns the acceleration of the projectile in the x direction. 
    It takes in its position as the only arguments
    This function is called by rungeKuttaOrbits function
    """
    global G # the gravitational constant is initialised like this so that it can be used in this function
    global massEarth #the same goes for the mass of the Earth
    return (-G*massEarth*x)/((x**2+y**2)**(3/2)) # here from Newton's law of gravitation we return the acceleration on a projectile in the x direction

def accelerationCalcY(x,y):
    """
    This function calculates and returns the acceleration of the projectile in the y direction. 
    It takes in its position as the only arguments
    This function is called by rungeKuttaOrbits function
    """
    global G #glabel variables are initialised
    global massEarth
    return (-G*massEarth*y)/((x**2+y**2)**(3/2))# here from Newton's law of gravitation we return the acceleration on a projectile in the y direction

def rungeKuttaOrbits(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, orbitNumber = -1):
    """
    This function calculates the orbital path using runge kutta method.
    It is called for part a of the assesed task
    A while loop is used to perform the iterations, an orbit count or a duration is used as the end conditions.
    """    
    global G
    global massEarth
    
    h = deltaTime # this is the size of the time steps which is defined by the user and brought into the function.
    time = [] # creating an empty array where the values of time are stored.
    time.append(0) #setting the first value in the time array to 0s
    kPos = [[0 for x in range(4)] for y in range(2)] #here we create multi-demensional arrays, 4x2, where the values for k in the runge kutta method are stored. This array is dedicated to the k's for position.
    kV = [[0 for x in range(4)] for y in range(2)] # same as the line above but for k's used in the velocity calculations.
    velocityX = [] #creating more empty arrays, for velocity and position.
    velocityY = []
    posX = []
    posY = []
    
    velocityX.append(startingVelocityX) #appending the starting values ofr veloctiy and position.
    velocityY.append(startingVelocityY)
    posX.append(startingX)
    posY.append(startingY)    
    i = 0 #  i is the counter used in the while loop below, to keep track of the number of iterations performed.
    
    startingAngle = 180*math.atan(startingX/startingY)/math.pi #calculate starting angle
    orbitalRadius = [] #Initialise this empty array which will hold the distace from Earth
    totalEnergy = []
    angle = [] # This array will hold the anglular position of the projectile from Earth with 0 degrees pointing towards the starting position.
    orbitalRadius.append((math.sqrt(startingX**2+startingY**2)))#here we append the starting orbital radius at the starting position
    totalEnergy.append(0.5*(startingVelocityX**2+startingVelocityY**2)-G*massEarth/(orbitalRadius[0]))
    angle.append(startingAngle) #here we append the starting angle
    orbitCount = 0 # this value contians the number of orbits completed
    looped = True # this boolean values asks whether the projectile has passed the point where the angle changes from 360 to 0 degrees
    orbitLoop = -1 # this variable will contain the number of iterations in one orbit, however, its defualt is -1 to account for the fact that the projectile may never complete an orbit
    negativeSection = 0 # In order to caculate the anglular position in 360 degrees circles, then 180 degrees needs to be added on to the trigonometric equation in certian quatiles. This variable contains the correct factor.
    forceStop = False
    
    while (time[i] < duration or duration == -1) and (orbitCount <= orbitNumber-1 or orbitNumber == -1) and orbitalRadius[i] > earthRadius: # a while loop which looks at the maximum duration allowed and the number of orbits, it choses whichever comes last as its benchmark for stopping. it also stops the simulation when there is a collision with the Earth
        
        #k1s
        kPos[0][0] = velocityX[i] # this value is k1 for the x position. It is just the velocity of the rocket at its current position.
        kPos[1][0] = velocityY[i] #this value is k1 for the y position
        kV[0][0] = accelerationCalcX(posX[i], posY[i]) #this value is k1 for the x velocity. At its current position what is the acceleration of the projectile
        kV[1][0] = accelerationCalcY(posX[i], posY[i]) # this value is k1 for the y velocity
        
        #k2s
        kPos[0][1] = velocityX[i] + h*kV[0][0]/2 #what would its velocity be if it carried on at its initial acceleration (calculated in k1 for x velocity) for half a time step
        kPos[1][1] = velocityY[i] + h*kV[1][0]/2
        kV[0][1] = accelerationCalcX(posX[i] + h*kPos[0][0]/2, posY[i] + h*kPos[1][0]/2) # if it continued at the velocity in k2 for x position for half a time step what would the acceleration on the projectile be.
        kV[1][1] = accelerationCalcY(posX[i] + h*kPos[0][0]/2, posY[i] + h*kPos[1][0]/2) 
        
        #k3s
        kPos[0][2] = velocityX[i] + h*kV[0][1]/2 # if it carried on at the acceleration calculated for k2 in x velocity for half a time step, what would its velocity be
        kPos[1][2] = velocityY[i] + h*kV[1][1]/2
        kV[0][2] = accelerationCalcX(posX[i] + h*kPos[0][1]/2, posY[i] + h*kPos[1][1]/2) # if carried on at the velocity calculated in k2 for half a time step then what would its accelaration be
        kV[1][2] = accelerationCalcY(posX[i] + h*kPos[0][1]/2, posY[i] + h*kPos[1][1]/2)
        
        #k4s
        kPos[0][3] = velocityX[i] + h*kV[0][2]# if it carried on at the acceleration calcualted in k3 fro a whole timestep, then what would its velocity be 
        kPos[1][3] = velocityY[i] + h*kV[1][2]
        kV[0][3] = accelerationCalcX(posX[i] + h*kPos[0][2], posY[i] + h*kPos[1][2]) #if it continued at the velocity calculated in k3 for a whole time step, then what would its accelaration be
        kV[1][3] = accelerationCalcY(posX[i] + h*kPos[0][2], posY[i] + h*kPos[1][2]) 
        
        time.append(time[i]+h) #here the new times step is appended to the time array
        velocityX.append(velocityX[i]+(h/6)*(kV[0][0]+2*kV[0][1]+2*kV[0][2]+kV[0][3])) # the velocity in x is appended, after combining the ks for velocity in x
        velocityY.append(velocityY[i]+(h/6)*(kV[1][0]+2*kV[1][1]+2*kV[1][2]+kV[1][3])) # the velocity in y is appended, after combining the ks for velocity in y
        posX.append(posX[i]+(h/6)*(kPos[0][0]+2*kPos[0][1]+2*kPos[0][2]+kPos[0][3])) # the x position is appended, after combinging the ks for x position
        posY.append(posY[i]+(h/6)*(kPos[1][0]+2*kPos[1][1]+2*kPos[1][2]+kPos[1][3])) # the y position is appended, after combinging the ks for z position
        i +=1 # i is incremented by 1
        
        orbitalRadius.append(math.sqrt(posX[i]**2+posY[i]**2)) # using the position the orbital radius is calculated
        if orbitalRadius[i] <= earthRadius: # if the rocket collides with the Earth
            print("Collision with Earth Detected")
        totalEnergy.append(0.5*(velocityX[i]**2+velocityY[i]**2)-G*massEarth/(orbitalRadius[i])) # the total energy at each time step is calculated by summing the gravitational potential with the kinetic 
        if posY[i] < 0: #if the y coordinate is negative
            negativeSection = 1
        elif posX[i] < 0: #if the x coordinate is negative and the y coordinate is positive
            negativeSection = 2
        else: # if the y and x coordinate are positive
            negativeSection = 0
        angle.append(180*math.atan(posX[i]/posY[i])/math.pi + 180*negativeSection) # calculate the angle for the 360 degrees around Earth using the negativeSection variable to add the correct factors depending on which quartile the projectile is in
        
        if i==1: #on the first iteration of the while loop
            if angle[i]-angle[i-1] < 0 or posX[i]-posX[i-1] <0: #works out orbit direction
                direction = "anti-clockwise"
                if startingAngle == 0:
                    startingAngle = 360 # setting 0 to be 360 so that orbit counter works
            else:
                direction = "clockwise"
        if i > 1: #after the first iteration of the while loop
            if (angle[i]-angle[i-1] < 0 and direction == "clockwise") or (angle[i]-angle[i-1] > 0 and direction == "anti-clockwise"): # if it crosses over the 360 degree mark
                looped = False # this is set to false when the projectile has crossed the 360 degree angle but hasn't completed a full orbit because the starting angle is not 0 degrees
        if (angle[i]-startingAngle >= 0 and looped == False and direction == "clockwise") or (angle[i]-startingAngle <= 0 and looped == False and direction == "anti-clockwise"): # if it completes an orbit
            looped = True 
            orbitCount += 1 # adding 1 to the orbit count
            if orbitCount == 1: #when the first orbit is completed
                orbitLoop = i #the number of time steps completed in one orbit, can be used to work out the orbital period
        
    return posX, posY, orbitalRadius, angle, orbitLoop, orbitCount, direction, time, totalEnergy # returning the relevant arrays
    
    
def dynamicMoon(moonPosX, moonPosY, velocityXMoon, velocityYMoon, h):
    """
    This function calculates the position of the moon. It is called by moonPass in each iteration.
    For this section of the simulation we are not assuming the moon is stationary
    We use the Runge-Kutta method to calculate its position after each time step
    """
    kPosMoon = [[0 for x in range(4)] for y in range(2)] # initialising the 2x2 k matricies
    kVMoon = [[0 for x in range(4)] for y in range(2)]
    
    kPosMoon[0][0] = velocityXMoon # this value is k1 for the x position. It is just the velocity of the rocket at its current position.
    kPosMoon[1][0] = velocityYMoon #this value is k1 for the y position
    kVMoon[0][0] = accelerationCalcX(moonPosX, moonPosY) #this value is k1 for the x velocity. At its current position what is the acceleration of the projectile
    kVMoon[1][0] = accelerationCalcY(moonPosX, moonPosY) # this value is k1 for the y velocity
    
    #k2s
    kPosMoon[0][1] = velocityXMoon + h*kVMoon[0][0]/2 #what would its velocity be if it carried on at its initial acceleration (calculated in k1 for x velocity) for half a time step
    kPosMoon[1][1] = velocityYMoon + h*kVMoon[1][0]/2
    kVMoon[0][1] = accelerationCalcX(moonPosX + h*kPosMoon[0][0]/2, moonPosY + h*kPosMoon[1][0]/2) # if it continued at the velocity in k2 for x position for half a time step what would the acceleration on the projectile be.
    kVMoon[1][1] = accelerationCalcY(moonPosX + h*kPosMoon[0][0]/2, moonPosY + h*kPosMoon[1][0]/2)
    
    #k3s
    kPosMoon[0][2] = velocityXMoon + h*kVMoon[0][1]/2 # if it carried on at the acceleration calculated for k2 in x velocity for half a time step, what would its velocity be
    kPosMoon[1][2] = velocityYMoon + h*kVMoon[1][1]/2
    kVMoon[0][2] = accelerationCalcX(moonPosX + h*kPosMoon[0][1]/2, moonPosY + h*kPosMoon[1][1]/2) # if carried on at the velocity calculated in k2 for half a time step then what would its accelaration be
    kVMoon[1][2] = accelerationCalcY(moonPosX + h*kPosMoon[0][1]/2, moonPosY + h*kPosMoon[1][1]/2)
    
    #k4s
    kPosMoon[0][3] = velocityXMoon + h*kVMoon[0][2] # if it carried on at the acceleration calcualted in k3 fro a whole timestep, then what would its velocity be 
    kPosMoon[1][3] = velocityYMoon + h*kVMoon[1][2]
    kVMoon[0][3] = accelerationCalcX(moonPosX + h*kPosMoon[0][2], moonPosY + h*kPosMoon[1][2]) #if it continued at the velocity calculated in k3 for a whole time step, then what would its accelaration be
    kVMoon[1][3] = accelerationCalcY(moonPosX + h*kPosMoon[0][2], moonPosY + h*kPosMoon[1][2])
    
    velocityXMoon = velocityXMoon+(h/6)*(kVMoon[0][0]+2*kVMoon[0][1]+2*kVMoon[0][2]+kVMoon[0][3]) # the velocity in x is appended, after combining the ks for velocity in x
    velocityYMoon = velocityYMoon+(h/6)*(kVMoon[1][0]+2*kVMoon[1][1]+2*kVMoon[1][2]+kVMoon[1][3]) # the velocity in y is appended, after combining the ks for velocity in y
    moonPosX = moonPosX+(h/6)*(kPosMoon[0][0]+2*kPosMoon[0][1]+2*kPosMoon[0][2]+kPosMoon[0][3]) # the x position is appended, after combinging the ks for x position
    moonPosY = moonPosY+(h/6)*(kPosMoon[1][0]+2*kPosMoon[1][1]+2*kPosMoon[1][2]+kPosMoon[1][3]) # the y position is appended, after combinging the ks for y position
    
    return moonPosX, moonPosY, velocityXMoon, velocityYMoon # return the position and velocity back to moonPass
    
def moonCalcX(x,y,Mx,My, angle, velocityX, velocityY, massRocket, rocketForce):
    """
    This function calculates and returns the acceleration of the projectile in the x direction for part b. 
    It takes in the position of the projectile and the position of the moon as arguments.
    It also takes in the velocity of the projectile and its mass and the force that the rocket engines produce.
    In this simulation the rocket transfers from a low earth orbit to the moon slingshot and then back to the low earth orbit
    In order to perform the transfer the rockets must be fired.
    There are different stages of the rockets flight and there is a different acceleration for the different stages
    Whenever the rocket engines are not being fired the only force on the projectile is gravity
    This function is called by moonPass function
    """
    global G # initialising global variables
    global massEarth
    global massMoon
    global rocketStage
    xMoon = x-Mx # here we calculate the position of the projectile relative to the moon. Ie with the centre of the moon at (0,0)
    yMoon = y-My #same as line above but y coordinate
    speed = math.sqrt(velocityX**2 + velocityY**2) #here we calculate the scalar quantity speed of the projectile
    if rocketStage == 2 or rocketStage == 2.5: # if the rocket is in the acceleration stage
        rocketX = (rocketForce*velocityX)/(speed*massRocket) #calculating the acceleration on the rocket in the x direction due to the rocket engines being fired.
        return (-G*massEarth*x)/((x**2+y**2)**(3/2))+(-G*massMoon*xMoon)/((xMoon**2+yMoon**2)**(3/2))+rocketX #here we return the accelaration of the projectile
    elif rocketStage == 4 or rocketStage == 4.5 or rocketStage == 5.5: # if the rocket is in the decelaration stage
        rocketX = (rocketForce*velocityX)/(speed*massRocket) #again we calculate the acceleration of the rocket in the x direction 
        return (-G*massEarth*x)/((x**2+y**2)**(3/2))+(-G*massMoon*xMoon)/((xMoon**2+yMoon**2)**(3/2))-rocketX # here we calculate the accelaration of the projectile, the force from the rocket engines is subtracted because the rockets are acting in the opposite direction.
    else: # if the rocket is in free flight
        return (-G*massEarth*x)/((x**2+y**2)**(3/2))+(-G*massMoon*xMoon)/((xMoon**2+yMoon**2)**(3/2)) #return only the accelaration due to gravity by combining forces from moon and earth.
     
    
def moonCalcY(x,y,Mx,My, angle, velocityX, velocityY, massRocket, rocketForce):
    """
    This function calculates and returns the acceleration of the projectile in the x direction for part b. 
    It performs the same task as the function above but for the y direction this only.
    This function is called by moonPass function
    """
    global G # initialising global variables
    global massEarth
    global massMoon
    global rocketStage
    xMoon = x-Mx #here we calculate the position of the projectile relative to the moon. Ie with the centre of the moon at (0,0)
    yMoon = y-My #same as line above but y coordinate
    speed = math.sqrt(velocityX**2 + velocityY**2) #here we calculate the scalar quantity speed of the projectile
    if rocketStage == 2 or rocketStage == 2.5: # if the rocket is in the acceleration stage
        rocketY = (rocketForce*velocityY)/(speed*massRocket) #calculating the acceleration on the rocket in the y direction due to the rocket engines being fired.
        return (-G*massEarth*y)/((x**2+y**2)**(3/2))+(-G*massMoon*yMoon)/((xMoon**2+yMoon**2)**(3/2))+rocketY #here we return the accelaration of the projectile, with the rocket engine accelaration added on.
    elif rocketStage == 4 or rocketStage == 4.5 or rocketStage == 5.5: # if the rocket is in the decelaration stage
        rocketY = (rocketForce*velocityY)/(speed*massRocket) #again we calculate the acceleration of the rocket in the y direction 
        return (-G*massEarth*y)/((x**2+y**2)**(3/2))+(-G*massMoon*yMoon)/((xMoon**2+yMoon**2)**(3/2))-rocketY # here we calculate the accelaration of the projectile, the force from the rocket engines is subtracted because the rockets are acting in the opposite direction.
    else:  # if the rocket is in free flight
        return (-G*massEarth*y)/((x**2+y**2)**(3/2))+(-G*massMoon*yMoon)/((xMoon**2+yMoon**2)**(3/2))#return only the accelaration due to gravity by combining forces from moon and earth.
    
def moonPass(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, massRocket, rocketForce, rocketTransferDuration, moonStartAngle, manual = False):
    """
    In this function the velocity and position of the rocket is calculated it is called for part b of the assesed practical
    The aim of this function is to, using the runge kutta method, calcualte the position of the rocket/projectile as it makes one orbit around
    Earth and then transfers to a different path, by use of rocket engines, then flies past the moon, getting as close as possible to the moon enabling
    the rocket to take images of the moon's surface. Afterwards, the rocket engines fire agian and the rocket is put back into the same low Earth orbit
    as before.
    This function is called when the user selects part b
    """
    global rocketStage # initialising the global variables
    global massMoon
    
    moonPosX = earthMoonDistance*math.sin(math.pi*moonStartAngle/180) #m Here we have the x coordinate of the moon
    moonPosY = earthMoonDistance*math.cos(math.pi*moonStartAngle/180) #m Here the Y coordinate
    moonVelocity = math.sqrt(G*massEarth/earthMoonDistance) #the velocity of the moon as calculated by the Vis-Visa equation for a circle
    velocityXMoon = moonVelocity*math.cos(math.pi*moonStartAngle/180) # here we set the x and y velocity components of the moon's starting conditions
    velocityYMoon = -moonVelocity*math.sin(math.pi*moonStartAngle/180)
    
    h = deltaTime # this is the time step size, which can be altered by the user.
    time = [] # creating an empty array where the values of time are stored.
    time.append(0) #setting the first value in the time array to 0s
    kPos = [[0 for x in range(4)] for y in range(2)]  #here we create multi-demensional arrays, 4x2, where the values for k in the runge kutta method are stored. This array is dedicated to the k's for position.
    kV = [[0 for x in range(4)] for y in range(2)] # same as the line above but for k's used in the velocity calculations.
    velocityX = [] #creating more empty arrays, for velocity, position and speed.
    velocityY = []
    posX = []
    posY = []
    speed = []
    
    velocityX.append(startingVelocityX) #here we append the first value of the array to the starting values defined by the user.
    velocityY.append(startingVelocityY)
    posX.append(startingX)
    posY.append(startingY)
    i = 0 #  i is the counter used in the while loop below, to keep track of the number of iterations performed.
    speed.append(math.sqrt(velocityX[i]**2+velocityY[i]**2)) #here we append the starting value for the scalar value speed.
    
    moonPosXArray = [] #initialising arrays for the moon's position and velocity
    moonPosYArray = []
    velocityXMoonArray = []
    velocityYMoonArray = []    
    moonPosXArray.append(moonPosX)
    moonPosYArray.append(moonPosY)
            
    startingAngle = 180*math.atan(startingY/-startingX)/math.pi #calculate starting angle
    orbitalRadius = []  #Initialise this empty array which will hold the distace from Earth
    moonDistance = []
    totalEnergy = []
    angle = [] # This array will hold the anglular position of the projectile from Earth with 0 degrees pointing towards the starting position.
    orbitalRadius.append((math.sqrt(startingX**2+startingY**2))) #here we append the starting orbital radius at the starting position
    moonDistance.append((math.sqrt((startingX-moonPosX)**2+(startingY-moonPosY)**2)))
    angle.append(startingAngle) #here we append the starting angle
    totalEnergy.append(0.5*(startingVelocityX**2+startingVelocityY**2)-G*massEarth/(orbitalRadius[0])-G*massMoon/(moonDistance[0]))    
    orbitCount = 0 # uneeded
    looped = True # unneeded
    orbitLoop = -1 # unndeeded
    negativeSection = 0 # In order to caculate the anglular position in 360 degrees circles, then 180 degrees needs to be added on to the trigonometric equation in certian quatiles. This variable contains the correct factor.
    
    rocketStage = 1 #initialise the stage of the projectile flight to 1
    
    while rocketStage != 6 and time[i]<duration: # while the rocket has completed all of the stages of flight and the timer hasn't run out for maximum allowed flight length.
        #k1s
        kPos[0][0] = velocityX[i] # this value is k1 for the x position. It is just the velocity of the rocket at its current position.
        kPos[1][0] = velocityY[i] #this value is k1 for the y position
        kV[0][0] = moonCalcX(posX[i], posY[i], moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce) #this value is k1 for the x velocity. At its current position what is the acceleration of the projectile
        kV[1][0] = moonCalcY(posX[i], posY[i], moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce) # this value is k1 for the y velocity
        
        #k2s
        kPos[0][1] = velocityX[i] + h*kV[0][0]/2 #what would its velocity be if it carried on at its initial acceleration (calculated in k1 for x velocity) for half a time step
        kPos[1][1] = velocityY[i] + h*kV[1][0]/2
        kV[0][1] = moonCalcX(posX[i] + h*kPos[0][0]/2, posY[i] + h*kPos[1][0]/2, moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce) # if it continued at the velocity in k2 for x position for half a time step what would the acceleration on the projectile be.
        kV[1][1] = moonCalcY(posX[i] + h*kPos[0][0]/2, posY[i] + h*kPos[1][0]/2, moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce)
        
        #k3s
        kPos[0][2] = velocityX[i] + h*kV[0][1]/2 # if it carried on at the acceleration calculated for k2 in x velocity for half a time step, what would its velocity be
        kPos[1][2] = velocityY[i] + h*kV[1][1]/2
        kV[0][2] = moonCalcX(posX[i] + h*kPos[0][1]/2, posY[i] + h*kPos[1][1]/2, moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce) # if carried on at the velocity calculated in k2 for half a time step then what would its accelaration be
        kV[1][2] = moonCalcY(posX[i] + h*kPos[0][1]/2, posY[i] + h*kPos[1][1]/2, moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce)
        
        #k4s
        kPos[0][3] = velocityX[i] + h*kV[0][2] # if it carried on at the acceleration calcualted in k3 fro a whole timestep, then what would its velocity be 
        kPos[1][3] = velocityY[i] + h*kV[1][2]
        kV[0][3] = moonCalcX(posX[i] + h*kPos[0][2], posY[i] + h*kPos[1][2], moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce) #if it continued at the velocity calculated in k3 for a whole time step, then what would its accelaration be
        kV[1][3] = moonCalcY(posX[i] + h*kPos[0][2], posY[i] + h*kPos[1][2], moonPosX, moonPosY, angle[i], velocityX[i], velocityY[i], massRocket, rocketForce)
        
        time.append(time[i]+h) #here the new times step is appended to the time array
        velocityX.append(velocityX[i]+(h/6)*(kV[0][0]+2*kV[0][1]+2*kV[0][2]+kV[0][3])) # the velocity in x is appended, after combining the ks for velocity in x
        velocityY.append(velocityY[i]+(h/6)*(kV[1][0]+2*kV[1][1]+2*kV[1][2]+kV[1][3])) # the velocity in y is appended, after combining the ks for velocity in y
        posX.append(posX[i]+(h/6)*(kPos[0][0]+2*kPos[0][1]+2*kPos[0][2]+kPos[0][3])) # the x position is appended, after combinging the ks for x position
        posY.append(posY[i]+(h/6)*(kPos[1][0]+2*kPos[1][1]+2*kPos[1][2]+kPos[1][3])) # the y position is appended, after combinging the ks for y position
        speed.append(math.sqrt(velocityX[i]**2+velocityY[i]**2)) # the speed is calculated and appended, by finding the magnitude of the velocity in the x-y plane
        i +=1 # i is incremented by 1
        
        if manual == False: # if the moon is not stationary
            moonPosX, moonPosY, velocityXMoon, velocityYMoon  = dynamicMoon(moonPosX, moonPosY, velocityXMoon, velocityYMoon, h) # call the function to find the position and velocity of the moon.
            moonPosXArray.append(moonPosX) #add the values to the relevent arrays
            moonPosYArray.append(moonPosY)
            velocityXMoonArray.append(velocityXMoon)
            velocityYMoonArray.append(velocityYMoon)
            
        
        if time[i-1]+h > duration and manual == True: # if we come to the end of the simulation
            rocketStage == 6
        
        orbitalRadius.append(math.sqrt(posX[i]**2+posY[i]**2)) # the orbital radius is calculated and appended
        moonDistance.append(math.sqrt((posX[i]-moonPosX)**2+(posY[i]-moonPosY)**2)) # calculating the distance to the moon
        totalEnergy.append(0.5*(velocityX[i]**2+velocityY[i]**2)-G*massEarth/(orbitalRadius[i])-G*massMoon/(moonDistance[i])) # the total energy at each time step is calculated by summing the gravitational potential with the kinetic 
        if posX[i] > 0: # if the x coordinate of its position in positive (remember Earth is at (0,0))
            negativeSection = 1 
        elif posY[i] < 0: # if the y coordinate of its position is negative
            negativeSection = 2
        else:
            negativeSection = 0
        angle.append(180*math.atan(posY[i]/-posX[i])/math.pi + 180*negativeSection) # calculate and append the angle, adding on the correct factor of 180 to create the 360 degree circle
        
        if manual == True and orbitalRadius[i] <= earthRadius: # if a collision with Earth is detected
            rocketStage = 6 # stop the simulation
            print("Collision with Earth Detected")
        
        if manual == True and moonDistance[i] <= moonRadius: #if a collision with the moon is detected
            rocketStage = 6 # stop the simulation
            print("Collision with Moon Detected")
            
        if manual == False: # all the different stages for the automatic simulation, each different stage corresponds to the force that needs to be applied on the rocket.
            if i > 1: # if there has been more than one iteration of the while loop
                if angle[i]-angle[i-1] < 0 and rocketStage == 2: #if the angle jumps from 360 degrees to 0 which it will do on every complete circle.
                    rocketStage = 2.5 
                if angle[i]-angle[i-1] < 0 and rocketStage == 4:#if the angle jumps from 360 degrees to 0 which it will do on every complete circle.
                    rocketStage = 4.5
                if angle[i]-angle[i-1] < 0 and rocketStage == 5:#if the angle jumps from 360 degrees to 0 which it will do on every complete circle.
                    rocketStage = 5.25
                if angle[i]-angle[i-1] < 0 and rocketStage == 5.75:#if the angle jumps from 360 degrees to 0 which it will do on every complete circle.
                    rocketStage = 6
            if rocketStage == 1 and angle[i]/360 > 1-rocketTransferDuration/2: #if rocket stage equals 1 and the anle where the rockets come on has been exceeded
                rocketStage = 2
            if rocketStage == 2.5 and angle[i]/360 > rocketTransferDuration/2: #if rocket stage equals 2.5 and the anle where the rockets go off has been exceeded
                rocketStage = 3
            if rocketStage == 3 and angle[i]/360 > 0.75-rocketTransferDuration/48: #if rocket stage equals 3 and the anle where the rockets come on has been exceeded
                rocketStage = 4
            if rocketStage == 4 and angle[i]/360 > 0.75+rocketTransferDuration/48: #if rocket stage equals 4.5 and the anle where the rockets go off has been exceeded
                rocketStage = 5
            if rocketStage == 5.25 and angle[i]/360 > 0.25-rocketTransferDuration/3.4:
                rocketStage = 5.5
            if rocketStage == 5.5 and angle[i]/360 > 0.25+rocketTransferDuration/3.4:
                rocketStage = 5.75

    return posX, posY, speed, time, totalEnergy, moonPosXArray, moonPosYArray, velocityXMoonArray, velocityYMoonArray
    
class Window(Frame): #create a class that contains the functions used by tkinter for the GUI window

    def __init__(self, master=None): # this initial function declares the nature of the frame
        Frame.__init__(self, master)
        self.master = master # in our case we always have master = none
        self.init_window() #calls init_window function
        
    #creation of init window
    def init_window(self):
        self.master.title("Orbit Simulator") #set the name for the window
        self.pack(fill=BOTH, expand=1, padx = 5) #allowing the widget to take the full space of the root window
        
        titleFrame = Frame(self, relief=FLAT, borderwidth=10) # creating the different sections
        selectionFrame1 = Frame(self, relief=GROOVE, borderwidth=3)
        selectionFrame2 = Frame(self, relief=GROOVE, borderwidth=3)
        selectionFrame3 = Frame(self, relief=FLAT, borderwidth=3)
        outputFrame = Frame(self, relief=FLAT, borderwidth=3)
        quitFrame = Frame(self, relief=FLAT, borderwidth=3)
        
        titleFrame.grid(row = 0) #positioning the different sections
        selectionFrame1.grid(row = 1, sticky = W+E)
        selectionFrame2.grid(row = 2)
        selectionFrame3.grid(row = 3)
        outputFrame.grid(row = 4)
        quitFrame.place(x = 550, y = 460) #manually selecting the x and y position
        
        quitButton = Button(quitFrame, text="Quit", command = self.quitApplication).grid(sticky = E+S) #creating a button instance with a command to close the GUI, it calls the function quitApplication
        
        self.inputErrorText = StringVar()# initialising text for labels as empty strings # these need to be attached to self so that they can be accessed by all functions which are a part of the window.
        self.outputText = StringVar()
        self.textInput2Variable = StringVar()
        self.textInput3Variable = StringVar()
        self.textInput5Variable = StringVar()
        self.textInput6Variable = StringVar()
        self.textInput8Variable = StringVar()
        self.textInput9Variable = StringVar()
        self.textInput12Variable = StringVar()
        self.textInput14Variable = StringVar()
        self.textInput15Variable = StringVar()
        
        self.outputText.set("")
        self.inputErrorText.set("")
        
        self.title = Label(titleFrame, text="Orbit Simulator", font = ("TkDefaultFont 22 underline"), width = 33) #creating a large title for the GUI
        self.title.grid(sticky = E+W) # position the title
        
        def coordinateSelect(): #if the user selects the radiobutton which choose the coordinate type
            if self.coordinate.get() == 0: # if the user selects polar coordinates
                self.textLabel2.config(state = "normal") #activating certain widgets
                self.textInput2.config(state = "normal")
                self.textLabel3.config(state = "normal")
                self.textInput3.config(state = "normal")
                self.textLabel5.config(state = "disabled") #deactivating certain widgets
                self.textInput5.config(state = "disabled")
                self.textLabel6.config(state = "disabled")
                self.textInput6.config(state = "disabled")
            else: #if the user selects cartesian coordinates
                self.textLabel2.config(state = "disabled")
                self.textInput2.config(state = "disabled")
                self.textLabel3.config(state = "disabled")
                self.textInput3.config(state = "disabled")
                self.textLabel5.config(state = "normal")
                self.textInput5.config(state = "normal")
                self.textLabel6.config(state = "normal")
                self.textInput6.config(state = "normal")
        def circularSelect(): #if the user selects a radiobutton which chooses the type of orbit
            if self.circular.get() == 0: #if the user wants to manually choose their velocities
                self.textLabel8.config(state = "normal")
                self.textInput8.config(state = "normal")
                self.textLabel9.config(state = "normal")
                self.textInput9.config(state = "normal")
            else: # if the user wants a circualr orbit
                self.textLabel8.config(state = "disabled")
                self.textInput8.config(state = "disabled")
                self.textLabel9.config(state = "disabled")
                self.textInput9.config(state = "disabled")
        def durationTypeSelect(): #when the user selects a radiobutton corresponding to when the simulation should end
            if self.durationType.get() == 0: # if the user wants a certain number of revolutions
                self.textInput12.config(state = "normal")
                self.textInput14.config(state = "disabled")
            else: # if the user wants the sim to end after a certain time.
                self.textInput12.config(state = "disabled")
                self.textInput14.config(state = "normal")
                
        self.coordinate = IntVar()
        self.coordinate.set(2) #have the coordiate initially set at 2 i.e. neither of them
        
        self.textLabel1 = Label(selectionFrame1, text="Polar Coordinates: ")  # create a text label
        self.tickBox1 = Radiobutton(selectionFrame1, variable=self.coordinate, value = 0, command = coordinateSelect) #create a radiobutton
        self.textLabel1.grid(row=1, column = 0, sticky = E) #position the text label
        self.tickBox1.grid(row=1, column = 1, sticky = E) # position the radiobutton
        
        self.textLabel4 = Label(selectionFrame1, text="Cartesian Coordinates: ") 
        self.tickBox4 = Radiobutton(selectionFrame1, variable=self.coordinate, value = 1, command = coordinateSelect)
        self.textLabel4.grid(row=2, column = 0, sticky = E)
        self.tickBox4.grid(row=2, column = 1, sticky = E)
        
        self.textLabel2 = Label(selectionFrame1, text="Altitude (km): ") # creates a label attaches itself to self. the text label is a child of the window \n adds in a new line
        self.textInput2 = Entry(selectionFrame1, width=7, textvariable = self.textInput2Variable) # creates a text input field which has space for 7 characters
        self.textLabel2.grid(row=1, column = 2, sticky = E) #placing the text label on the window at the specified x and y pixel coordinates
        self.textInput2.grid(row=1, column = 3, sticky = E)
        
        self.textLabel3 = Label(selectionFrame1, text="Angle (°): ") 
        self.textInput3 = Entry(selectionFrame1, width=7, textvariable = self.textInput3Variable)
        self.textLabel3.grid(row=1, column = 4, sticky = E) 
        self.textInput3.grid(row=1, column = 5, sticky = E)
        
        self.textLabel5 = Label(selectionFrame1, text="Starting X-Coordinate (m): ") 
        self.textInput5 = Entry(selectionFrame1, width=7, textvariable = self.textInput5Variable)
        self.textLabel5.grid(row=2, column = 2, sticky = E) 
        self.textInput5.grid(row=2, column = 3, sticky = E) 
        
        self.textLabel6 = Label(selectionFrame1, text="Starting Y-Coordinate (m): ") 
        self.textInput6 = Entry(selectionFrame1, width=7, textvariable = self.textInput6Variable)
        self.textLabel6.grid(row=2, column = 4, sticky = E) 
        self.textInput6.grid(row=2, column = 5, sticky = E)
        
        self.circular = IntVar()
        self.circular.set(2)
        
        self.textLabel7 = Label(selectionFrame1, text="Manually Enter Velocity: ") 
        self.tickBox7 = Radiobutton(selectionFrame1, variable=self.circular, value = 0, command = circularSelect)
        self.textLabel7.grid(row=3, column = 0, sticky = E) 
        self.tickBox7.grid(row=3, column = 1, sticky = E)
        
        self.textLabel10 = Label(selectionFrame1, text="Circualr Orbit: ") 
        self.tickBox10 = Radiobutton(selectionFrame1, variable=self.circular, value = 1, command = circularSelect)
        self.textLabel10.grid(row=4, column = 0, sticky = E) 
        self.tickBox10.grid(row=4, column = 1, sticky = E)

        self.textLabel8 = Label(selectionFrame1, text="Starting X-Velocity (m/s): ") 
        self.textInput8 = Entry(selectionFrame1, width=7, textvariable = self.textInput8Variable)
        self.textLabel8.grid(row=3, column = 2, sticky = E) 
        self.textInput8.grid(row=3, column = 3, sticky = E)

        self.textLabel9 = Label(selectionFrame1, text="Starting Y-Velocity (m/s): ") 
        self.textInput9 = Entry(selectionFrame1, width=7, textvariable = self.textInput9Variable)
        self.textLabel9.grid(row=3, column = 4, sticky = E) 
        self.textInput9.grid(row=3, column = 5, sticky = E)    
        
        self.durationType = IntVar()
        self.durationType.set(2)
        
        self.textLabel11 = Label(selectionFrame1, text="Orbit Number: ") 
        self.tickBox11 = Radiobutton(selectionFrame1, variable=self.durationType, value = 0, command = durationTypeSelect)
        self.textLabel11.grid(row=5, column = 0, sticky = E)
        self.tickBox11.grid(row=5, column = 1, sticky = E)
        
        self.textLabel13 = Label(selectionFrame1, text="Duration: ")
        self.tickBox13 = Radiobutton(selectionFrame1, variable=self.durationType, value = 1, command = durationTypeSelect)
        self.textLabel13.grid(row=6, column = 0, sticky = E)
        self.tickBox13.grid(row=6, column = 1, sticky = E)
        
        self.textInput12 = Entry(selectionFrame1, width=7, textvariable = self.textInput12Variable)
        self.textInput12.grid(row=5, column = 2, sticky = W)
        
        self.textInput14 = Entry(selectionFrame1, width=7, textvariable = self.textInput14Variable)
        self.textInput14.grid(row=6, column = 2, sticky = W)
        
        self.textLabel15 = Label(selectionFrame1, text="Delta Time (s): ")
        self.textInput15 = Entry(selectionFrame1, width=7, textvariable = self.textInput15Variable)
        self.textLabel15.grid(row=7, column = 0, sticky = E)
        self.textInput15.grid(row=7, column = 1, sticky = E)
        
        self.textLabel16 = Label(selectionFrame1, text="Force: 160400 N")
        self.textLabel16.grid(row=8, column = 0, sticky = E)
        
        self.textLabel17 = Label(selectionFrame1, text="Delta Time: 50 s")
        self.textLabel17.grid(row=9, column = 0, sticky = E)
        
        self.inputError = Label(selectionFrame1, textvariable=self.inputErrorText, fg="red")
        self.inputError.grid(row = 8, columnspan = 5)
        
        def sectionSelect():
            """
            This function runs when the user clicks on one of the radio buttons to select a part of the excersise. 
            It works out which radio button they selected and disables/fills in the correct widgets
            """
            self.MyInput = self.buttonValue.get() # gets the value of the radiobutton that the user selected.
            if self.MyInput == 1: # if it was the first radio button, prepare for part a
            
                self.textLabel1.grid(row=1, column = 0, sticky = E)  # add and position the relevant widgets for this section of the simulation
                self.tickBox1.grid(row=1, column = 1, sticky = E)
                self.textLabel4.grid(row=2, column = 0, sticky = E)
                self.tickBox4.grid(row=2, column = 1, sticky = E)
                self.textLabel2.grid(row=1, column = 2, sticky = E)
                self.textInput2.grid(row=1, column = 3, sticky = E)
                self.textLabel3.grid(row=1, column = 4, sticky = E) 
                self.textInput3.grid(row=1, column = 5, sticky = E)
                self.textLabel5.grid(row=2, column = 2, sticky = E) 
                self.textInput5.grid(row=2, column = 3, sticky = E) 
                self.textLabel6.grid(row=2, column = 4, sticky = E) 
                self.textInput6.grid(row=2, column = 5, sticky = E)
                self.textLabel7.grid(row=3, column = 0, sticky = E) 
                self.tickBox7.grid(row=3, column = 1, sticky = E)
                self.textLabel10.grid(row=4, column = 0, sticky = E) 
                self.tickBox10.grid(row=4, column = 1, sticky = E)
                self.textLabel8.grid(row=3, column = 2, sticky = E) 
                self.textInput8.grid(row=3, column = 3, sticky = E)
                self.textLabel9.grid(row=3, column = 4, sticky = E) 
                self.textInput9.grid(row=3, column = 5, sticky = E) 
                self.textLabel11.grid(row=5, column = 0, sticky = E) 
                self.tickBox11.grid(row=5, column = 1, sticky = E)
                self.textLabel13.grid(row=6, column = 0, sticky = E) 
                self.tickBox13.grid(row=6, column = 1, sticky = E)
                self.textInput12.grid(row=5, column = 2, sticky = W)
                self.textInput14.grid(row=6, column = 2, sticky = W)
                self.textLabel15.grid(row=7, column = 0, sticky = E)
                self.textInput15.grid(row=7, column = 1, sticky = E)
                
                self.textLabel16.grid_forget() #remove these widgets
                self.textLabel17.grid_forget()
                
                self.inputErrorText.set("") #set these text labels to empty
                self.outputText.set("")
                
                #here we add in suggested starting conditions for this section, the user is free to change them.
                self.tickBox1.select() #select polar coordinates radiobutton
                self.coordinate.set(0)
                coordinateSelect()
                self.textInput2Variable.set("400")
                self.textInput3Variable.set("0")
                self.tickBox10.select()
                self.circular.set(1)
                circularSelect()
                self.tickBox11.select()
                self.durationType.set(0)
                durationTypeSelect()
                self.textInput12Variable.set("3")
                self.textInput15Variable.set("1")
                
            elif self.MyInput == 2: # if it is the second radio button then prepare for part b
                selectionFrame1.grid_rowconfigure(1, weight = 1) # here we readjust the rows and columns so that we can centre the widgets
                selectionFrame1.grid_rowconfigure(2, weight = 1)
                selectionFrame1.grid_rowconfigure(3, weight = 1)
                selectionFrame1.grid_columnconfigure(0, weight = 1)
                selectionFrame1.grid_columnconfigure(1, weight = 1)
                
                self.textLabel16.grid(row=1, column = 0, sticky = E) # add these widgets
                self.textLabel17.grid(row=2, column = 0, sticky = E)
                self.textLabel15.grid(row=3, column = 0, sticky = E)
                self.textInput15.grid(row=3, column = 1, sticky = W)
                
                self.textInput14.grid_forget() # remove these widgets
                self.textInput12.grid_forget()
                self.tickBox13.grid_forget()
                self.textLabel13.grid_forget()
                self.tickBox11.grid_forget()
                self.textLabel11.grid_forget()
                self.textInput9.grid_forget()
                self.textLabel9.grid_forget()
                self.textInput8.grid_forget()
                self.textLabel8.grid_forget()
                self.tickBox10.grid_forget()
                self.textLabel10.grid_forget()
                self.tickBox7.grid_forget()
                self.textLabel7.grid_forget()
                self.textInput6.grid_forget()
                self.textLabel6.grid_forget()
                self.textInput5.grid_forget()
                self.textLabel5.grid_forget()
                self.textInput3.grid_forget()
                self.textLabel3.grid_forget()
                self.textInput2.grid_forget()
                self.textLabel2.grid_forget()
                self.tickBox4.grid_forget()
                self.textLabel4.grid_forget()
                self.tickBox1.grid_forget()
                self.textLabel1.grid_forget()
                self.textLabel15.grid_forget()
                self.textInput15.grid_forget()
                
                self.inputErrorText.set("")
                self.outputText.set("")
                    
            elif self.MyInput == 3: # if part b - manual is selected 
                self.textLabel1.grid(row=1, column = 0, sticky = E)  #add these widgets
                self.tickBox1.grid(row=1, column = 1, sticky = E)
                self.textLabel4.grid(row=2, column = 0, sticky = E)
                self.tickBox4.grid(row=2, column = 1, sticky = E)
                self.textLabel2.grid(row=1, column = 2, sticky = E)
                self.textInput2.grid(row=1, column = 3, sticky = E)
                self.textLabel3.grid(row=1, column = 4, sticky = E) 
                self.textInput3.grid(row=1, column = 5, sticky = E)
                self.textLabel5.grid(row=2, column = 2, sticky = E) 
                self.textInput5.grid(row=2, column = 3, sticky = E) 
                self.textLabel6.grid(row=2, column = 4, sticky = E) 
                self.textInput6.grid(row=2, column = 5, sticky = E)
                self.textLabel8.grid(row=3, column = 0, sticky = E) 
                self.textInput8.grid(row=3, column = 1, sticky = E)
                self.textLabel9.grid(row=3, column = 2, sticky = E) 
                self.textInput9.grid(row=3, column = 3, sticky = E) 
                self.textLabel13.grid(row=4, column = 0, sticky = E) 
                self.textInput14.grid(row=4, column = 1, sticky = W)
                self.textLabel15.grid(row=5, column = 0, sticky = E)
                self.textInput15.grid(row=5, column = 1, sticky = E)
                
                self.textLabel16.grid_forget() #remove these widgets
                self.textLabel17.grid_forget()
                self.textLabel7.grid_forget()
                self.tickBox7.grid_forget()
                self.textLabel10.grid_forget()
                self.tickBox10.grid_forget()
                self.textLabel11.grid_forget()
                self.tickBox11.grid_forget()
                self.textInput12.grid_forget()
                self.tickBox13.grid_forget()
                
                self.inputErrorText.set("")
                self.outputText.set("")
                
                self.tickBox1.select() #add these suggested starting conditions
                self.coordinate.set(0)
                coordinateSelect()
                self.textInput2Variable.set("7000")
                self.textInput3Variable.set("270")
                self.circular.set(0)
                circularSelect()
                self.textInput8Variable.set("0")
                self.textInput9Variable.set("7569.7")
                self.durationType.set(1)
                durationTypeSelect()
                self.textInput14Variable.set("941760")
                self.textInput15Variable.set("1")
                self.textInput15Variable.set("50")
            
            
        self.button = Button(selectionFrame3, text="Calculate", command = self.calculate) #creating a button instance with a command to call the submit1 function, which is a part of the window class (self) ie self.submit1
        self.button.grid(row=0, sticky = W+E)
        self.output = Label(outputFrame, textvariable=self.outputText) #create a label for the output text after the simulation has run to go
        self.output.grid(row=0, columnspan = 2)
        
        options = [("(a)", 1), ("(b)", 2), ("(b) - Manual", 3),] #an array containing the different options for the radio button
        self.buttonValue = IntVar() # initialising buttonValue as an integer variable
        i = 0
        rb = [0]*len(options) # there are three different radiobuttons, each one will go in the array rb, which is being initialised here.
        for text, value in options: # loop over the entries in options, taking out the text and the values.
            rb[i] = Radiobutton(selectionFrame2, text=text, variable=self.buttonValue, value=value, command = sectionSelect).grid(row=0, column = i) #create the radio buttons, pack is a way of adding the radio button widgets to the GUI, we place them at the top left
            i+=1
            
        self.buttonValue.set(1) # select part a
        sectionSelect()
    
    def calculate(self):
        """
        This function is excecuted when calculate is clicked, firstly it performs an input validation
        to make sure the user hasn't entered anything in incorrectly.
        Then it runs the simulations and displays the results.
        """
        self.MyInput = self.buttonValue.get()
        self.inputErrorText.set("")
        if self.MyInput == 1: # if the part b radio button was selected, run part a
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            if self.coordinate.get() == 0: # if the user has selected to use polar coordinates
                try:  # a try-catch loop is the best way to perform this validation routine.
                    altitude = self.textInput2.get() # collect the text from the first text field on the screen
                    altitude = float(altitude)*10**3 # try and convert this text to a float and convert from km to m
                    if altitude <= 0: # if it is less than or equal to 0
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for altitude")# the error message lets the user know what they did wrong
                        errorOn = True
                except: # if there was any error in the code above then this will run
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for altitude") # This lets the user know they didn't enter a float
                    errorOn = True
                    
                try:  
                    angle = self.textInput3.get() 
                    angle = float(angle) 
                    if angle < 0 or angle > 360: 
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value between 0 and 360 for angle")
                        errorOn = True
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for angle")
                    errorOn = True
                    
                startingX = (altitude+earthRadius)*math.sin(angle*math.pi/180) #convert the polar coordinates into cartesian
                startingY = (altitude+earthRadius)*math.cos(angle*math.pi/180)
                
            elif self.coordinate.get() == 1: # if the user selects cartesian coordinates
                try:
                    startingX = self.textInput5.get() 
                    startingX = float(startingX)
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting X position")
                    errorOn = True
                    
                try:  
                    startingY = self.textInput6.get() 
                    startingY = float(startingY) 
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting Y position") 
                    errorOn = True
            else:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Please select coordinate type ")
                errorOn = True
                
            if math.sqrt(startingX**2+startingY**2) <= earthRadius:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"The position you have selected is within the Earth's Atmosphere")
                errorOn = True
                
            if self.circular.get() == 0:
                try:  
                    startingVelocityX = self.textInput8.get() 
                    startingVelocityX = float(startingVelocityX) 
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting X velocity") 
                    errorOn = True
                    
                try:  
                    startingVelocityY = self.textInput9.get() 
                    startingVelocityY = float(startingVelocityY) 
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting Y velocity") 
                    errorOn = True
            elif self.circular.get() == 1: # if the user wants the orbit to be circular use a simplified version of the vis-visa equation to calcualte the x and y components of velocity.
                radius = math.sqrt(startingX**2+startingY**2)
                velocity = math.sqrt(G*massEarth/radius)
                startingVelocityX = velocity*startingY/(math.sqrt(startingX**2+startingY**2))
                startingVelocityY = -velocity*startingX/(math.sqrt(startingX**2+startingY**2))
                
            else:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Please select orbit type ")
                errorOn = True
                
                
            if self.durationType.get() == 0: # if the user wants to use the orbit number as the selector
                try:  
                    orbitNumber = self.textInput12.get() 
                    orbitNumber = int(orbitNumber) 
                    duration = -1 #means that duration will not be considered.
                    if orbitNumber <= 0: 
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Orbit Number")
                        errorOn = True
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter an integer for Orbit Number") 
                    errorOn = True
            elif self.durationType.get() == 1: #means that the user wants time to be the selector
                try:  
                    duration = self.textInput14.get() 
                    duration = float(duration) 
                    orbitNumber = -1 #means that orbit number is irrelevant
                    if duration <= 0: 
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Duration")
                        errorOn = True
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter an float for Duration") 
                    errorOn = True
            else:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Please select duration type ")
                errorOn = True
                
            try:  
                deltaTime = self.textInput15.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Delta Time")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter an float for Delta Time") 
                errorOn = True
                            
            if errorOn == False:
                """
                Within this if statement, the program calls the orbit function and and provides starting conditions.
                Then creates a graph of the orbit and a graph showing how the orbital radius varies with time.
                It also calculates the eccentricity of the orbit, the direction of the orbit and how many orbits were completed.
                """
                
                print("running the show part (a)")
                
                ####### ADD THIS CODE TO GEREATE GRPAH ON ENERGY DEVIATION AGAINST COMPUTER TIME ######                
#                energyDeviation = []
#                computingTime = []
#                deltaTimeArray = [0.1,0.25,0.5,0.75,1,1.5,2,3,4,5,10,20,50,100,150,200,250,400,500]
#                
#                for deltaTime in deltaTimeArray:
#                    startTime = timer.time()
#                    posX, posY, orbitalRadius, angle, orbitLoop, orbitCount, direction, time, totalEnergy = rungeKuttaOrbits(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, orbitNumber)
#                    endTime = timer.time() # the timer is ended
#                    computingTime.append(endTime-startTime) #the computing time is calculated
#                    energyDeviation.append(numpy.std(totalEnergy))
#                    print(deltaTime, numpy.std(totalEnergy), endTime-startTime)
#                plt.loglog(computingTime, energyDeviation)
#                plt.xlabel("Computing Time (s)")
#                plt.ylabel("Energy Deviation (J)")
#                plt.show()
                
                #######
                
                startTime = timer.time() # here we start the timer that will measure how long the computation will take
                posX, posY, orbitalRadius, angle, orbitLoop, orbitCount, direction, time, totalEnergy = rungeKuttaOrbits(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, orbitNumber) #here we call the runge kutta orbit calculation
                endTime = timer.time() # the timer is ended
                computingTime = endTime-startTime #the computing time is calculated
                print("Computing Time: "+str(computingTime)+"(s)") #and subsequently printed
                self.outputText.set("Computing Time: "+str("%.2g" % computingTime)+"s") #and then added to the GUI
                a = max(orbitalRadius[0:orbitLoop])/2 # semi-major axis of the orbit
                b = min(orbitalRadius[0:orbitLoop])/2 # semi-minor axis of the orbit
                
                e = math.sqrt(1-b**2/a**2) # the eccentricity of the orbit
                print("Eccentricity: ", e) # eccentricity is printed
                print("Orbit Duration:", str(orbitLoop*deltaTime)+"s") # the duration of the orbit flight in seconds
                
                if direction == "clockwise": # if the projectile move clockwise around Earth
                    orbitCompletion = "Orbit Number: "+str("%.5f" % (orbitCount+angle[len(posX)-1]/360)) # here the number of orbits, including a fraction of a complete orbit before the simulation ended
                else: # if the projectile moves anti-clockwise around Earth
                    orbitCompletion = "Orbit Number: "+str("%.5f" % (orbitCount+(1-angle[len(posX)-1]/360))) # the same value as two lines above is printed with the fact that they travel in a different direction taken into account.                
                self.outputText.set(self.outputText.get()+"\nEccentricity: "+str("%.2g" % e)) #Adding details of the plot to the GUI
                self.outputText.set(self.outputText.get()+"\n Orbit Duration:"+str("%.2f" % (orbitLoop*deltaTime))+"s")
                self.outputText.set(self.outputText.get()+"\n"+orbitCompletion)
                
                circle= plt.Circle((0, 0), 6371000, color='g', fill = False) # create an Earth sized circle to place on the groph
                fig, ax = plt.subplots() # Here we create the figure and axis of a graph
                ax.add_artist(circle) # we add the circle to the graph
                ax.plot(posX, posY) # then we plot the path the projectile took
                plt.xlabel("X (m)") #here we set the axis labels
                xLlim, xHlim = ax.get_xlim() # getting the upper and lower limits automatically assigned by matplotlib
                ax.xaxis.set_ticks(np.arange(xLlim, xHlim+1, xHlim/2)) #setting the x-ticks manually, so that the numbers don't overlap
                plt.ylabel("Y (m)")
                plt.show() #plotting the graph to the console
                
                plt.plot(time, orbitalRadius) # here we plot how the orbital radius changes with time
                plt.xlabel("Time (s)")
                plt.ylabel("Radius (m)")
                plt.show()
                
                plt.plot(time, totalEnergy) # here we plot the total energy against time
                plt.xlabel("Time (s)")
                plt.ylabel("Total Energy (J)")
                plt.show()            

        elif self.MyInput == 2: # if the part b radio button was selected, run part b
            """
            Within this if statement, the program transfers a rocket after one low earth orbit to a by pass of the moon 
            and then back into a low earth orbit. The low Earth orbit is 7000km altitude.
            It performs the transfers by changing the velocity, ie a one kick of the rocket boosters.
            It goes back into the same orbit by perfroming an identical rocket boost aftwards, however, this only works if the 
            by pass of the moon is symetrical.
            """
            
            print("running the show part (b)")
            
            radius = 7000000+earthRadius #m #the starting value for radius of the low earth orbit
            
            velocity = math.sqrt(G*massEarth/radius) # vis-visa equation for circular orbit used to calculate velocity for low Earth orbit
            
            startAngle = 270 #degrees
            boostAngle = 0 # the angle of the directional vector of the starting velocity
            #moonPassSpeed = 6000#7569.7 #m/s # the speed required to slingshot the moon.
            
            massRocket = 30000 # kg #This mass is approximately the launch mass of Apollo 13.
            rocketForce = 160400 # Newtons #largest ever engine is 7 million Newtons # this is the force required to transfer the rocket to the by-pass orbit
            rocketTransferDuration = 0.03 #corresponds to angle as fraction of 360 degrees in which rockets are fired. The transfer period is centred at 270 degrees
            
            moonStartAngle = 28.5 #degrees
            
            startingVelocityX = velocity*math.sin(boostAngle*math.pi/180) #m/s # here we turn the speed and direction of the starting velocity into a vector in x,y
            startingVelocityY = velocity*math.cos(boostAngle*math.pi/180) #m/s#m/s
            
            startingX = radius*math.sin(startAngle*math.pi/180) #here we turn the position vector, originally given in polar coordinates to cartesian coordinates.
            startingY = radius*math.cos(startAngle*math.pi/180) #as before the centre of Earth is at the origin
            
            deltaTime = 50 # secs #this is the value of the time step used in the runge-kutta method.
            duration = 14*60*60*24 #secs # why did appolo only take 5 days?
            
            startTime = timer.time() #starts the timer used to calculate the computing time
            posX, posY, speed, time, totalEnergy, moonPosX, moonPosY, velocityXMoon, velocityYMoon = moonPass(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, massRocket, rocketForce, rocketTransferDuration, moonStartAngle)
            endTime = timer.time() #ends the timer
            computingTime = endTime-startTime #subtracts the two from each other to give the computing time
            print("Duration: "+str(computingTime)) # prints the computing time
            self.outputText.set("Duration: "+str("%.3g" % computingTime)+"s")
            moonDistance = [0]*len(posX) #initialises the array that contains the distance of the rocket to the moon at each time step, fills it with 0s and makes it the correct length
            earthDistance = [0]*len(posX) # initialises the array that contains the distance of the rocket to the Earth
            
            for i in range(len(posX)): #loop over all the time steps
                moonDistance[i] = math.sqrt((posX[i]-moonPosX[i])**2+((posY[i])-moonPosY[i])**2)-moonRadius #use posX and posY to calcualte the distance of the Rocket to the moon's surface
                earthDistance[i] = math.sqrt((posX[i])**2+(posY[i])**2)-earthRadius # same method used to calcualted the distance to the Earths surface.
                
            closeApproachMoon = min(moonDistance) # this is the closest the rocket get to the moon's surface
            closeApproachEarth = min(earthDistance) # this is the closest the rocket gets to Earth's surface
            print("Closest moon approach: ", closeApproachMoon) #prints the closest moon approach
            print("Flight Duration: "+str(len(posX)*deltaTime)+"s") #prints the flight duration in s
            print("Flight Duration: "+str(len(posX)*deltaTime/(60*60*24))+" days") #prints the flight duration in days
            self.outputText.set(self.outputText.get()+"\nClosest moon approach: "+str("%.2f" % closeApproachMoon)+"m")
            self.outputText.set(self.outputText.get()+"\nFlight Duration: "+str("%.4g" % (len(posX)*deltaTime))+"s")
            self.outputText.set(self.outputText.get()+"\nFlight Duration: "+str("%.3f" % (len(posX)*deltaTime/(60*60*24)))+" days")
            
            circleEarth= plt.Circle((0, 0), 6371000, color='g', fill = False) #creates a circle for the graph of Earths size
            circleMoon = plt.Circle((moonPosX[moonDistance.index(min(moonDistance))],moonPosY[moonDistance.index(min(moonDistance))]), 1737100, color = "r", fill = False) #creates a circle for the graph of the moon and puts it in the correct position.
            fig, ax = plt.subplots() #create the axis for the plot
            ax.add_artist(circleEarth) # add the circles to the axis
            ax.add_artist(circleMoon)
            ax.plot(posX,posY) # plot the path the rocket travels
            ax.plot(moonPosX, moonPosY)
            ax.set_xlim([-50000000,450000000]) #set the x axis limits
            ax.set_ylim([-400000000,400000000]) #set the y axis limits
            plt.xlabel("X (m)")
            plt.ylabel("Y (m)")
            plt.show()          
            
            circleEarth= plt.Circle((0, 0), 6371000, color='g', fill = False) #creates a circle for the graph of Earths size
            circleMoon = plt.Circle((moonPosX[moonDistance.index(min(moonDistance))],moonPosY[moonDistance.index(min(moonDistance))]), 1737100, color = "r", fill = False) #creates a circle for the graph of the moon and puts it in the correct position.
            fig, ax = plt.subplots() #create the axis for the plot
            ax.add_artist(circleEarth) # add the circles to the axis
            ax.add_artist(circleMoon)
            ax.plot(posX,posY) # plot the path the rocket travels
            ax.plot(moonPosX, moonPosY)
            ax.set_xlim([340000000,400000000]) #set the x axis limits
            ax.set_ylim([20000000,80000000]) #set the y axis limits
            plt.xlabel("X (m)")
            plt.ylabel("Y (m)")
            plt.show()
            
            plt.plot(time, moonDistance) #plot the distance from the moon against timestep
            plt.xlabel("Time (s)")
            plt.ylabel("Distance (m)")
            plt.show()
            
            plt.plot(time, totalEnergy) #plot the total energy against time
            plt.xlabel("Time (s)")
            plt.ylabel("Energy (J)")
            plt.show()
                
        elif self.MyInput == 3: #This section is the manual part of b
            errorOn = False
            
            if self.coordinate.get() == 0: # if the first radio button is selected.
                try:  # a try-catch loop is the best way to perform this validation routine.
                    altitude = self.textInput2.get() # collect the text from the first text field on the screen
                    altitude = float(altitude)*10**3 # try and convert this text to a float and convert from km to m
                    if altitude <= 0: # if it is less than or equal to 0
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for altitude")# the error message lets the user know what they did wrong
                        errorOn = True
                except: # if there was any error in the code above then this will run
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for altitude") # This lets the user know they didn't enter a float
                    errorOn = True
                    
                try:
                    angle = self.textInput3.get() 
                    angle = float(angle) 
                    if angle < 0 or angle > 360: 
                        self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value between 0 and 360 for angle")
                        errorOn = True
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for angle")
                    errorOn = True
                    
                startingX = (altitude+earthRadius)*math.sin(angle*math.pi/180)
                startingY = (altitude+earthRadius)*math.cos(angle*math.pi/180)
                
            elif self.coordinate.get() == 1:
                try:
                    startingX = self.textInput5.get() 
                    startingX = float(startingX)
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting X position")
                    errorOn = True
                    
                try:  
                    startingY = self.textInput6.get() 
                    startingY = float(startingY) 
                except: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting Y position") 
                    errorOn = True
            else:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Please select coordinate type ")
                errorOn = True
                
            if math.sqrt(startingX**2+startingY**2) <= earthRadius:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"The position you have selected is within the Earth's Atmosphere")
                errorOn = True
                
            try:  
                startingVelocityX = self.textInput8.get() 
                startingVelocityX = float(startingVelocityX) 
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting X velocity") 
                errorOn = True
                
            try:  
                startingVelocityY = self.textInput9.get() 
                startingVelocityY = float(startingVelocityY) 
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Starting Y velocity") 
                errorOn = True
       
            try:  
                duration = self.textInput14.get() 
                duration = float(duration) 
                orbitNumber = -1
                if duration <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Duration")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter an float for Duration") 
                errorOn = True
                
            try:  
                deltaTime = self.textInput15.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Delta Time")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter an float for Delta Time") 
                errorOn = True
                
            if errorOn == False:
                """ 
                Within this statement the user has selected their conditions for a moon flight simulation
                The function calls moonPass which performs the simulation.
                """
                
                print("running the show part (b) - Manual")
                
                massRocket = 0
                rocketForce = 0
                rocketTransferDuration = 0
                moonStartAngle = 90
                
                startTime = timer.time() #starts the timer used to calculate the computing time
                posX, posY, speed, time, totalEnergy, moonPosX, moonPosY, velocityXMoon, velocityYMoon = moonPass(deltaTime, duration, startingX, startingY, startingVelocityX, startingVelocityY, massRocket, rocketForce, rocketTransferDuration, moonStartAngle, manual = True)
                endTime = timer.time() #ends the timer
                computingTime = endTime-startTime #subtracts the two from each other to give the computing time
                print("Duration: "+str(computingTime)) # prints the computing time
                self.outputText.set("Duration: "+str("%.3g" % computingTime)+"s")
                
                moonDistance = [0]*len(posX) #initialises the array that contains the distance of the rocket to the moon at each time step, fills it with 0s and makes it the correct length
                earthDistance = [0]*len(posX) # initialises the array that contains the distance of the rocket to the Earth
                
                for i in range(len(posX)): #loop over all the time steps
                    moonDistance[i] = math.sqrt((posX[i]-384402000)**2+(posY[i])**2)-moonRadius #use posX and posY to calcualte the distance of the Rocket to the moon's surface
                    earthDistance[i] = math.sqrt((posX[i])**2+(posY[i])**2)-earthRadius # same method used to calcualted the distance to the Earths surface.
                    
                closeApproachMoon = min(moonDistance) # this is the closest the rocket get to the moon's surface
                closeApproachEarth = min(earthDistance) # this is the closest the rocket gets to Earth's surface
                print("Closest moon approach: ", closeApproachMoon) #prints the closest moon approach
                print("Flight Duration: "+str(len(posX)*deltaTime)+"s") #prints the flight duration in s
                print("Flight Duration: "+str(len(posX)*deltaTime/(60*60*24))+" days") #prints the flight duration in days
                self.outputText.set(self.outputText.get()+"\nClosest moon approach: "+str("%.2f" % closeApproachMoon)+"m")
                self.outputText.set(self.outputText.get()+"\nFlight Duration: "+str("%.4g" % (len(posX)*deltaTime))+"s")
                self.outputText.set(self.outputText.get()+"\nFlight Duration: "+str("%.3f" % (len(posX)*deltaTime/(60*60*24)))+" days")
                
                circleEarth= plt.Circle((0, 0), 6371000, color='g', fill = False) #creates a circle for the graph of Earths size
                circleMoon = plt.Circle((384402000,0), 1737100, color = "r", fill = False) #creates a circle for the graph of the moon and puts it in the correct position.
                fig, ax = plt.subplots() #create the axis for the plot
                ax.add_artist(circleEarth) # add the circles to the axis
                ax.add_artist(circleMoon)
                ax.plot(posX,posY) # plot the path the rocket travels
                ax.set_xlim([-50000000,450000000]) #set the x axis limits
                ax.set_ylim([-200000000,200000000]) #set the y axis limits
                plt.xlabel("X (m)")
                plt.ylabel("Y (m)")
                plt.show()
                
                plt.plot(time, moonDistance) #plot the distance from the moon against timestep
                plt.xlabel("Time (s)")
                plt.ylabel("Distance (m)")
                plt.show()
                
                plt.plot(time, totalEnergy) #plot the total energy against time
                plt.xlabel("Time (s)")
                plt.ylabel("Energy (J)")
                plt.show()
            
    def quitApplication(self): #  this function closes the gui 
        root.destroy() # it destroys the variable root, which is the main 
                
root = Tk() #Tk() is a function in tkinter
root.geometry("600x500") #setting the size of the window

app = Window(root) # calls the Window class
root.mainloop() # opens the GUI
