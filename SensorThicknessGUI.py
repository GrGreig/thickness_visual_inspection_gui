import tkinter as tk
import os.path
import pandas as pd
import numpy as np
import datetime as dt

entryY = 100
entryX = 20

def SaveData():
    measurements = thicknessVar.get()
    vpx = vpxVar.get()
    wafer = wVar.get()
    comment = commentBox.get('1.0','end-1c')

    #Check if the all fields have been filled
    if measurements == "" or vpx == "" or wafer == "":
        outVar.set('Please make sure all values have been entered and try again.')
    # If they have been filled save a data file.
    else :
        # Compute the average thickness
        measureList = measurements.split()
        floatList = [float(item) for item in measureList]
        thickness = sum(floatList)/len(floatList)

        #Get information from the config file then open the inventory list and check if the sensor is in there.
        config = open('thickness_config.txt', 'r')
        lines = config.readlines()
        pathToSave = lines[1].rstrip()
        pathToInventory = lines[3].rstrip() + 'sensor_inventory.csv'
        instrument = lines[5].rstrip()
        config.close()

        #pathToSave = '' #'C:/Users/Graham Greig/Documents/Python Scripts/'
        #pathToInventory = 'C:/Users/Graham Greig/Desktop/production_database_scripts-master_old/production_database_scripts-master/inventory.csv'
        data = pd.read_csv(pathToInventory, header=1) 
        IDs = data['alternativeIdentifier'].tolist()
        SNs = data['#serialNumber'].tolist()
        locations = data['currentLocation'].tolist()
        sensorTypes = data['type'].tolist()

        #IDExists = false
        targetID = 'VP' + vpx + '-W' + wafer
        if targetID not in IDs:
            outVar.set('Could not find this sensor in the inventory. Make sure the sensor '
            'has been recived and the inventory list has been updated.')
        else : 
            #Get the index of the row to have data extracted from.
            filePrefix = 'VP%s-W%05d_HMThickness_' % (vpx, int(wafer)) 
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
            f.write('Batch: VP' + vpx + '\n')
            f.write('Wafer: %05d\n' % int(wafer))
            f.write('Component: ' + SN + '\n')
            f.write('Date: ' + str(date) + '\n')
            f.write('Time: '+ str(time) + '\n')
            f.write('Institute: ' + location + '\n')
            f.write('TestType: ATLAS18_HM_THICKNESS_V1\n')
            f.write('Instrument: ' + instrument + '\n')
            f.write('RunNumber: ' + str(numfile) + '\n')
            f.write('Comments: ' + comment + '\n')
            f.write('AvThickness: ' + str(thickness) + '\n')
            f.close()
            outVar.set('File ' + fileName + ' Saved!')

# GUI Setup              
root = tk.Tk()

outVar = tk.StringVar()
vpxVar = tk.StringVar()
wVar = tk.StringVar()
thicknessVar = tk.StringVar()
commentVar = tk.StringVar()

frame = tk.Frame(root, height = 350, width = 390)
frame.pack()

title = tk.Label(frame, text = 'Sensor Thickness Data Production', font = ('calibri', 18))
title.place(x = 25, y = 40 )

savebutton = tk.Button(frame, text = "Save Data", command = lambda: SaveData())
savebutton.place(x = entryX + 280, rely = 0.9)

VPXLabel = tk.Label(frame, text = 'VP')
VPXLabel.place(x = entryX, y = entryY)
VPXBox = tk.Entry(frame, textvariable = vpxVar, justify = 'left' , width = 6)
VPXBox.place(x = entryX + 20, y = entryY)

WaferLabel = tk.Label(frame, text = 'W')
WaferLabel.place(x = entryX + 70, y = entryY)
WaferBox = tk.Entry(frame, textvariable = wVar, justify = 'left' , width = 5)
WaferBox.place(x = entryX + 89, y = entryY)

thicknessLabel = tk.Label(frame, text = 'Measurements (um)')
thicknessLabel.place(x = entryX + 130, y = entryY)
thicknessBox = tk.Entry(frame, textvariable = thicknessVar, justify = 'left' , width = 16)
thicknessBox.place(x = entryX + 245, y = entryY)

commentLabel = tk.Label(frame, text = 'Comments')
commentLabel.place(x = entryX, y = entryY +  40)
commentBox = tk.Text(frame, width = 49, height = 2, font = ('calibri', 10))
commentBox.place(x = entryX, y = entryY + 60)

outBox = tk.Message(frame, textvariable = outVar, font = ('calibri', 10), width = 344, relief = 'sunken', justify = 'left')
outBox.place(x = entryX, y = entryY + 120)
outVar.set('Please fill all fields and the optional comment field then press save to produce a sensor thickness data file.'
'Multiple thickness values can be entered but must be separated by a space.')

root.mainloop()

