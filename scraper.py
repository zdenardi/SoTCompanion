from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from requests import Request, Session
from pprint import pprint
from dotenv import load_dotenv
import os

REFERER = "https://www.seaofthieves.com/"
load_dotenv()

class SoTScraper:
    def getCookies():
        chrome_options = Options()
        chrome_options.headless = True
        browser = webdriver.Chrome(options=chrome_options)
        browser.get("https://www.seaofthieves.com/login")
        time.sleep(1)
        emailInput = browser.find_element(By.ID, "i0116")
        emailInput.send_keys(os.environ["SOT_UN"])

        nextButton = browser.find_element(By.ID, "idSIButton9")
        nextButton.click()

        time.sleep(2)
        passwordInput = browser.find_element(By.ID, "i0118")
        passwordInput.send_keys(os.environ["SOT_PW"])

        time.sleep(2)

        submitBtn = browser.find_element(By.ID, "idSIButton9")
        submitBtn.click()

        time.sleep(2)
        acceptBtn = browser.find_element(By.ID, "acceptButton")
        acceptBtn.click()

        all_cookies = browser.get_cookies()

        cookies_dict = {}

        for cookie in all_cookies:
            cookies_dict[cookie["name"]] = cookie["value"]

        RAT_COOKIE = cookies_dict["rat"]
        return cookies_dict

    def getCrew(sentCookies: dict):
        URL = "https://www.seaofthieves.com/api/profilev2/guild-members?guild=43ed79d7-6af4-4391-b540-d66bc7829c3e"
        s = Session()
        req = Request("GET", URL, cookies=sentCookies, headers={"referer": REFERER})
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        crew_list: list = resp.json()
        return crew_list

    def printCrew():
        crew_list = SoTScraper.getCrew()
        for crew in crew_list:
            print(crew["Gamertag"] + "|" + crew["Role"])

    def getShips(sentCookies: dict):
        ships_url = "https://www.seaofthieves.com/api/profilev2/guild-ships?guild=43ed79d7-6af4-4391-b540-d66bc7829c3e"
        s = Session()
        req = Request(
            "GET", ships_url, cookies=sentCookies, headers={"referer": REFERER}
        )
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        ships_list = resp.json()
        pprint(ships_list)
        return ships_list["Ships"]

    def getChronicle(sentCookies: dict):
        chronicle_url = "https://www.seaofthieves.com/api/profilev2/guild-chronicle?guild=43ed79d7-6af4-4391-b540-d66bc7829c3e"
        s = Session()
        req = Request(
            "GET", chronicle_url, cookies=sentCookies, headers={"referer": REFERER}
        )
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        feed = resp.json()
        # pprint(feed)
        return feed["Feed"]
