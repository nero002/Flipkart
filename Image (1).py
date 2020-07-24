from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException,ElementClickInterceptedException,NoSuchElementException
from requests import get
from time import sleep
from bs4 import BeautifulSoup as soup
import requests
import shutil
import os
# from imgscrape import imgscrape

def download_image(product_name,my_url, file_location,img_index):
    img_bytes = requests.get(my_url).content
    
    file_location = os.path.join(file_location,product_name)
    if(not os.path.exists(file_location)):
        os.makedirs(file_location)

    with open(os.path.join(file_location,str(img_index+1)+'.jpg'), 'wb') as img_file:
        img_file.write(img_bytes)
        # print(f'{} was downloaded...')

my_url = 'https://www.flipkart.com/search?q=blenders&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY'
single_page_url = "https://www.flipkart.com/handy-trendy-7-speed-beater-180-w-stand-mixer-electric-whisk/p/itm9430c8957245f?pid=HBLFG5SQQDT7J7KU&lid=LSTHBLFG5SQQDT7J7KUDOATHI&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=fc47e5d3-8db1-41ff-b5ba-a54a1c61143d.HBLFG5SQQDT7J7KU.SEARCH&ppt=sp&ppn=sp&ssid=9d1gq2sdio0000001594268602419&qH=7c7cec5ba22a5060"


def get_product_urls(search_url):
    driver_options = webdriver.ChromeOptions()
    #use to hide browser
    # driver_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=driver_options)
    # driver = webdriver.Chrome()
    driver.get(search_url)

    containers = driver.find_elements_by_xpath("(//div[@class='_1HmYoV _35HD7C'])[2]//div[@class='_3liAhj']//a[@class='Zhf2z-']")

    for container in containers:
        download_all_images(container.get_attribute('href'))

def download_all_images(url):
    driver_options = webdriver.ChromeOptions()
    #use to hide browser
    # driver_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=driver_options)
    # driver = webdriver.Chrome()
    driver.get(url)
    delay = 2 # seconds

    img_list_class = "LzhdeS"
    li_class = "_4f8Q22 _2y_FdK"
    image_class = "_1Nyybr"
    product_name_container = "_9E25nV"
    

    product_name = driver.find_element_by_xpath("//h1[@class='{}']".format(product_name_container)).get_attribute("innerText")
    product_name = "".join([c for c in product_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    print(product_name)

    try:
        img_line_driver = driver.find_element_by_xpath("//ul[@class='{}']".format(img_list_class))
        thumbnails = img_line_driver.find_elements_by_xpath("//li[@class='{}']".format(li_class))
        print(len(thumbnails))
    except NoSuchElementException: 
        image_tag = driver.find_element_by_xpath("//img[contains(@class,'{}')]".format(image_class))
        image_url = image_tag.get_attribute('srcset').split(" ")[0]
        print(image_url)
        download_image(product_name,image_url,os.path.join(os.getcwd(),'images'),1)
        driver.quit()
        return None

        
    for i,thumbnail in enumerate(thumbnails):
        hover = ActionChains(driver).move_to_element(thumbnail)
        hover.perform()
        image_tag = driver.find_element_by_xpath("//img[contains(@class,'{}')]".format(image_class))
        image_url = image_tag.get_attribute('srcset').split(" ")[0]
        print(image_url)
        download_image(product_name,image_url,os.path.join(os.getcwd(),'images'),i)
        sleep(0.1)
        #next btn for next page
try:
		# sleep(2)
		results = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='_1HmYoV _35HD7C' and @style='flex-grow: 1; overflow: auto;']")))
		# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
		#scrolling till next page 
		for i in range(1,int(driver.execute_script("return document.getElementsByClassName('_3fVaIS')[0].offsetTop")/100)):
			wait_scroll(i)

    try:
			next_btn = driver.find_element_by_xpath("//a//span[text()='Next']")
			next_btn.click()
	except Exception as e:
			print(str(e))
		break
	
    driver.quit()


if __name__ =="__main__":
    # download_all_images(single_page_url)
    get_product_urls(my_url)

