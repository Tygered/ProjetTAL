# coding: utf-8
oldPosNltk = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk', "r")
oldText = oldPosNltk.read()
oldPosNltk.close()
ref = []
with open('/home/jeremy/TAL/TP_1/wsj_0010_sample.pos.ref', "r") as f:
	for line in f:
		ref.append(line.split(None, 1)[0])
file = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk', "w")
with open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk.temp', "r") as fn:
	for linen in fn:
		if linen.split(None, 1)[0] in ref :
			#print("found match")
			file.write(linen)
file.close()
#file = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.pos.ref', "r")
#ref = file.read()
#file.close()
#file = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk', "w")

def translate(text, vocab, separator="\t", unknown="."):
    """
    Cette fonction prend un texte en deux colonnes avec
    les étiquettes et convertit celles-ci en un autre
    format spécifié par un vocabulaire.
    """

    lima = text.split("\n")
    for i,line in enumerate(lima):
        spl = line.split(separator)
        if len(spl) < 2:
            continue
        # Aller chercher dans le vocabulaire la valeur correspondante
        spl[1] = vocab.get(spl[1], unknown)
        lima[i] = separator.join(spl)

    return "\n".join(lima)

def build_vocab(dico):
    """
    Cette fonction prend une table de conversion entre deux
    syntaxes et construit un vocabulaire sous forme de dictionnaire.
    """

    lines = dico.split("\n")
    res = {}
    for line in lines:
        spl = line.split(" ")
        if len(spl) < 2:
            continue
        res[spl[0]] = spl[1]
    return res

with open("POSTags_PTB_Universal_Linux.txt") as f:
        nltk_univ_vocab = build_vocab(f.read())

file = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.nltk', "r")

with open('/home/jeremy/TAL/TP_1/wsj_0010_sample.txt.pos.univ.nltk', "w") as f:
	f.write(translate(file.read(), nltk_univ_vocab))

file.close()

ref = open('/home/jeremy/TAL/TP_1/wsj_0010_sample.pos.ref', "r")

with open('/home/jeremy/TAL/TP_1/wsj_0010_sample.pos.univ.ref', "w") as f:
	f.write(translate(ref.read(), nltk_univ_vocab))

ref.close()

#$ python evaluate.py wsj_0010_sample.txt.pos.univ.nltk wsj_0010_sample.pos.univ.ref 
#Word precision: 0.654545454545
#Word recall: 0.654545454545
#Tag precision: 0.654545454545
#Tag recall: 0.654545454545
#Word F-measure: 0.654545454545
#Tag F-measure: 0.654545454545

# On peut en conclure que la transformation en tag universel rajoute une grande imprecision a cause des tags manquants.


















