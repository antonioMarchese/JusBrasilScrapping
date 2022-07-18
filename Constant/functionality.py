from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import Constant.constant as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time

import os

class JusBrasil(webdriver.Chrome):
    def __init__(self, driver_path=r";C:/Selenium", teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += r";C:/Selenium"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(JusBrasil, self).__init__(options=options)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_phone(self, names, search_names, search_city_name):
        phones = []
        i = 0
        wait = WebDriverWait(self, 4.0)
        for name in search_names:
            if (i % 7 == 0):
                time.sleep(10.0)
            new_link = const.GOOGLE_SEARCH + name + '+' + search_city_name
            self.get(new_link)
            i += 1
            try:
                phone = self.find_element(
                    By.CSS_SELECTOR,
                    'span[class="LrzXr zdqRlf kno-fv"]'
                ).text
            except NoSuchElementException:
                try:
                    self.find_element(By.CSS_SELECTOR, 'div[class="cXedhc"]').click()
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[class="LrzXr zdqRlf kno-fv"]')))
                    phone = self.find_element(By.CSS_SELECTOR, 'span[class="LrzXr zdqRlf kno-fv"]').text
                except:
                    try:
                        phone = self.find_element(By.CSS_SELECTOR, 'div[class="eigqqc"]').text
                    except:
                        phone = 'Não encontrado'
                        names.remove(name.replace('+', ' '))

            if phone != 'Não encontrado':
                if phone not in phones:
                    phones.append(phone)
                    print(f'{name.replace("+", " ")}: {phone}')
                else:
                    names.remove(name.replace('+', ' '))

        phones = pd.Series(phones)
        phones = phones.loc[phones != 'Não encontrado']
        df = pd.DataFrame({'Nome': names, 'Telefone': phones})
        arq = pd.ExcelWriter(f'{search_city_name.strip("advogado+").replace("+", "-")}.xlsx')
        df.to_excel(arq, 'JusBrasil', index=False)
        arq.save()
