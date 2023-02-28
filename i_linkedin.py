from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


with open("ediwow.json", "w") as f:
    json.dump([], f)


def write_json(new_data, filename='ediwow.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

browser = webdriver.Firefox()
browser.get('https://www.linkedin.com/jobs/search/?currentJobId=3488504801&geoId=103644278&keywords=python')

items = []

last_height = browser.execute_script("return document.body.scrollHeight")

itemTargetCount = 700

while itemTargetCount > len(items):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    new_height = browser.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

    elem_list = browser.find_element(
    By.CSS_SELECTOR, "ul.jobs-search__results-list")

    elements = elem_list.find_elements(
    By.XPATH, '//div[contains(@class,"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")]')
    textElements = []

    for element in elements:

         Job = element.find_element(By.CSS_SELECTOR, 'span.sr-only').text
         Company = "NULL"
         Comp_url = "NULL"
         Location = "NULL"

         textElements.append({Job: Job})

         try:
            Company = element.find_element(
            By.TAG_NAME, 'h4').text

            textElements.append({Company: Company})
         except:
             pass
         
         try:
            Comp_url = element.find_element(
            By.CLASS_NAME, 'hidden-nested-link').get_attribute('href')

            textElements.append({Comp_url: Comp_url})
         except:
             pass
         
         try:
             Location = element.find_element(
            By.CSS_SELECTOR, 'span.job-search-card__location').text
             
             textElements.append({Location: Location})
         except:
              pass
         
         items = textElements

         print(items)
         print(len(items))

         write_json({
                "Job Title:": Job,
                "Company:": Company,
                "Company Url:": Comp_url,
                "Location:": Location
            })

