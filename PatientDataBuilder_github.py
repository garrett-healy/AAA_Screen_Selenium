import pandas
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#getting the patient ID data
path = input('Enter the path for your patient ID file: ')
start_date = input('Enter the start date for the data build (YYYY-MM-DD): ')
end_date = input('Enter the end date for the data build (YYYY-MM-DD): ')
patient_df = pandas.read_csv(path, converters = {'Patient ID': str})

i=0

#start of the build process
for x in patient_df['Patient ID']:
    #chrome seems to work on VA system
    driver = webdriver.Chrome()
    driver.get("https://voogle.vha.med.va.gov/search")
    time.sleep(5)
    assert "Voogle" in driver.title
    accept_button = driver.find_element(By.CSS_SELECTOR, 'button.p-ripple.p-element.p-button.p-component.p-button-primary')
    accept_button.click()

    #building patient data
    elem_build = driver.find_element(By.CSS_SELECTOR, 'button.p-ripple.p-element.p-button.p-component.p-button-rounded.p-button-sm.custom-button-color-navy')
    elem_build.click()
    elem_build_search = driver.find_element(By.CSS_SELECTOR, 'input#float-ICN.p-inputtext.p-component.p-element.ng-untouched.ng-pristine.ng-valid')
    elem_build_search.clear()
    elem_build_search.send_keys(x)
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
    ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform() #moves you over to custom tab
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(start_date).perform() #establishes the start date of the data
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(end_date).perform() #establishes the end date of the data
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.RETURN).perform() #builds data
    time.sleep(5)
    driver.close()
    i=i+1

print(i)
