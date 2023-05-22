from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
import logging
from time import sleep
from auth import email, password
from datetime import datetime
from datetime import timedelta

now = datetime.now()
now_and_week = now + timedelta(days=7)
RESTAURANT_URL = f"https://resy.com/cities/ny/don-angie?date={now_and_week.year}-{now_and_week.month:02}-{now_and_week.day:02}&seats=4"

driver = webdriver.Firefox()
driver.get(RESTAURANT_URL)
driver.set_window_size(3000, 3000)

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
sleep(2)

# Login to Resy 
login_form = driver.find_element(By.CLASS_NAME, "LoginForm")
email_input = login_form.find_element(By.ID, 'email').send_keys(email)
password_input = login_form.find_element(By.ID, 'password').send_keys(password)
logging.info("Email and password has been filled out.")
login_buttons = login_form.find_elements(By.XPATH, "//button[@type='submit']")
if len(login_buttons) == 0: 
    raise Exception("Login button not found!")
login_buttons[0].click()
sleep(2)

# Wait till 9:00 AM 
opening_timestamp = now.replace(hour=9, minute=0, second=0, microsecond=0).timestamp()
nowstamp = now.timestamp()
time_delta = opening_timestamp - nowstamp
if time_delta < 0: 
    raise Exception("Opening time was in the past!")
sleep(time_delta)


# Open reservation modal
'''
date_lists = driver.find_elements(By.CLASS_NAME, "ReservationButtonList")
date_list = date_lists[0] if date_lists else None
if not date_list:
    raise Exception("Reservation list not found!")
'''
date_buttons = driver.find_elements(By.CLASS_NAME, "ReservationButton")
print(len(date_buttons))
date_button = None
for button in date_buttons:
    if int(button.get_attribute("id").split("/")[-3].split(":")[-3]) >= 17:
        date_button = button
        break
if not date_button: 
    raise Exception("No date found!")
actions = ActionChains(driver)
actions.move_to_element(date_button).perform()
date_button.click()
sleep(2)

# Reserve 
iframes = driver.find_elements(By.XPATH, "//iframe")
found_iframe = None
for iframe in iframes: 
    if iframe.get_attribute("src").startswith("https://widgets.resy.com"):
        found_iframe = iframe
if not found_iframe: 
    raise Exception("Reservation modal not found!") 
driver.switch_to.frame(found_iframe)
reservation_footers = driver.find_elements(By.CLASS_NAME, "WidgetPageFooter")
if len(reservation_footers) == 0: 
    raise Exception("Reservation modal footer not found!")
reserve_buttons = reservation_footers[0].find_elements(By.XPATH, "//button")
found_reserve_button = None
for reserve_button in reserve_buttons: 
    if "Reserve" in reserve_button.text:
        found_reserve_button= reserve_button
if not found_reserve_button:
    raise Exception("Reserve button not found!")
found_reserve_button.click()
for confirm_button in reserve_buttons: 
    if "Confirm" in confirm_button.text:
        confirm_button.click()
        break
logging.info("Success!")
sleep(5)

driver.quit()