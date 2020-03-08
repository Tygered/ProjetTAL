import nltk
from nltk import word_tokenize
from nltk import pos_tag


text = "It's works !"
tokens_text = word_tokenize(text)
print(tokens_text)
tags_text = pos_tag(tokens_text)
print(tags_text)

with open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt', "r") as file:
	file_text = file.read()
token_file = word_tokenize(file_text)
print(token_file)
file.close()
tags_file = pos_tag(token_file)
print(tags_file)
f = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk.temp', "w")

for tup in tags_file:
	f.write(tup[0]+"\t"+tup[1]+"\n")

f.close()

# $ python evaluate.py wsj_0010_sample.txt.pos.nltk wsj_0010_sample.pos.ref 
#Word precision: 0.936363636364
#Word recall: 0.919642857143
#Tag precision: 0.936363636364
#Tag recall: 0.919642857143
#Word F-measure: 0.927927927928
#Tag F-measure: 0.927927927928

