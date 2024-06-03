from flask import Flask, render_template, jsonify
from datetime import datetime
import final_project as fp

####################################################################
app = Flask(__name__)

####################################################################
# Initialize lists to store events and times gathered from the calendar
suggestions = []
cor_dates = []

#get the Schedule objects created from the final_project file
soup = fp.createSoup()
events = fp.parseSchedule(soup)
for event in events:
    #to get the titles
    suggestions.append(event._title)
    #to get the time and convert them into the same format
    year = event._year
    month = event._month
    date = event._date
    hour = event._hour
    if hour != None:
        time = datetime(year, month, date, hour)
    else:
        time = datetime(year, month, date)
    cor_dates.append(time)

# Create a library pairing an event with its time
target_dates = {}

for i in range(len(suggestions)):
    event = suggestions[i]
    date = cor_dates[i]
    target_dates[event] = date

####################################################################
@app.route('/')
def index():
    return render_template('index.html', suggestions = suggestions, target_dates = target_dates)
