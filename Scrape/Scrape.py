import random
import re
import sys
from time import sleep
from huepy import *

from selenium import webdriver


class Scrape:
    driver: webdriver
    search_pattern: str

    def __init__(self, geckodriver: str = "geckodriver", headless: bool = False) -> None:
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webnotifications.serviceworker.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)
        if headless:
            options.add_argument('--headless')

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        self.driver = webdriver.Firefox(executable_path=geckodriver, firefox_profile=firefox_profile, options=options, service_log_path="log/geckodriver.log")

    def set_pattern(self, pattern):
        self.search_pattern = pattern

    def wait(self, i: int = None, muted=False):
        """Wait the device :param i: number of seconds to wait, if None will be
        a random number between 1 and 3 :type i: int

        Args:
            i (int): seconds to wait
        """
        if i is None:
            i = random.randint(1, 3)
        if muted:
            sleep(i)
        else:
            for remaining in range(i, 0, -1):
                print(run('Waiting for {} seconds.'.format(remaining)), end='\r', flush=True)
                sleep(1)
            sys.stdout.write("\033[K")  # Clear to the end of line

    def __open_group(self, group: str):
        group_url = "https://www.facebook.com/groups/{}/".format(group)
        self.driver.get(url=group_url)
        print(good("Opening group: {}".format(group_url)))
        self.wait()
        if len(self.driver.find_elements_by_css_selector(".ns63r2gh > span:nth-child(1)")) > 0:
            self.driver.find_element_by_css_selector("div.gjzvkazv:nth-child(4)").click()

    def get_posts(self, group: str, amount: int = 35):
        r = []
        xpath_comment = "//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa fgxwclzu a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh m9osqain']"

        self.__open_group(group=group)

        permalinks = []

        while len(permalinks) < amount:
            permalinks = list(dict.fromkeys(
                permalinks + [a.split("/")[1] for a in re.findall(r'permalink/.+?/', self.driver.page_source)]))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        for pl in permalinks:
            url_post = "https://www.facebook.com/groups/{}/permalink/{}/".format(group, pl)
            self.driver.get(url=url_post)
            print(good("Opening post: {}".format(url_post)))
            self.wait(3)
            if len(self.driver.find_elements_by_xpath(xpath_comment)) > 0:
                self.driver.find_element_by_xpath(xpath_comment).click()
                while True:
                    try:
                        self.driver.find_element_by_xpath("//span[@class='j83agx80 fv0vnmcu hpfvmrgz']").click()
                    except Exception:
                        break  # cannot click the button anymore


            r = r + re.findall(
                self.set_pattern(),
                self.driver.find_element_by_xpath("//div[@class='lzcic4wl']").text,
                re.MULTILINE)

        return list(dict.fromkeys(r))
