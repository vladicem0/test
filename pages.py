import os
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Locators:
    url = 'https://sbis.ru/'
    download_url = 'https://sbis.ru/download?tab=plugin&innerTab=default'
    contacts = (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/a')
    tensor = (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[1]/div/'
                        'div/div[2]/div/a/img')
    content_block = '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[5]/div/div/div[1]/div'
    photo_container = (By.XPATH,
                       '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[2]')
    location = (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[3]/div[2]/'
                          'div[1]/div/div[2]/span/span')
    new_location = (By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div[2]/div/ul/li[43]/span/span')
    partners_list = (By.XPATH, '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[3]/'
                               'div/div[2]/div[2]/div/div[2]/div[1]/div[3]')
    download = (By.XPATH,
                '/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[3]/ul/li[8]/a')
    plugin = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div[2]')
    file = (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/'
                      'div[2]/div[2]/div/a')


class Page:
    def __init__(self, browser) -> None:
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    def get_base_page(self) -> None:
        self.browser.get(Locators.url)

    def get_current_url(self) -> str:
        return self.browser.current_url

    def get_page_title(self) -> str:
        return self.browser.title

    def go_to_contacts(self) -> None:
        self.wait.until(ec.presence_of_element_located(Locators.contacts))
        self.wait.until(ec.visibility_of(self.browser.find_element(*Locators.contacts)))
        self.wait.until(ec.element_to_be_clickable(self.browser.find_element(*Locators.contacts)))
        sleep(2)
        self.browser.find_element(*Locators.contacts).click()

    def go_to_tensor(self) -> None:
        self.wait.until(ec.presence_of_element_located(Locators.tensor))
        self.wait.until(ec.visibility_of(self.browser.find_element(*Locators.tensor)))
        self.wait.until(ec.element_to_be_clickable(self.browser.find_element(*Locators.tensor)))
        self.browser.find_element(*Locators.tensor).click()
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def go_to_about(self) -> None:
        url = self.browser.find_element('xpath', f'{Locators.content_block}/p[4]/a').get_attribute('href')
        self.browser.get(url)
        self.wait.until(ec.url_to_be(url))

    def get_title(self) -> str:
        self.wait.until(ec.presence_of_element_located(('xpath', Locators.content_block)))
        return self.browser.find_element('xpath', f'{Locators.content_block}/p[1]').get_attribute('innerHTML')

    def get_photo(self) -> list[tuple[int, int]]:
        self.wait.until(ec.presence_of_element_located(Locators.photo_container))
        container = self.browser.find_element(*Locators.photo_container)
        photo = [(container.find_element('xpath', f'./div[{i + 1}]/a/div[1]/img').get_attribute('width'), container.
                  find_element('xpath', f'./div[{i + 1}]/a/div[1]/img').get_attribute('height')) for i in range(4)]
        return photo

    def get_location(self) -> str:
        self.wait.until(ec.presence_of_element_located(Locators.location))
        return self.browser.find_element(*Locators.location).get_attribute('innerHTML')

    def get_partners(self) -> list:
        self.wait.until(ec.presence_of_element_located(Locators.partners_list))
        partners = self.browser.find_element(*Locators.partners_list)
        return partners.find_elements('xpath', './*')

    def set_location(self) -> None:
        self.wait.until(ec.presence_of_element_located(Locators.location))
        self.wait.until(ec.element_to_be_clickable(self.browser.find_element(*Locators.location)))
        self.browser.find_element(*Locators.location).click()
        self.wait.until(ec.presence_of_element_located(Locators.new_location))
        self.wait.until(ec.element_to_be_clickable(self.browser.find_element(*Locators.new_location)))
        self.browser.find_element(*Locators.new_location).click()

    def download_plugin(self) -> str:
        self.wait.until(ec.presence_of_element_located(Locators.download))
        url = self.browser.find_element(*Locators.download).get_attribute('href')
        self.browser.get(url)
        self.wait.until(ec.presence_of_element_located(Locators.plugin))
        self.browser.find_element(*Locators.plugin).click()
        self.browser.get(Locators.download_url)
        self.wait.until(ec.presence_of_element_located(Locators.file))
        self.browser.find_element(*Locators.file).click()
        return self.browser.find_element(*Locators.file).get_attribute('href').split('/')[-1]

    def download_waiting(self, filename: str) -> None:
        for _ in range(120):
            time.sleep(0.5)
            if os.path.isfile(filename) and round(os.path.getsize(filename) / 1024 / 1024, 2) == self.plugin_size():
                break

    def plugin_size(self) -> float:
        self.wait.until(ec.presence_of_element_located(Locators.file))
        size = self.browser.find_element(*Locators.file).get_attribute('innerHTML')
        return float(size.split()[2])
