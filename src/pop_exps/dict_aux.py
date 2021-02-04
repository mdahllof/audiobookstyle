import csv
import re
import statistics

from pop_aux.bs_04_19 import corpus_work_list, doc_conll_struct, \
    section_division, add_udpaths, sent_lemmas, \
    add_listcats, METAFIELDS, corpus_15_19
from pop_aux.termdict import TermDict
from pop_exps.lex_diversity import richness_sets

POS_REGEXES = ['NN.*', 'PN.*', 'VB.*', 'AB.*', 'JJ.*', 'PP.*', 'MAD.*',
               'MID.*', 'VB[|]PRS.*', 'VB[|]PRT.*']

pron_lemmas = {'jag_PRON': 'first', 'vi_PRON': 'first', 'du_PRON': 'first',
               'ni_PRON': 'second', 'han_PRON': 'third', 'hon_PRON': 'third',
               'de_PRON': 'third'}


def sent_len(sent):
    wc = 0
    for w in sent:
        if re.match(r'[\d\w].*', w[1]):
            wc += 1
    return wc


def collectcode(sent):
    lscounts = [0, 0]
    recounts = [0, 0]
    lemmasets = [['jag_PRON', 'vi_PRON'],
                 ['han_PRON', 'hon_PRON', 'de_PRON']]
    tagregexes = ['VB[|]PRS.*', 'VB[|]PRT.*']
    for ls in sent:
        for i in range(len(lemmasets)):
            if ls[2] + '_' + ls[3] in lemmasets[i]:
                lscounts[i] += 1
        for i in range(len(tagregexes)):
            if re.match(tagregexes[i], ls[4]):
                recounts[i] += 1
    str(round((100 * lscounts[0]) /
              (lscounts[0] + lscounts[1])))
    str(round((100 * recounts[1]) /
              (recounts[0] + recounts[1])))


def mk_corpus_check_art1(csvfile):
    cwl = corpus_15_19(corpus_work_list())
    add_listcats(cwl)
    with open(csvfile, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(METAFIELDS + ['listyears'])
        for book in cwl:
            book_data = [str(book[k]) for k in METAFIELDS + ['listyears']]
            csvwriter.writerow(book_data)


def mk_pos_relfrqs(csvfile):
    cwl = corpus_15_19(corpus_work_list())
    add_listcats(cwl)
    vkeys = [re.sub(r'[^\w]', '', tagre) for tagre in POS_REGEXES]
    with open(csvfile, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(METAFIELDS + vkeys)
        for book in cwl:
            parags = doc_conll_struct(book['file'])
            wc = 0
            tag_count = TermDict()
            for parag in parags:
                if not section_division(parag):
                    for sent in parag:
                        for ls in sent:
                            wc += 1
                            tag_count.update_dict(ls[4], lowercase=False)
            tagre_count = TermDict()
            for tagre in POS_REGEXES:
                for postag in tag_count.keylist():
                    if re.match(tagre, postag):
                        tagre_count.update_dict(tagre, tag_count[postag],
                                                lowercase=False)
            relfreqs = {}
            for tagre in POS_REGEXES:
                tagrekey = re.sub(r'[^\w]', '', tagre)
                relfreqs[tagrekey] = round((1000000 * tagre_count[tagre])/wc)
            book_data = [str(book[k]) for k in METAFIELDS]
            pos_rel_freqs = [str(relfreqs[k]) for k in vkeys]
            csvwriter.writerow(book_data + pos_rel_freqs)


def mk_struct_stats(csvfile):
    cwl = corpus_15_19(corpus_work_list())
    add_listcats(cwl)
    vkeys = ['wc', 'slm', 'slsd', 'plm', 'plsd', 'ddm', 'ddsd']
             # 'slloq', 'slmd', 'slupq', 'mddm', 'mddsd', 'vddm', 'vddsd'
    with open(csvfile, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(METAFIELDS + vkeys)
        for book in cwl:
            parags = doc_conll_struct(book['file'])
            depdepths = []
            maxdepdepths = []
            vdepdepths = []
            sent_lengths = []
            parag_lengths = []
            for parag in parags:
                if not section_division(parag):
                    parag_lengths.append(0)
                    for sent in parag:
                        sl = sent_len(sent)
                        if sl > 0:
                            sent_lengths.append(sl)
                            parag_lengths[-1] += sl
                        add_udpaths(sent)
                        sdds = []
                        for w in sent:
                            if re.match(r'\w.*', w[1]):
                                sdds.append(len(w[10]))
                        depdepths.extend(sdds)
                        if len(sdds) > 0:
                            maxdepdepths.append(max(sdds))
                        for w in sent:
                            if re.match(r'VB.*', w[4]):
                                vdepdepths.append(len(w[10]))
            quart = statistics.quantiles(sent_lengths, n=4,
                                         method='inclusive')
            vd = {'wc': sum(sent_lengths),
                  'slm': round(1000 * statistics.mean(sent_lengths)),
                  'slsd': round(1000 * statistics.pstdev(sent_lengths)),
                  'plm': round(1000 * statistics.mean(parag_lengths)),
                  'plsd': round(1000 * statistics.pstdev(parag_lengths)),
                  # 'slloq': round(1000 * quart[0]),
                  # 'slmd': round(1000 * quart[1]),
                  # 'slupq': round(1000 * quart[2]),
                  'ddm': round(1000 * statistics.mean(depdepths)),
                  'ddsd': round(1000 * statistics.pstdev(depdepths))}
                  # 'mddm': round(1000 * statistics.mean(maxdepdepths)),
                  # 'mddsd': round(1000 * statistics.pstdev(maxdepdepths)),
                  # 'vddm': round(1000 * statistics.mean(vdepdepths)),
                  # 'vddsd': round(1000 * statistics.pstdev(vdepdepths))
            book_data = [str(book[k]) for k in METAFIELDS]
            cat_rel_freqs = [str(vd[k]) for k in vkeys]
            csvwriter.writerow(book_data + cat_rel_freqs)


def mk_gram_relfrqs_aux(csvfile):
    cwl = corpus_15_19(corpus_work_list())
    add_listcats(cwl)
    with open(csvfile, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        for book in cwl:
            parags = doc_conll_struct(book['file'])
            wc = 0
            pos_count = TermDict()
            dep_count = TermDict()
            for parag in parags:
                if not section_division(parag):
                    for sent in parag:
                        for ls in sent:
                            wc += 1
                            dep_count.update_dict('r_' + ls[7],
                                                  lowercase=False)
                            pos_count.update_dict('p_' + ls[4][:2],
                                                  lowercase=False)
            book_data = [str(book[k]) for k in METAFIELDS] + [str(wc)]
            for t in pos_count.top_scored_terms(100000):
                book_data.extend(['p' + t.term, t.val])
            for t in dep_count.top_scored_terms(100000):
                book_data.extend(['r' + t.term, t.val])
            csvwriter.writerow(book_data)


def mk_gram_relfrqs(csvpre):
    mk_gram_relfrqs_aux(csvpre + '_aux.csv')
    dict_tot = TermDict()
    dict_docs = []
    metas = []
    with open(csvpre + '_aux.csv', newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            dict_docs.append(TermDict())
            metas.append(row[:len(METAFIELDS)])
            wc = int(row[len(METAFIELDS)])
            fvpairs = row[len(METAFIELDS) + 1:]
            for i in range(0, len(fvpairs), 2):
                rf = int(fvpairs[i + 1]) / wc
                rfi = round(rf * 1000000)
                dict_docs[-1].update_dict(fvpairs[i], rfi)
                dict_tot.update_dict(fvpairs[i], rf)
    keys = [t.term for t in dict_tot.top_scored_terms(100000)]
    keys2 = {'p': [], 'r': []}
    for k in keys:
        keys2[k[:1]].append(k)
    with open(csvpre + '_fields.csv', mode='w', newline='',
              encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        for k in keys2['p'] + keys2['r']:
            csvwriter.writerow([k])
    with open(csvpre + '.csv', mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        fields = METAFIELDS + [k[1:] for k in keys2['p'] + keys2['r']]
        csvwriter.writerow(fields)
        for i in range(len(metas)):
            book_data = metas[i]
            book_data = book_data + [dict_docs[i][k] for
                                     k in keys2['p'] + keys2['r']]
            csvwriter.writerow(book_data)


def read_n(parags, n):
    wlst = []
    for parag in parags:
        if not section_division(parag):
            for sent in parag:
                for tkn in sent:
                    if re.match(r'\w.*', tkn[2]):
                        wlst.append(tkn)
                    if len(wlst) >= n:
                        return wlst


def mk_lexrich_stats(lemmadictcsv, csvfile):
    cwl = corpus_15_19(corpus_work_list())
    add_listcats(cwl)
    common, nonrare = richness_sets(lemmadictcsv)
    vkeys = ['n', 'common', 'rare']
    for pos in ['all', 'NN', 'VB', 'JJ']:
        for vk in ['ttr']:  # ['t', 'n', 'ttr']
            vkeys.append(vk + pos)
    with open(csvfile, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(METAFIELDS + vkeys)
        for book in cwl:
            lemlist = {'all': [], 'NN': [], 'VB': [], 'JJ': []}
            parags = doc_conll_struct(book['file'])
            tokens = read_n(parags, 10000)
            for tkn in tokens:
                if tkn[4][:2] in ['NN', 'VB', 'JJ']:
                    lemlist[tkn[4][:2]].append(tkn[2])
                lemlist['all'].append(tkn[2] + '_' + tkn[4][:2])
            ccount = 0
            rarecount = 0
            for lm in sent_lemmas(tokens):
                if lm in common:
                    ccount += 1
                elif lm not in nonrare:
                    rarecount += 1
            vd = {'n': len(tokens),
                  'common': round(ccount / 10),  # permille from 10000
                  'rare': round(rarecount / 10)}
            for pos in ['all', 'NN', 'VB', 'JJ']:
                vd['n' + pos] = len(lemlist[pos])
                vd['t' + pos] = len(set(lemlist[pos]))
                vd['ttr' + pos] = round((1000*vd['t' + pos])/vd['n' + pos])
            book_data = [str(book[k]) for k in METAFIELDS]
            cat_rel_freqs = [str(vd[k]) for k in vkeys]
            csvwriter.writerow(book_data + cat_rel_freqs)


