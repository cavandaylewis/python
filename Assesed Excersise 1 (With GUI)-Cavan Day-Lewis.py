# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:34:17 2016

@author: Cavan Day-Lewis
"""

#here I import the modules that 
from tkinter import * # importing tkinter which is the module that generates the GUI
import math 
import numpy as np
import matplotlib.pyplot as plt # importing mathplotlib the library used to generate graphs
import time # needed to create a timer, used in the non - gui version.

import os # needed to remove files
from PIL import Image #importing python image loader - this is used to display images

def arctanExpansion(x,N):
    """
    This function calculates the series expansion for arctan(x) it can deal with x is any real number. The number of
    iterations the user wants is specified in the integer argument N; and the floating point argument, x, is the value of x 
    to put into arctan(x). The user specifies both of these values.
    """
    inverseXpositive = False #initialising variables
    inverseXnegative = False 
    if abs(x)>1:
        if x>0:
            inverseXpositive = True #whether we are going to inverse x as it is greater than 1
        else:
            inverseXnegative = True #whether we are going to inverse x as it is less than -1
        x = 1/x
    arctan = 0
    part = [0.0]*(N+1) #create an empty array with N values. This array will contain the terms in the summation
    arctanArr = [0.0]*(N+1) #create an empty array with N values. This array will contain the arctan values as N increases
    for n in range(N+1): # for loop over all the values of N
        part[n] = (((-1)**n/(2*n+1))*x**(2*n+1)) # perform the calculation and populates the array: part
        arctan += part[n] #sum the terms
        arctanArr[n] = (arctan)
    if inverseXpositive == True: #if x is greater than 1
        return math.pi/2-arctan, arctanArr, part #return pi/2 - arctan and the other arrays we populated
    elif inverseXnegative == True:
        return -math.pi/2-arctan, arctanArr, part #return -pi/2 - arctan and the other arrays we populated
    else:
        return arctan, arctanArr, part #return arctan and the other arrays we populated

class Window(Frame): #create a class that contains the functions used by tkinter for the GUI window

    def __init__(self, master=None): # this initial function declares the nature of the frame
        Frame.__init__(self, master)
        self.master = master # in our case we always have master = none
        self.init_window() #calls init_window function
        
    #Creation of init_window
    def init_window(self): # self is the window class itself
        self.master.title("Arctan Expansion GUI") #changing the title of our master widget  
        self.pack(fill=BOTH, expand=1) #allowing the widget to take the full space of the root window
        quitButton = Button(self, text="Quit", command = self.quitApplication) #creating a button instance with a command to close the GUI, it calls the function quitApplication
        quitButton.place(x=180, y=350) #placing the button on my window
        
        self.inputErrorText1 = StringVar() # initialising text for labels as empty strings
        self.inputErrorText2 = StringVar() # these need to be attached to self so that they can be accessed by all functions which are a part of the window.
        self.inputErrorText3 = StringVar()
        self.inputErrorText4 = StringVar()
        
        self.outputText1 = StringVar()        
        self.outputText2 = StringVar()
        self.outputText3 = StringVar()
        
        self.textLabel1 = Label(self, text="Enter your value for N here:") # creates a label attaches itself to self. the text label is a child of the window
        self.textInput1 = Entry(self, width=7) # creates a text input field which has space for 7 characters
        self.input1error = Label(self, textvariable=self.inputErrorText1, fg="red") # creating another label this time the text is the empty strings we defined above, the values have the ability to change. The text wil be red.
        self.textLabel2 = Label(self, text="Enter your value for x here: \nYou can enter mathmatical formulas accepted by python \n e.g. 1/math.sqrt(3)") # \n adds in a new line
        self.textInput2 = Entry(self, width=40)
        self.input2error = Label(self, textvariable=self.inputErrorText2, fg="red")
        self.button1 = Button(self, text="Calculate", command = self.submit1) #creating a button instance with a command to call the submit1 function, which is a part of the window class (self) ie self.submit1
        self.output1 = Label(self, textvariable=self.outputText1)
        
        self.textLabel3 = Label(self, text="Enter your value for N here:") #we continue to generate widgets for our window
        self.textInput3 = Entry(self, width=7)
        self.input3error = Label(self, textvariable=self.inputErrorText3, fg="red")
        self.button2 = Button(self, text="Calculate", command = self.submit2)
        self.output2 = Label(self, textvariable=self.outputText2)
        self.openGraphButton = Button(self, text="Open Graph", command = self.openGraph)
        self.graphGenerated = False # initialising a variable to state whether the graph for part d has been generated or not yet.
        
        self.textLabel4 = Label(self, text="Enter your value for N here:")
        self.textInput4 = Entry(self, width=7)
        self.input4error = Label(self, textvariable=self.inputErrorText4, fg="red")
        self.button3 = Button(self, text="Calculate", command = self.submit3)
        self.output3 = Label(self, textvariable=self.outputText3)
                
        def sectionSelect(): 
            """
            This function runs when the user clicks on one of the radio buttons to select a part of the excersise. 
            It works out which radio button they selected and adds the correct widgets to the GUI
            """
            self.MyInput = buttonValue.get() # gets the value of the radiobutton that the user selected.
            if self.MyInput == 1: # if it was the first radio button, add widgets for part (a)
                self.textLabel1.place(x=120, y=40) #placing the text label on the window at the specified x and y pixel coordinates
                self.textInput1.place(x=180, y=60)
                self.input1error.place(x=220, y=60)
                self.textLabel2.place(x=60, y=85)
                self.textInput2.place(x=80, y=140)
                self.input2error.place(x=325, y=140)
                self.button1.place(x=175, y=160) 
                self.output1.place(x=200-self.output1.winfo_width()/2, y=190) # for the x coordinate we half the width of the label widget and half the width of the window and subtract the two so that the label is exacly central.
                
                self.textLabel3.place_forget() # incase these widgets are currently being displayed on the window we want to remove them
                self.textInput3.place_forget()
                self.button2.place_forget()
                self.output2.place_forget()
                self.openGraphButton.place_forget()
                
                self.textLabel4.place_forget()
                self.textInput4.place_forget()
                self.button3.place_forget()
                self.output3.place_forget()
               
            elif self.MyInput == 2: #if it was the second radio button, add widgets for part (d)
                self.textLabel1.place_forget()
                self.textInput1.place_forget()
                self.input1error.place_forget()
                self.textLabel2.place_forget()
                self.textInput2.place_forget()
                self.input2error.place_forget()
                self.button1.place_forget()
                self.output1.place_forget()
                
                self.textLabel3.place(x=120, y=40)
                self.textInput3.place(x=180, y=60)
                self.input3error.place(x=220, y=60)
                self.button2.place(x=175, y=85)
                self.output2.place(x=200-self.output2.winfo_width()/2, y=115)
                if self.graphGenerated == True: # if a graph has been generated before then the button to display the graph can be shown
                    self.openGraphButton.place(x=180,y=160)
                else: # otherwise it can't be displayed
                    self.openGraphButton.place_forget()
                
                self.textLabel4.place_forget()
                self.textInput4.place_forget()
                self.input4error.place_forget()
                self.button3.place_forget()
                self.output3.place_forget()
            elif self.MyInput == 3: # if it was the third radio button add widgets for part (f)
                self.textLabel1.place_forget()
                self.textInput1.place_forget()
                self.input1error.place_forget()
                self.textLabel2.place_forget()
                self.textInput2.place_forget()
                self.input2error.place_forget()
                self.button1.place_forget()
                self.output1.place_forget()
                
                self.textLabel3.place_forget()
                self.textInput3.place_forget()
                self.input3error.place_forget()
                self.button2.place_forget()
                self.output2.place_forget()
                self.openGraphButton.place_forget()
                
                self.textLabel4.place(x=120, y=40)
                self.textInput4.place(x=180, y=60)
                self.input4error.place(x=220, y=60)
                self.button3.place(x=175, y=85)
                self.output3.place(x=200-self.output3.winfo_width()/2, y=115)
            
        options = [("part (a)", 1), ("part (d)", 2), ("part (f)", 3),] #an array containing the different options for the radio button
        buttonValue = IntVar() # initialising buttonValue as an integer variable
        i = 0
        rb = [0]*3 # there are three different radiobuttons, each one will go in the array rb, which is being initialised here.
        for text, value in options: # loop over the entries in options, taking out the text and the values.
            rb[i] = Radiobutton(self, text=text, variable=buttonValue, value=value, command = sectionSelect).pack(side=LEFT, anchor=N) #create the radio buttons, pack is a way of adding the radio button widgets to the GUI, we place them at the top left
            i+=1
        
    def quitApplication(self): #  this function closes the gui
        root.destroy() # it destroys the variable root, which is the main 
        
    def submit1(self): # when the user clicks calculate for part (a) this code is run.
        try: # a try-catch loop is the best way to perform this validation routine.
            N = self.textInput1.get() # collect the text from the first text field on the screen
            N = int(N) # try and convert this text to an integer
            if N > 0: # if it is greater than 0
                self.inputErrorText1.set("") #there is no error with what the user entered so the error message can remain blank
            else:
                self.inputErrorText1.set("Enter a value greater than 0") # the error message lets the user know what they did wrong
                print(N, "is not greater than 0")
        except: # if there was any error in the code above then this will run
            print(N, "is not an int")
            self.inputErrorText1.set("Enter an integer") # this lets the user know that they didn't enter an integer
        
        try: # this is the try-catch loop for the x value that the user entered.
            xUnevaluated = self.textInput2.get()
            x = float(eval(xUnevaluated)) # try and mathmatecally evaluate the users input and then put it into a float
            self.inputErrorText2.set("") # if there was no error with this, no error message will be displayed
        except:
            self.inputErrorText2.set("This cannot be evaluated to a float") # letting the user know that their input was invalid
            print(xUnevaluated, " cannot be evaluated to a float")
        
        if  self.inputErrorText1.get() == "" and self.inputErrorText2.get() == "": # if there are no error messages displayed
            arctan,arctanArr,part = arctanExpansion(x,N) # call the arctan expansion function passing through x and N
            print("arctan("+str(x)+") =",arctan) 
            self.outputText1.set("Your Input:\n x = "+str(xUnevaluated)+"\nN = "+str(N)+"\n\nOutput:\narctan("+str(x)+") = "+str(arctan)) # display the reults on the GUI
            self.update_idletasks() # this makes sure that all code up to this point has been executed, it is needed for the line below , we need to make sure the text has been put to the label before we calculate its width.
            self.output1.place(x=200-self.output1.winfo_width()/2, y=190) # used to make sure that the output is central to the window
            
            #plt.plot(range(N+1), part) # this was used to show how the value for arctan changes as more terms are added up to N
            #plt.ylim(-0.001,0.001)
            #plt.show()
            #plt.plot(range(N+1), arctanArr, "g-")
            #plt.show()
        
    def submit2(self): # when the user clicks calculate for part (d).
        try: # performs the same validation routine for N as it did for part (a)
            N = self.textInput3.get()
            N = int(N)
            if N > 0:
                self.inputErrorText3.set("")
            else:
                self.inputErrorText3.set("Enter a value greater than 0")
                print(N, "is not greater than 0")
        except:
            print(N, "is not an int")
            self.inputErrorText3.set("Enter an integer")
        
        if self.inputErrorText3.get() == "": # if there was no error with the users input.
            xMin = -2 # initialising variables
            xMax = 2
            xSteps = 0.01
            xArr = [0.0]*(int((xMax-xMin)/xSteps)+1) # create an empty array of floats with the correct number of spaces for x between -2 and 2 with intervals of 0.01 i.e. 400
            yArr = [0.0]*(int((xMax-xMin)/xSteps)+1)
            yArr2 = [0.0]*(int((xMax-xMin)/xSteps)+1)
            n=0
            for x in np.arange(xMin,xMax+xSteps,xSteps): # this creates 400 values of x incrementing by 0.01 from -2 until 2 inclusively. np.arange makes it possible to increment by a floating point value, (the xMax+xSteps makes sure that it is inclusive of 2)
                xArr[n] = x # put x value in this array
                yArr[n] = math.atan(x) #np.arctan(x) # can use numpy here too, this appends values of arctan(x) from the built in maths functions
                arctan, arctanArr, part = arctanExpansion(x,N) #calls our expansion function
                yArr2[n] = arctan # populates another y array with our values of arctan.
                n+=1 #increment n by 1
                
            self.outputText2.set("Your Input:\nN = "+str(N)+"\n\nOutput:\n") #display the output
            self.update_idletasks() # make sure any idle tasks have been executed
            self.output2.place(x=200-self.output2.winfo_width()/2, y=115) #centre the output
            plt.plot(xArr, yArr, "b-", xArr, yArr2,"g-") #produce a graph with two lines, blue line is arctan(x) generated by built in function, green line is arctan(x) generated by taylor expansion
            plt.xlim(-2,2) #this forces the x limits on the graph to be -2 and 2
            #plt.show() # this is for displaying the graph in the console
            
            try: # try and remove the output.png file, but if it can't because it doesn't exist that doesn't matter.
                os.remove("output.png") # remove the old file output.png if there is one # checking that this
            except:
                pass
            plt.savefig("output.png", dpi=160, bbox_inches="tight") #save the plot as a png called output, dpi is dots per inch, bbox_inches = "tight" represents no wasted space on the outside of the plot
            plt.close() #close the plot now that we have finished
            
            self.openGraphButton.place(x=170,y=160) #place the open graph button
            self.graphGenerated = True # set this variable to show that a graph has been generated
    
    def openGraph(self): #this function is called when the open graph button is clicked
        image = Image.open('output.png') # here we load the image output.png
        image.show() # here we display the image output.png
        
    def submit3(self): # when the user clicks calculate for part (f) this code is run.
        try: # same try-catch loop as for part(a) and (d)
            N = self.textInput4.get()
            N = int(N)
            if N > 0:
                self.inputErrorText4.set("")
            else:
                self.inputErrorText4.set("Enter a value greater than 0")
                print(N, "is not greater than 0")
        except:
            print(N, "is not an int")
            self.inputErrorText4.set("Enter an integer")
        
        if  self.inputErrorText4.get() == "": # if there is no error with N
            x = [0.0]*3 # set x to be an empty float array with 3 values
            term = [0.0]*3 # set term to be an empty float array with 3 values
            x[0] = 0.5 # set the first value in x to be 1/2
            x[1] = 0.2
            x[2] = 0.125
            
            for i in range(3): # i increases by 1 until before 3 starting at 0
                arctan, arctanArr, part = arctanExpansion(x[i],N) #calculate the arctan of x using the expansion function
                term[i]= arctan # add the value of arctan(x) to the term array
            piApprox = 4*(term[0]+term[1]+term[2]) # add together all of the terms and multiply by 4 to get an approximation for pi
            print("Pi is approxamately:", piApprox)
            piErr = math.pi-piApprox # calculate the error on pi based on the built in computer value.
            print("The error on that value of pi is:", piErr)
            self.outputText3.set("Your Input:\nN = "+str(N)+"\n\nOutput:\nPi is approximately: "+str(piApprox)+"\nWith an error: "+str(piErr)) #display the result
            self.update_idletasks()       
            self.output3.place(x=200-self.output3.winfo_width()/2, y=115) # centre the output
            

root = Tk() #Tk() is a function in tkinter
root.geometry("400x400") #setting the size of the window

app = Window(root) # calls the Window class
root.mainloop() # opens the GUI




#######################################################################################################################
###                                                   VERSION WITHOUT GUI                                           ###
#######################################################################################################################
                                                   
#
#def arctanExpansion(x,N):
#    """
#    This function calculates the series expansion for arctan(x) it can deal with x is any real number. The number of
#    iterations the user wants is specified in the integer argument N; and the floating point argument, x, is the value of x 
#    to put into arctan(x). The user specifies both of these values.
#    """
#    inverseXpositive = False
#    inverseXnegative = False
#    if abs(x)>1:
#        if x>0:
#            inverseXpositive = True
#        else:
#            inverseXnegative = True
#        x = 1/x
#    arctan = 0
#    part = [0.0]*(N+1)
#    arctanArr = [0.0]*(N+1)
#    for n in range(N+1):
#        part[n] = (((-1)**n/(2*n+1))*x**(2*n+1))
#        arctan += part[n]
#        arctanArr[n] = (arctan)
#    if inverseXpositive == True:
#        return math.pi/2-arctan, arctanArr, part
#    elif inverseXnegative == True:
#        return -math.pi/2-arctan, arctanArr, part
#    else:
#        return arctan, arctanArr, part
#
#MyInput = "0"
#while MyInput != "q":
#    MyInput = input("Enter a choice, 'a', 'd', 'e', 'f' or 'q' to quit: ")
#    print("You entered the choice: ", MyInput)
#    if MyInput == "a":
#        print("You have chosen part (a)")
#        """
#        In this section the user can input values for x and N and the program will calculate a value for arctan(x) 
#        using N itereations in the Taylor expansion. It also displays a graph which shows how the value of 
#        arctan(x) changes with N.
#        """
#        
#        isint = False
#        while isint == False:
#            N = input("Please enter a value for N (positive integer):")
#            try:
#                N = int(N)
#                if N > 0:
#                    isint = True
#                else:
#                    isint = False
#                    print(N, "is not greater than 0")
#            except:
#                isint = False
#                
#        isfloat = False
#        while isfloat == False:
#            xUnevaluated = input("Please enter a value for x (float):")
#            try:
#                x = float(eval(xUnevaluated))
#                isfloat = True
#            except:
#                isfloat = False
#                print(xUnevaluated, "is not a float or cannot be evaluated")
#                
#        arctan,arctanArr,part = arctanExpansion(x,N)
#        print("artan("+str(x)+") =",arctan)
#        
#        plt.plot(range(N+1), part)
#        plt.ylim(-0.001,0.001)
#        plt.show()
#        plt.plot(range(N+1), arctanArr, "g-")
#        plt.show()
#        
#    elif MyInput == "d":
#        print("You have chosen part (d)")
#        """
#        This section iterates over values of x from -2 to 2 and compares our function of arctan 
#        to the computer built in function of arctan with values of N inputted by the user.
#        """
#        
#        xMin = -2
#        xMax = 2
#        xSteps = 0.01
#        
#        isint = False
#        while isint == False:
#            N = input("Please enter a value for N (positive integer):")
#            try:
#                N = int(N)
#                if N > 0:
#                    isint = True
#                else:
#                    isint = False
#                    print(N, "is not greater than 0")
#            except:
#                isint = False
#                print(N, "is not an int")
#        
#        x = xMin
#        xArr = [0.0]*(int((xMax-xMin)/xSteps))
#        yArr = [0.0]*(int((xMax-xMin)/xSteps))
#        yArr2 = [0.0]*(int((xMax-xMin)/xSteps))
#        yArr3 = [0.0]*(int((xMax-xMin)/xSteps))
#        n=0
#        while x<=xMax: #change this to for x in range(-2,2, 0.01):
#            xArr[n] = x
#            yArr[n] = math.atan(x)
#            arctan, arctanArr, part = arctanExpansion(x,N)
#            yArr2[n] = arctan
#            yArr3[n] = math.atan(x)-arctan
#            x += xSteps
#            n+=1
#            
#        plt.plot(xArr, yArr, "b-", xArr, yArr2,"g-")
#        plt.show()
#        
#        plt.plot(xArr, yArr3)
#        plt.show()
#        #plt.plot(range(N+1), arctanArr, "g-")
#        #plt.show()
#        
#    elif MyInput == "e":
#        print("You have chosen part (e)")
#        """
#        This section calculates an approximation to pi using 4*artan(1) = pi. 
#        It will also produce a graph showing how the value converges.
#        """
#        isint = False
#        while isint == False:
#            N = input("Please enter a value for N (positive integer):")
#            try:
#                N = int(N)
#                if N > 0:
#                    isint = True
#                else:
#                    isint = False
#                    print(N, "is not greater than 0")
#            except:
#                isint = False
#                print(N, "is not an int")
#        
#        start = time.time()
#
#        arctan, arctanArr, part = arctanExpansion(1,N)
#        piApproxArr = []
#        for items in arctanArr:
#            piApproxArr.append(items*4)
#            
#        upperBoundary = round(round(math.pi,7)+0.00000005,8)
#        lowerBoundary = round(round(math.pi,7)-0.00000005,8)
#        plt.plot(range(N+1), piApproxArr, "b-", range(N+1), [upperBoundary]*(N+1),"g-", range(N+1), [lowerBoundary]*(N+1),"g-")
#        #plt.ylim(3.14159,3.1416)
#        plt.show()
#        print(arctan*4, math.pi, arctan*4-math.pi)
#        if arctan*4<upperBoundary and arctan*4>lowerBoundary:
#            print("Correct to 7dp")
#        else:
#            print("Value of N not big enough")
#        end = time.time()
#        print("Time elapsed:", end-start)
#        
#        
#    elif MyInput == "f":
#        print("You have chosen part (f)")
#        """
#        This section calculates an approxamation to pi, The user can choose a number of iterations, the more iterations the more
#        accurate the result. This makes use of the fact that: pi/4 = arctan(1/2)+arctan(1/5)+arctan(1/8)
#        """
#        x = [0.0]*3
#        term = [0.0]*3
#        arctanArr = [[]]*3
#        x[0] = 0.5
#        x[1] = 0.2
#        x[2] = 0.125
#        
#        isint = False
#        while isint == False:
#            N = input("Please enter a value for N (positive integer):")
#            try:
#                N = int(N)
#                if N > 0:
#                    isint = True
#                else:
#                    isint = False
#                    print(N, "is not greater than 0")
#            except:
#                isint = False
#                print(N, "is not an int")
#                
#        start = time.time()
#                
#        for i in range(3):
#            arctan, arctanArr[i], part = arctanExpansion(x[i],N)
#            term[i]= arctan
#            
#        piApproxArr = [0.0]*(N+1)
#        for n in range(N+1):
#            piApproxArr[n] = 4*(arctanArr[0][n]+arctanArr[1][n]+arctanArr[2][n])
#        
#        plt.plot(range(N+1), piApproxArr,"b-" , range(N+1),[math.pi]*(N+1) ,"g-")
#        plt.show()        
#        
#        piApprox = 4*(term[0]+term[1]+term[2])
#        print("Pi is approxamately:", piApprox)
#        piErr = math.pi-piApprox
#        print("The error on that value of pi is:", piErr)
#        
#        upperBoundary = round(round(math.pi,12)+0.0000000000005,13)
#        lowerBoundary = round(round(math.pi,12)-0.0000000000005,13)        
#        
#        if piApprox<upperBoundary and piApprox>lowerBoundary:
#            print("Correct to 12dp")
#        else:
#            print("Value of N not big enough")
#        end = time.time()
#        print("Time elapsed:", end-start)
#        
#    else:
#        if MyInput != "q":
#            print("This is not a valid choice")
#print("You have chosen to finish - goodbye.")
