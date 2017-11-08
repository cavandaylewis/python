# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 11:14:59 2017

@author: Cavan Day-Lewis
"""

#importing modules
import math
import numpy as np
import matplotlib.pyplot as plt
import time

def simpsonsRule(inputtedFunction, lowerLim, upperLim, N, multiplier = 1, power = 1): #the multiplier and power are by defult 1
    """
    This function performs an integration using Simpson's Rule, it takes in the arguments, lowerLim, upperLim and
    N.
    """
    runningTotal = 0
    h = (upperLim-lowerLim)/N
    f = [0.0]*(N+1) #initialise the array
    for i in range(N+1): # for all of the intervals
        x = lowerLim+h*i
        f[i] = inputtedFunction(multiplier*x**power) #calculate the value of the function
        if i%2 == 1: #if i is odd
            coeff = 4
        else: # if i is even
            if i == 0 or i == N: # if i is not at the end or begining
                coeff = 1
            else:
                coeff = 2
        runningTotal = runningTotal + coeff*f[i] #multiply by the coefficient and then add to a running total.
    integral = (h/3)*runningTotal 
    return integral # return the integral

def mysin(w, N = 1000):
    return simpsonsRule(math.sin, 0, w, N, math.pi/2, 2)
    
def mycos(w, N = 1000):
    return simpsonsRule(math.cos, 0, w, N, math.pi/2, 2)

def myIntegral(x, y, z, k, xprime, yprime): # the function for 2D fresnel fraction.
    return np.exp(((1j*k)/(2*z))*((x-xprime)**2+(y-yprime)**2))
    
def simpsonsRule2D(inputtedFunction, lowerLim, upperLim, N, x, y, z, k): 
    """
    This function is the 2D version of Simpson's rule and is used to perform Fresnel's diffraction.
    """
    upperLim = rho/2
    lowerLim = -rho/2
    h = (upperLim-lowerLim)/N
    f = [[0.0]*(N+1)]*(N+1)
    runningTotal = 0
    for i in range(N): #the for loop for the yprime values
        yprime = lowerLim+h*i
        if i%2 == 1:
            coeff1 = 4
        else:
            if i == 0 or i == N-1:
                coeff1 = 1
            else:
                coeff1 = 2
        for j in range(N): # the nested for loop
            xprime = lowerLim+h*j
            if j%2 == 1:
                coeff2 = 4
            else:
                if j ==0 or j == N-1:
                    coeff2 = 1
                else:
                    coeff2 = 2
            coeff = coeff1*coeff2
            """
            Previous method used to caluclate coefficients, less efficient
            if i%2 == 1 and j%2 == 1: #if i and j odd #set coefficients
                coeff = 16
            else:
                if j%2 == 0: #if j even
                    if j == 0 or j == N-1:
                        if i%2 == 0:
                            if i == 0 or i == N-1:
                                coeff = 1
                            else:
                                coeff = 2
                        else:
                            coeff = 4
                    else:
                        if i%2 == 0:
                            if i == 0 or i == N-1:
                                coeff = 2
                            else:
                                coeff = 4
                        else:
                            coeff = 8
                else:
                    coeff = 8
            """
            f[i][j] = coeff*inputtedFunction(x, y, z, k, xprime, yprime)
            runningTotal = runningTotal + f[i][j]
    
    integral = (h*h/9)*runningTotal
    return integral
            

MyInput = "0"
while MyInput != "q":
    MyInput = input("Enter a choice, 'a', 'b', 'c', 'e' or 'q' to quit: ")
    print("You entered the choice: ", MyInput)
    if MyInput == "a":
        #print("This program performs integration using Simpson's Rule.")
        isstring = False
        while isstring == False:
            inputtedFunction = input("Please enter the function you wish to integrate over: ")
            try:
                inputtedFunction = eval(inputtedFunction) #some test to make sure that it is a valid function to input.
                isstring = True
            except:
                isstring = False
                print("The function inputted is invalid")
                
        isfloat = False
        while isfloat == False:
            lowerLimUnevaluated = input("Please enter a value for the lower limit of integration (float):")
            try:
                lowerLim = float(eval(lowerLimUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(lowerLimUnevaluated, "is not a float or cannot be evaluated")
        
            isfloatUL = False
            while isfloatUL == False:
                upperLimUnevaluated = input("Please enter a value for the upper limit of integration (float):")
                try:
                    #perform check to make sure upperLim is greater than lower lim
                    upperLim = float(eval(upperLimUnevaluated))
                    isfloat = True
                    isfloatUL = True
                    if lowerLim >= upperLim:
                        isfloat = False
                        print("Upper limit must be greater than lower limit")
                except:
                    isfloatUL = False
                    print(upperLimUnevaluated, "is not a float or cannot be evaluated")
        
        
        isint = False
        while isint == False:
            N = input("Please enter a value for the number of intervals N (even positive integer):")
            try:
                N = int(N)
                if N > 0 and N%2 == 0:
                    isint = True
                else:
                    isint = False
                    print(N, "is not greater than 0 or is not even")
            except:
               isint = False
               
        integration = simpsonsRule(inputtedFunction, lowerLim, upperLim, N)
        print(integration)
        """"
        #This code plots a log-log differnce against N, where the difference is the value of integration taken away from the integration for the N value before.
        
        previous = simpsonsRule(math.sin, 0, math.pi, 2)
        n = 0
        P = 1000
        x = [0]*int(P/2)
        difference = [0.0]*int(P/2)
        for i in range(2,P+2,2):
            current = simpsonsRule(math.sin, 0, math.pi, i)
            difference[n] = abs(current-previous)
            x[n] = i
            previous = current
            n +=1
        
        plt.loglog(difference)
        plt.xlabel("Log of N")
        plt.ylabel("Log of Difference")
        plt.show()
        """
        
        
    elif MyInput == "b":
        """
        write two functions to evaluate the sin and cos terms of the fresnel integrals
        """
        isfloat = False
        while isfloat == False:
            wUnevaluated = input("Please enter a value for w (float): ")
            try:
                w = float(eval(wUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(wUnevaluated, "is not a float or cannot be evaluated")
        print("Integral of sine when w = "+str(w)+": ", mysin(w), "Integral of cosine when w = "+str(w)+": ", mycos(w))
        
    elif MyInput == "c":
        """
        Produces a graph showing I divided by I0 in fresnel's diffraction. 
        """
        isint = False
        while isint == False:
            N = input("Please enter a value for the number of intervals N (even positive integer):")
            try:
                N = int(N)
                if N > 0 and N%2 == 0:
                    isint = True
                else:
                    isint = False
                    print(N, "is not greater than 0 or is not even")
            except:
               isint = False
               
        isint = False
        while isint == False:
            NumPoints = input("Please enter a value for the number of points in the image (positive integer) *200:")
            try:
                NumPoints = int(NumPoints)
                if NumPoints > 0:
                    isint = True
                else:
                    isint = False
                    print(NumPoints, "is not greater than 0")
            except:
               isint = False
               print(NumPoints, "is not an integer")
               
        print("Creating Plot...")
        start = time.time()
        minVal = -5
        maxVal = 10
        #NumPoints = 200
        interval = float(maxVal-minVal)/float(NumPoints)
        w = np.arange(minVal,maxVal,interval)
        IbyInaught = [0.0]*NumPoints
        for i in range(NumPoints):
            IbyInaught[i] = (0.5)*((mysin(w[i],N)+0.5)**2+(mycos(w[i],N)+0.5)**2)
        
        plt.plot(w,IbyInaught)
        plt.xlabel("w")
        plt.ylabel(r'$\frac{I}{I_{0}}$')
        plt.show()
        
        end = time.time()
        print("Time elapsed: ", str(end-start))
    
    elif MyInput == "e":
        
        isint = False
        while isint == False:
            N = input("Please enter a value for the number of intervals N (even positive integer) *50:")
            try:
                N = int(N)
                if N > 0 and N%2 == 0:
                    isint = True
                else:
                    isint = False
                    print(N, "is not greater than 0 or is not even")
            except:
               isint = False        
               
        isfloat = False
        while isfloat == False:
            zUnevaluated = input("Please enter a value for z (float) *0.0004: ")
            try:
                z = float(eval(zUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(zUnevaluated, "is not a float or cannot be evaluated")
                
        isfloat = False
        while isfloat == False:
            wavelengthUnevaluated = input("Please enter a value for wavelength (float) *0.6*10**-6: ")
            try:
                wavelength = float(eval(wavelengthUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(wavelengthUnevaluated, "is not a float or cannot be evaluated") 
                
        isfloat = False
        while isfloat == False:
            rhoUnevaluated = input("Please enter a value for rho (float) *0.0001: ")
            try:
                rho = float(eval(rhoUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(rhoUnevaluated, "is not a float or cannot be evaluated")
        
        isint = False
        while isint == False:
            NumPoints = input("Please enter a value for the number of points in the image (positive integer) *30:")
            try:
                NumPoints = int(NumPoints)
                if NumPoints > 0:
                    isint = True
                else:
                    isint = False
                    print(NumPoints, "is not greater than 0")
            except:
               isint = False
               print(NumPoints, "is not an integer")
        
        isfloat = False
        while isfloat == False:
            imagesizeUnevaluated = input("Please enter a value for image size (float) *0.002: ")
            try:
                imagesize = float(eval(imagesizeUnevaluated))
                isfloat = True
            except:
                isfloat = False
                print(imagesizeUnevaluated, "is not a float or cannot be evaluated")
                
        #z = 0.0004#0.0004 # distance to screen in m (5mm)
        #wavelength = 0.6*10**-6#0.6*10**-6 
        #N = 50
        #rho = 0.0001#0.0001#2.5*10**-4 # size of apperture
        lowerLim = -rho/2
        upperLim = rho/2
        k = 2*math.pi/wavelength #wavenumber of light

        
        #NumPoints = 30
        startX = -imagesize/2 # 2.5*10**-2 # -0.001 
        startY = -imagesize/2
        finalX = imagesize/2
        finalY = imagesize/2
        
        delta = (finalX-startX)/NumPoints
        intensity = np.zeros((NumPoints+1,NumPoints+1))
        
        
        start = time.time()        
        print("Creating plot...")
        
        for i in range(NumPoints+1):
            y = startY + delta*i
            for j in range(NumPoints+1):    
                x = startX + delta*j
                L = (1/wavelength*z)*simpsonsRule2D(myIntegral, lowerLim, upperLim, N, x, y, z, k)
                J = L.conjugate()
                intensity[i,j] = abs(L*J)
        
        plt.imshow(intensity, extent = [startX,finalX,startY,finalY]) # plots a 2D graph of intensity and changes the x and y ticks
        plt.xlabel("x") #sets the labels for the graph
        plt.ylabel("y")
        plt.show()
        end = time.time()
        
        print("z = "+str(z)+", wavelength = "+str(wavelength)+", rho = "+str(rho)+", N = "+str(N)+", NumPoints = "+str(NumPoints)+", Start X = "+str(startX)+", Final X = "+str(finalX)+", Start Y = "+str(startY)+", Final Y = "+str(finalY))
        print("Time elapsed: ", str(end-start))
    else:
        if MyInput != "q":
            print("This is not a valid choice")
print("You have chosen to finish - goodbye.")

"""
Ideas to make it better:
- add Gui - will do
- compare with different methods of integration (e.g. monte carlo)
- Produce Eulers spiral
- Different types of integrals - exact value - expected value
- Include error calculations
- compare with the simpsons rule module
- compare with other built in modules that perform integration.
- could investigate a circular apperture.
"""

    
