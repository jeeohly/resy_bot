from selenium import webdriver
from selenium.webdriver.common.by import By 
import logging
from time import sleep
from .auth import email, password

driver = webdriver.Firefox()
driver.get("https://resy.com/cities/ny/don-angie?date=2023-05-21&seats=4")

# Open login modal
header = driver.find_element(By.CLASS_NAME, "MenuContainer")
buttons = header.find_elements(By.XPATH, '//button')
open_login_modal_button = None 
for button in buttons: 
    if "Log in" in button.text: 
        open_login_modal_button = button
        break 
if not open_login_modal_button: 
    raise Exception("Button to open login modal not found!")
open_login_modal_button.click() 
sleep(3)

# Go to login with email/password
login_modal = driver.find_element(By.CLASS_NAME, "AuthView")
login_modal_buttons = login_modal.find_elements(By.XPATH, '//button')
login_with_email_button = None 
for button in login_modal_buttons: 
    if "Email" in button.text: 
        login_with_email_button = button 
        break
if not login_with_email_button: 
    raise Exception("Login with email button not found!")
login_with_email_button.click()
sleep(3)

# Login to Resy 
login_form = driver.find_element(By.CLASS_NAME, "LoginForm")
email_input = login_form.find_element(By.ID, 'email').send_keys(email)
password_input = login_form.find_element(By.ID, 'password').send_keys(password)
logging.info("Email and password has been filled out.")
login_buttons = login_form.find_elements(By.XPATH, "//button[@type='submit']")
login_button = login_buttons[0] if len(login_buttons) > 0 else None 
if not login_button: 
    raise Exception("Login button not found!")
sleep(3)
login_button.click()
sleep(3)

driver.quit()