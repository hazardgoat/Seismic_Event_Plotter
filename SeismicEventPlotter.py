'''
Using a user defined time interval, this script pulls data in XML form from the NCEDC (Northern California Earthquake Data Center) 
website (https://service.ncedc.org/fdsnws/event/1/), covering X number of hours back from the present, and then parses it to extract 
the time, latitude, longitude, and magnitude of seismic events captured by their network. It then plots the data on a zoomable Stamen 
map, color coding by magnitude, where each marker displays the magnitude and time of each event. This map is saved as an HTML file 
and automatically opened in the default web browser. The program then refreshes the data at the user defined time interval. When 
CTRL+C is pressed, the user will be prompted to either amend the monitoring interval or exit the program.
'''


from urllib.request import urlopen  #allows the urlopen function to be called from the urllib.request modual, whi;ch itself allows urls to be opened
from xml.etree.ElementTree import parse #allows the parse function to be called from the xml.etree.ElementTree modual, which itself alllows XML data to be parsed and created
from itertools import zip_longest   #allows zip_longest function to be called from the itertools modual so lists of uneven lengths can be zipped
import arrow    #package that provides imporved function over native time modual
from time import sleep  #allows the sleep function to be called from the time modual, which itself is used for time-related functions
import folium   #mapping package
import webbrowser   #modual for dispaying web-based documents (i.e. html file)


'''
This function asks the user to define the number of hours back from the present to pull seismic readings. 
The same value is also used to determine the refresh interval.
'''
def TimeWindow(hoursShift, firstRun):
    while True:
        if firstRun == True:
            hoursShift = input('Enter the desired interval hours between each map refresh (must be >= 1): ')
        try:
            if type(hoursShift) is int:
                break
            if len(hoursShift) < 1:
                hoursShift = 6
                print('Default selected:', hoursShift, 'hours')
            elif type(hoursShift) is str:
                hoursShift = int(hoursShift)
            print('Plotting the last', hoursShift, 'hours of strong motion events')
            print('Plot refresh interval set for every', hoursShift, 'hours')
            print('*** To change interval time or exit the program, press CTRL+C ***')
            break
        except:
            print('Error: Value must be a number')
            #exit()
    return hoursShift

'''
This function opens the XML file hosted on the NCEDC website for a user defined number of hours back from the present, loads it
into a tree, and then gets the root element of the tree.
'''
def GetData(hoursShift):
    utcNow = arrow.utcnow()
    utcStart = utcNow.shift(hours=-hoursShift).format('YYYY-MM-DDTHH:mm:ss')
    utcEnd = utcNow.format('YYYY-MM-DDTHH:mm:ss')
    urlHand = urlopen('https://service.ncedc.org/fdsnws/event/1/query'\
                +'?start='+utcStart+'&end='+utcEnd+'&catalog'\
                +'=NCSS&includeallmagnitudes=true&includearrivals=false&'\
                +'includemechanisms=false&orderby=time&format=xml')
    tree = parse(urlHand)
    root = tree.getroot()
    return root, utcNow

'''
This function parses the data loaded into the tree, extracting the time, latitude, longitude, and magnitude of seismic events
and sorts them to respective lists.
'''
def ParseData(root):
    unifiedData = []
    latitude = []
    longitude = []
    time = []
    magnitude = []
    names = {'latitude':latitude, 'longitude':longitude, 'time':time, 'mag':magnitude}
    for key, value in names.items():
        for category in root.iter():
            if category.tag == '{http://quakeml.org/xmlns/bed/1.2}' + key:
                for item in category:
                    if item.tag == '{http://quakeml.org/xmlns/bed/1.2}value':
                        data = item.text
                        value.append(data)
                    else: continue
            else: continue
    return unifiedData, latitude, longitude, time, magnitude

'''
This function takes the previously created lists and creates a lists of tuples that are comprised of the elements of each list in order,
such that the specific data of each event is grouped together.
'''
def UnifyData(unifiedData, latitude, longitude, time, magnitude):
    unifiedData = list(zip_longest(latitude, longitude, time, magnitude, fillvalue =''))
    return unifiedData

'''
This function plots the seismic event data by location on a zoomable Stamen map using markers. The markers are color-coded by magnitude
and when selected display the time and magnitude of the event. It then saves the map as an HTML file and automatically opens it in the
user's default browser.
'''
def PlotMap(unifiedData):
    m = folium.Map(location=[37.8712783000847, -122.27342497671098], 
            zoom_start=6, tiles='Stamen Terrain', zoom_control=True)
    magnitudeColors = {1:'lightgray', 2:'green', 3:'blue', 4:'orange', 5:'lightred', 
                6:'red', 7:'darkred', 8:'purple', 9:'darkpurple', 10:'black'}
    eventColor = ''
    for event in unifiedData:
        for i in event:
            if i == event[3]:
                try:
                    magFloat = float(event[3])
                except:
                    pass
                latStr = event[0]
                longStr = event[1]
                timeStr = event[2]
                magFloat = magFloat
                for key, value in magnitudeColors.items():
                    previousKey = key - 1
                    try:
                        if magFloat > previousKey and magFloat <= key:
                            eventColor = value
                    except:
                        eventColor = 'white'
                    convertedTime = str(arrow.get(timeStr).format('YYYY-MM-DD HH:mm:ss'))
                    folium.Marker(
                        location=[latStr, longStr],
                        popup=('Magnitude: '+event[3]+', '+'Time: '+convertedTime),
                        icon=folium.Icon(color=eventColor, icon='info-sign'),
                    ).add_to(m)
    print(
        '### Magnitude Legend ###', 'Unknown = white', '0-1 = '+magnitudeColors[1], '1-2 = '+magnitudeColors[2], 
        '2-3 = '+magnitudeColors[3], '3-4 = '+magnitudeColors[4], '4-5 = '+magnitudeColors[5], '5-6 = '+magnitudeColors[6],
        '6-7 = '+magnitudeColors[7], '7-8 = '+magnitudeColors[8], '8-9 = '+magnitudeColors[9], '9-10 = '+magnitudeColors[10],
        sep='\n'
        )
    m.save("map.html")
    webbrowser.open("map.html")

'''
This the main function. It calls all the other functions in the appropriate order and passes their returned values
into the next function.
'''
def Main(hoursShift, firstRun):
    hoursShift = TimeWindow(hoursShift, firstRun)
    root, utcPrevious = GetData(hoursShift)
    unifiedData, latitude, longitude, time, magnitude = ParseData(root)
    unifiedData = UnifyData(unifiedData, latitude, longitude, time, magnitude)  
    PlotMap(unifiedData)
    return utcPrevious, hoursShift


yesList = ['y', 'Y', 'yes', 'Yes', 'YES']
noList = ['n', 'N', 'no', 'No', 'NO']
count = 0
firstRun = True
hoursShift = 0
utcPrevious, hoursShift = Main(hoursShift, firstRun)
firstRun = False

while True:
    try:
        currentTime = arrow.utcnow()
        futureTime = utcPrevious.shift(hours=+hoursShift)
        if currentTime >= futureTime:
            utcPrevious, hoursShift = Main(hoursShift, firstRun)
            count = 0
        else:
            sleep(300)
            count = count + 1
            print('loop', count, 'of 12 before next data refresh')
        continue
    except KeyboardInterrupt:
        while True:
            changeHours = input('Stopping program. Would you like to change the hours? (y/n): ')
            if changeHours not in yesList and changeHours not in noList:
                print('Error: Must enter (y/n)')
                continue   
            if len(changeHours) < 0:
                changeHours = 'n'
                print('Default selected: n')
            if changeHours in yesList:
                break
            else:
                print('Exiting program...')
                exit()
        firstRun = True
        utcPrevious, hoursShift = Main(hoursShift, firstRun)
