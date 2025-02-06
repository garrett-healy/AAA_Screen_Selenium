import selenium
import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.relative_locator import locate_with
import time

#getting the patient ID data
path = input('Enter the path for your patient ID file: ')
search = input('Enter the term you want to search: ') #example would be 'abomdinal aortic aneurysm'
output_file = input('What do you want to name your output file: ') #example would be 'RMR_Patients_2025'
output_file = output_file+'.xslx'
patient_df = pd.read_csv(path, converters = {'Patient ID': str})
d = []
titles = ['Patient ID', 'Date','Report Text']
d.append(titles)

y=patient_df['Patient ID']
i=0

#chrome seems to work on VA system
driver = webdriver.Chrome()
driver.get("https://voogle.vha.med.va.gov/search")
time.sleep(5)
driver.maximize_window()
assert "Voogle" in driver.title
accept_button = driver.find_element(By.CSS_SELECTOR, 'button.p-ripple.p-element.p-button.p-component.p-button-primary')
accept_button.click()

#individual scraper per patient
for x in y:
    i=i+1
    try:
        patient_id = x
        #scraping the data
        ##finding the search bar
        elem_search = driver.find_element(By.CSS_SELECTOR, 'input.p-element.p-autocomplete-input.p-inputtext.p-component.ng-star-inserted')
        elem_search.clear()
        elem_search.send_keys(patient_id)
        ##needs to wait to load the patient's name
        time.sleep(15)
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(driver).send_keys(Keys.RETURN).perform()
        time.sleep(15)
        
        ##searches for term
        ActionChains(driver).send_keys(Keys.TAB).perform()
        ActionChains(driver).send_keys(Keys.TAB).perform()
        ActionChains(driver).send_keys(Keys.TAB).perform()
        ActionChains(driver).send_keys(Keys.TAB).perform()
        ActionChains(driver).send_keys(search).perform()
        time.sleep(15)

        #tries to get an exact match, otherwise grabs the first option
        try:
            elem_search_result = driver.find_element("xpath","//*[contains(text(), '"+search+"')]")
            elem_search_result.click()
            print("term found")
        except:
            elem_search.click()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.RETURN).perform()
            print("term not found")
        time.sleep(5)
        
        ##clicks on the rads tab
        elem_rads_tab = driver.find_element("xpath","//*[contains(text(), 'Rad')]")
        elem_rads_tab.click()
        time.sleep(5)
        entered_date_column = driver.find_element("xpath","//*[contains(text(), 'Entered Date')]")
        entered_date_column.click()
        time.sleep(3)
        
        try: 
            ##opening report text with relative locators
            report_text_header = elem_rads_tab = driver.find_element("xpath","//*[contains(text(), 'Report Text')]")
            open_report_text = driver.find_element(locate_with(By.TAG_NAME, 'div').below(report_text_header))
            open_report_text.click()
            time.sleep(3)

            ##gathers report text and entered date
            report_text = driver.find_element(By.CSS_SELECTOR, 'p')
            printout_report_text = report_text.text
            entered_date_text = driver.find_element(locate_with(By.TAG_NAME, 'div').below(entered_date_column))
            printout_entered_date_text = entered_date_text.text
            
            ##closes report text
            close_button = driver.find_element(By.CSS_SELECTOR, 'svg.p-dialog-header-close-icon.p-icon')
            close_button.click()

            report_list = [patient_id, printout_entered_date_text, printout_report_text]
            d.append(report_list)

        except:
            print("You excepted")
            report_list = [patient_id, 'data not found exception', 'data not found exception']
            d.append(report_list)
            print(i)

        driver.back()
        time.sleep(5)
        print(i)
    except:
        print("You timed out")
        report_list = [patient_id, 'time out exception', 'time out exception']
        d.append(report_list)
        driver.back()
        time.sleep(5)
        print(i)

output_df = pd.DataFrame(data=d)
output_df.to_excel(output_file)
driver.close()
