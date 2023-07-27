def start():
    import requests
    from bs4 import BeautifulSoup
    import json

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
        
        datadict = {}
        for i in data:
            if i[1] not in datadict:
                datadict[i[1]] = []
            datadict[i[1]] += [[i[3],i[5][:2],i[6],i[9]]]
            
        
        # json
        with open('data.json', 'w') as json_file:
            json.dump(datadict, json_file)
        
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

#data format
#{"ACT201": [["SHO", "01", "Su(02:00 PM-03:20 PM-UB21913) Tu(02:00 PM-03:20 PM-UB21913)", "0"], ["FMZ", "10", "Su(11:00 AM-12:20 PM-UB41404) Tu(11:00 AM-12:20 PM-UB41404)", "0"]], "ANT103": [["TBA", "01", "Mo(03:05 PM-04:00 PM-UB100202) We(03:05 PM-04:00 PM-UB100202)", "14"], ["TBA", "02", "Mo(04:10 PM-05:05 PM-UB100202) We(04:10 PM-05:05 PM-UB100203)", "35"]]}
