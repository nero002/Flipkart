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
import WebScrape_Flipkart
# from imgscrape import imgscrape

def download_image(product_name,my_url, file_location,img_index):
    img_bytes = requests.get(my_url).content
    
    file_location = os.path.join(file_location,product_name)
    if(not os.path.exists(file_location)):
        os.makedirs(file_location)

    with open(os.path.join(file_location,str(img_index+1)+'.jpg'), 'wb') as img_file:
        img_file.write(img_bytes)
        # print(f'{} was downloaded...')

my_url = 'https://www.flipkart.com/search?q=Cooker&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=offas-pos=1&as-type=HISTORY'
single_page_url = "https://www.flipkart.com/greenchef-tadka-pan-10-cm-high-quality-diameter/p/itm95b795f6f093c?pid=PTPFT7EF2HHW6DQH&lid=LSTPTPFT7EF2HHW6DQHWJBXT2&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=fd0f7b1e-e819-4722-becd-b182410a41c1.PTPFT7EF2HHW6DQH.SEARCH&ppt=sp&ppn=sp&ssid=uouw8ygo6o0000001595754895204&qH=d338d8fe084054a6"


def get_product_urls(search_url):
    driver_options = webdriver.ChromeOptions()
    #use to hide browser
    # driver_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=driver_options)
    # driver = webdriver.Chrome()
    delay = 4
    driver.get(search_url)

    while(True):
        sleep(4)
        containers = driver.find_elements_by_xpath("(//div[@class='_1HmYoV _35HD7C'])[2]//div[@class='_3liAhj']//a[@class='Zhf2z-']")
            
        for container in containers:
            download_all_images(container.get_attribute('href'))

        results = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='_1HmYoV _35HD7C'][2]")))

        #scrolling till next page 
        for i in range(1,int(driver.execute_script("return document.getElementsByClassName('_3fVaIS')[0].offsetTop")/100)):
            WebScrape_Flipkart.wait_scroll(i,driver)

        try:
            next_btn = driver.find_element_by_xpath("//a//span[text()='Next']")
            next_btn.click()
        except Exception as e:
            print(str(e))
            break

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
    
    try:
        product_name = driver.find_element_by_xpath("//h1[@class='{}']".format(product_name_container)).get_attribute("innerText")
        product_name = "".join([c for c in product_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        print(product_name)
    except:
        print("Page not loaded properly, Skipping...")
        return
    try:
        img_line_driver = driver.find_element_by_xpath("//ul[@class='{}']".format(img_list_class))
        thumbnails = img_line_driver.find_elements_by_xpath("//li[@class='{}']".format(li_class))
        # print(len(thumbnails))
    except NoSuchElementException: 
        image_tag = driver.find_element_by_xpath("//img[contains(@class,'{}')]".format(image_class))
        image_url = image_tag.get_attribute('srcset').split(" ")[0]
        # print(image_url)
        
        download_image(product_name,image_url,os.path.join(os.getcwd(),'images'),1)
        driver.quit()
    
        return None

        
    for i,thumbnail in enumerate(thumbnails):
        hover = ActionChains(driver).move_to_element(thumbnail)
        hover.perform()
        try:
            image_tag = driver.find_element_by_xpath("//img[contains(@class,'{}')]".format(image_class))
            image_url = image_tag.get_attribute('srcset').split(" ")[0]
            # print(image_url)
            download_image(product_name,image_url,os.path.join(os.getcwd(),'images'),i)
            sleep(0.1)
        except:
            print("Thumbnail was not of an image")

        #next btn for next page
    
    
    driver.quit()


if __name__ =="__main__":
    # download_all_images(single_page_url)
    get_product_urls(my_url)

