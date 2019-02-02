from string import punctuation
from nltk.parse.corenlp import CoreNLPDependencyParser

def get_parent_idx(compound):
    return int(compound[2])

def get_word(compound):
    return compound[0]

def get_pos(compound):
    return compound[1]

def get_sentence_type(compound):
    return compound[3]

class TextDepTree:
    def __init__(self):
        self.dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

def split_text(text):
    res = []
    beg = 0
    end = 0
    for ch in text:
        if ch == '.' or \
            ch == '?' or \
            ch == ':':
            newS = text[beg: end+1]
            res.append(newS)
            beg = end+1
        end+=1
    newS = text[beg:]
    if len(newS) > 0:
        res.append(newS)
    return res     

def get_parse(self, text, display_tree = False):
    final = []
    splitted = split_text(text)
    for x in splitted:
        parse = next(self.dep_parser.raw_parse(x))
        if display_tree:
            print(x)
            #display(parse)
        res = [x.split('\t') for x in parse.to_conll(4).split('\n')]
        res = [x for x in res if len(x) == 4]
        final.append(res)
    return final