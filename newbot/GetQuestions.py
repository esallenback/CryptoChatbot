from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, sys

fh = open('new_keywords.txt')
for keyword in fh:

    keyword = keyword.rstrip()
    questionslinks = []

    driver = webdriver.Firefox()
    driver.get("http://www.quora.com/search?q=" + keyword)

    count=0
    total=10000

    SCROLL_PAUSE_TIME = 3.5

    while True:

        count += 1
        if count > total:
            break;

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for line in soup.findAll('a', attrs = {'class' : 'question_link'}):
      q_url = BeautifulSoup(str(line), "html.parser").find('a').get('href')
      questionslinks.append(q_url)

    driver.close()

    with open('question_new/'+ keyword + '_questions.txt','w',encoding='utf-8') as f:
        for i in range(len(questionslinks)):
            f.write(questionslinks[i]+'\n')

