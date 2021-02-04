import csv
import re

from pop_aux.exphelp import store_on_csv
from pop_aux.termdict import TermDict, TermEntry
from pop_aux.bs_04_19 import corpus_15_19, corpus_work_list, \
    doc_conll_struct, section_division, sent_lemmas, add_udpaths


def mk_lemma_freq_dict(csvf):
    cwl = corpus_15_19(corpus_work_list())
    wc = 0
    totfreqs = TermDict()
    docfreqs = TermDict()
    for book in cwl:
        parags = doc_conll_struct(book['file'])
        docdict = TermDict()
        for parag in parags:
            if not section_division(parag):
                for sent in parag:
                    for lm in sent_lemmas(sent):
                        wc += 1
                        docdict.update_dict(lm)
        for lem in docdict.keyset():
            if docdict[lem] > 1:
                docfreqs.update_dict(lem)
                totfreqs.update_dict(lem, docdict[lem])
    ents = []
    for key in docfreqs.keyset():
        if len(key) > 39:
            print(key)  # excluded
        elif totfreqs[key] > 3:
            ents.append(TermEntry(key, docfreqs[key]))
    ents.sort()
    rows = [['LEMMA_COUNT', -1, wc]]
    for e in ents:
        rows.append([e.term, e.val, totfreqs[e.term]])
    store_on_csv(csvf, rows)


def richness_sets(lemmadictcsv):
    common = set()
    nonrare = set()
    with open(lemmadictcsv, newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if int(row[1]) >= 163:  # 95%
                common.add(row[0])
            if int(row[1]) >= 9:  # 5%
                nonrare.add(row[0])
    return common, nonrare




