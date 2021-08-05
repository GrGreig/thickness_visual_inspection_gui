import tkinter as tk
import os.path
import pandas as pd
import numpy as np
import datetime as dt
from tkinter import *
from tkinter import filedialog

entryY = 100
entryX = 20

def get_image_names(file_entry_box, limit):
    """Gets the image names for the given file entry box. Will only allow up to 4 images."""
    #Have the user select an image
    file_path = filedialog.askopenfilenames(initialdir = 'C:/Users/Graham Greig/Documents/Python Scripts/DataFileGUIs/', title = 'Select Images')

    #Insert the image name into the listbox.
    for i in file_path:
        file_name = i.split('/').pop()
        for j in range(limit):
            if file_entry_box.get(j) == "" : 
                file_entry_box.delete(j)
                file_entry_box.insert(j,file_name)
                break
            output_text.set('Error: Too many images selected. The limit is ' + str(limit) + '. Only taking initial files and will not overwite.'
            ' Remove images if you wish to replace.')

def remove_selected(file_entry_box):
    """Removes the selected images from the given file entry box."""
    index = file_entry_box.curselection()
    file_entry_box.delete(index)

def get_file_output_name_and_path(file_prefix, path_to_save):
    """Determines the name of the file path and file path by searching if previous files have been saved.
    Returns the file name and the full path to the file."""
    n = 1
    file_name = file_prefix + '001.dat'
    full_path = path_to_save + file_name
    while os.path.exists(full_path) :
        n += 1
        file_name = file_prefix + f"{n:03d}.dat"
        full_path = path_to_save + file_name
    run_number = n
    return file_name, full_path, run_number

def get_config_data():
    """Extracts necessary data from the config file like the path to the inventory and the path to save."""
    current_directory = os.path.dirname(__file__)
    config = open((current_directory + '/visual_inspection_config.txt'), 'r')
    lines = config.readlines()
    path_to_save = lines[1].rstrip()
    path_to_inventory = lines[3].rstrip() + 'inventory.csv'
    config.close()
    return path_to_inventory, path_to_save

def get_sensor_data(path_to_inventory):
    """Gets lists of IDs, Serial numbers, locations and sensor types from the Inventory list."""
    data = pd.read_csv(path_to_inventory, header=1) 
    IDs = data['ID'].tolist()
    SNs = data['#serialNumber'].tolist()
    locations = data['currentLocation'].tolist()
    sensor_types = data['type'].tolist()
    return IDs, SNs, locations, sensor_types

def write_defect_text(file_entry_box, defect_type, defect_location, file, index):
    """Generates fromatted text for damage type, location and image. Writes this to the file."""
    image_string = 'Images' + str(index) + ': '
    start_flag = False
    for i in range(4):
        image_name = file_entry_box.get(i)
        if image_name != "":
            if start_flag == False:
                image_string += image_name
                start_flag = True
            else:
                image_string += ', ' + image_name
    if image_string != 'Images' + str(index) + ': ':
        file.write('Location' + str(index) + ': ' + defect_location.get() + '\n')
        file.write('DamageType' + str(index) + ': ' + defect_type.get() + '\n')
        file.write(image_string + '\n')

def save_data():
    """Composes a text file and saves the data to it in the database file format."""
    vpx = vpx_variable.get()
    wafer = w_variable.get()
    comment = comment_box.get('1.0','end-1c')

    #Check if the all fields have been filled
    if vpx == "" or wafer == "" or pass_fail_box.curselection() == ():
        output_text.set('Please make sure all mandatory values have been entered and try again.')
    # If they have been filled save a data file.
    else :
    
        #Get information from the config file then open the inventory list and 
        #check if the sensor is in there.
        path_to_inventory, path_to_save = get_config_data()
        
        IDs, SNs, locations, sensor_types = get_sensor_data(path_to_inventory)
        
        #IDExists = false
        target_id = 'VPX' + vpx + '-W' + wafer
        if target_id not in IDs:
            output_text.set('Could not find this sensor in the inventory. Make sure the sensor '
            'has been recived and the inventory list has been updated.')
        else : 
            #Get the index of the row to have data extracted from.
            file_prefix = 'VPX%s-W%05d_VisInspectionV2_' % (vpx, int(wafer)) 
            row = IDs.index(target_id)

            #Get the strings to make the header for file.
            SN = SNs[row]
            location = locations[row]
            sensor_type = sensor_types[row]
            date = dt.datetime.now().strftime('%d %b %Y')
            time = dt.datetime.now().time()
            time = time.replace(microsecond=0)

            # Determine the data file to write to.
            file_name, full_path, run_number = get_file_output_name_and_path(file_prefix, path_to_save)
            
            #Open the data file and write to it.
            file = open(full_path,'w+')
            file.write(file_name + '\n')
            file.write('Type: ' + sensor_type + '\n')
            file.write('Batch: VPX' + vpx + '\n')
            file.write('Wafer: %05d\n' % int(wafer))
            file.write('Component: ' + SN + '\n')
            file.write('Date: ' + str(date) + '\n')
            file.write('Time: '+ str(time) + '\n')
            file.write('Institute: ' + location + '\n')
            file.write('TestType:' + test_selection.get() + '\n')
            file.write('RunNumber: ' + str(run_number) + '\n')
            file.write('Result: ' + pass_fail_box.get(pass_fail_box.curselection()[0]) + '\n')
            file.write('Comments: ' + comment + '\n')
            file.write('ScratchPadImage: ' + scratch_pad_box.get(0) + '\n')
        
            #Now go through the boxes and add each damage type if they are filled.
            write_defect_text(file_entry_box_1, choosen_defect_1, defect_location_1_box, file, 1)
            write_defect_text(file_entry_box_2, choosen_defect_2, defect_location_2_box, file, 2)
            write_defect_text(file_entry_box_3, choosen_defect_3, defect_location_3_box, file, 3)
            write_defect_text(file_entry_box_4, choosen_defect_4, defect_location_4_box, file, 4)
            write_defect_text(file_entry_box_5, choosen_defect_5, defect_location_5_box, file, 5)
            write_defect_text(file_entry_box_6, choosen_defect_6, defect_location_6_box, file, 6)

            file.close()
            output_text.set('File ' + file_name + ' Saved!')

# GUI Setup              
root = tk.Tk()

output_text = tk.StringVar()
vpx_variable = tk.StringVar()
w_variable = tk.StringVar()
thickness_variable = tk.StringVar()
comment_variable = tk.StringVar()
location_variable_1 = tk.StringVar()
location_variable_2 = tk.StringVar()
location_variable_3 = tk.StringVar()
location_variable_4 = tk.StringVar()
location_variable_5 = tk.StringVar()
location_variable_6 = tk.StringVar()

frame = tk.Frame(root, height = 600, width = 1050)
frame.pack()

title = tk.Label(frame, text = 'Sensor Visual Inspection Data \n Production', font = ('calibri', 18))
title.place(x = 40, y = 10 )

save_button = tk.Button(frame, text = "Save Data", command = lambda: save_data())
save_button.place(x = entryX + 150, rely = 0.9)

browser_button_1 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_1, 4))
browser_button_1.place(x = 720, y = 30)

browser_button_2 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_2, 4))
browser_button_2.place(x = 720, y = 120)

browser_button_3 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_3, 4))
browser_button_3.place(x = 720, y = 210)

browser_button_4 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_4, 4))
browser_button_4.place(x = 720, y = 300)

browser_button_5 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_5, 4))
browser_button_5.place(x = 720, y = 390)

browser_button_6 = tk.Button(frame, text = "Find Image Names", command = lambda: get_image_names(file_entry_box_6, 4))
browser_button_6.place(x = 720, y = 480)

browser_button_scratch_pad = tk.Button(frame, text = "Find Image Name", command = lambda: get_image_names(scratch_pad_box, 1))
browser_button_scratch_pad.place(x = entryX + 260, y = entryY + 170)

remove_button_scratch_pad = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(scratch_pad_box))
remove_button_scratch_pad.place(x = entryX + 260, y = entryY + 210)

remove_button_1 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_1))
remove_button_1.place(x = 720, y = 70)

remove_button_2 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_2))
remove_button_2.place(x = 720, y = 160)

remove_button_3 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_3))
remove_button_3.place(x = 720, y = 250)

remove_button_4 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_4))
remove_button_4.place(x = 720, y = 340)

remove_button_5 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_5))
remove_button_5.place(x = 720, y = 430)

remove_button_6 = tk.Button(frame, text = "Remove Selected", command = lambda: remove_selected(file_entry_box_6))
remove_button_6.place(x = 720, y = 520)

pass_fail_box = tk.Listbox(frame, width = 5, relief = 'groove', height = '2')
pass_fail_box.place(x = entryX + 135, y = entryY)
pass_fail_box.insert(0,"Pass")
pass_fail_box.insert(1,"Fail")

#Setup the File entry blocks
file_entry_box_1_label = tk.Label(frame, text = "Defect 1 Image Names")
file_entry_box_1_label.place(x = 400, y = 10)
file_entry_box_1 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_1.insert(0,"")
file_entry_box_1.insert(1,"")
file_entry_box_1.insert(2,"")
file_entry_box_1.insert(3,"")
file_entry_box_1.place(x = 400, y = 30)

file_entry_box_2_label = tk.Label(frame, text = "Defect 2 Image Names")
file_entry_box_2_label.place(x = 400, y = 100)
file_entry_box_2 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_2.insert(0,"")
file_entry_box_2.insert(1,"")
file_entry_box_2.insert(2,"")
file_entry_box_2.insert(3,"")
file_entry_box_2.place(x = 400, y = 120)

file_entry_box_3_label = tk.Label(frame, text = "Defect 3 Image Names")
file_entry_box_3_label.place(x = 400, y = 190)
file_entry_box_3 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_3.insert(0,"")
file_entry_box_3.insert(1,"")
file_entry_box_3.insert(2,"")
file_entry_box_3.insert(3,"")
file_entry_box_3.place(x = 400, y = 210)

file_entry_box_4_label = tk.Label(frame, text = "Defect 4 Image Names")
file_entry_box_4_label.place(x = 400, y = 280)
file_entry_box_4 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_4.insert(0,"")
file_entry_box_4.insert(1,"")
file_entry_box_4.insert(2,"")
file_entry_box_4.insert(3,"")
file_entry_box_4.place(x = 400, y = 300)

file_entry_box_5_label = tk.Label(frame, text = "Defect 5 Image Names")
file_entry_box_5_label.place(x = 400, y = 370)
file_entry_box_5 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_5.insert(0,"")
file_entry_box_5.insert(1,"")
file_entry_box_5.insert(2,"")
file_entry_box_5.insert(3,"")
file_entry_box_5.place(x = 400, y = 390)

file_entry_box_6_label = tk.Label(frame, text = "Defect 6 Image Names")
file_entry_box_6_label.place(x = 400, y = 460)
file_entry_box_6 = tk.Listbox(frame, width = 50, height = 4, relief = 'groove')
file_entry_box_6.insert(0,"")
file_entry_box_6.insert(1,"")
file_entry_box_6.insert(2,"")
file_entry_box_6.insert(3,"")
file_entry_box_6.place(x = 400, y = 480)

scratch_pad_box_label = tk.Label(frame, text = "Scratch Pad Image (Optional)")
scratch_pad_box_label.place(x = entryX, y = entryY + 170)
scratch_pad_box = tk.Listbox(frame, width = 40, height = 1, relief = 'groove')
scratch_pad_box.insert(0,"")
scratch_pad_box.place(x = entryX, y = entryY + 190)

choosen_defect_1 = StringVar()
choosen_defect_1.set("")

choosen_defect_2 = StringVar()
choosen_defect_2.set("")

choosen_defect_3 = StringVar()
choosen_defect_3.set("")

choosen_defect_4 = StringVar()
choosen_defect_4.set("")

choosen_defect_5 = StringVar()
choosen_defect_5.set("")

choosen_defect_6 = StringVar()
choosen_defect_6.set("")

defect_type_1 = tk.OptionMenu(frame, choosen_defect_1, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_1.place(x = 840, y = 28)

defect_type_2 = tk.OptionMenu(frame, choosen_defect_2, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_2.place(x = 840, y = 118)

defect_type_3 = tk.OptionMenu(frame, choosen_defect_3, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_3.place(x = 840, y = 208)

defect_type_4 = tk.OptionMenu(frame, choosen_defect_4, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_4.place(x = 840, y = 298)

defect_type_5 = tk.OptionMenu(frame, choosen_defect_5, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_5.place(x = 840, y = 388)

defect_type_6 = tk.OptionMenu(frame, choosen_defect_6, "", "mark", "debris", "scuffing", "suction cup mark", 
"blotch", "pit", "deposit", "scratch", "deep scratch", "chip", "mismatched serial number", "metal short",
"metal break")
defect_type_6.place(x = 840, y = 478)

defect_location_label_1 = tk.Label(frame, text = 'Defect Location')
defect_location_label_1.place(x = 840, y = 60)
defect_location_1_box = tk.Entry(frame, textvariable = location_variable_1, justify = 'left' , width = 30)
defect_location_1_box.place(x = 840, y = 80)

defect_location_label_2 = tk.Label(frame, text = 'Defect Location')
defect_location_label_2.place(x = 840, y = 150)
defect_location_2_box = tk.Entry(frame, textvariable = location_variable_2, justify = 'left' , width = 30)
defect_location_2_box.place(x = 840, y = 170)

defect_location_label_3 = tk.Label(frame, text = 'Defect Location')
defect_location_label_3.place(x = 840, y = 240)
defect_location_3_box = tk.Entry(frame, textvariable = location_variable_3, justify = 'left' , width = 30)
defect_location_3_box.place(x = 840, y = 260)

defect_location_label_4 = tk.Label(frame, text = 'Defect Location')
defect_location_label_4.place(x = 840, y = 330)
defect_location_4_box = tk.Entry(frame, textvariable = location_variable_4, justify = 'left' , width = 30)
defect_location_4_box.place(x = 840, y = 350)

defect_location_label_5 = tk.Label(frame, text = 'Defect Location')
defect_location_label_5.place(x = 840, y = 420)
defect_location_5_box = tk.Entry(frame, textvariable = location_variable_5, justify = 'left' , width = 30)
defect_location_5_box.place(x = 840, y = 440)

defect_location_label_6 = tk.Label(frame, text = 'Defect Location')
defect_location_label_6.place(x = 840, y = 510)
defect_location_6_box = tk.Entry(frame, textvariable = location_variable_6, justify = 'left' , width = 30)
defect_location_6_box.place(x = 840, y = 530)

vpx_label = tk.Label(frame, text = 'VPX')
vpx_label.place(x = entryX, y = entryY)
vpx_box = tk.Entry(frame, textvariable = vpx_variable, justify = 'left' , width = 5)
vpx_box.place(x = entryX + 30, y = entryY)

wafer_label = tk.Label(frame, text = 'W')
wafer_label.place(x = entryX + 70, y = entryY)
wafer_box = tk.Entry(frame, textvariable = w_variable, justify = 'left' , width = 5)
wafer_box.place(x = entryX + 89, y = entryY)

test_selection = tk.StringVar()
test_selection.set("ATLAS18_VIS_INSPECTION_V2")

test_type = tk.OptionMenu(frame, test_selection, "ATLAS18_VIS_INSPECTION_V2", "VIS_INSP_RES_MOD_V2")
test_type.place(x = entryX + 170, y = entryY)

comment_label = tk.Label(frame, text = 'Comments (Optional)')
comment_label.place(x = entryX, y = entryY + 40)
comment_box = tk.Text(frame, width = 52, height = 6, font = ('calibri', 10))
comment_box.place(x = entryX, y = entryY + 60)

output_text_box = tk.Message(frame, textvariable = output_text, font = ('calibri', 10), width = 344, relief = 'sunken', justify = 'left')
output_text_box.place(x = entryX, y = entryY + 250)
output_text.set('Please enter the sensor VPX, wafer number and optional comment field. Select Pass of fail. To insert file names, browse for the files and'
'shift select all you would like up to a maximum of 4 per defect. Select a defect type for each defect and explicitly describe the location of the defect.'
'Location desctiptions should be in the format: Corner (top/bottom, left/wright), Edge (top, bottom, left, right), Guard ring (top, bottom, left, right), '
'Segment number, strip(s) numbers (for the defects in the active area). Saving will produce a database ready .dat file.')

root.mainloop()
