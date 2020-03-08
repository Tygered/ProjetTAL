#Code python TP1
import os
import re

#Def define a function/method
def build_vocab(file):
    with open(file, "r") as f: #ouvre fichier avec le nom f
        vocab_text = f.read().split("\n")
    #define dictionnary
    vocab = {} #is empty
    for line in vocab_text:
        split_line = line.split(" ")
        vocab[split_line[0]] = split_line[-1] # -1 = last element of a list
    return vocab   

def convert_tags(file, vocab):
    with open(file) as f:
        word_text = re.split(" |\n", f.read())
    res = []
    for word in word_text:
        split_word = word.split("_")
        if len(split_word) < 2:
            continue

        split_word[1] = vocab.get(split_word[1], split_word[1])
        res.append("_".join(split_word)) #join word and tag + add underscore
    return " ".join(res)

def convert_ref(file, vocab):
    with open(file) as f:
        word_text = f.read().split("\n")
    res = []
    for word in word_text:
        split_word = re.split(" |\t", word)
        if len(split_word) < 2:
            continue
        split_word[1] = vocab.get(split_word[1], split_word[1])
        res.append("\t".join(split_word)) #join word and tag + add underscore
    return "\n".join(res)
        
if __name__ == '__main__':
    text_path = 'C:\\Users\\homy-\\OneDrive\\Bureau\\Pops\\ET5\\TAL\\TP1\\wsj_0010_sample.txt.pos.stanford'
    vocab_path = 'C:\\Users\\homy-\\OneDrive\\Bureau\\Pops\\ET5\\TAL\\TP1\\POSTags_PTB_Universal_Linux.txt'
    ref_path = 'C:\\Users\\homy-\\OneDrive\\Bureau\\Pops\\ET5\\TAL\\TP1\\wsj_0010_sample.pos.ref'
    with open(fichier, 'w') as f:
        f.write(convert_tags(text_path, build_vocab(vocab_path)))
    with open(fichier, 'w') as f:
        f.write(convert_ref(ref_path, build_vocab(vocab_path)))
    
