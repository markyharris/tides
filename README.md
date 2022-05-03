<b>E-Ink Tide Charts Display</b><br>
This software uses one of two web sources of tide data to display a Tide Chart on a Waveshare 7 by 5 tri-color display.<br>
See https://www.waveshare.com/7.5inch-e-paper-hat-b.htm for more information and pricing from Waveshare.<br><br>
This software is written specifically to the size and 3-color nature of this display. However, the layouts are in a separate module and can be modified to fit other sizes of display if the desire is there. Theoretically a 2 color 7x5 could be used as well.

For specific info on using e-paper display with RPi, see;<br>
https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper<br>
For information on the specific display used for this project see;<br>
https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)<br>

There are 3 major python files;<br>
  <pre><code>
  tides_main.py
  tides_display.py
  tides_layouts.py</code></pre><br>
  
<b>SETUP SPI INTERFACE:</b><br>
At the cmd line prompt; 'pi@raspberrypi:~ $' enter the following;
  <pre><code>
  sudo raspi-config
  3 - Interface Options
  I4 SPI Enable this? Yes </code></pre><br>
<i>Note: You can change the hostname and password if desired at this point, but its optional</i></br>
Answer 'Yes' when you exit raspi-config to Reboot the RPi </br>

<b>SETUP GITHUB ON RPI:</b></br>
After RPi boots up and you login through your SSH client, enter;</br>
  <pre><code>
  sudo apt update
  sudo apt-get install git
  git --version </pre></code>
If you receive a git version number than you are good to go.</br>

<b>COPY FILES FROM GITHUB:</b><br>
Enter;
  <pre><code>
  sudo git clone https://github.com/markyharris/tides.git
  cd tides
  ls -la </pre></code>
This should list the files copied from github to verify it worked properly</br>

<b>SETUP SOFTWARE</b>
Open 'tides_layouts.py', read the instructions and fill in the location information required.
<pre><code>
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
</pre></code>

<i><b>Note:</b> layout0 uses an image created by https://www.tide-forecast.com/, scraped and converted to 1 bit image
to display. While layout1 uses data from an API at https://tidesandcurrents.noaa.gov/map/index.html to plot
the data using matplotlib library. There is an advantage to layout0 in that you can display tide charts from around 
the world, while layout1 is for the US only. But layout1 can is more readable and can display 7 days worth of tide info.</i>

<b>RUNNING SOFTWARE</b>
From the command line enter;
<pre><code>
sudo python3 tides_main.py  0 # 0 = layout0, 1 = layout1</pre></code>

If you leave the number off it will default to whatever the variable 'use_disp_format' is set to in 'tides_main.py'
<pre><code>
use_disp_format = 0 # 0 = layout0, 1 = layout1</pre></code>
