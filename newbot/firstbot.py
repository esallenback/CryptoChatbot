from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


#TSV formatted with a column header,
#ID\tQuestion\tAnswer
def trainFromTSV(chatbot, filename):

    #file should include a header row
    trainer = ListTrainer(chatbot, show_training_progress=False)
    
    datafile = open(filename, 'r')
    line = datafile.readline()
    isEnd = False
    linesTrained = 0
    while not isEnd:
        line = datafile.readline()
        if linesTrained%1000 == 0:
            print(linesTrained, "lines trained so far")
        if not line:
            isEnd = True
        else:
            linelist = line.split('\t')
            #remove ID field
            linelist.pop(0)
            linelist[1] = linelist[1].strip()
            #add question, add answer
            trainer.train(linelist)
            linesTrained += 1
    return linesTrained
                

def main():
    chatbot = ChatBot(
        "CryptoCurrent",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3',
        read_only=True
    )

    datafile = "chatbot-development12.tsv"

    ans = input("Train? (y/n): ")
    if ans.lower()=='y':
        print("using datafile", datafile)
        print("Lines trained", trainFromTSV(chatbot, datafile))
    elif ans.lower() != 'n':
        print("y/n only please")
        return 1
    
    
    notDone = True
    print("Talk to me, or 'exit' to stop")
    while notDone:
        try:
            userResponse = input(">>")
            if userResponse == "exit":
                notDone = False
                print("goodbye!")
            else:
                bot_input = chatbot.get_response(userResponse)
                print(bot_input)
                if(bot_input=="No value for search_text was available on the provided input"):
                    raise ValueError("No message given")
        except(KeyboardInterrupt, EOFError, SystemExit):
            notDone = False
            print("oh, bye then!")
        except(ValueError):
            print("Hello? Anyone there?")
        except:
            print("uh oh! exception thrown")
            notDone = True
main()