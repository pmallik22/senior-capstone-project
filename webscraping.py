from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sqlite3

def database_to_seach_terms(database_name):
    conn = sqlite3.connect(database_name)     
    cursor = conn.cursor() 

    query = f"SELECT {"book_title"} FROM {"reading_requirements"}"
    cursor.execute(query)

    dictionary = {}
    initial_list = [row[0] for row in cursor.fetchall()]

    for term in initial_list:
        value = "rft.btitle=" + term.replace(" ", "+") + "&rft.genre"
        dictionary[term] = value

    conn.close()

    return dictionary       

def scrape(url, target_text):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Firefox(options=options)  

    try:
        driver.get(url)  # Open the URL in the browser

        wait = WebDriverWait(driver, 15)
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/div/div/div/div/div[1]/label/span[1]')))
        search_button.click()
                                                                            
        time.sleep(10)   # Wait for the search results to load

        # Locate all span elements with the specified class
        title_elements = driver.find_elements(By.CLASS_NAME, "Z3988")

        # Iterate over all the span elements and check their 'title' attribute
        found = False
        for index, span in enumerate(title_elements, start=1):
            title_content = span.get_attribute("title")

            if target_text in title_content:
                found = True

        return found
    finally:
        driver.quit()

def scrape_and_store(url, database_name):

    terms = database_to_seach_terms(database_name)

    conn = sqlite3.connect(database_name)     
    cursor = conn.cursor() 

    url = (url + "/search?queryString=") 
    for term in terms.keys():  
        book_url = (url + term.replace(" ", "%20"))
        print(term)

        result = scrape(book_url, terms[term])

        cursor.execute(
            "UPDATE reading_requirements SET availability = ? WHERE book_title = ?",
            ("yes" if result else "no", term)  
        )   # Update the database

    conn.commit()  
    conn.close()