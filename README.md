# thickness_visual_inspection_gui

GUIs for production of sensor thickness and sensor visual inspection data files. Intend to make executables in the future.

Requirements: Best to install and run through Anaconda (https://www.anaconda.com/) as this will include all necessary libraries

Both files need their respective config files set to save data to the correct direcories.

Uses the inventory.csv produced by the production database to minimize the number of inputs. https://gitlab.cern.ch/cambridge-ITK/production_database_scripts.git To work properly this must be updated with the following command:

python inventory2CSV.py --project S --componentType SENSOR --currentLocation <my_Location> --property ID --outfile inventory.csv

Where <my_Location> is your local sites DB code. For example TRIUMF, FZU, CAM or SFU.

# Thickness GUI
Takes multiple measurements separated by spaces and produces the arithmetic mean of the inputs.

# Visual Inspection GUI
Allows the user to select up to 10 images to be named in the file.

