import csv
import re

from expaux.dataformatting import TermDict, TermEntry, store_on_csv
from expaux.bs_04_19 import corpus_15_19, work_list_conll, \
    doc_conll_struct, section_division, sent_lemmas, add_udpaths


def mk_dep_frqs():
    cwl = work_list_conll()
    totfreqs = TermDict()
    docfreqs = TermDict()
    for book in cwl:
        parags = doc_conll_struct(book['file'])
        docdict = TermDict()
        for parag in parags:
            if not section_division(parag):
                for sent in parag:
                    add_udpaths(sent)
                    for w in sent:
                        if re.match(r'\w.*', w[1]):
                            for i in range(0, len(w[10]) - 1):
                                docdict.update_dict(w[10][i] + '_' +
                                                    w[10][i + 1])
        for feat in docdict.keyset():
            if docdict[feat] > 1:
                docfreqs.update_dict(feat)
                totfreqs.update_dict(feat, docdict[feat])
    ents = []
    for key in docfreqs.keyset():
        if totfreqs[key] > 3:
            ents.append(TermEntry(key, totfreqs[key]))
    ents.sort()
    store_on_csv('C:/popres/exploredicts/depbigfreqs.csv',
                 [[e.term, docfreqs[e.term], e.val] for e in ents])


def depbig_nonrare_set():
    nonrare = set()
    with open('C:/popres/exploredicts/depbigfreqs.csv',
              newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if int(row[2]) >= 1000:
                nonrare.add(row[0])
    return nonrare


def mk_lemma_freq_dict(csvf):
    cwl = corpus_15_19(work_list_conll())
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


def lemma_selection(lemmadictcsv, dfrq, tfrq):
    lsel = set()
    with open(lemmadictcsv, newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if int(row[1]) >= dfrq and int(row[2]) >= tfrq:
                lsel.add(row[0])
    lsell = list(lsel)
    lsell.sort()
    return lsell


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


# if __name__ == '__main__':
    # mk_possible_section_stats()
    # mk_lemma_freq_dict()
    # mk_dep_frqs()
