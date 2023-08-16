import random

from selenium import webdriver
from selenium.webdriver.common.by import By

# function to web scrape the list of internships off of levels.fyi
def get_internship_list():

    url = 'https://www.levels.fyi/internships/?track=Software%20Engineer&timeframe=Summer%20-%202024'
    driver = webdriver.Chrome()

    driver.get(url)

    internship_list = []

    # get all the listings of internships
    listings = driver.find_elements(By.CLASS_NAME, 'media.company-info-cell')

    # from the listings, get the name and location of the internships
    for listing in listings:
        name = listing.find_element(By.TAG_NAME, 'h6').text
        location = listing.find_element(By.TAG_NAME, 'p').text

        # put the name and location into a dictionary
        internship = {'name': name, 'location': location}

        # then add each one to the list
        internship_list.append(internship)

    # after getting the data, close the driver
    driver.quit()

    # return the list
    return internship_list

# function to respond to discord command messages
def handle_response(message: str) -> str:
    p_message = message.lower()
    
    if p_message =='roll':
        return str(random.int(1,6))
    
    if p_message == '!help':
        return "Hi! I am Internship Bot, I will keep you updated if any new internships are listed on levels.fyi for the summer 2024 season."

    
    
    
