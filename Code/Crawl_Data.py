import pandas as pd 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException , ElementNotInteractableException
from selenium.webdriver.common.by import By
from time import sleep
import random

df_housingPrice = pd.read_csv('BatDongSan.csv')
# Retrieve data from all pages
for z in range(2,1001):
    try:
        # declare browser
        driver = webdriver.Chrome("chromedriver.exe")
        
        # oepn url
        url = "https://batdongsan.com.vn/ban-can-ho-chung-cu/1pn/p{}?rs=2,3,4,5".format(z)
        driver.get(url)
        
        # get price
        elems_price = driver.find_elements(By.CLASS_NAME , "re__card-config-price")
        price = [elem_price.text for elem_price in elems_price]
        
        # list to save number of bathrooms
        lst_bathrooms = []
        
        # lấy ra sống phòng tắm    
        for i in range(1,len(price) + 1):
            if i == 11: 
                lst_bathrooms.append(0)
                continue
            # Truy cập tới phần tử div có xpath như chuỗi truyền vào
            elem_div = driver.find_element("xpath" , "/html/body/div[6]/div/div[1]/div[3]/div[{}]/a/div[2]/div[1]/div[1]/div[1]".format(i))
            # Đếm số lượng thẻ span có trong thẻ div
            check_numSpan = elem_div.find_elements(By.TAG_NAME , "span")
            number_tagSpan = len(check_numSpan)
            # Kiển tra xem có những dữ liệu không có giá trị nhà tắm thì để NAN vào trong list
            if number_tagSpan == 8 or number_tagSpan == 6:
                lst_bathrooms.append(0)
            else:
                temp = elem_div.find_elements(By.CLASS_NAME , "re__card-config-toilet")
                lst_bathrooms.append(temp[0].text)
        
        # get link / title
        elems = driver.find_elements(By.CSS_SELECTOR , ".re__card-info-content")
        title = [elem.text.split('\n')[0] for elem in elems]
        
        # get acreage
        elems_acreage = driver.find_elements(By.CLASS_NAME , "re__card-config-area")
        acreage = [elem_acreage.text for elem_acreage in elems_acreage]
            
        # get bedrooms 
        elems_bedrooms = driver.find_elements(By.CLASS_NAME, 're__card-config-bedroom')
        bedrooms = [elem_bedrooms.text for elem_bedrooms in elems_bedrooms]
        
        # get address
        div_location = driver.find_elements(By.CLASS_NAME, "re__card-location")
        address = [location.text for location in div_location]
        
        # append dataframe
        df_temp = pd.DataFrame(list(zip(title , acreage , price , bedrooms , lst_bathrooms , address)) , columns=('Title' , 'Area' , 'Price' , 'Bedrooms' , 'Bathrooms' , 'Address'))
        df_housingPrice = pd.concat([df_housingPrice , df_temp])
        
    except:
        print(z)
        continue
# extract to file .CSV
df_housingPrice.to_csv("Data_BatDongSan.csv" , index = False)
































    
