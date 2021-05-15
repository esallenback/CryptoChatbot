from selenium.webdriver import Firefox
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from firstbot import *
import time

driver = Firefox()

driver.get("http://localhost:3000/")

filename = "APIkeys.txt"

with open(filename) as f:
    content = f.readlines()
    f.close()
#Password
chatbotUname = content[0]
chatbotPasswd = content[1]

try:
    
    element = driver.find_element_by_id("username").send_keys(chatbotUname)
    element = driver.find_element_by_id("passwd").send_keys(chatbotPasswd)
    element = driver.find_element_by_xpath("/html/body/div/div/div/form/div/button").click()
    print("sign in succesful")
except (exceptions.NoSuchElementException):
    print("no sign in found")

theBot = initializeBot(False, "chatbot-development12.tsv")

try:
    

    #wait until page loads
    
    #select chat
    driver.implicitly_wait(30)
    chatNameCSS = ".ce-chat-card"
    element = driver.find_element_by_css_selector(chatNameCSS)

    while True:
        #Read message

        element = driver.find_elements_by_class_name("message")
        numMsg = len(element)

        lastMessageText = element[len(element)-1].text
        theirMessages = driver.find_elements_by_id("message-their")

        lastTheirMessagetext = theirMessages[len(theirMessages)-1].text

        
        #check if last sent message is from user or bot
        if(lastMessageText == lastTheirMessagetext):
            print(" ---------- last from user -------")
            #last message from user
            #generate response
            userIn = lastTheirMessagetext
            botres = getResponse(theBot, userIn)

            #type and send response
            chatboxCSSselector = ".message-input"
            isGoodMsg = "Was that a good response? Yes or no"
            element = driver.find_element_by_css_selector(chatboxCSSselector).send_keys(botres.text + " " + isGoodMsg)

            sendButtonCSSselect = ".send-button"
            element = driver.find_element_by_css_selector(sendButtonCSSselect).click()

            numMsg += 1
            
            
            
            didRespond = False
            while ( not didRespond):
                time.sleep(3)
                element = driver.find_elements_by_class_name("message")

                if(len(element) > numMsg):
                    didRespond = True
                    
                    lastMessageText = element[len(element)-1].text
                    print(lastMessageText)
                    if(lastMessageText.lower() == "yes"):
                        print("training response")
                        trainMsg(theBot, userIn, botres.text)
                    
                    else:
                        print("adding response to list")
                        with open("badresponses.tsv", 'a') as f:
                            line = userIn + "\t" + botres.text + "\n"
                            f.write(line)
                            f.close()
                    thankUser = "Thank you for your feedback"
                    element = driver.find_element_by_css_selector(chatboxCSSselector).send_keys(thankUser)
                    element = driver.find_element_by_css_selector(sendButtonCSSselect).click()
            
                            
        
        #check if last sent message is from user or bot
        if(lastMessageText == lastTheirMessagetext):

            time.sleep(15)
        else:
            print(" ----- last from bot -------")
            #last message from bot
            time.sleep(5)
        

except (exceptions.NoSuchElementException):
    print("No chatbox found")

