import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#-----------------------------------------------------------------------------------------------------------------

username = ''
password = ''
year="2023"
session= 'Summer 2023'

#-----------------------------------------------------------------------------------------------------------------
def merge_json():
    f = open('data_time.json')
    data_time = json.load(f)
    f.close()
    del data_time[0]
    dict1= {}
    for i in data_time:
        if i[2] in dict1:
            if i[4] in dict1[i[2]]:
                dict1[i[2]][i[4]]+= " "+i[5][:2]+"("+i[6]+"-"+i[7]+"-"+i[8]+")"
                dict1[i[2]]=dict(sorted(dict1[i[2]].items()))
            else:
                dict1[i[2]].update( {i[4]: i[5][:2]+"("+i[6]+"-"+i[7]+"-"+i[8]+")"}) 
        else:
            dict1[i[2]]= {i[4]: i[5][:2]+"("+i[6]+"-"+i[7]+"-"+i[8]+")"}
    
    f = open('data_seat.json')
    data_seat = json.load(f)
    f.close()
    del data_seat[0]

    dict2= {}
    for j in data_seat:
        if j[2] not in dict1:
            continue
        elif j[7] not in dict1[j[2]]:
            continue
        seat = j[10]
        if seat== "\xa0":
            seat= "0"
        if j[2] in dict2:
            dict2[j[2]].append( [j[5], j[7], dict1[j[2]][j[7]], seat ])
        else:
            dict2[j[2]]= [[j[5], j[7], dict1[j[2]][j[7]], seat ]]
            
    return dict2

def start_sync(name= "data.json"):
    datadict= merge_json()
    # URL of the website to scrape
    url = "https://usis.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the desired data from the parsed HTML
        # In this example, we'll retrieve the table rows and print their contents
        table = soup.find('table')
        rows = table.find_all('tr')
        
        data = []  # Array to store the rows
        
        for row in rows:
            cells = row.find_all('td')
            row_data = []  # Array to store the cell data
            for cell in cells:
                row_data.append(cell.text.strip())  # Append the cell content to the row data array
            data.append(row_data)  # Append the row data to the main data array
        
        for i in data:
            if i[1] in datadict:
                for j in datadict[i[1]]:
                    if j[1]==i[5][:2]:
                        j[2]=i[6]
                        break

            
        
        # json
        with open(name, 'w') as json_file:
            json.dump(datadict, json_file)
        
    else:
        print("Failed to retrieve data. Status code:", response.status_code)


def get_current_minutes():
    # Get the current local time
    current_time = time.localtime()

    # Extract the minutes from the current time
    minutes = current_time.tm_min

    return minutes


def loading_wait(id="load_jqgrid-grid-studentStatusCourseList" ):
    def style_attribute_changes(locator, style_value):
        def inner(driver):
            element = driver.find_element(*locator)
            style = element.get_attribute("style")
            return style_value in style
        return inner
    wait = WebDriverWait(driver, 100)
    div_locator = (By.ID, id)
    initial_state = "display: none;"
    wait.until(EC.presence_of_element_located(div_locator))
    wait.until(style_attribute_changes(div_locator, initial_state))
    
def table(name="data_seat.json", id= "jqgrid-grid-studentStatusCourseList"):
    page_source = driver.page_source

    # Create a Beautiful Soup object from the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    data= []

    # Find the table element using its ID
    table = soup.find("table", {"id":id })

    # Get all the rows from the table
    rows = table.find_all("tr")

    # Iterate over the rows and extract the data
    for row in rows:
        # Get the cells within each row
        cells = row.find_all("td")
        
        # Extract the data from each cell
        data.append([cell.text for cell in cells])

    # Dump the data list into a JSON file
    with open(name, "w") as json_file:
        json.dump(data, json_file)

login_url = 'https://usis.bracu.ac.bd/academia/login'
seat_status_url = 'https://usis.bracu.ac.bd/academia/dashBoard/show#/academia/studentCourse/showCourseStatusByStudent'


# Configure Selenium to use the Chrome WebDriver
driver = webdriver.Chrome()  # Replace with the actual path to chromedriver
# Navigate to the login page
driver.get(login_url)

# Fill in the login form
username_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))
password_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'password')))
username_field.send_keys(username)
password_field.send_keys(password)

# Submit the login form
submit_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
submit_button.click()

# Wait for the seat_status page to load
driver.get(seat_status_url)


#seat status page
dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'academiaYear')))
select = Select(dropdown)
select.select_by_visible_text(year)
time.sleep(1)
dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'academiaSession')))
select = Select(dropdown)
select.select_by_visible_text(session)


#---------------------------------------------------------------------
driver.execute_script("window.open('about:blank','_blank');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://usis.bracu.ac.bd/academia/dashBoard/show#/academia/studentCourse/showClassScheduleInTabularFormatByStudent?') 

dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'academiaYear')))
select = Select(dropdown)
select.select_by_visible_text(year)
time.sleep(1)

dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'academiaSession')))
select = Select(dropdown)
select.select_by_visible_text(session)

loading_wait("load_jqgrid-grid-studentClassSchedule")
dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-pg-selbox')))
select = Select(dropdown)
select.select_by_visible_text('All')
loading_wait("load_jqgrid-grid-studentClassSchedule")
table("data_time.json","jqgrid-grid-studentClassSchedule")
#---------------------------------------------------------------------
driver.switch_to.window(driver.window_handles[0])
loading_wait()

dropdown=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-pg-selbox')))
select = Select(dropdown)
select.select_by_visible_text('All')

loading_wait()
table()
start_sync()

while True:
    time.sleep(10)
    button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="refresh-button"]')))
    button.click()
    loading_wait()
    table()
    start_sync()
    if get_current_minutes()!=0:
        driver.switch_to.window(driver.window_handles[1])
        button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="refresh-button"]')))
        button.click()
        loading_wait("load_jqgrid-grid-studentClassSchedule")
        table("data_time.json","jqgrid-grid-studentClassSchedule")
        start_sync()
        driver.switch_to.window(driver.window_handles[0])



