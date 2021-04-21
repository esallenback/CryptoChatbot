import os
import re

training_file = 'training_4.txt'

with open(training_file, "r") as f:
    paras = f.read().split("\n")

with open('chatbot-development12.tsv','w',encoding='utf-8') as f:
    f.write("ID\tQuestion\tAnswer\n")

id = 1
data = ""
for para in paras:
    if para.startswith("- -"):
        data = ""
        data = str(id) + "\t" + str(para[4:])
    if para.startswith("  -"):
        if data != "":
            if "\t" in para:
                continue;
            data1 = para[4:]
            if len(data1) < 2:
                continue;

            result = re.sub(r'[^\x00-\x7f]',r'', data1)
            if len(result) < 2:
                continue;
            data2 = result.split('.', 1)
            tmp = data2[0]
            if len(tmp) < 2:
                continue;

            if re.search('qlink_', tmp):
                continue;
            if re.search('http', tmp):
                continue;

            tmp = tmp.replace("<b>", "")
            tmp = tmp.replace("</b>", "")
            tmp = tmp.replace("<i>", "")
            tmp = tmp.replace("</i>", "")

            tmp2 = tmp.split(' ')
            if len(tmp2) > 20:
                continue;

            data += "\t" + tmp + ".\n"
            with open('chatbot-development12.tsv','a+',encoding='utf-8') as f:
                clean_string = re.sub(r'[^a-zA-Z0-9.=/\"\'\s,\(\)\{\}\[\];:\<\>\-_]', r'', data)
                f.write(clean_string)
            data = ""
            id += 1

