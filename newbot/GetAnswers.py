import requests
from bs4 import BeautifulSoup
import re, sys

fh = open('keywords.txt')
for keyword in fh:

    questionList = []
    answerList = []

    keyword = keyword.rstrip()

    #build training data header

    outfile = 'answers_4/' + keyword + '.yml'
    with open(outfile,'w',encoding='utf-8') as f:
        f.write('categories:\n')
        f.write('- ' + keyword + '\n')
        f.write('conversations:\n')

    fh = open('questions/' + keyword + '_questions.txt')
    i=0
    for link in fh:
        if link < 'questionslinks':
            s= requests.Session()
            url='https://www.quora.com'+link.rstrip()
            i+=1
            print(str(i)+":" +url)

            try:
              url_htm = s.get(url)

              soup = BeautifulSoup(url_htm.text, "html.parser")

              if "No Answers Yet" in url_htm.text:
                continue

              answer_length = 0
              answer_text = ''
              question_text = ''

              for link in soup.find_all('div', id = re.compile('_answer_content$')):
                  if link.find('div', {'class:','ui_qtext_expanded'}):
                      for line in link.find('div', {'class:','ui_qtext_expanded'}).findAll('p', {'class:','ui_qtext_para u-ltr u-text-align--start'}):
      
                          if len(list(line.children)) > 0: 
                              answer=list(line.children)[0]
                              answer_length = answer_length + len(answer)
                              if (answer_length > 500 and answer_text != ''):
                                  break
                              else:
                                  answer_text += str(answer) + ' '
                      if answer_text:
                          break

              if soup.find('div', attrs = {'class' : 'question_text_edit'}):
                  if soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1'):
                      if soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1').find('span', {'class:','ui_qtext_rendered_qtext'}):
                          question_text = list(soup.find('div', attrs = {'class' : 'question_text_edit'}).find('h1').find('span', {'class:','ui_qtext_rendered_qtext'}).children)[-1]

              if answer_text != "":
                  if question_text != '':
                      with open(outfile,'a+',encoding='utf-8') as f:
                          f.write('- - ' + str(question_text) + '\n')
                          answer_1 = answer_text.split('.', 1)
                          f.write('  - ' + str(answer_1[0]) + '\n')
            except requests.exceptions.RequestException:
                print("Connection issue")
                continue
