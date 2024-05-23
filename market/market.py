from types import TracebackType
from typing import Type

import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from .constant import *



class Market(webdriver.Edge):
    def __init__(self, driver_path=";C:\SeleniumDrivers") -> None:
        self.driver_path= driver_path
        os.environ['PATH'] +=self.driver_path
        
        options=webdriver.EdgeOptions()
        #ignore brower warning error
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        #keep the browser open for testing
        options.add_experimental_option('detach',True)
        
        #initialize the Edge driver with options
        super(Market,self).__init__(options=options)
        
    
           
    def land_first_page(self):
        self.get(WOOLWORTH_URL)
        
    def enter_postcode(self):
        input_postcode = self.find_element('id','wx-digital-catalogue-autocomplete')
        input_postcode.send_keys(POSTCODE)
        
        
    def select_first_postcode_option(self):
        select_postcode = WebDriverWait(self, 5).until(
        EC.element_to_be_clickable(
            (By.ID, 'wx-digital-catalogue-autocomplete-item-0')
        )
    )
        select_postcode.click()

    def click_read_catalogue_button(self):
        read_catalogue_button = WebDriverWait(self, 5).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, 'core-button-secondary')
        )
    )
        read_catalogue_button.click()

    def get_category_list(self):
        """
        Return categories elements and category list for further extraction
        """
        action = ActionChains(self)
        #need to click on the item of a drop down list menu.
        hover_element = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.ID, 'sf-navcategory-button'))
            )
        action.move_to_element(hover_element).perform()
        
        categories = self.find_elements(By.CLASS_NAME, 'sf-navcategory-link')
        category_names=[]
        for category in categories:
            category_name = category.text
            category_names.append(category_name)
        return categories,category_names
        
    def click_next_page(self):
        try:
            next_page_btn = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'a[aria-label="Next page"]')))
            next_page_btn.click()
            import time 
            time.sleep(2)
            return True
        except Exception as e:
            return False  

    
    def extract_products_in_category(self):
        products = []
        while True:
            page_products = self.get_products_from_current_page()
            products.extend(page_products)
            if not self.click_next_page():
                break
        return products   
        
             
    def get_products_from_current_page(self):
        try:
            def try_get_text(parent:WebDriver, selector, default):
                try:
                    return parent.find_element(By.CSS_SELECTOR, selector).text
                except:
                    return default

            def try_get_attribute(parent:WebDriver, selector, attribute, default):
                try:
                    return parent.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute)
                except:
                    return default
            # Wait until elements are present
            products = WebDriverWait(self, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'sf-item-content'))
            )
            #find chilren elements
            #child_elements = products[0].find_elements(By.XPATH, "./child::*")
            
            product_list= []
            
            for product in products:
                data = {
                    "title": try_get_text(product, ".sf-item-heading", "NA"),
                    "price": try_get_text(product, ".sf-pricedisplay", "NA"),
                    "option_suffix": try_get_text(product, ".sf-optionsuffix", "NA"),
                    "sale_price": try_get_text(product, ".sf-saleoptiontext", "NA"),
                    "regular_price": try_get_text(product, ".sf-regprice", "NA"),
                    "regoptiondesc": try_get_text(product, ".sf-regoptiondesc", "NA"),
                    "saving": try_get_text(product, ".sf-regprice", "NA"),
                    "offer_valid": try_get_text(product, ".sale-dates", "NA"),
                    "comparative_text": try_get_text(product, ".sf-comparativeText", "NA"),
                    "sale_option": try_get_text(product,".sf-saleoptiondesc","NA")
                    
                }
                product_list.append(data)
            return product_list
            
        except Exception as e:
            print(f"An error occurred: {e}")
                        
        
        
        
            
        