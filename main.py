import time
from datetime import datetime, timedelta
import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging

########################
# logging configurations
########################
now = datetime.now()
logFolder = 'logs'
if not os.path.exists('logs'):
    os.makedirs(logFolder)

programTimeFormat = now.strftime('%Y-%m-%d-%H-%M-%S')
logFileName = os.path.join(logFolder, f"{programTimeFormat}.log")
logging.basicConfig(
    filename=logFileName,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d-%H-%M-%S',
    level=logging.INFO,
    encoding="UTF-8"
)
########################
# reading data from source excel file
########################
df = pd.read_excel("source/source.xlsx")
########################
# configs for chrome driver
########################
sleepTime = df.loc[0, 'sleep_time']
programWholeSleepTime = df.loc[0, 'program_sleep_time']
chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--log-level=0")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chromeOptions)
######################
# beginning to crawl from excell file
######################
while True:
    print('program started ')
    for i in df.itertuples():
        try:
            urlToCLick = i[df.columns.get_loc('urls') + 1]
            with requests.Session() as s:
                driver.get(urlToCLick)
                successfulResponseMessage = f"""
                successfully visited {urlToCLick} 
                sleeping for {sleepTime} seconds
                """
                print(successfulResponseMessage)
                logging.info(successfulResponseMessage)
                time.sleep(sleepTime)
        except Exception as e:
            print(f"error occurred in program with message: {e}")
            logging.error("Exception occurred", exc_info=True)

    nextClickTime = now + timedelta(minutes=programWholeSleepTime)
    print(f"""
            program clicked all the links sleeping for {programWholeSleepTime} minutes 
            and next run in {nextClickTime}
        """)
    time.sleep(programWholeSleepTime * 60)
