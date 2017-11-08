# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:01:49 2017

@author: Cavan Day-Lewis
"""

#here I import modules
from tkinter import * # importing tkinter which is the module that generates the GUI
import math #a math kit
import matplotlib.pyplot as plt # used to create graphs
import numpy as np #another maths module
import time as timer #for time

#Add global variables
g = 9.81 # m/s^2 # accelarataion due to gravity
P0 = 1.2 # kg/m^3 # air density # could get this to vary as height varies
MolarMassAir = 28.9645/(1000*6.022*10**23) #g/mol.
BoltzmannConstant = 1.38064852*10**-23 # m^2*kgs^-2*K^-1
G = 6.67*10**-11 # Gravitational constant
earthMass = 5.972*10**24# kg
earthRadius = 6371*1000 #m
lapseRate = 6.49 #9.8 #degreesC per km

def accelerationDueToGravity(y): 
    """This function is used to calcualte the acceleration due to gravity at a certain altitude"""
    global G #here I bring the global values into my function
    global earthMass
    global earthRadius
    return (-G*earthMass)/(y+earthRadius)**2 #return the acceleration due to gravity

def analyticalMethod(y0,time, k,m):
    """Here I calculate the analytical values for height and velocity, note: nothing is dependent on deltaTime"""
    global g
    y = y0 - m/(2*k)*math.log(math.cosh(math.sqrt(k*g/m)*time)**2)
    velocity = -math.sqrt(m*g/k)*math.tanh(math.sqrt(k*g/m)*time)
    return y, velocity #return the velocity and the height
    
def variableK(y, k0, T):
    """This function is called when there is a vaiable air density, ie we are making use of the sclae height"""
    global P0
    global BoltzmannConstant
    global MolarMassAir
    
    H = 7.64*1000 #This is the scale hight
    #H = BoltzmannConstant*T/MolarMassAir*g
    k = k0*math.exp(-y/H)
    return k

def EulersMethod(Height0,time0,velocity0, deltaTime, k0, m, dump = False, variableRho = False, variableG = False, T0 = 16):
    global g
    global lapseRate
    n = 0
    # while loop to measure
    y = []
    velocity = []
    time = []
    y.append(Height0)
    velocity.append(velocity0)
    time.append(time0)
    
    yAnalytical = []
    velocityAnalytical = []
    yAnalytical.append(Height0)
    velocityAnalytical.append(velocity0)
    
    yDifference = []
    velocityDifference = []
    yDifference.append(0)
    velocityDifference.append(0)
    
    speedOfSound = []
    speedOfSound.append((331.4+((273+T0-(lapseRate*y[0])/1000)-273)*0.6)*-1)
    
    while y[n]>0: # could theoretically add a restitution coefficient then create a bouncing ball.
        if dump == True:
            print("Time:", "%.2f" % time[n],"Height:", "%.2f" % y[n], "%.2f" % yAnalytical[n], "Velocity:", "%.2f" % velocity[n], "%.2f" % velocityAnalytical[n])
            #print("Time:", time[n],"Height:", y[n],"Velocity:", velocity[n])
        
        if (y[n] > 17000):
            T = 273+T0-(lapseRate*17000-1*(y[n]-17000))/1000 #Temperature change above 17km according to ICAO
        else:
            T = 273+T0-(lapseRate*y[n])/1000 # Describes how temperature varies with altitude
        
        y.append(y[n] + deltaTime*velocity[n])
        if variableRho == True:
            k = variableK(y[n], k0, T)
        else:
            k = k0
        if variableG == True:
            g = accelerationDueToGravity(y[n])
        velocity.append(velocity[n] - deltaTime*(g+k*(abs(velocity[n])*velocity[n])/m))
        time.append(time[n] + deltaTime)
        #yAnalytical[n+1], velocityAnalytical[n+1] = analyticalMethod(Height0,time[n+1],k,m)   
        
        yAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[0])
        velocityAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[1])
        
        yDifference.append(y[n]-yAnalytical[n])
        velocityDifference.append(velocity[n]-velocityAnalytical[n])
        
        #if speedOfsoundOn == True:
        speedOfSound.append((331.4+(T-273)*0.6)*-1) #equation to calculate the speed of sound for certain values of 
        
        n+=1
    return time, velocity, y, velocityAnalytical, yAnalytical, n, yDifference, velocityDifference, speedOfSound
    
def EulersModifiedMethod(Height0,time0,velocity0, deltaTime, k0, m, dump = False, variableRho = False, variableG = False, T0 = 16):
    global g
    global lapseRate
    n = 0
    # while loop to measure
    y = []
    velocity = []
    time = []
    y.append(Height0)
    velocity.append(velocity0)
    time.append(time0)
    
    yAnalytical = []
    velocityAnalytical = []
    yAnalytical.append(Height0)
    velocityAnalytical.append(velocity0)
    
    yDifference = []
    velocityDifference = []
    yDifference.append(0)
    velocityDifference.append(0)
    
    speedOfSound = []
    speedOfSound.append((331.4+((273+T0-(lapseRate*y[0])/1000)-273)*0.6)*-1)
    while y[n]>0: # could theoretically add a restitution coefficient then create a bouncing ball.
        if dump == True:
            print("Time:", "%.2f" % time[n],"Height:", "%.2f" % y[n], "%.2f" % yAnalytical[n], "Velocity:", "%.2f" % velocity[n], "%.2f" % velocityAnalytical[n])
            #print("Time:", time[n],"Height:", y[n],"Velocity:", velocity[n])
        
        if (y[n] > 17000):
            T = 273+T0-(lapseRate*17000-1*(y[n]-17000))/1000 #standard Temperature above 11km according to ICAO
        else:
            T = 273+T0-(lapseRate*y[n])/1000 # Describes how temperature varies with altitude
        
        if variableRho == True:
            k = variableK(y[n], k0, T)
        else:
            k = k0
        
        velocityMid = velocity[n] - (deltaTime/2)*(g+k*(abs(velocity[n])*velocity[n])/m)
        y.append(y[n] + deltaTime*velocityMid)
        
        if variableG == True:
            g = accelerationDueToGravity(y[n])
            
        
        velocity.append(velocity[n] - deltaTime*(g+k*(abs(velocityMid)*velocityMid)/m))
        time.append(time[n] + deltaTime)
        #yAnalytical[n+1], velocityAnalytical[n+1] = analyticalMethod(Height0,time[n+1],k,m)   
        
        yAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[0])
        velocityAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[1])
        
        yDifference.append(y[n]-yAnalytical[n])
        velocityDifference.append(velocity[n]-velocityAnalytical[n])
        
        #if speedOfsoundOn == True:
        speedOfSound.append((331.4+(T-273)*0.6)*-1) #equation to calculate the speed of sound for certain values of 
        
        n+=1
    return time, velocity, y, velocityAnalytical, yAnalytical, n, yDifference, velocityDifference, speedOfSound
    
def RungeKuttaMethod(Height0,time0,velocity0, deltaTime, k0, m, dump = False, variableRho = False, variableG = False, T0 = 16):
    global g
    global lapseRate
    n = 0
    # while loop to measure
    y = []
    velocity = []
    time = []
    y.append(Height0)
    velocity.append(velocity0)
    time.append(time0)
    
    yAnalytical = []
    velocityAnalytical = []
    yAnalytical.append(Height0)
    velocityAnalytical.append(velocity0)
    
    yDifference = []
    velocityDifference = []
    yDifference.append(0)
    velocityDifference.append(0)
    
    speedOfSound = []
    speedOfSound.append((331.4+((273+T0-(lapseRate*y[0])/1000)-273)*0.6)*-1)
    while y[n]>0: # could theoretically add a restitution coefficient then create a bouncing ball.
        if dump == True:
            print("Time:", "%.2f" % time[n],"Height:", "%.2f" % y[n], "%.2f" % yAnalytical[n], "Velocity:", "%.2f" % velocity[n], "%.2f" % velocityAnalytical[n])
            #print("Time:", time[n],"Height:", y[n],"Velocity:", velocity[n])
        
        if (y[n] > 17000):
            T = 273+T0-(lapseRate*17000-1*(y[n]-17000))/1000 #standard Temperature above 11km according to ICAO
        else:
            T = 273+T0-(lapseRate*y[n])/1000 # Describes how temperature varies with altitude
            
        if variableRho == True:
            k = variableK(y[n], k0, T)
        else:
            k = k0
        
        kY1 = velocity[n]
        kVel1 = -(g+(k/m)*abs(velocity[n])*velocity[n])
        kY2 = velocity[n]+(deltaTime/2)*kVel1
        kVel2 = -(g+(k/m)*abs(kY2)*kY2)        
        kY3 = velocity[n]+(deltaTime/2)*kVel2
        kVel3 = -(g+(k/m)*abs(kY3)*kY3)  
        kY4 = velocity[n]+deltaTime*kVel3
        kVel4 = -(g+(k/m)*abs(kY4)*kY4)  
        
        velocity.append(velocity[n]+(deltaTime/6)*(kVel1+2*kVel2+2*kVel3+kVel4))
        y.append(y[n]+(deltaTime/6)*(kY1+2*kY2+2*kY3+kY4))
        
        if variableG == True:
            g = accelerationDueToGravity(y[n])
            
        
        #velocity.append(velocity[n] - deltaTime*(g+k*(abs(velocityMid)*velocityMid)/m))
        time.append(time[n] + deltaTime)
        #yAnalytical[n+1], velocityAnalytical[n+1] = analyticalMethod(Height0,time[n+1],k,m)   
        
        yAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[0])
        velocityAnalytical.append(analyticalMethod(Height0,time[n+1],k,m)[1])
        
        yDifference.append(y[n]-yAnalytical[n])
        velocityDifference.append(velocity[n]-velocityAnalytical[n])
        
        #if speedOfsoundOn == True:
        speedOfSound.append((331.4+(T-273)*0.6)*-1) #equation to calculate the speed of sound for certain values of 
        
        n+=1
    return time, velocity, y, velocityAnalytical, yAnalytical, n, yDifference, velocityDifference, speedOfSound


class Window(Frame): #create a class that contains the functions used by tkinter for the GUI window

    def __init__(self, master=None): # this initial function declares the nature of the frame
        Frame.__init__(self, master)
        self.master = master # in our case we always have master = none
        self.init_window() #calls init_window function
        
    #creation of init window
    def init_window(self):
        self.master.title("Free Fall Simulator")
        self.pack(fill=BOTH, expand=1, padx = 5) #allowing the widget to take the full space of the root window
        
        titleFrame = Frame(self, relief=FLAT, borderwidth=10)
        selectionFrame1 = Frame(self, relief=GROOVE, borderwidth=3)
        selectionFrame2 = Frame(self, relief=GROOVE, borderwidth=3)
        selectionFrame3 = Frame(self, relief=FLAT, borderwidth=3)
        outputFrame = Frame(self, relief=FLAT, borderwidth=3)
        quitFrame = Frame(self, relief=FLAT, borderwidth=3)
        
        titleFrame.grid(row = 0)
        selectionFrame1.grid(row = 1)
        selectionFrame2.grid(row = 2)
        selectionFrame3.grid(row = 3)
        outputFrame.grid(row = 4, sticky = W)
        quitFrame.place(x = 350, y = 660)
        
        quitButton = Button(quitFrame, text="Quit", command = self.quitApplication).grid(sticky = E+S) #creating a button instance with a command to close the GUI, it calls the function quitApplication
        #quitButton.place(x=180, y=350) #placing the button on my window
        
        
        #Don't need to make things hide and appear
        self.inputErrorText1 = StringVar() 
        self.inputErrorText2 = StringVar() 
        
        self.inputErrorText = StringVar()# initialising text for labels as empty strings # these need to be attached to self so that they can be accessed by all functions which are a part of the window.
        
        self.check8 = BooleanVar() # initialising boolean variables for checkbuttons and radiobuttons
        self.check9 = BooleanVar()
        self.check10 = BooleanVar()
        self.check11 = BooleanVar()
        self.check12 = BooleanVar()
        self.check13 = BooleanVar()
        self.check14 = BooleanVar()
        
        self.outputText = StringVar()
        
        self.textInput1Variable = StringVar()
        self.textInput2Variable = StringVar()
        self.textInput3Variable = StringVar()
        self.textInput4Variable = StringVar()
        self.textInput5Variable = StringVar()
        self.textInput6Variable = StringVar()
        self.textInput7Variable = StringVar()
        
        self.outputText.set("")
        self.inputErrorText.set("")
        
        self.title = Label(titleFrame, text="Free Fall Simulator", font = ("TkDefaultFont 22 underline"))
        self.title.grid(sticky = E+W)
        
        self.textLabel1 = Label(selectionFrame1, text="Starting Height (m): ") # creates a label attaches itself to self. the text label is a child of the window \n adds in a new line
        #print(self.textLabel1.cget("font"))
        self.textInput1 = Entry(selectionFrame1, width=7, textvariable = self.textInput1Variable) # creates a text input field which has space for 7 characters
        #self.input1error = Label(selectionFrame1, textvariable=self.inputErrorText1, fg="red") # creating another label this time the text is the empty strings we defined above, the values have the ability to change. The text wil be red.
        self.textLabel1.grid(row=1, column = 0, sticky = E) #placing the text label on the window at the specified x and y pixel coordinates
        self.textInput1.grid(row=1, column = 1, sticky = E)
        #self.input1error.grid(row=8, column = 2, sticky = E)
        
        self.textLabel2 = Label(selectionFrame1, text="Starting Velocity (m/s): ")
        self.textInput2 = Entry(selectionFrame1, width=7, textvariable = self.textInput2Variable)
        #self.input2error = Label(selectionFrame1, textvariable=self.inputErrorText2, fg="red")
        self.textLabel2.grid(row=2, column = 0, sticky = E)
        self.textInput2.grid(row=2, column = 1, sticky = E)
        #self.input2error.grid(row=9, column = 2, sticky = E)

        self.textLabel3 = Label(selectionFrame1, text="Delta Time (s): ")
        self.textInput3 = Entry(selectionFrame1, width = 7, textvariable = self.textInput3Variable)
        #self.input3error = Label(selectionFrame1, textvariable=self.inputErrorText3, fg="red")
        self.textLabel3.grid(row=3, column = 0, sticky = E)
        self.textInput3.grid(row=3, column = 1, sticky = W)
        #self.input3error.grid(row=10, column = 2, sticky = W)

        self.textLabel4 = Label(selectionFrame1, text="Mass (kg): ")
        self.textInput4 = Entry(selectionFrame1, width = 7, textvariable = self.textInput4Variable)
        #self.input4error = Label(selectionFrame1, textvariable=self.inputErrorText4, fg="red")
        self.textLabel4.grid(row=4, column = 0, sticky = E)
        self.textInput4.grid(row=4, column = 1, sticky = W)
        #self.input4error.grid(row=11, column = 2, sticky = W)

        self.textLabel5 = Label(selectionFrame1, text="Ground Temperature (°C): ")
        self.textInput5 = Entry(selectionFrame1, width=7, textvariable = self.textInput5Variable)
        #self.input5error = Label(selectionFrame1, textvariable=self.inputErrorText5, fg="red")
        self.textLabel5.grid(row=5, column = 0, sticky = E)
        self.textInput5.grid(row=5, column = 1, sticky = W)
        #self.input5error.grid(row=12, column = 2, sticky = W)

        self.textLabel6 = Label(selectionFrame1, text="Drag Coefficient:")
        self.textInput6 = Entry(selectionFrame1, width=7, textvariable = self.textInput6Variable)
        #self.input6error = Label(selectionFrame1, textvariable=self.inputErrorText6, fg="red")
        self.textLabel6.grid(row=6, column = 0, sticky = E)
        self.textInput6.grid(row=6, column = 1, sticky = W)
        #self.input6error.grid(row=13, column = 2, sticky = W)

        self.textLabel7 = Label(selectionFrame1, text="Area (m^2):")
        self.textInput7 = Entry(selectionFrame1, width=7, textvariable = self.textInput7Variable)
        #self.input7error = Label(selectionFrame1, textvariable=self.inputErrorText7, fg="red")
        self.textLabel7.grid(row=7, column = 0, sticky = E)
        self.textInput7.grid(row=7, column = 1, sticky = W)
        #self.input7error.grid(row=14, column = 2, sticky = W)
        

        self.textLabel8 = Label(selectionFrame1, text="Vary Density:")
        self.tickBox8 =   Checkbutton(selectionFrame1, variable = self.check8) # here we create a tick box
        #self.input8error = Label(selectionFrame1, textvariable=self.inputErrorText8, fg="red")
        self.textLabel8.grid(row=1, column = 3, sticky = E)
        self.tickBox8.grid(row=1, column = 4, sticky = W)
        #self.input8error.grid(row=15, column = 5, sticky = W)

        self.textLabel9 = Label(selectionFrame1, text="Vary Acceleration:")
        self.tickBox9 = Checkbutton(selectionFrame1, variable = self.check9)
        #self.input9error = Label(selectionFrame1, textvariable=self.inputErrorText9, fg="red")
        self.textLabel9.grid(row=2, column = 3, sticky = E)
        self.tickBox9.grid(row=2, column = 4, sticky = W)
        #self.input9error.grid(row=16, column = 5, sticky = W)

        self.textLabel10 = Label(selectionFrame1, text="Speed of Sound comparision:")
        self.tickBox10 = Checkbutton(selectionFrame1, variable = self.check10)
        #self.input10error = Label(selectionFrame1, textvariable=self.inputErrorText10, fg="red")
        self.textLabel10.grid(row=3, column = 3, sticky = E)
        self.tickBox10.grid(row=3, column = 4, sticky = W)
        #self.input10error.grid(row=17, column = 5, sticky = W)
        
        self.textLabel14 = Label(selectionFrame1, text="Analytical Method:")
        self.tickBox14 = Checkbutton(selectionFrame1, variable = self.check14)
        #self.input14error = Label(selectionFrame1, textvariable=self.inputErrorText14, fg="red")
        self.textLabel14.grid(row=4, column = 3, sticky = E)
        self.tickBox14.grid(row=4, column = 4, sticky = W)
        #self.input14error.grid(row=18, column = 5, sticky = W)

        self.methodValue = IntVar()
        self.methodValue.set(3)

        self.textLabel11 = Label(selectionFrame1, text="Euler's Method:")
        #self.tickBox11 = Checkbutton(self, variable = self.check11).grid(row=12, column = 1, sticky = W)
        self.tickBox11 = Radiobutton(selectionFrame1, variable=self.methodValue, value = 0)
        #self.input11error = Label(selectionFrame1, textvariable=self.inputErrorText11, fg="red")
        self.textLabel11.grid(row=5, column = 3, sticky = E)
        self.tickBox11.grid(row=5, column = 4, sticky = W)
        #self.input11error.grid(row=19, column = 5, sticky = W)

        self.textLabel12 = Label(selectionFrame1, text="Euler's Modified:")
        #self.tickBox12= Checkbutton(self, variable = self.check12).grid(row=13, column = 1, sticky = W)
        self.tickBox12 = Radiobutton(selectionFrame1, variable=self.methodValue, value = 1)
        #self.input12error = Label(selectionFrame1, textvariable=self.inputErrorText12, fg="red")
        self.textLabel12.grid(row=6, column = 3, sticky = E)
        self.tickBox12.grid(row=6, column = 4, sticky = W)
        #self.input12error.grid(row=20, column = 5, sticky = W)

        self.textLabel13 = Label(selectionFrame1, text="Runge-Kutta:")
        #self.tickBox13 = Checkbutton(self, variable = self.check13).grid(row=14, column = 1, sticky = W)
        self.tickBox13 = Radiobutton(selectionFrame1, variable=self.methodValue, value = 2)
        #self.input13error = Label(selectionFrame1, textvariable=self.inputErrorText13, fg="red")
        self.textLabel13.grid(row=7, column = 3, sticky = E)
        self.tickBox13.grid(row=7, column = 4, sticky = W)
        #self.input13error.grid(row=21, column = 5, sticky = W)
        
        self.inputError = Label(selectionFrame1, textvariable=self.inputErrorText, fg="red")
        self.inputError.grid(row = 8, columnspan = 5)
        
        self.graphLeftButton = Button(outputFrame, text="Go Left", command = self.graphLeft)
        self.graphLeftButtonOn = False # initialising a variable to state whether the graph for part d has been generated or not yet.
        self.graphRightButton = Button(outputFrame, text="Go Right", command = self.graphRight)
        self.graphRightButtonOn = False # initialising a variable to state whether the graph for part d has been generated or not yet.
        
       
        
        def sectionSelect(): 
            """
            This function runs when the user clicks on one of the radio buttons to select a part of the excersise. 
            It works out which radio button they selected and disables/fills in the correct widgets
            """
            self.MyInput = self.buttonValue.get() # gets the value of the radiobutton that the user selected.
            if self.MyInput == 1: # if it was the first radio button, prepare for a manual calculation
                self.textInput1.config(state="normal")
                self.textInput2.config(state="normal")
                self.textInput3.config(state="normal")
                self.textInput4.config(state="normal")
                self.textInput5.config(state="normal")
                self.textInput6.config(state="normal")
                self.textInput7.config(state="normal")
                self.tickBox8.config(state = "normal")
                self.tickBox9.config(state = "normal")
                self.tickBox10.config(state = "normal")
                self.tickBox11.config(state = "normal")
                self.tickBox12.config(state = "normal")
                self.tickBox13.config(state = "normal")
                self.tickBox14.config(state = "normal")
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 2: #if it was the second radio button, prepare for part (a)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("1000")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="normal")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="normal")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="normal")
                self.textInput7Variable.set("1")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.deselect()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 3: #if it was the second radio button, prepare for part (b)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("1000")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="normal")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="normal")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="normal")
                self.textInput7Variable.set("1")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.deselect()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.select()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 4:#if it was the second radio button, prepare for part (c)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("1000")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="disabled")
                self.textInput3Variable.set("")
                self.textInput4.config(state="normal")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="normal")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="normal")
                self.textInput7Variable.set("1")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.deselect()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 5:#if it was the second radio button, prepare for part (d)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("1000")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="disabled")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="disabled")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="disabled")
                self.textInput7Variable.set("")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.deselect()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 6:#if it was the second radio button, prepare for part (e)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("39045")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="normal")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="normal")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="normal")
                self.textInput7Variable.set("1")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.select()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.select()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 7:#if it was the second radio button, prepare for part (f)
                self.textInput1.config(state="disabled")
                self.textInput1Variable.set("")
                self.textInput2.config(state="disabled")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="disabled")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="disabled")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="disabled")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="disabled")
                self.textInput7Variable.set("")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.select()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.select()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.deselect()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
            elif self.MyInput == 8:#if it was the second radio button, prepare for part (g)
                self.textInput1.config(state="normal")
                self.textInput1Variable.set("39045")
                self.textInput2.config(state="normal")
                self.textInput2Variable.set("0")
                self.textInput3.config(state="normal")
                self.textInput3Variable.set("0.1")
                self.textInput4.config(state="normal")
                self.textInput4Variable.set("100")
                self.textInput5.config(state="normal")
                self.textInput5Variable.set("16")
                self.textInput6.config(state="normal")
                self.textInput6Variable.set("1.2")
                self.textInput7.config(state="normal")
                self.textInput7Variable.set("1")
                self.tickBox8.config(state = "disabled")
                self.tickBox8.select()
                self.tickBox9.config(state = "disabled")
                self.tickBox9.deselect()
                self.tickBox10.config(state = "disabled")
                self.tickBox10.deselect()
                self.tickBox11.config(state = "disabled")
                self.tickBox11.deselect()
                self.tickBox12.config(state = "disabled")
                self.tickBox12.select()
                self.tickBox13.config(state = "disabled")
                self.tickBox13.deselect()
                self.tickBox14.config(state = "disabled")
                self.tickBox14.deselect()
                self.outputGraph.config(image="")
                self.outputText.set("")
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
        
        self.button = Button(selectionFrame3, text="Calculate", command = self.calculate) #creating a button instance with a command to call the submit1 function, which is a part of the window class (self) ie self.submit1
        self.button.grid(row=0, sticky = W+E)
        self.output = Label(outputFrame, textvariable=self.outputText)
        self.output.grid(row=0, columnspan = 2)
        self.outputGraph = Label(outputFrame)
        self.outputGraph.grid(row = 1, columnspan = 2)
        self.graphSize = 65 #65 is defualt, 160 for using pictures in report
        
        options = [("Manual", 1), ("(a)", 2), ("(b)", 3), ("(c)", 4),("(d)", 5),("(e)", 6),("(f)", 7),("(g)", 8),] #an array containing the different options for the radio button
        self.buttonValue = IntVar() # initialising buttonValue as an integer variable
        i = 0
        rb = [0]*len(options) # there are three different radiobuttons, each one will go in the array rb, which is being initialised here.
        for text, value in options: # loop over the entries in options, taking out the text and the values.
            rb[i] = Radiobutton(selectionFrame2, text=text, variable=self.buttonValue, value=value, command = sectionSelect).grid(row=0, column = i) #create the radio buttons, pack is a way of adding the radio button widgets to the GUI, we place them at the top left
            i+=1
            
            
    def calculate(self):
        self.MyInput = self.buttonValue.get()
        if self.MyInput == 1: # if it was the first radio button, prepare for a manual calculation
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True
                
            varyDensity = self.check8.get()
            varyAcceleration = self.check9.get()
            speedOfSoundComparison = self.check10.get()
            analyticalMethod = self.check14.get()

            if self.methodValue.get() != 0 and self.methodValue.get() != 1 and self.methodValue.get() != 2:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"At least 1 ODE solving method must be chosen")
                errorOn = True
                
            if analyticalMethod == True and varyDensity == True and errorOn == True:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Warning Anylitical method doesn't work well for non-constant air density")
                
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                if analyticalMethod == True and varyDensity == True:
                    self.inputErrorText.set("Warning Anylitical method doesn't work well for non-constant air density")
                k = (Cd*P0*A)/2
                if self.methodValue.get() == 0: # perform Euler's Method
                    dump = False
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, dump, varyDensity, varyAcceleration, T0)
                    method = "Euler's"
                elif self.methodValue.get() == 1: #perform Euler's Modified method
                    dump = False
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersModifiedMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, dump, varyDensity, varyAcceleration, T0)
                    method = "Euler's Modified"
                elif self.methodValue.get() == 2: # perform the Runge-Kutta
                    dump = False
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = RungeKuttaMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, dump, varyDensity, varyAcceleration, T0)
                    method = "Runge-Kutta"
                    
                if analyticalMethod == True:
                    plt.plot(time, y, "b-", label= method)
                    plt.plot(time,  yAnalytical, "r-",label = "Analytical Method")
                    plt.legend()
                    plt.xlabel("Time (s)")
                    plt.ylabel("Height (m)")
                    try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                        os.remove("manual-1.png") # remove the old file output.png if there is one # checking that this
                    except:
                        pass
                    plt.savefig("manual-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                    plt.close() #close the plot now that we have finished     
                
                    
                    if speedOfSoundComparison == True:
                        plt.plot(time, velocity, "b-", label = method)
                        plt.plot(time, velocityAnalytical, "r-", label = "Analytical")
                        plt.plot(time, speedOfSound, "g-", label = "Speed of sound")
                        plt.legend()
                        plt.xlabel("Time (s)")
                        plt.ylabel("Velocity (m/s)")
                        try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                            os.remove("manual-2.png") # remove the old file output.png if there is one # checking that this
                        except:
                            pass
                        plt.savefig("manual-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                        plt.close() #close the plot now that we have finished     
                
                    else:
                        plt.plot(time, velocity, "b-", label = method)
                        plt.plot(time, velocityAnalytical, "r-", label = "Analytical")
                        plt.legend()
                        plt.xlabel("Time (s)")
                        plt.ylabel("Velocity (m/s)")
                        try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                            os.remove("manual-2.png") # remove the old file output.png if there is one # checking that this
                        except:
                            pass
                        plt.savefig("manual-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                        plt.close() #close the plot now that we have finished     
                
                        
                    plt.plot(time, yDifference)
                    plt.xlabel("Time (s)")
                    plt.ylabel("Height Difference (m)")
                    try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                        os.remove("manual-3.png") # remove the old file output.png if there is one # checking that this
                    except:
                        pass
                    plt.savefig("manual-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                    plt.close() #close the plot now that we have finished     
                    
                    plt.plot(time, velocityDifference)
                    plt.xlabel("Time (s)")
                    plt.ylabel("Velocity Difference (m/s)")
                    try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                        os.remove("manual-4.png") # remove the old file output.png if there is one # checking that this
                    except:
                        pass
                    plt.savefig("manual-4.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                    plt.close() #close the plot now that we have finished
                    self.graphs = ["manual-1.png","manual-2.png","manual-3.png","manual-4.png"]
                
                else: 
                    k = (Cd*P0*A)/2
                    plt.plot(time, y)
                    plt.xlabel("Time (s)")
                    plt.ylabel("Height (m)")
                    try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                        os.remove("manual-1.png") # remove the old file output.png if there is one # checking that this
                    except:
                        pass
                    plt.savefig("manual-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                    plt.close() #close the plot now that we have finished     
                
                    if speedOfSoundComparison == True:
                        plt.plot(time, velocity, "b-", label = "Velocity")
                        plt.plot(time, speedOfSound, "r-",label="Speed of sound")
                        plt.legend()
                        plt.xlabel("Time (s)")
                        plt.ylabel("Velocity= (m/s)")
                        try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                            os.remove("manual-2.png") # remove the old file output.png if there is one # checking that this
                        except:
                            pass
                        plt.savefig("manual-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                        plt.close() #close the plot now that we have finished     
                        
                    else:
                        plt.plot(time, velocity)
                        plt.xlabel("Time (s)")
                        plt.ylabel("Velocity= (m/s)")
                        try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                            os.remove("manual-2.png") # remove the old file output.png if there is one # checking that this
                        except:
                            pass
                        plt.savefig("manual-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                        plt.close() #close the plot now that we have finished     
                    self.graphs = ["manual-1.png","manual-2.png"]
                
                photo = PhotoImage(file="manual-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
                            
        elif self.MyInput == 2: #if it was the second radio button run part (a)
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True        
        
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                dump = True
                k = (Cd*P0*A)/2
                
                time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, dump)
                
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()        
                lns1 = ax1.plot(time, y, "g-", label = "Height")
                ax1.set_xlabel("Time (s)")
                ax1.set_ylabel("Height (m)", color = "g")
                lns2 = ax2.plot(time, velocity, "b-", label = "Velocity")
                ax2.set_ylabel("Velocity (m/s)", color = "b")
                lns = lns1+lns2
                labs = [l.get_label() for l in lns]
                ax1.legend(lns, labs)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(a).png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(a).png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished                
                
                photo = PhotoImage(file="part(a).png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                #self.outputText.set("Output: \n Task Finished")
                
                if self.graphLeftButtonOn == True:
                    self.graphLeftButton.grid_forget()
                if self.graphRightButtonOn == True:
                    self.graphRightButton.grid_forget()
                
                
                
        elif self.MyInput == 3: # if it was the third radio button add widgets for part (b)
            """
            This section of code has been written to compare the values from Euler's Method with the analytical method
            """
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True
                
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                
                k = (Cd*P0*A)/2
                time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m)
                
                #plt.subplot(221)
                plt.plot(time, y, "b-", label= "Eulers")
                plt.plot(time,  yAnalytical, "r-", label = "Analytical")
                plt.legend()
                plt.xlabel("Time (s)")
                plt.ylabel("Height (m)")
                #plt.show()
                
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(b)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(b)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                #plt.subplot(222)
                plt.plot(time, velocity, "b-", label= "Eulers")
                plt.plot(time, velocityAnalytical, "r-", label = "Analytical")
                plt.legend()
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
                #plt.show()
                
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(b)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(b)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                #plt.subplot(223)
                plt.plot(time, yDifference)
                plt.xlabel("Time (s)")
                plt.ylabel("Height Difference (m)")
                
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(b)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(b)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                #plt.subplot(224)
                plt.plot(time, velocityDifference)
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity Difference (m/s)")
                #plt.tight_layout()
                #plt.show()
                
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(b)-4.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(b)-4.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                photo = PhotoImage(file="part(b)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(b)-1.png","part(b)-2.png","part(b)-3.png","part(b)-4.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
            
        elif self.MyInput == 4: #code below for part c
        
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True
            
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                deltaTime = [0.01,0.1,0.2,0.3,0.5,0.75,1,1.5,3, 5]
            
                k = (Cd*P0*A)/2
                
                terminalVelocity = [0.0]*len(deltaTime)
                terminalHeightDifference = [0.0]*len(deltaTime)
                
                for i in range(len(deltaTime)):
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime[i], k, m)        
                    plt.plot(y, velocity, label= "Delta Time: "+str(deltaTime[i])+"s")
                    terminalVelocity[i] = abs(velocity[N]) # the final velocity
                    terminalHeightDifference[i] = yDifference[N]
                plt.xlabel("Height (m)")
                plt.ylabel("Velocity (m)")
                plt.axis([max(y),min(y),min(velocity),max(velocity)])
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(c)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(c)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished   
                    
                plt.plot(deltaTime, terminalVelocity, "bx" )
                plt.xlabel("Delta Time (s)")
                plt.ylabel("Terminal Velocity (m/s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(c)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(c)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished   
                
                plt.loglog(deltaTime, terminalHeightDifference, "bx")
                plt.xlabel("Delta Time (s)")
                plt.ylabel("Terminal Height Difference (m)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(c)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(c)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                photo = PhotoImage(file="part(c)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(c)-1.png","part(c)-2.png","part(c)-3.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
            
            
        elif self.MyInput == 5: #code below for part d
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
            
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")   
        
            
                m = 100 # 100kg
                Cd = 1.2 #drag coefficient
                # A = 1 # m^2 # cross sectional area of free fall object
                A = np.array([0.01,0.02,0.04,0.075,0.1,0.25,0.5,1,2,3,4,5,6,7,8,9,10,20])
                m = [100.0]*len(A)
                k = (Cd*P0*A)/2
                
                impactTime = [0.0]*len(m)
                timeFor90 = [0.0]*len(m)
                ratioKM = [0.0]*len(m)
                terminalVelocity = [0.0]*len(m)
                
                #plt.figure(1)
                #fig2 = plt.figure(2)
                              
                for i in range(len(m)):
                    ratioKM[i] = k[i]/m[i]
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k[i], m[i])        
                    plt.figure(1)                    
                    plt.plot(time, y, label = "K/M: "+str(ratioKM[i])+r"m$^{-1}$")
                    plt.figure(2)
                    plt.plot(time, velocity, label = "K/M: "+str(ratioKM[i])+r"m$^{-1}$")                    
                    impactTime[i] = time[N]
                    terminalVelocity[i] = abs(velocity[N])
                    j = 0
                    while abs(velocity[j]) < terminalVelocity[i]*0.9:
                        j += 1
                    timeFor90[i] = time[j]
                plt.figure(1)
                plt.xlabel('Time (s)')
                plt.ylabel('Height (m)')
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(d)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(d)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished    
                plt.figure(2)
                plt.ylabel('Velocity (m/s)')
                plt.xlabel('Time (s)')
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(d)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(d)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished   
                    
                plt.plot(ratioKM, impactTime)
                plt.xlabel(r"K/M (m$^{-1}$)")
                plt.ylabel("Impact Time (s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(d)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(d)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished
                
                plt.loglog(ratioKM, terminalVelocity, "bx")
                plt.xlabel(r"K/M (m$^{-1}$)")
                plt.ylabel("Terminal Velocity (m/s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(d)-4.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(d)-4.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished    
                
                plt.loglog(ratioKM, timeFor90, "bx")
                plt.xlabel(r"K/M (m$^{-1}$)")
                plt.ylabel("Time taken to reach 90% of Terminal Velocity (m/s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(d)-5.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(d)-5.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                photo = PhotoImage(file="part(d)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(d)-1.png","part(d)-2.png","part(d)-3.png","part(d)-4.png","part(d)-5.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
        
        elif self.MyInput == 6: # code below for part e
            
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True
        
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                k = (Cd*P0*A)/2 # 
                
                time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, False, True, False, T0)
                
                mach = []                
                for i in range(len(time)):
                    mach.append(velocity[i]/speedOfSound[i])
                    
                #mach = velocity/speedOfSound
                
                plt.plot(time, y, "b-")
                plt.xlabel("Time (s)")
                plt.ylabel("Height (m)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(e)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(e)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished    
                
                plt.plot(time, velocity, "b-", label= "Projectile Velocity") 
                plt.plot(time, speedOfSound, "r-",label = "Speed of Sound")
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
                plt.legend(loc = 'center right')
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(e)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(e)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished    
                
                plt.plot(time, mach)
                plt.xlabel("Time (s)")
                plt.ylabel("Mach (A.U)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(e)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(e)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                photo = PhotoImage(file="part(e)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(e)-1.png","part(e)-2.png","part(e)-3.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
        
        elif self.MyInput == 7: #code below for part f
             #can also do my comparison for temperature
            #can include equations for speed of sound and plot that on the velocity graph.
            #StartingHeight = 39045 # 1000 m
        
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                StartingHeight = np.array([10, 20, 40, 60, 80, 100, 150, 200,250, 300, 350, 400, 450, 500 ,600 ,700 ,800])
            
                StartingVelocity = 0
                m = 100 # 100kg
                Cd = 1.2 #drag coefficient
                A = 1 # m^2 # cross sectional area of free fall object
                #A = np.array([0.01,0.02,0.04,0.075,0.1,0.25,0.5,1,2,3,4,5,6,7,8,9,10,20])
                #m = [100.0]*len(A)
                m = 100 #kg
                k = (Cd*P0*A)/2 # 
                T = 260 #Temperature (K)
        
                maximumSpeed = [0.0]*len(StartingHeight)
                fallDuration = [0.0]*len(StartingHeight)
                        
                
                for i in range(len(StartingHeight)):
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight[i], 0, StartingVelocity, deltaTime, k, m, False, True, False, T)        
                    plt.plot(y, velocity, label = "Starting Height: "+str(StartingHeight[i]))
                    maximumSpeed[i] = 0
                    for j in range(len(velocity)):
                        if velocity[j] < maximumSpeed[i]:
                            maximumSpeed[i] = velocity[j]
                            
                    fallDuration[i] = time[len(time)-1]
                plt.xlabel("Height (m)")
                plt.ylabel("velocity (m/s)")
                #plt.axis([max(y),min(y),min(velocity),max(velocity)])
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                plt.plot(StartingHeight, maximumSpeed,"b-")
                plt.xlabel("Starting Height (m)")
                plt.ylabel("Maximum Velocity (m/s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                plt.plot(StartingHeight, fallDuration,"b-")
                plt.xlabel("Starting Height (m)")
                plt.ylabel("Fall Duration (s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     


                #Second part of section f - comparison of differend Cd*A/m values
                StartingHeight = 39045
                StartingVelocity = 0
                m = 100 # 100kg
                Cd = 1.2 #drag coefficient
                # A = 1 # m^2 # cross sectional area of free fall object
                #A = np.array([0.01,0.02,0.04,0.075,0.1,0.25,0.5,1,2,3,4,5])
                A = np.array([0.01,0.02,0.04,0.075,0.1,0.25,0.5,1,2,3])
                k = (Cd*P0*A)/2
                cdAOVERm = Cd*A/m
                m = [m]*len(A)
                maximumSpeed = [0.0]*len(A)
                fallDuration = [0.0]*len(A)
                        
                
                for i in range(len(A)):
                    time, velocity, y, velocityAnalytical, yAnalytical, N, yDifference, velocityDifference, speedOfSound = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k[i], m[i], False, True, False, T)        
                    plt.plot(y, velocity, label = r"$\frac{C_{d}A}{m}$: "+str(cdAOVERm[i])+r"$\frac{m^{2}}{kg}$")
                    maximumSpeed[i] = 0
                    for j in range(len(velocity)):
                        if velocity[j] < maximumSpeed[i]:
                            maximumSpeed[i] = velocity[j]
                            
                    fallDuration[i] = time[len(time)-1]
                plt.xlabel("Height (m)")
                plt.ylabel("velocity (m/s)")
                #plt.axis([max(y),min(y),min(velocity),max(velocity)])
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-4.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-4.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                plt.plot(cdAOVERm, maximumSpeed,"b-")
                plt.xlabel(r"$\frac{C_{d}A}{m} (\frac{m^{2}}{kg})$")
                plt.ylabel("Maximum Velocity (m/s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-5.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-5.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                plt.plot(cdAOVERm, fallDuration,"b-")
                plt.xlabel(r"$\frac{C_{d}A}{m} (\frac{m^{2}}{kg})$")
                plt.ylabel("Fall Duration (s)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(f)-6.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(f)-6.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished     
                
                photo = PhotoImage(file="part(f)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(f)-1.png","part(f)-2.png","part(f)-3.png","part(f)-4.png","part(f)-5.png","part(f)-6.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
                
        
        elif self.MyInput == 8: # If the runs part g
            
            errorOn = False # error on determines whether there is an error in the users input, here we are initialising it to false
            
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingHeight = self.textInput1.get() # collect the text from the first text field on the screen
                StartingHeight = float(StartingHeight) # try and convert this text to a float
                if StartingHeight <= 0: # if it is less than or equal to 0
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for starting height")# the error message lets the user know what they did wrong
                    errorOn = True
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting height") # This lets the user know they didn't enter a float
                errorOn = True
                
            try:  # a try-catch loop is the best way to perform this validation routine.
                StartingVelocity = self.textInput2.get() # collect the text from the first text field on the screen
                StartingVelocity = float(StartingVelocity) # try and convert this text to a float
            except: # if there was any error in the code above then this will run
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for starting velocity")
                errorOn = True
                
            try:
                deltaTime = self.textInput3.get() 
                deltaTime = float(deltaTime) 
                if deltaTime <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for delta time")
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for delta time")
                
            try: 
                m = self.textInput4.get() 
                m = float(m) 
                if m <= 0: 
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for mass")
                    errorOn = True
            except: 
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for mass")                
                errorOn = True
                
            try:
                T0 = self.textInput5.get()
                T0 = float(T0)
                if T0 < -273:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than or equal to -273 for ground temperature")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for ground temperature")
                errorOn = True
                
            try:
                Cd = self.textInput6.get()
                Cd = float(Cd)
                if Cd <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for drag coefficient")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for drag coefficient")
                errorOn = True
                
            try:
                A = self.textInput7.get()
                A = float(A)
                if A <= 0:
                    self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a value greater than 0 for Area")
                    errorOn = True
            except:
                self.inputErrorText.set(self.inputErrorText.get()+"\n"+"Enter a float for Area")
                errorOn = True
            
            if errorOn == False: # under the conditions that there are no errors with the users input
                #perform the calculations
                self.inputErrorText.set("")
                k = (Cd*P0*A)/2 # 
                
                time1, velocity1, y1, velocityAnalytical1, yAnalytical1, N1, yDifference1, velocityDifference1, speedOfSound1 = EulersMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, False, True, False, T0)
                time2, velocity2, y2, velocityAnalytical2, yAnalytical2, N2, yDifference2, velocityDifference2, speedOfSound2 = EulersModifiedMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, False, True, False, T0)
                time3, velocity3, y3, velocityAnalytical3, yAnalytical3, N3, yDifference3, velocityDifference3, speedOfSound3 = RungeKuttaMethod(StartingHeight, 0, StartingVelocity, deltaTime, k, m, False, True, False, T0)
                
                if len(time1)>=len(time2):
                    modifiedDifferenceLength = len(time2)
                    modifiedNewTime = time2
                else:
                    modifiedDifferenceLength = len(time1)
                    modifiedNewTime = time1
                    
                if len(time2)>=len(time3):
                    kuttaDifferenceLength = len(time3)
                    kuttaNewTime = time3
                else:
                    kuttaDifferenceLength = len(time2)
                    kuttaNewTime = time2
                    
        
                #modifiedNewTime = [0.0]*(modifiedDifferenceLength)  
                modifiedYDifference = [0.0]*(modifiedDifferenceLength)        
                modifiedVelocityDifference = [0.0]*(modifiedDifferenceLength)    
                
                #kuttaNewTime = [0.0]*(kuttaDifferenceLength)  
                kuttaYDifference = [0.0]*(kuttaDifferenceLength)
                kuttaVelocityDifference = [0.0]*(kuttaDifferenceLength)
                
                for i in range(modifiedDifferenceLength):
                    modifiedYDifference[i] = y1[i]-y2[i]
                    modifiedVelocityDifference[i] = velocity1[i]-velocity2[i]
                    
                for i in range(kuttaDifferenceLength):
                    kuttaYDifference[i] = y2[i]-y3[i]
                    kuttaVelocityDifference[i] = velocity2[i]-velocity3[i]
                
                mach = []                
                for i in range(len(time3)):
                    mach.append(velocity3[i]/speedOfSound3[i])
                    
                #mach = velocity/speedOfSound
                
                plt.plot(time1, y1, "b-", label = "Euler's Method")
                plt.plot(time2, y2, "r-", label = "Euler's Modified")
                plt.plot(time3, y3, "g-", label = "Runge-Kutta")
                plt.xlabel("Time (s)")
                plt.ylabel("Height (m)")
                plt.legend()
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-1.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-1.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished  
                
                plt.plot(time1, velocity1, "b-", label = "Euler's Method")
                plt.plot(time2, velocity2, "r-", label = "Euler's Modified")
                plt.plot(time3, velocity3, "g-", label = "Runge-Kutta")
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
                plt.legend(loc = "center right")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-2.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-2.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished  
                
                plt.plot(time3, velocity3, "b-", label = "Runge-Kutta")
                plt.plot(time3, speedOfSound3, "r-", label = "Speed of sound")
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
                plt.legend(loc = "center right")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-3.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-3.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished  
                
                plt.plot(time3, mach, label = "Runge-Kutta")
                plt.xlabel("Time (s)")
                plt.ylabel("Mach (A.U)")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-4.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-4.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished  
                
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                ax1.set_title("Euler's and Euler's Modified Comparison")
                ax1.plot(modifiedNewTime, modifiedYDifference, "g-")
                ax1.set_xlabel("Time (s)")
                ax1.set_ylabel("Height Difference (m)", color="g")
                ax2.plot(modifiedNewTime, modifiedVelocityDifference, "b-")
                ax2.set_ylabel("Velocity Difference (m/s)", color = "b")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-5.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-5.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished    
                
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                ax1.set_title("Modified Euler's and Runge-Kutta Comparison")
                ax1.plot(kuttaNewTime, kuttaYDifference, "g-")
                ax1.set_xlabel("Time (s)")
                ax1.set_ylabel("Height Difference (m)", color="g")
                ax2.plot(kuttaNewTime, kuttaVelocityDifference, "b-")
                ax2.set_ylabel("Velocity Difference (m/s)", color = "b")
                try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                    os.remove("part(g)-6.png") # remove the old file output.png if there is one # checking that this
                except:
                    pass
                plt.savefig("part(g)-6.png", dpi=self.graphSize, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
                plt.close() #close the plot now that we have finished  
                
                photo = PhotoImage(file="part(e)-1.png")
                self.outputGraph.config(image = photo)
                self.outputGraph.photo = photo
                self.graphPos = 1
                
                self.graphs = ["part(g)-1.png","part(g)-2.png","part(g)-3.png", "part(g)-4.png", "part(g)-5.png", "part(g)-6.png"]
                
                #add graph left and right buttons
                self.graphLeftButton.grid(row=2, column = 0)
                self.graphRightButton.grid(row=2, column = 1)
                self.graphLeftButton.config(state = "disabled")
                self.graphRightButton.config(state = "normal")
                self.graphLeftButtonOn = True
                self.graphRightButtonOn = True
            
    def quitApplication(self): #  this function closes the gui 
        root.destroy() # it destroys the variable root, which is the main 
        
    def graphLeft(self): #this function is called when the open graph button is clicked
        if self.graphPos != 1:
            self.graphRightButton.config(state = "normal")
            self.graphPos = self.graphPos - 1
            photo = PhotoImage(file=self.graphs[self.graphPos-1])
            self.outputGraph.config(image = photo)
            self.outputGraph.photo = photo
            if self.graphPos == 1:
                self.graphLeftButton.config(state = "disabled")
    def graphRight(self): #this function is called when the open graph button is clicked
        if self.graphPos != len(self.graphs):
            self.graphLeftButton.config(state = "normal")
            self.graphPos = self.graphPos + 1
            photo = PhotoImage(file=self.graphs[self.graphPos-1])
            self.outputGraph.config(image = photo)
            self.outputGraph.photo = photo
            if self.graphPos == len(self.graphs):
                self.graphRightButton.config(state = "disabled")
        
        
root = Tk() #Tk() is a function in tkinter
root.geometry("400x700") #setting the size of the window

app = Window(root) # calls the Window class
root.mainloop() # opens the GUI

