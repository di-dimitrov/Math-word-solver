from text_parse import *
from IPython.display import clear_output

def replaceFormula(q,cnt, start, end):
    beg = q.find(start)
    if beg == -1:
        return q, -1
    end = q.find(end)
    if end == -1:
        return False
    string = q[beg: end + len(start)]
#     print(string)
    formula_name = " formula" + str(cnt) + " "
    q = q.replace(string, formula_name, 1)
    formula = (formula_name[1:-1], string[2:-2])
#     print(q, formula)
    return q, formula

def normalizeQuestion(q, beg, end):
    cnt = 1
    q, formula = replaceFormula(q,cnt, beg, end)
    formula_obj = {}
    if formula != -1:
        formula_obj[formula[0]] = formula[1]
    while(formula != -1):
        cnt += 1
        q, formula =replaceFormula(q,cnt, beg, end)
        if formula != -1:
            formula_obj[formula[0]] = formula[1]
#     print(q, formula_obj)
    return q, formula_obj

def transformQuestions(q_dicts):
    resQs = []
    for (cnt, q) in enumerate(q_dicts):
        newQ, formulas = normalizeQuestion(q['question'], "\(", "\)")
        resQs.append((newQ, formulas))
    return resQs

def find_sentence_child(tree, parentId, sent_type, not_pos_tag = -1):
    for (ind, node) in enumerate(tree):
        if get_parent_idx(node) == parentId and \
            get_sentence_type(node) == sent_type and \
            (not_pos_tag == -1 or not_pos_tag not in get_pos(node)):
                return (ind+1,node)
    return -1

def find_pos_tag_child(tree, parentId, pos_tag, not_sent_type = -1):
    for (ind,node) in enumerate(tree):
        if get_parent_idx(node) == parentId and \
            pos_tag in get_pos(node) and \
            (not_sent_type == -1 or get_sentence_type(node) != not_sent_type):
                return (ind+1,node)
    return -1

def add_unknown_helping(res, tree):
#     print(res)
    nsubj = find_sentence_child(tree, res[-1:][0][0], 'nsubj', 'W')
#     print(nsubj)
    if nsubj != -1:
        res.append(nsubj)
    else:
        n_word = find_pos_tag_child(tree, res[-1:][0][0], 'NN')
#         print(n_word)
        if n_word != -1:
            res.append(n_word)
    compounds = find_sentence_child(tree, res[-1:][0][0], 'compound')
    has_compound = False
    if compounds != -1:
        res.append(compounds)
        has_compound = True
    n_word = -1
    if has_compound:
        n_word = find_pos_tag_child(tree, res[-2:][0][0], 'NN', 'compound')
    else:
        n_word = find_pos_tag_child(tree, res[-1:][0][0], 'NN', 'compound')
    if n_word != -1:
        res.append(n_word)
    return res

def getUnknownW(tree):
    res = []
    w_word = [(ind + 1, q) for (ind, q) in enumerate(tree) if 'W' in q[1]]
    if w_word != []:
        res.append(w_word[0])
        if get_sentence_type(w_word[0][1]) == 'nsubj':
            res.append((get_parent_idx(w_word[0][1]), tree[get_parent_idx(w_word[0][1]) - 1]))
        if res != []:
            res = add_unknown_helping(res, tree)
    return res

def getUnknownV(tree, res):
#     print(tree)
#     print(res)
    v_word = [(ind + 1, q) for (ind, q) in enumerate(tree) if 'V' in q[1]][-1:]
    if v_word != []:
        res.append(v_word[0])
#         print(v_word)
    if res == []:
        return res
    res = add_unknown_helping(res, tree)
    return res

def findUnknown(text, display_tree = False):
    parse = get_parse(text, display_tree)
#     display(parse)
    unknown = []
    for tree in parse:
        unknown = getUnknownW(tree)
        if unknown == []: 
            continue
        else:
            break
    if len(unknown) <= 1:
        getUnknownV(parse[-1], unknown)
    if unknown == []:
        return (text, "fail")
    else:
        return (text, unknown)

def get_unknows(q_dicts):
    resQs = transformQuestions(q_dicts)
    qSWithUnknown = []
    cnt = 1
    for x in resQs:
        clear_output()
        print(cnt)
        cnt+=1
        unknown = findUnknown(x[0], False)
        qSWithUnknown.append((unknown[0], unknown[1], x[1]))
    return qSWithUnknown