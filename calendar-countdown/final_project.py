import requests
from bs4 import BeautifulSoup as BS
import os

####################################################################
class Schedule:
    __slots__ = ('_title', '_year', '_month', '_date', '_hour', '_semester')

    def __init__(self, title: str, year: int, month: int, date: int, hour: int, semester: str):
        '''
        This method defines the instance variables under the class Schedule.
        Parameter:
            self
            title       a string indicating the title and year of the event
            year        an int indicating the year of the event
            month       an int indicating the month of the event
            date        an int indicating the date of the event
            hour        an int indicating the time (hour) of the event
            semester    a stirng indicating the semester of the event
        '''
        self._title = title
        self._year = year
        self._month = month
        self._date = date
        self._hour = hour
        self._semester = semester

####################################################################
def parseSchedule(soup: "BeautifulSoup") -> "[Schedule]":
    '''
    Accepts a single BeautifulSoup object as its argument and parses out the useful information
    Parameters:
        soup: BeautifulSoup object
    Returns:
        A list of Schedule objects containing event details (title, date, time, semester).
    '''
    #Initializes an empty list to store information
    schedules = []

    # Finding all tables containing different semesters' schedules
    semester_tables = soup.find_all('table')

    for table in semester_tables:
        semester_name = table.find_previous('h2').text.strip() #Extracts the name of the semester associated with the current table
        split_semester_info = semester_name.split()
        year = int(split_semester_info[1])
        semester = split_semester_info[0]

        rows = table.find_all('tr') #Finds all table rows within the table

        #Loops through each row, starting from the second row
        for row in rows:
            cells = row.find_all('td') #Finds all cells in the row

            if len(cells) >= 2: #ensures that a row contains a date and an event
                # Extracting date and time information from <strong>
                strong_date = cells[0].find('strong')
                if strong_date:
                    date_time = strong_date.text.strip()

                # Separate date and time more explicitly
                date_time_parts = date_time.split(',')

                date = date_time_parts[0].strip()  # Take only the date part
                #to only take the starting date of an event lasting for more than one day
                if "-" in date:
                    date = date.split('-')[0]
                elif "–" in date: #different types of dashes used in the website
                    date = date.split('–')[0]

                #to convert the date fetched  into numbers
                month_date = date.split()
                month_dic = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, 'November':11, "December":12}
                month = month_dic[month_date[0]]
                date = int(month_date[1])

                if len(date_time_parts) > 1:  # If time information exists
                    time = date_time_parts[1].strip()  # Extract time
                    time_12 = time.split()
                    hour = int(time_12[0])
                    if time_12[1] == "P.M.":
                        hour = hour+12

                else:  # If not a time specified
                    hour = None    # Set blank

                # Extracting title and additional event details from <em>
                em_title = cells[1].find('em')
                if em_title:
                    title = em_title.text.strip()
                    if title[-1] == '*': #remove the '*' at the end of some entries
                        title = title[:-1]
                    title = f"{title} ({year})"

                # Create Schedule object and append to the list
                schedule = Schedule(title, year, month, date, hour, semester)
                schedules.append(schedule)
    return schedules

####################################################################
def createSoup():
    '''
    This function fetches for the information needed for the website. It saves the HTML file, reads the concent, and saves it as a BeautifulSoup object.
    Parameter:
        None
    Returns:
        A BeautifulSoup object containing information in the HTML
    '''
    # save the calendar url as a local file, read the content, and save it as a BeautifulSoup object
    url = "https://catalog.bates.edu/resources/academic-calendar"
    fname = "bates_calendar.html"

    if not os.path.exists(fname):
        resp = requests.get(url)
        with open(fname, "wb") as outfile:
            outfile.write(resp.content)

    with open(fname, "rb") as infile:
        content = infile.read()
    soup = BS(content, features = "html.parser")
    return(soup)

####################################################################
def main():
    # Call createSoup function
    soup = createSoup()

    # Call parseSchedule function
    events = parseSchedule(soup)

####################################################################
if __name__ == "__main__":
    main()
