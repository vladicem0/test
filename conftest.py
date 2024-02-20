import pytest
import os
from selenium import webdriver


@pytest.fixture(scope='session')
def browser():
    options = webdriver.FirefoxOptions()
    options.binary_location = r'C:\Program Files\Firefox Developer Edition\firefox.exe'
    options.set_preference("browser.download.dir", os.getcwd())
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()
