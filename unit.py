import unittest
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox(executable_path = 'C:/Users/Nishank TV/Desktop/test/geckodriver.exe')
driver.get('http://localhost:8000/')
time.sleep(10)

abutton = driver.find_element_by_class_name("btn1")
action = ActionChains(driver)
ActionChains(driver).move_to_element(abutton).click().perform()
time.sleep(10)
sbutton = driver.find_element_by_class_name("btn3")
driver.execute_script("arguments[0].scrollIntoView();", sbutton)
ActionChains(driver).move_to_element(sbutton).click().perform()
time.sleep(10)


#driver.find_element_by_class_name("testbtn1").send_keys(os.getcwd()+"\Un.png")
#driver.find_element_by_class_name("testbtn2").click() """


z=driver.find_element_by_class_name("tit3")
driver.execute_script("arguments[0].scrollIntoView();", z)
z=z.text
print(z)
class webTest(unittest.TestCase):
    def test_get(self):
        self.assertEquals(self.z,"Your Loan Will Not Get Approved")
        