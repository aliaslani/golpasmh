# -*- coding: utf-8 -*-
import json
import re
import sys
import time
from datetime import datetime
from datetime import timedelta
import pause
import random

import pytesseract
from anticaptchaofficial.imagecaptcha import imagecaptcha
from PIL import Image
from selenium import webdriver
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

data = json.loads(sys.argv[1])
USERNAME = data["Username"]
PASSWORD = data["Password"]
# # myProxy = data["kargozariID"]
URL = data["Brokerage"]
NAMAD = data["Namad"]
QUANTITY = data["Quantity"]
MINRATIO = data["Minratio"]
MINQUEUE = data["Minqueue"]

STARTTIME = data["Starttime"]
STARTTIME = datetime.strptime(STARTTIME, '%H:%M').time()
STOPTIME = data["Stoptime"]
STOPTIME = datetime.strptime(STOPTIME, '%H:%M').time()
# Quantity = data["INF"][0]["info"][1]["value"]
# Price = data["INF"][0]["info"][2]["value"]
# conditions = data["conditions"]
ROBOT = data["Robot"]
# bs_ratio = 1

# groupname = re.findall(r"groupname=(.*)&", URL)[0]
Nickname = "Seyed"
# url = "https://online.ansarbankbroker.ir/Login"
path = "/home/ali/test/python/mofid"
# Continue = False
submit_order = False
# t_dif = timedelta(hours=0, minutes=0)


# proxy = Proxy(
#     {
#         "proxyType": ProxyType.MANUAL,
#         "httpProxy": myProxy,
#         "ftpProxy": myProxy,
#         "sslProxy": myProxy,
#         "noProxy": "",
#     }
# )



# print("webdriver launched")

opts = Options()
opts.headless = True
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("window-size=1980,960")
opts.add_argument("screenshot")
driver = webdriver.Firefox()

driver.get(URL)



def Time(H, M, S, MS):
    today = datetime.now()
    start_time = today.replace(hour=H, minute=M, second=S, microsecond=MS) - timedelta(hours=0, minutes=0)
    pause.until(start_time)

def MatchTime(STARTTIME, STOPTIME):
    if (datetime.now() + timedelta(hours=4, minutes=30)).time()  > STARTTIME and (datetime.now() + timedelta(hours=4, minutes=30)).time() < STOPTIME:
        return True
    else:
        return False

def check_status(NAMAD):
    url = "http://tsetmc.ir/Loader.aspx?ParTree=15"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "search")))
    search_icon = driver.find_element_by_id("search")
    search_icon.click()
    search_box = driver.find_element_by_id("SearchKey")
    search_box.send_keys(NAMAD)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/table")
        )
    )
    search_box.send_keys(Keys.TAB)
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
    WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_id("d01").text.strip() != ""
    )
    WebDriverWait(driver, 15000).until(EC.text_((By.ID, "d01"), "مجاز"))
    # status = driver.find_element_by_id("d01").text
    driver.quit()
    return True


def LogIn(url, Username, Password):
    count_U = 0
    result_U = True
    
    
    
    while result_U and count_U < 3:
        # try:
        count_U += 1
        if URL == "https://online.samanbourse.com/":
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div[2]/div[1]/multi-login/div/div[2]/ul/li[1]",
                    )
                )
            )
            el = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[1]/multi-login/div/div[2]/ul/li[1]"
            )

            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(el, -5, 1)
            action.click()
            action.perform()
        elif URL == "https://online.ansarbankbroker.ir/Login":
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div[2]/div[2]/div[1]/div/multi-login/div/div[2]/ul/li[1]",
                    )
                )
            )
            el = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div[2]/div[1]/div/multi-login/div/div[2]/ul/li[1]"
            )

            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(el, -5, 1)
            action.click()
            action.perform()
        username_field = driver.find_element_by_id("txtusername1")
        username_field.clear()
        username_field.send_keys(Username)

        password_field = driver.find_element_by_id("txtpassword1")
        password_field.clear()
        password_field.send_keys(Password)

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "captcha-img-web"))
        )
        captcha_img = driver.find_element_by_id("captcha-img-web")
        location = captcha_img.location
        size = captcha_img.size

        driver.save_screenshot(f"{path}/captcha_image/{Nickname}shot.png")
        x = location["x"]
        y = location["y"]
        w = size["width"]
        h = size["height"]
        width = x + w
        height = y + h

        im = Image.open(f"{path}/captcha_image/{Nickname}shot.png")
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(f"{path}/captcha_image/{Nickname}captcha.png")
        capcha = Image.open(f"{path}/captcha_image/{Nickname}captcha.png")
        rgb_im = capcha.convert("RGB")
        rgb_im.save(f"{path}/captcha_image/{Nickname}captcha.jpg")

        solver = imagecaptcha()
        # solver.set_verbose(1)
        solver.set_key("ea623198a0f5ba7564e3f84e10804b2e")
        captcha_text = solver.solve_and_return_solution(
            f"{path}/captcha_image/{Nickname}captcha.jpg"
        )
        captcha_box = driver.find_element_by_id("txtCaptcha")
        if captcha_text != 0:
            captcha_box.send_keys(captcha_text)
            captcha_box.send_keys(Keys.ENTER)
            if URL == "https://online.ansarbankbroker.ir/Login":
                WebDriverWait(driver, 30).until(
                    EC.url_contains("https://online.ansarbankbroker.ir/Customer/")
                )

                Continue = True
                result_U = False
                # print("Log In")
            elif URL == "https://online.samanbourse.com/":
                WebDriverWait(driver, 30).until(
                    EC.url_contains("https://online.samanbourse.com/Customer/")
                )
                print("Log In")
                Continue = True
                result_U = False
                # print("Log In")


        # except:
        #     driver.quit()


def GetParameters(NAMAD):

    webdriver.ActionChains(driver).send_keys(Keys.F5).perform()
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "BuySellBotton"))
    )

    # time.sleep(10)
    buysellbtn = driver.find_element_by_id("BuySellBotton")
    # buysellbtn.click()
    driver.execute_script("arguments[0].click();", buysellbtn)
    time.sleep(1)
    if not driver.find_element_by_id("drpExchangeList"):
                driver.execute_script("arguments[0].click();", buysellbtn)
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "drpExchangeList"))
    )

    namad_search = driver.find_element_by_id("drpExchangeList")
    namad_search.clear()
    namad_search.send_keys(NAMAD)
    time.sleep(1)
    for i in range(30):
        namad_search.send_keys(Keys.BACKSPACE)
    # namad_search.send_keys(Keys.BACKSPACE)
    namad_search.send_keys(NAMAD)
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/ul"))
    )
    time.sleep(1)

    namad_search.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    namad_search.send_keys(Keys.ENTER)
    time.sleep(2)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "ClosingPrice10"))
    )

    # GroupState = driver.find_element_by_id("GroupState10").text

    max_allowed_price = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/span[2]/span[1]"
            
        ).text.replace(",", "")
    )

    min_allowed_price = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/span[2]/span[3]"
        ).text.replace(",", "")
    )

    max_price_buy = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/div[2]/div/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td[3]"
        ).text.replace(",", "")
    )

    min_price_sell = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/div[2]/div/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td[4]"
        ).text.replace(",", "")
    )

    last_traded_price = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[1]/td/div[2]/span[1]"
        ).text.replace(",", "")
    )

    last_traded_price_percent = float(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[1]/td/div[2]/span[2]"
        )
        .text.replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("%", "")
    )

    yesterday_price = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td[2]/span"
        ).text.replace(",", "")
    )
    buy_queue = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]"
        ).text.replace(",", "")
    )
    sell_queue = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/div[2]/div/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td[5]"
        ).text.replace(",", "")
    )

    number_of_trade = int(
        driver.find_element_by_xpath(
            "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[2]/span"
        ).text.replace(",", "")
    )

    # closing_price_percent = int(
    #     driver.find_elements_by_xpath(
    #         "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]/span[1]"
    #     )
    #     .text.replace(",", "")
    #     .replace("(", "")
    #     .replace(")", "")
    #     .replace("%", "")
    # )

    # closing_price = int(
    #     driver.find_elements_by_xpath(
    #         "/html/body/div[1]/table/tbody/tr[4]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td[1]/div[2]/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]/span[2]"
    #     ).text.replace(",", "")
    # )
    parameters = [
        buy_queue,
        sell_queue,
        max_allowed_price,
        min_allowed_price,
        max_price_buy,
        min_price_sell,
        # closing_price,
        # closing_price_percent,
        yesterday_price,
        last_traded_price,
        last_traded_price_percent,
        number_of_trade,
    ]
    print("Got Parameters.")
    return parameters
    # print("buy_queue: ", buy_queue)
    # print("sell_queue: ", sell_queue)
    # print("max_allowed_price: ", max_allowed_price)
    # print("min_allowed_price: ", min_allowed_price)
    # print("max_price_buy: ", max_price_buy)
    # print("min_price_sell: ", min_price_sell)
    # print("closing_price: ", closing_price)
    # print("closing_price_percent: ", closing_price_percent)
    # print("yesterday_price: ", yesterday_price)
    # print("last_trade_price: ", last_traded_price)
    # print("last_traded_price_percent: ", last_traded_price_percent)
    # print("number_of_trade: ", number_of_trade)

# def PishGoshayesh(NAMAD, MINRATIO ):
#         [
#             buy_queue,
#             sell_queue,
#             max_allowed_price,
#             min_allowed_price,
#             max_price_buy,
#             min_price_sell,
#             closing_price,
#             closing_price_percent,
#             yesterday_price,
#             last_traded_price,
#             last_traded_price_percent,
#             number_of_trade,
#         ] = GetParameters(NAMAD)
#         if buy_queue < MINRATIO * sell_queue:
#             if min_price_sell < yesterday_price + 0.03 * yesterday_price:
#                 my_sell_price = min_allowed_price
#             else:
#                 my_sell_price = yesterday_price - 0.05 * yesterday_price
#             Sell(NAMAD, my_sell_price, QUAN)
#             [
#             buy_queue,
#             sell_queue,
#             max_allowed_price,
#             min_allowed_price,
#             max_price_buy,
#             min_price_sell,
#             closing_price,
#             closing_price_percent,
#             yesterday_price,
#             last_traded_price,
#             last_traded_price_percent,
#             number_of_trade,
#         ] = GetParameters(NAMAD)
#         if buy_queue > MINRATIO * sell_queue:
#             CancelOrder(NAMAD)



def Sell(NAMAD, PRICE, QUANTITY):
    global submit_order, driver

    webdriver.ActionChains(driver).send_keys(Keys.F5).perform()
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "BuySellBotton"))
    )

    buysellbtn = driver.find_element_by_id("BuySellBotton")
    driver.execute_script("arguments[0].click();", buysellbtn)
    if not driver.find_element_by_id("drpExchangeList"):
        driver.execute_script("arguments[0].click();", buysellbtn)

    namad_search = driver.find_element_by_id("drpExchangeList")
    namad_search.clear()
    namad_search.send_keys(NAMAD)
    time.sleep(1)
    for i in range(30):
        namad_search.send_keys(Keys.BACKSPACE)
    namad_search.send_keys(NAMAD)
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/ul"))
    )
    time.sleep(1)

    namad_search.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    namad_search.send_keys(Keys.ENTER)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "txtCount"))
    )
    quantity_field = driver.find_element_by_id("txtCount")
    quantity_field.clear()
    quantity_field.send_keys(int(QUANTITY))
    price_field = driver.find_element_by_id("txtPrice")
    price_field.clear()
    # time.sleep(1)
    price_field.send_keys(int(PRICE))
    # print("Submit Parameters")
    time.sleep(5)

    sell_key = driver.find_element_by_id("btnSell")
    driver.execute_script("arguments[0].click();", sell_key)
    submit_order = True
    print('Sell Order Submited')
def CancelOrder(Namad):
    global submit_order, driver

    webdriver.ActionChains(driver).send_keys(Keys.F5).perform()
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "tblTodayOrders"))
    )
    table_element = driver.find_element_by_id("tblTodayOrders")
    elements = table_element.find_elements_by_xpath(".//tr[@class='']")
    for element in elements:
        entries = element.text.split(' ')[:5]
        print(entries)
        if entries[0] == NAMAD:
            removeButton = element.find_element_by_xpath(".//td[@cname='action']/img[@class='removeButton']")
            driver.execute_script("arguments[0].click();", removeButton)
            time.sleep(3)
            disapear = driver.find_element_by_xpath("/html/body/div[1]")
            driver.execute_script(
                "arguments[0].setAttribute('style', '');", disapear
            )
            # WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, 'btnyes'))
            # )
            btnyes = driver.find_elements_by_xpath('//*[@id="btnyes"]')[1]
            
            driver.execute_script("arguments[0].click();", btnyes)
            

        print('Order Canceled')
def exit():
    sys.exit("User terminate the robot!")

def HeyneBazar(NAMAD, MINQUEUE, QUANTITY, CONT=True):
    # while MatchTime(STARTTIME, STOPTIME):
    
    while CONT:
    
        [
            buy_queue,
            sell_queue,
            max_allowed_price,
            min_allowed_price,
            max_price_buy,
            min_price_sell,
            #closing_price,
            #closing_price_percent,
            yesterday_price,
            last_traded_price,
            last_traded_price_percent,
            number_of_trade,
        ] = GetParameters(NAMAD)
        if buy_queue < int(MINQUEUE):
            my_sell_price = yesterday_price + yesterday_price * 0.04
            Sell(NAMAD, my_sell_price, QUANTITY)
            CONT = False
            # exit()

        else:
            time.sleep(10)

# def ChangeStatus(NAMAD, QUANTITY):
#     while MatchTime(STARTTIME, STOPTIME):
#         while check_status(NAMAD):
    
#             [
#                 buy_queue,
#                 sell_queue,
#                 max_allowed_price,
#                 min_allowed_price,
#                 max_price_buy,
#                 min_price_sell,
#                 #closing_price,
#                 #closing_price_percent,
#                 yesterday_price,
#                 last_traded_price,
#                 last_traded_price_percent,
#                 number_of_trade,
#             ] = GetParameters(NAMAD)
#             if buy_queue < int(MINQUEUE):
#                 my_sell_price = yesterday_price + yesterday_price * 0.04
#                 Sell(NAMAD, my_sell_price, QUANTITY)
#                 CONT = False

#             else:
#                 time.sleep(10)
            

    
LogIn(URL, USERNAME, PASSWORD)
if ROBOT == "heynebazar":
    HeyneBazar(NAMAD, MINQUEUE, QUANTITY, CONT=True)
# elif robot == "pishgoshayesh":
#     PishGoshayesh(NAMAD, MINRATIO)
# elif robot == "changestatus":
#     ChangeStatus(NAMAD)

