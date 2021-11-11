# Seismic Event Plotter
<p align="center">
  <img alt="" style=" margin-left: 50px;margin-right: 50px;" src="https://user-images.githubusercontent.com/74040471/140024638-2875b24f-0249-4d23-8a89-57b63ccfe4db.png"/>
</p>

Utilizing a User defined time interval, this python script pulls data from the Northern California Earthquake Data Center (NCEDC) 
website (https://service.ncedc.org/fdsnws/event/1/) in XML form, and then parses it to extract 
the latitude, longitude, time, and magnitude of strong motion events captured by their network. It then plots the data on a zoomable Stamen 
map, color coding by magnitude, where each marker displays the magnitude and time of their respective event when selected. This map is saved as an HTML file 
and automatically opened in the User's default web browser in a new tab. The program then refreshes the data at the user defined time interval. When 
CTRL+C is pressed, the user will be prompted to either amend the monitoring interval or exit the program.

Planned future features:
1) GUI
2) Embedded Legend
3) Data type selection
4) User specifed date-time ranges
