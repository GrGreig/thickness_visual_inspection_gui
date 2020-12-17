import tkinter as tk
import os.path
import pandas as pd
import numpy as np
import datetime as dt
from tkinter import filedialog

entryY = 100
entryX = 20

def getImageNames():
    #Have the user select images
    filePath = filedialog.askopenfilenames(initialdir = 'C:/Users/Graham Greig/Documents/Python Scripts/DataFileGUIs/', title = 'Select Images')

    #Insert the image names into the listbox.
    for i in filePath:
        fileName = i.split('/').pop()
        for j in range(10):
            if fileEntry.get(j) == "" : 
                fileEntry.delete(j)
                fileEntry.insert(j,fileName)
                break
            outVar.set('Error: Too many files selected. The limit is 10. Remove one or more files to insert.')

def removeSelected():
    index = fileEntry.curselection()
    fileEntry.delete(index)

def saveData():
    vpx = vpxVar.get()
    wafer = wVar.get()
    comment = commentBox.get('1.0','end-1c')

    #Check if the all fields have been filled
    if vpx == "" or wafer == "" or passFail.curselection() == ():
        outVar.set('Please make sure all mandatory values have been entered and try again.')
    # If they have been filled save a data file.
    else :
    
        #Get information from the config file then open the inventory list and check if the sensor is in there.
        config = open('visual_inspection_config.txt', 'r')
        lines = config.readlines()
        pathToSave = lines[1].rstrip()
        pathToInventory = lines[3].rstrip() + 'inventory.csv'
        config.close()
        
        #pathToSave = '' #'C:/Users/Graham Greig/Documents/Python Scripts/'
        #pathToInventory = 'C:/Users/Graham Greig/Desktop/production_database_scripts-master_old/production_database_scripts-master/inventory.csv'
        data = pd.read_csv(pathToInventory, header=1) 
        IDs = data['ID'].tolist()
        SNs = data['#serialNumber'].tolist()
        locations = data['currentLocation'].tolist()
        sensorTypes = data['type'].tolist()

        #IDExists = false
        targetID = 'VPX' + vpx + '-W' + wafer
        if targetID not in IDs:
            outVar.set('Could not find this sensor in the inventory. Make sure the sensor '
            'has been recived and the inventory list has been updated.')
        else : 
            #
        
            #Get the index of the row to have data extracted from.
            filePrefix = 'VPX%s-W%05d_VisInspection_' % (vpx, int(wafer)) 
            row = IDs.index(targetID)

            #Get the strings to make the header file.
            SN = SNs[row]
            location = locations[row]
            sensorType = sensorTypes[row]
            date = dt.datetime.now().strftime('%d %b %Y')
            time = dt.datetime.now().time()
            time = time.replace(microsecond=0)

            # Determine the data file to write to.
            numfile = 1
            fileName = filePrefix + '001.dat'
            fullPath = pathToSave + fileName
            while os.path.exists(fullPath) :
                numfile += 1
                if numfile < 10 :
                    fileName = filePrefix + '00' + str(numfile) + '.dat'
                elif numfile < 100 :
                    fileName = filePrefix + '0' + str(numfile) + '.dat'
                else:
                    fileName = filePrefix + str(numfile) + '.dat'
                fullPath = pathToSave + fileName
            
            #Open the data file and write to it.
            f = open(fullPath,'w+')
            f.write(fileName + '\n')
            f.write('Type: ' + sensorType + '\n')
            f.write('Batch: VPX' + vpx + '\n')
            f.write('Wafer: %05d\n' % int(wafer))
            f.write('Component: ' + SN + '\n')
            f.write('Date: ' + str(date) + '\n')
            f.write('Time: '+ str(time) + '\n')
            f.write('Institute: ' + location + '\n')
            f.write('TestType: ATLAS18_VIS_INSPECTION_V1\n')
            f.write('Result: ' + passFail.get(passFail.curselection()[0]) + '\n')
            f.write('Comments: ' + comment + '\n')
            index = 1
            for i in range(10) :
                imageName = fileEntry.get(i)
                if imageName != "" :
                    f.write('Image' + str(index) + ": " + imageName + '\n')
                    index += 1
            f.close()
            outVar.set('File ' + fileName + ' Saved!')

# GUI Setup              
root = tk.Tk()

outVar = tk.StringVar()
vpxVar = tk.StringVar()
wVar = tk.StringVar()
thicknessVar = tk.StringVar()
commentVar = tk.StringVar()

frame = tk.Frame(root, height = 600, width = 390)
frame.pack()

title = tk.Label(frame, text = 'Sensor Visual Inspection Data \n Production', font = ('calibri', 18))
title.place(x = 40, y = 10 )

savebutton = tk.Button(frame, text = "Save Data", command = lambda: saveData())
savebutton.place(x = entryX + 280, rely = 0.9)

browserbutton = tk.Button(frame, text = "Find Image Names", command = lambda: getImageNames())
browserbutton.place(x = entryX + 200, y = entryY)

removebutton = tk.Button(frame, text = "Remove Selected", command = lambda: removeSelected())
removebutton.place(x = entryX + 200, y = entryY + 240)

passFail = tk.Listbox(frame, width = 5, relief = 'groove', height = '2')
passFail.place(x = entryX + 140, y = entryY)
passFail.insert(0,"Pass")
passFail.insert(1,"Fail")





#Setup the File entry blocks
fileEntryLabel = tk.Label(frame, text = "Image Names")
fileEntryLabel.place(x = entryX, y = entryY + 40)
fileEntry = tk.Listbox(frame, width = 50,relief = 'groove')
fileEntry.insert(0,"")
fileEntry.insert(1,"")
fileEntry.insert(2,"")
fileEntry.insert(3,"")
fileEntry.insert(4,"")
fileEntry.insert(5,"")
fileEntry.insert(6,"")
fileEntry.insert(7,"")
fileEntry.insert(8,"")
fileEntry.insert(9,"")
fileEntry.place(x = entryX, y = entryY + 60)

VPXLabel = tk.Label(frame, text = 'VPX')
VPXLabel.place(x = entryX, y = entryY)
VPXBox = tk.Entry(frame, textvariable = vpxVar, justify = 'left' , width = 5)
VPXBox.place(x = entryX + 30, y = entryY)

WaferLabel = tk.Label(frame, text = 'W')
WaferLabel.place(x = entryX + 70, y = entryY)
WaferBox = tk.Entry(frame, textvariable = wVar, justify = 'left' , width = 5)
WaferBox.place(x = entryX + 89, y = entryY)

commentLabel = tk.Label(frame, text = 'Comments')
commentLabel.place(x = entryX, y = entryY + 270)
commentBox = tk.Text(frame, width = 49, height = 2, font = ('calibri', 10))
commentBox.place(x = entryX, y = entryY + 290)

outBox = tk.Message(frame, textvariable = outVar, font = ('calibri', 10), width = 344, relief = 'sunken', justify = 'left')
outBox.place(x = entryX, y = entryY + 340)
outVar.set('Please enter the sensor VPX, wafer number and optional comment field. Select Pass of fail. To insert file names, browse for the files and'
'shift select all you would like up to a maximum of 10. Saving will produce a database ready .dat file.')

root.mainloop()
