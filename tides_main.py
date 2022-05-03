# tides_main.py
# E-Paper TIDES Display - by Mark Harris
#
# This script uses the images created at https://www.tide-forecast.com/ for layout0
# And layout1 uses matplotlib to plot data taken from api.tidesandcurrents.noaa.gov; 
# https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20220423&range=168&interval=60&station=9410170&product=predictions&datum=STND&time_zone=gmt&units=english&format=json

# Imports
from tides_layouts import *
import time
import requests
import json
import sys

# epd7in5b_V2 = 3-color 7 by 5 display. Change this based on the display used.
# find 'epd = epd7in5b_V2.EPD()' towards bottom and change also if needed.
# These are located in the directory 'waveshare_epd'
from waveshare_epd import epd7in5b_V2

# Layouts - add new layouts to this list as necessary
layout_list = [layout0,layout1] # Add layout routine names here

use_disp_format = 0 # 0 = layout0, 1 = layout1
interval = 3600 * 12 # 3600 = 1 hour * num of hours

# Check for cmdline args and use passed variables instead of the defaults above
if len(sys.argv) > 1:
    use_disp_format = int(sys.argv[1].upper())    

def main():    
    for index, item in enumerate(layout_list):
        if index == use_disp_format:
            print("Layout",index) # debug
            layout_list[index](display) # call appropriate layout


    # Print to e-Paper - This is setup to display on 7x5 3 color waveshare panel. epd7in5b_V2
    # To use on 2 color panel, remove ', epd.getbuffer(display.im_red)' from 6 lines lower.
    # All calls to 'display.draw_red.text' will need to be changed to display.draw_black.text
    # The author has not tried this, but this should accommodate the 2 color display.
    print("Updating screen...")
    try:
        epd.init()          
        time.sleep(1)
        print("Printing METAR Data to E-Paper")
        epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
        print("Done")
        time.sleep(2)

    except:
        print("Printing error")
    print("------------")
    return True


# Execute code starting here.
if __name__ == "__main__":
    epd = epd7in5b_V2.EPD() # Instantiate instance for display.
  
    while True:        
        try:
#            error = 1/0 #debug  # forces error to test the try-except statements
#       if True:  # used instead of the try-except statements for debug purposes.
#            current_time = time.strftime("%m/%d/%Y %H:%M", time.localtime())               
            print("Updated " + time.strftime("%m/%d/%Y %H:%M", time.localtime())  )
            print("Creating display")
            epd.init()
            epd.Clear()
            display = Display()

            main() # Build METAR data to display using specific layout
                                    
            # Setup update interval
            print("Sleeping for ",interval/3600," Hours") # debug
            time.sleep(interval) # Sets interval of updates. 3600 = 1 hour
            epd.init()
            epd.sleep()
            
        except Exception as e:
            time.sleep(2)
            print("Error Occurred in Main While Loop")
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print(e)
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            
            # Print to e-Paper that there is an error
            epd.init()
            epd.Clear()            
            display = Display()
            
            # If error caused because weather.gov server hiccuped, then display image and wait to retry
            if "properties" in str(e) or "index out of" in str(e) or "HTTPSConnectionPool" in str(e): # METAR not being provided
                display.draw_icon(70, 10, "b", 660, 470, "testpattern3")
                
            # Otherwise another processing error occured so we'll display the message on the e-paper
            else: 
                msg1 = "- Error Occurred -"
                msg2 = "One Moment While We Try Again..."    
            
                w, h = display.draw_black.textsize(msg1, font=font48)
                display.draw_black.text((400-(w/2), 170), msg1, fill=0, font=font48)
                w, h = display.draw_black.textsize(msg2, font=font24)            
                display.draw_red.text((400-(w/2), 230), msg2, fill=0, font=font24)
                
                display.draw_black.text((40, 340), str(e), fill=0, font=font24)
                display.draw_black.text((40, 370), str(exception_type), fill=0, font=font24)
                display.draw_black.text((40, 400), str(filename), fill=0, font=font24)
                display.draw_black.text((40, 430), "Line number: "+str(line_number), fill=0, font=font24)
            
            print("Printing Error info to E-Paper...")
            epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
            print("Done")
            time.sleep(60) # Sets interval of updates. 60 = 1 minute
            epd.init()
            epd.sleep()