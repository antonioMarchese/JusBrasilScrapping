from bs4 import BeautifulSoup
import requests
import time
from Constant.functionality import JusBrasil
import Constant.constant as const


def get_lawyer_num(city_link):
    content = requests.get(const.BASE_URL + city_link).text # Set the correct URL
    soup = BeautifulSoup(content, 'lxml')
    return int(soup.find('span', class_="LawyersSearchPage-header-title-results").text.strip('( advogados)').replace('.', ''))

def get_names(link, num):
    names = []
    search_names = []
    n = 25 if (num >= 250) else int(num/10)
    # If the city has 250+ lawyers, we don't need all names, so we only get the first 250. Otherwise, we must get all names
    content = requests.get(link).text
    soup = BeautifulSoup(content, 'lxml')

    for i in range(n):
        # The next few lines allow us to get names in different pages -> the url changes
        if i > 0:
            new_link = link + '?p=' + str(i + 1)
            content = requests.get(new_link).text
            soup = BeautifulSoup(content, 'lxml')

        lawyer = soup.find_all('h3', class_='LawyerCard-name')
        for person in lawyer:
            names.append(person.text)
            search_names.append(person.text.replace(' ', '+'))
    return names, search_names

with JusBrasil(teardown=True) as bot:
    for city in const.CITY_LINKS:
        print("Extracting lawyers number...\n")
        num = get_lawyer_num(city)
        names, search_names = get_names(const.BASE_URL + city, num)
        print('Extracting phones...')
        bot.get_phone(names, search_names, city)
        print("Successfully extracted phones. Ready for the next round.\n")
        time.sleep(15)
    bot.quit()
