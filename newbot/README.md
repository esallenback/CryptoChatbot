# Newbot readme

To get started, set up a python virtual environment.
Please note this project is being developed with python version 3.8

All python libraries are available in requirements.txt. Run

`pip install -r requirements.txt` 

to install all required python dependencies. After that, the main file
to run the website is app.py. With flask, simply run

`flask run`

to get a local copy of the bot up and running. Alternatively run app.py

Note this bot is trained with the database.sqlite3 file provided. This
file can be generated via the generateDB.py file. This takes a 
significant amount of time. A sample human readable dataset is provided 
in chatbot-development12.tsv. A starter database.sqlite3 file is 
provided to avoid having to spendtime training from inital clone.

GetAnswers.py, GetQuestions.py, and generateData.py are the scripts used
to develop an elementary dataset to train the chatbot. An example output
used to train the model would be chatbot-development12.tsv

The current next steps of this bot is refactoring the old bot code 
which is able to pull realtime data from sources to be compatible with 
the machine learning Q&A model.

Other future goals for the back end include:
 * Machine learning datasets from other sources (ex wikipedia, news sources)
 * Generating a prediction model to provide rudimentary investment advice

A rudimentary front end is provided for simple interaction with the 
main features but is not what our final product will look like. We 
intend to shift to react for a more fully fleshed out display.