# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

FILE_TEMP = ''

SMTP_SERVER = ''
SMTP_PORT = 0
USERNAME = ''
PASSWORD = ''
EMAIL = ''

class OnePlusNotif(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.fr/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_one_plus_notif(self):
        # Starting from google.fr
        driver = self.driver
        driver.get(self.base_url + "/")

        # Search for oneplus one
        self.find_element_and_wait(By.ID, "lst-ib").clear()
        self.find_element_and_wait(By.ID, "lst-ib").send_keys("oneplus one")

        # Go to the website one plus one
        self.find_element_and_wait(By.LINK_TEXT, "OnePlus One - OnePlus.net").click()

        # Click buy button
        self.find_element_and_wait(By.XPATH, "//botton[@onclick='showBuyPopWin()']").click()

        # Click buy on Sandstone Black
        black_phone = self.find_element_and_wait(By.XPATH, "//h4[contains(text(),'Sandstone Black')]")
        black_phone.find_element_by_xpath("(//a[contains(text(),'Buy')])[4]").click()

        # Check if we find the text "Sold out"
        if self.find_element_and_wait(By.XPATH, "//h3[contains(text(),'Sold out')]"):
            print 'phone unavailable'
        elif self.find_element_and_wait(By.XPATH, "//h3[contains(text(),'added into cart')]"):
            print 'phone available'
            self.mail_notifier(driver)

    def mail_notifier(self, driver):
        # Create dir c:\\temp if not exist
        if not os.path.exists(os.path.dirname(FILE_TEMP)):
            os.makedirs(os.path.dirname(FILE_TEMP))

        # Take a screenshot
        driver.get_screenshot_as_file(FILE_TEMP)

        # Send email
        self.send_email()

    def send_email(self):
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = 'OnePlus one'
        msg['From'] = "OnePus_One_Notifier"
        msg['To'] = EMAIL
        msg.preamble = 'Phone available !'

        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        with open(FILE_TEMP, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)

        # The actual mail send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    def find_element_and_wait(self, how, what):
        while self.is_element_present(how, what) is False:
            print "Loading web page - waiting element %s" % what
        return self.driver.find_element(by=how, value=what)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to.alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
