# tides_layouts.py
# Layouts for Tides Chart Display - Mark Harris

# Imports
from tides_display import *
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

# For Layout 0:
# Visit https://www.tide-forecast.com/ and enter location into search.
# When new page loads, verify it is displaying a tide chart for this location.
# In the URL, copy the portion that describes the location. i.e.
# https://www.tide-forecast.com/locations/Puerto-Penasco-Sonora-Mexico/tides/latest
# Copy the 'Puerto-Penasco-Sonora-Mexico' portion and use as the variable 'tide_loc'
tide_loc = "Puerto-Penasco-Sonora-Mexico"

# For Layout 1:
# Find station id and name at https://tidesandcurrents.noaa.gov/map/index.html
# Use map to pick a location and copy the location id and use it as variable 'station_id'
# And copy the station name and use it as location name in variable 'station_name'
station_id = "1615680" 
station_name = "Kahului, Kahului Harbor, HI" 
annotate_levels = 0 # 0 = no annotation, 1 = yes annotation, but it clutters display


# Utility routines   
def center_line(display,text,font=font24b,pos_x=400):
    w, h = display.draw_black.textsize(text, font=font)
    return(pos_x-(w/2))

def last_update():
    now = datetime.now()
    last_update = "Last Updated at "+now.strftime("%I:%M %p")
    return(last_update)


############
# layout0  #
############
# Tides using image created from https://www.tide-forecast.com/
# Enter location in variable 'tide_loc' above.
# This layout simply scrapes tide chart image and converts it to 1 bit image to display
def layout0(display):
    url = "https://www.tide-forecast.com/system/charts-png/"+tide_loc+"/tides.png" 
    display.show_pic(url, 5, 5, "wb", 1)
    

############
# layout1  #
############
# Tides using data downloaded from api.tidesandcurrents.noaa.gov
# This layout uses matplotlib python library to plot data downloaded from NOAA.
# It is limited to US locations.
def layout1(display):
    def sub_list(list,start,end):
        sublist = list[start:end]
        return sublist

    INTERVAL = "60" # 60 or hilo can be used. 60 provides more data points than hilo
    SAMPLES = "167" # number of samples to get from NOAA. 167 = 7 days at 1 hour per sample.
    DATUM = "MLLW" # STND is the other typical datum
    
    position = [] 
    time = [] 
    today = date.today()
    d1 = today.strftime("%Y%m%d")
    d2 = today.strftime("%m/%d")
    tide_date = d1
    week_dates = [d2]
    
    date_tmp = today
    for j in range(-1,5):
        date_tmp += timedelta(days=1)
        week_dates.append(date_tmp.strftime("%m/%d"))

    # Grab the data from NOAA
    tides = Tides(station_id,tide_date,INTERVAL,SAMPLES,DATUM)
    
    # Process NOAA data
    for object in tides.data["predictions"]:
        time.append(object["t"][11:13]) # grabs the hour of the sample
        position.append(float(object["v"])) # grabs the tide height

    maxlist = []
    minlist = []
    start = 0
    sample = (int(SAMPLES)/7)+1
    for j in range(7):
        end = int(start + sample)
        sublist = sub_list(position,start,end)
        start = end
        maxlist.append('{0:.2f}'.format(max(sublist))+" ft")
        minlist.append('{0:.2f}'.format(min(sublist))+" ft")
    
    # Create Graph
    plt.style.use('grayscale')
    plt.plot(position, linewidth=2.5, label="Tide Height")
    plt.ylabel('Height ft.')
    
    # Label data points - clutters the display, but does work.
    if annotate_levels:
        for index in range(len(position)):
            plt.annotate(position[index], (index, position[index]))
    
    plt.tick_params(
        axis='x',                  # changes apply to the x-axis
        which='both',              # both major and minor ticks are affected
        bottom=False,              # ticks along the bottom edge are off
        top=False,                 # ticks along the top edge are off
        labelbottom=False)         # labels along the bottom edge are off
    
    plt.margins(0) # Force chart line to start and stop at ends of chart box
    
    cell_text = [maxlist, minlist]
    columns = week_dates 
    rows = ["High Tide","Low Tide"]

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,    
                      colLabels=columns,
                      rowLabels=rows,
                      cellLoc='center',
                      loc='bottom')

    # Create legend.
    plt.legend()
    
    # Create Grid
    plt.grid(linestyle = '--', axis='y')
    
    # Save as pic
    plt.savefig("temp_pic.png")
    
    # Display chart and title on Epaper
    display.show_pic("dummyurl", 5, 0, "b", 0)
    display.draw_text_centered(1, station_name, font36b, "r")
    display.draw_text_centered(35, "Datum = "+DATUM+" - Timezone = GMT", font16b, "r")
