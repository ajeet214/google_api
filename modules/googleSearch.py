# from urllib.parse import urlencode, unquote
from bs4 import BeautifulSoup

from config import Config
from modules.sentiment import Sentiment_analysis
# import base64
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from config import Config


class GoogleSearch:

    def __init__(self):

        # self.proxy = self._get_proxy()
        self.neg_count = 0
        self.neu_count = 0
        self.pos_count = 0
        self.obj = Sentiment_analysis()
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extension")
        options.add_argument("--proxy-server=socks5://" + '185.193.36.122:23343')

        # self.driver = webdriver.Chrome(options=options)
        # remote webdriver
        self.driver = webdriver.Remote(
            command_executor='http://' + Config.SELENIUM_CONFIG['host'] + ':' + Config.SELENIUM_CONFIG[
                'port'] + '/wd/hub',
            desired_capabilities=options.to_capabilities(),
        )
        url = 'https://www.google.com/ncr'
        self.driver.get(url)

    # def _get_proxy(self):
    #     url = "http://credsnproxy/api/v1/proxy"
    #     try:
    #         req = requests.get(url=url)
    #         if req.status_code != 200:
    #             raise ValueError
    #         return req.json()
    #     except:
    #         return {"proxy_host": '93.95.100.181',
    #                 "proxy_port": '23345'}

    def get(self, query):

        html_list = []
        q = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')
        q.send_keys(query)
        q.send_keys(Keys.ENTER)
        sleep(0.1)
        # soup = BeautifulSoup(self.driver.page_source,'html.parser')
        html_list.append(self.driver.page_source)
        # print(soup.prettify())

        pages_on_window = self.driver.find_element_by_id('foot').find_element_by_tag_name('tr').text.replace('\n', '').replace('Next', '')
        print(pages_on_window, len(pages_on_window))

        for i in range(2, len(pages_on_window)):
            # print(i)
            try:
                self.driver.find_element_by_xpath('//*[@id="nav"]/tbody/tr/td[{}]/a'.format(i+1)).click()
                sleep(0.5)

                # --------or-------
                # self.driver.get('https://www.google.com/search?q={}&start={}'.format(query, i*10))
                # # html_list.append(BeautifulSoup(self.driver.page_source, 'html.parser').prettify())
                html_list.append(self.driver.page_source)
                # # print(BeautifulSoup(self.driver.page_source, 'html.parser'))
            except NoSuchElementException:
                pass

        self.driver.quit()

        # # print(html_list)
        final_list = []
        for i in html_list:
            # print(BeautifulSoup(i, 'html.parser').prettify())
            soup1 = BeautifulSoup(i, 'html.parser').find('div', id="search")
            for j in soup1.find_all('div', class_="g"):

                try:
                    temp_dict = dict()
                    header = j.find('div', class_="r")
                    # print(header.h3.text)
                    temp_dict['title'] = header.h3.text
                    temp_dict['url'] = header.a['href']

                    # checking for the type of search result
                    if '/news/' in temp_dict['url']:
                        temp_dict['type'] = 'news'
                    elif '/videos/' in temp_dict['url']:
                        temp_dict['type'] = 'video'
                    elif temp_dict['url'].startswith('https://www.youtube.com/watch'):
                        temp_dict['type'] = 'video'
                    else:
                        temp_dict['type'] = 'link'

                    des = j.find('div', class_='s')

                    if des.find('span', class_='f'):
                        temp_dict['datetime'] = des.find('span', class_='f').text.replace(',', '').replace('-', '').rstrip()

                        if 'hours ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now()-datetime.timedelta(hours=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            # int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif 'hour ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now()-datetime.timedelta(hours=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif 'minutes ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now()-datetime.timedelta(minutes=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif 'minute ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now() - datetime.timedelta(minutes=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif 'days ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now() - datetime.timedelta(days=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif 'day ago' in temp_dict['datetime']:
                            post_time = datetime.datetime.now() - datetime.timedelta(days=int(temp_dict['datetime'].lstrip()[0:2]))
                            post_time = post_time.strftime('%Y-%m-%d %H:%M:%S')

                            # Convert from human readable date to epoch
                            temp_dict['datetime'] = int(time.mktime(time.strptime(post_time, '%Y-%m-%d %H:%M:%S'))) - time.timezone

                        elif temp_dict['datetime'].istitle():
                            try:
                                temp_dict['datetime'] = int(
                                    datetime.datetime.strptime(temp_dict['datetime'].lstrip(), '%d %b %Y').timestamp())
                            except ValueError:
                                temp_dict['datetime'] = int(
                                    datetime.datetime.strptime(temp_dict['datetime'].lstrip(), '%b %d %Y').timestamp())

                        else:
                            temp_dict['datetime'] = int(
                                datetime.datetime.strptime(temp_dict['datetime'].lstrip(), '%d %b %Y').timestamp())

                    else:
                        temp_dict['datetime'] = None
                    temp_dict['content'] = des.text

                    pol = self.obj.analize_sentiment(des.text)
                    temp_dict['polarity'] = pol

                    if pol == 1:
                        temp_dict['polarity'] = "positive"
                        self.pos_count += 1
                    elif pol == -1:
                        temp_dict['polarity'] = "negative"
                        self.neg_count += 1
                    else:
                        temp_dict['polarity'] = "neutral"
                        self.neu_count += 1

                    if not temp_dict['content']:
                        temp_dict['content'] = None

                    final_list.append(temp_dict)

                # for image results
                except:
                    pass

        return final_list


if __name__ == '__main__':
    obj = GoogleSearch()
    print(obj.get('g20 2018 summit'))

# erica freymond