# coding: utf-8
import re, csv

from os.path import join

NAMED_ENTITIES = {
    "ORGANIZATION": "ORG",
    "PERSON": "PER",
    "LOCATION": "LOC",
    "O": "O"
}

def printq(number):
    print("\nQUESTION {}\n".format(number))

def extract_from_stanford(text, separator="_"):
    """
    Cette fonction sépare les tokens des tags dans les fichier d'entités nommées
    ou de part of speech fournis par stanford.
    """

    lines = text.split("\n")
    res = [[word.split(separator) for word in line.split(" ")] for line in lines]
    res = "\n\n".join(["\n".join(["\t".join(line) for line in sentence]) for sentence in res])
    return res

def stanford_to_conll(txt):
    """
    Cette fonction transforme les deux colonnes d'entités nommées au format PTB
    en format CoNLL.
    """

    txt = translate(txt, NAMED_ENTITIES)
    nes = [line.split("\t") for line in txt.split("\n")]
    nes = ne_to_conll(nes)
    return "\n".join("\t".join(line) for line in nes)

def extract_from_lima(filepath):
    """
    Cette fonction prend le chemin d'un fichier résultant
    d'une analyse lima, et renvoie les 2 colonnes qui nous
    intéressent : le token et l'étiquette.
    """

    def handle_line(ln):
        """Lambda pour gérer les lignes vides et remplies."""

        if ln == []:
            return ln
        else:
            return [ln[1], ln[3]]

    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\t")
        return "\n".join(["\t".join(handle_line(ln)) for ln in reader if ln == [] or not ln[0].startswith("#")])

def lima_to_conll(filepath):
    """
    Cette fonction prend le fichier résultant d'une analyse
    lima et convertit le résultat au format CoNLL.
    """

    def handle_line(ln):
        """Lambda pour gérer les lignes vides et remplies."""

        if ln == []:
            return ln
        else:
            return [ln[1], extract_ne(ln[9])]

    # Extraction des lignes
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\t")
        nes = [handle_line(ln) for ln in reader if ln == [] or not ln[0].startswith("#")]
    
    # Conversion en CoNLL
    nes = ne_to_conll(nes)
    return "\n".join(["\t".join(line) for line in nes])

def ne_to_conll(nes):
    """
    Cette fonction prend un tableau d'entités nommées et rajoute I ou B si
    le token est le premier de l'entité ou dans l'entité.
    """

    last = None
    for i,ne in enumerate(nes):
        if len(ne) < 2:
            last = None
            continue
        if ne[1] is "O":
            last = None
            continue
        if ne[1] == last:
            prefix = "I"
        else:
            last = ne[1]
            prefix = "B"
        nes[i][1] = "{}-{}".format(prefix, last)
    return nes

def extract_ne(misc):
    """
    Cette fonction extrait le type d'entité nommée
    dans la colonne lima.
    """

    ne = re.search("NE=[^.]+\.([^\|\n]+)[\|\n]?", misc)
    if ne:
        r = NAMED_ENTITIES.get(ne.group(1), "MISC")
        return r
    else:
        return "O"


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

def extract_sentences(annoted):
    """
    Cette fonction prend un fichier annoté et ne conserve que les
    token pour reconstruire les phrases, en supprimant les espaces
    dans les ponctuations importantes.
    """

    lines = annoted.split("\n")
    res = [None] * len(lines)
    for i,line in enumerate(lines):
        spl = line.split("\t")
        res[i] = spl[0]
    # Jointure de tous les mots par des espaces
    res = " ".join(res)
    # Suppression des espaces avant certaines ponctuations
    res = re.sub(" ([.,;:!])", "\\1", res)
    # Retablissement des sauts de lignes entre les phrases
    res = "\n\n".join(res.split("  "))
    return res
        

if __name__ == "__main__":

    # Generating Lima to Universal vocab table
    with open("../data/POSTags_LIMA_PTB_Linux.txt") as f:
        lima_ptb = f.read()
    
    with open("../data/POSTags_PTB_Universal_Linux.txt") as f:
        ptb_univ = build_vocab(f.read())

    with open("../data/generated/LIMA_UNIV.txt", "w+") as f:
        f.write(translate(lima_ptb, ptb_univ, separator=" "))
    
    print(">>> Lima to univ table generated: LIMA_UNIV.txt")

    ################
    #### PART I ####
    ################

    # QUESTION 1
    # Traduction du texte de référence Lima en Univ
    printq(1.1)

    with open("../data/generated/LIMA_UNIV.txt") as f:
        lima_univ_vocab = build_vocab(f.read())
        
    with open("../data/pos_reference.txt.lima") as f:
        lima = f.read()
    
    pos_ref_univ = translate(lima, lima_univ_vocab)
    with open("../data/generated/pos_reference.txt.univ", 'w+') as f:
        f.write(pos_ref_univ)
    
    print(">>> Reference file translated from lima to univ: pos_reference.txt.univ")
    
    # QUESTION 2
    # Extraction des phrases depuis le corpus annoté
    printq(1.2)
        
    sentences = extract_sentences(pos_ref_univ)
    
    with open("../data/generated/pos_test.txt", "w+") as f:
        f.write(sentences)
    
    print(">>> Sentences extracted from reference file: pos_test.txt")
    
    # QUESTION 3
    printq(1.3)

    # Extraction des colonnes des tags dans le résultat de Lima
    pos_lima = extract_from_lima("../data/taggings/pos_test.txt.lima")

    print(">>> POS tags extracted from pos_test.txt.lima.")

    # Extraction des colonnes des tags dans le résultat de Stanford
    with open("../data/taggings/pos_test.txt.stanford") as f:
        pos_stanford = extract_from_stanford(f.read())
    
    print(">>> POS tags extracted from pos_test.txt.stanford.")
    
    # pos_test.txt.pos.nltk

    # QUESTION 4
    # Traduction des résultats de POS tagging en univ
    printq(1.4)
                
    # Lima
    pos_lima_univ = translate(pos_lima, lima_univ_vocab)        
    with open("../data/generated/pos_test.txt.pos.lima.univ", "w+") as f:
        f.write(pos_lima_univ)

    print(">>> POS tags from lima converted to univ: pos_test.txt.pos.lima.univ.")

    # Stanford
    
    with open("../data/POSTags_PTB_Universal_Linux.txt") as f:
        stanford_univ_vocab = build_vocab(f.read())

    pos_stanford_univ = translate(pos_stanford, stanford_univ_vocab)
    
    with open("../data/generated/pos_test.txt.pos.stanford.univ", "w+") as f:
        f.write(pos_stanford_univ)

    print(">>> POS tags from stanford converted to univ: pos_test.txt.pos.stanford.univ.")

    if False:

        # TODO :
        
        # NLTK

        with open("../data/PATH_TO_NLTK_VOCAB_TABLE.txt") as f:
            nltk_univ_vocab = build_vocab(f.read())

        with open("../data/pos_test.txt.pos.nltk") as f:
            pos_nltk_univ = translate(f.read(), nltk_univ_vocab)
        
        with open("../data/generated/pos_test.txt.pos.nltk.univ", "w+") as f:
            f.write(pos_nltk_univ)
        
    # QUESTION 5
    printq(1.5)

    # Commandes a éxécuter pour évaluer les analyses

    print(">>> Ready to evaluate POS taggings:")
    print("$ python evaluate.py ../data/generated/pos_test.txt.pos.lima.univ ../data/generated/pos_reference.txt.univ")
    print("$ python evaluate.py ../data/generated/pos_test.txt.pos.stanford.univ ../data/generated/pos_reference.txt.univ")

    # python evaluate.py ../data/generated/pos_test.txt.pos.nltk.univ ../data/pos_reference.txt.univ

    # QUESTION 6

    # TODO : Conclusions

    #################
    #### PART II ####
    #################

    # QUESTION 1
    # Extraction des phrases depuis le texte de référence CoNLL
    printq(2.1)

    with open("../data/ne_reference.txt.conll") as f:
        sentences = extract_sentences(f.read())
    
    with open("../data/generated/ne_test.txt", "w+") as f:
        f.write(sentences)
    
    print(">>> Sentences extracted from NE reference file: ne_test.txt")
    
    # QUESTION 2
    printq(2.2)

    # Pour lima, voir ci-dessous

    # Extraction des colonnes des tags dans le résultat de Stanford
    with open("../data/taggings/ne_test.txt.stanford") as f:
        ne_stanford = extract_from_stanford(f.read(), separator="/")
    
    print(">>> Named entities extracted from stanford result.")
    
    # TODO : Generate files
    # ne_test.txt.ne.nltk

    # QUESTION 3
    # Traduction des résultats d'analyse au format CoNLL
    printq(2.3)

    # Lima
    ne_lima_conll = lima_to_conll("../data/taggings/ne_test.txt.lima")
    with open("../data/generated/ne_test.txt.ne.lima.conll", "w+") as f:
        f.write(ne_lima_conll)
    print(">>> Named entities extracted from lima result and converted to CoNLL: ne_test.txt.ne.lima.conll")

    # Stanford

    ne_stanford_conll = stanford_to_conll(ne_stanford)
    
    with open("../data/generated/ne_test.txt.ne.stanford.conll", "w+") as f:
        f.write(ne_stanford_conll)

    print(">>> Named entities extracted from stanford result and converted to CoNLL: ne_test.txt.ne.stanford.conll")
    
    if False:

        # TODO :
        
        # NLTK

        with open("../data/PATH_TO_NLTK_CONLL_VOCAB_TABLE") as f:
            nltk_conll_vocab = build_vocab(f.read())

        with open("../data/ne_test.txt.ne.nltk") as f:
            ne_nltk_conll = translate(f.read(), nltk_conll_vocab)
        
        with open("../data/generated/ne_test.txt.ne.nltk.conll", "w+") as f:
            f.write(ne_nltk_conll)

    # QUESTION 4
    printq(2.4)

    print(">>> Ready to evaluate NE tagging:")
    print("$ python evaluate.py ../data/generated/ne_test.txt.ne.lima.conll ../data/ne_reference.txt.conll")
    print("$ python evaluate.py ../data/generated/ne_test.txt.ne.stanford.conll ../data/ne_reference.txt.conll")
    #print("$ python evaluate.py ../data/generated/ne_test.txt.ne.nltk.conll ../data/ne_reference.txt.conll")

    # QUESTION 5

    # TODO : Conclusions
