#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 06:02:37 2018
@author: deepak
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urlparse import urlparse, parse_qs
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker



driver = webdriver.Firefox()

timout = 5


'''your login url'''
driver.get("https://kite.trade/connect/login?api_key=xxxxyyyyzzzzzzz1234")
 
dictionary={
        'Which brand of TV do you own? ( e.g. LG Sony, etc)': 'xxyyzz',
        'Which year did you complete your graduation? (e.g. 2000, 1990 etc)': 'xxyyzz',
        'What\'s the most famous landmark near your home? (e.g. Xyz Theater, XXX Mall, etc)':'xxyyzz',
        'What was the make of the first computer you owned? ( e.g. LG, Compaq etc)':'xxyyzz',
        'What is your birth place?':'xxyyzz'      
        }

# write your User Id
loginid = "AB1234"
# write your Password
password = "abc@123"
# write your PIN
loginpin = "123456"

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"userid"))).send_keys(loginid)
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"password"))).send_keys(password)




driver.find_element_by_tag_name('button').click()

driver.implicitly_wait(10)

try:
    element_present = EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print "Timed out waiting for finding password type to load"



''' Implementing new way of answering security questions'''
all_inputs=driver.find_elements_by_xpath("//input[@type='password']")
for inputs in all_inputs:
  string= dictionary.get(inputs.get_attribute("label"))
  driver.implicitly_wait(2)
  inputs.send_keys(string)

driver.find_element_by_tag_name('button').click()


try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, "navbar-links"))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print "Timed out waiting for page to load"
    
    
url=driver.current_url
parse_url = urlparse(url)
query = parse_qs(parse_url.query)
request_token=query.get('request_token')

api_key="Your api_key"
api_secret="Your api_secret"
kite=KiteConnect(api_key=api_key)

data = kite.generate_session(request_token[0], api_secret)

kws = KiteTicker("Your api_key" ,data["access_token"], "Your user_id")
