This is a repository for code utilizing Selenium to automate data gathering from the VA sytem. NOTE: This program can only be run on a VA computer and at no point should any data extracted with this code be taken from the VA system without prior approval from the Privacy Office!! 
In order to utilize the system, you must first build your patient data, and then you can extract reports. To start, you will need a CSV file with one column titled 'Patient ID'. This should be filled with all patient IDs you want to extract reports from. 
Then, run PatientDataBuilder. This will build the patient data in the system over a specified time range. 
Finally, run PatientDataScraper. This will extract the relevant data for all patients based on a specified search term to be ran through the NLP. 
Both files utilize Selenium. To install Selenium on your system, please read: https://www.selenium.dev/documentation/webdriver/getting_started/install_library/. 
