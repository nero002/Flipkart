from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from requests import get
from time import sleep
from bs4 import BeautifulSoup as soup
import requests
import shutil
import os

# Before running, "pip install selenium" and \
# download your corresponding webdriver for your chrome browser from https://chromedriver.chromium.org/downloads

# sroll for certain time to load img
def wait_scroll(mult):
    scroll_by = mult*100
    sleep(0.05)
    driver.execute_script("window.scrollTo(0, "+str(scroll_by)+");")


# def download_img(driver,filename):
# 	base_path = os.path.join(os.getcwd(),"images")
# 	image_url = driver.find_all('img')[0]['src']
# 	if("placeholder" in image_url):
# 		return
# 	# filename += driver.find_all('img')[0]['alt']
# 	print(driver.find_all('img')[0]['alt'])
# 	filename = r'{}'.format(os.path.join(base_path, filename) + ".jpeg")
# 	response = requests.get(image_url).content
# 	# print(response[:25], image_url)
# 	with open(filename, 'wb+') as handle:
# 		handle.write(response)

if __name__ == "__main__":
    my_url = 'https://www.flipkart.com/'
    search_term = "Chimneys"
    driver_options = webdriver.ChromeOptions()
    #use to hide browser
    #driver_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=driver_options)
    driver.get(my_url)
    delay = 15 # seconds
    login_close_btn = driver.find_element_by_xpath("//button[text()='✕']")
    login_close_btn.click()
    search_form = driver.find_element_by_xpath("//form[contains(@class,'header-form-search')]")
    input_field = search_form.find_element_by_xpath("//input[@name='q']")
    input_field.send_keys(search_term)

    search_button = search_form.find_element_by_xpath("//button[@type='submit']")
    search_button.click()

    filename = search_term + ".csv"
    f = open(filename, "a",encoding='utf-8')
    headers = "Product, Price, MRP , Description \n"
    f.write(headers)
    #remove special char form image name
    i=0
    not_allowed_chars = ["\\","/",":","*","?","\"","<",">","|"]
    # response_obj = requests.get(my_url + "1")
    # max_page_count = get_max_page(response_obj)
    # print(max_page_count)
    while(True):
        try:
            # sleep(2)
            results = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,"//div[@class='_1HmYoV _35HD7C' and @style='flex-grow: 1; overflow: auto;']")))
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
            #scrolling till next page 
            for i in range(1,int(driver.execute_script("return document.getElementsByClassName('_3fVaIS')[0].offsetTop")/100)):
                wait_scroll(i)

        #	temp = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,"(//img[@class='_1Nyybr  _30XEf0' and contains(@src,'.jpeg')])[20]")))
            page_html = results.get_attribute("innerHTML")

            page_soup = soup(page_html, "html.parser")

            containers11 = page_soup.findAll("div", {"class": "_3O0U0u"})
            for container in containers11:
                title_container = container.findAll("div", {"class": "_3wU53n"})

                product_name = title_container[0].text.replace("," ,"")

                price_con = container.findAll("div", {"class": "_1vC4OE _2rQ-NK"})
                price = price_con[0].text.replace("₹","Rs.")

                mrp = ""
                try:
                    mrp_con = container.findAll("div",{"class":"_3auQ3N _2GcJzG"})
                    mrp = mrp_con[0].text.replace("₹","Rs.")
                except:
                    mrp = "N/A"

                description_container = container.findAll("ul", {"class": "vFw0gD"})
                product_description = description_container[0].text

                f.write(product_name + "," + price.replace(",", "")+ ","  + mrp.replace(",", "") + "," +  product_description + "\n")
                # download_img(container,str(i)+'. '+product_name)
                base_path = os.path.join(os.getcwd(),"images")
                image_url = container.find_all('img')[0]['src']
                i += 1
                if("placeholder" in image_url):
                    print("placeholder image found for " + str(i))
                    continue
                # filename += driver.find_all('img')[0]['alt']
                # print(container.find_all('img')[0]['alt'])
                for remove_it in not_allowed_chars:
                    product_name = product_name.replace(remove_it,"")
                image_filename = os.path.join(base_path, product_name.replace(" ","_")) + ".jpeg"
                response = requests.get(image_url).content
                # print(response[:25], image_url)
                with open(image_filename, 'wb+') as handle:
                    handle.write(response)

                print("Saved file: " + product_name)
                # print("Product: " + product_name)
                # print("Price: " + price.encode('utf-8'))
                # print("Description" + product_description)
            try:
                next_btn = driver.find_element_by_xpath("//a//span[text()='Next']")
                next_btn.click()
            except Exception as e:
                print(str(e))
                break
        except TimeoutException:
            print("Page Timed Out")
        # print(results)
    # f.close()
    driver.quit()
