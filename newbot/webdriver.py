from selenium.webdriver import Firefox
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from firstbot import *

driver = Firefox()

driver.get("http://localhost:3000/")


#Password
chatbotUname = ""
chatbotPasswd = ""

try:
    
    element = driver.find_element_by_id("username").send_keys(chatbotUname)
    element = driver.find_element_by_id("passwd").send_keys(chatbotPasswd)
    element = driver.find_element_by_xpath("/html/body/div/div/div/form/div/button").click()
    print("sign in succesful")
except (exceptions.NoSuchElementException):
    print("no sign in found")

theBot = initializeBot(False, "chatbot-development12.tsv")

try:
    userIn = "What is the price of BTC"
    botres = getResponse(theBot, userIn)

    #wait until page loads
    
    #select chat
    driver.implicitly_wait(10)
    chatXpath = "/html/body/div/div/div[2]/div[1]/div/div/div[1]"
    element = driver.find_element_by_xpath(chatXpath)

   
    #Read message

    #Generate Response

    #respond
    chatboxXpath = "//*[@id=\"msg-textarea\"]"
    element = driver.find_element_by_xpath(chatboxXpath).send_keys(botres.text)

    sendXpath = "/html/body/div/div/div[2]/div[2]/div/div[3]/form[2]/div/button"
    element = driver.find_element_by_xpath(sendXpath).click()
except (exceptions.NoSuchElementException):
    print("No chatbox found")

