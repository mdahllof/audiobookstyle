import csv
import os
import re

META_DIR = 'C:/popcorpus/meta/'
CONLL_DIR = 'C:/popcorpus/conll/'
STANZA_DIR = 'C:/popcorpus/stanza/'
BS_CORPUS = META_DIR + 'book_data_201113.csv'
LISTDATA15_19 = META_DIR + 'list_positions_201203.csv'
BS_dstyle = META_DIR + 'dial_style.csv'  # MD 200918

NREGEX = r'(först|två|andra|trett|fyr|fjärd|fem|sext|sjund|' + \
         r'sjutt|ått|nio|nitt|tio|elv|elft|tolf|tolv|fjor|tjug|fört).*'

METAFIELDS = ['id', 'title', 'author1', 'author2', 'author_gender', 'category',
              'frmt1', 'frmt2']


# def corpus_list(csvfile=BS_04_19_CSV_v2):
#     corpus = []
#     with open(csvfile, newline='', encoding='utf8') as csvfile:
#         csvreader = csv.reader(csvfile)
#         for row in csvreader:
#             corpus.append(row)
#     return corpus


def csv_table(csvfile, key_fieldname):
    corpusd = {}
    with open(csvfile, newline='', encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if re.match(r'.*\d\d\d', row[key_fieldname]):
                corpusd[row[key_fieldname]] = row
    return corpusd


def add_listcats(cwl):
    listdata = csv_table(LISTDATA15_19, 'id')
    for book in cwl:
        hb = re.match(r'\d.*', listdata[book['id']]['hb_year'])
        pb = re.match(r'\d.*', listdata[book['id']]['pb_year'])
        bs_def = listdata[book['id']]['str_year']
        bs = re.match(r'\d.*', listdata[book['id']]['str_year'])
        book['frmt1'] = 'no'
        if hb and pb:
            book['frmt1'] = 'both'
        elif hb:
            book['frmt1'] = 'hb'
        elif pb:
            book['frmt1'] = 'pb'
        book['frmt2'] = 'na'
        if bs_def == 'na':
            book['frmt2'] = 'na'
        elif book['frmt1'] != 'no' and bs:
            book['frmt2'] = 'both'
        elif bs:
            book['frmt2'] = 'strm'
        elif book['frmt1'] != 'no':
            book['frmt2'] = 'sell'


def corpus_dict(csvfile):
    corpusd = {}
    with open(csvfile, newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if re.match(r'.*\d\d\d', row[0]):
                corpusd[row[0]] = row
    return corpusd


# bstream_001_allakansedig
def corpus_file_name_dict(ddir, i, j, fext='.txt'):
    filedict = {}
    for root, dirs, files in os.walk(ddir):
        for file in files:
            if file.endswith(fext):
                filedict[file[i:j]] = file
    return filedict


def text_spans(doclen, chunk_size, max_spans):
    if doclen < chunk_size:
        return [(0, doclen)]
    sl = min(doclen // chunk_size, max_spans)
    spans = [(0, round(doclen / sl))]
    for sp in range(sl - 1, 0, -1):
        spans.append(
            (spans[-1][1], spans[-1][1] + round((doclen - spans[-1][1]) / sp)))
    return spans


# corpus_work_list(BS_CORPUS, BS_PARSED_DIR, fext='.conll')

# SvB_BS_001_Da Vinci-koden
def bests_file_name_dict(ddir, regex='.*', fext='.txt'):  # old
    filedict = {}
    fextl = len(fext)
    for root, dirs, files in os.walk(ddir):
        for file in files:
            if re.match(regex, file) and file.endswith(fext):
                fid = file[:-fextl]
                filedict[fid] = file
    return filedict


def sent_lemmas(sent):
    lemlst = []
    for ls in sent:
        if re.match(r'\w.*', ls[2]) and \
                not re.match(r'\d.*', ls[2]) and \
                not re.match(r'PM.*', ls[4]):
            lemlst.append((ls[2] + '_' + ls[4][:2]).lower())
    return lemlst


def work_list_conll():
    wl = []
    filedict1 = bests_file_name_dict(CONLL_DIR, regex='Sv.*', fext='.conll')
    filedict2 = bests_file_name_dict(CONLL_DIR, regex='bs.*', fext='.conll')
    ydict = list_years(LISTDATA15_19)
    with open(BS_CORPUS, newline='', encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if re.match('Sv.*', row['id']) and row['id'] in filedict1:
                row['file'] = CONLL_DIR + filedict1[row['id']]
            elif re.match('bs.*', row['id']) and row['id'] in filedict2:
                row['file'] = CONLL_DIR + filedict2[row['id']]
            row['listyears'] = str(ydict[row['id']])
            wl.append(row)
    return wl


def work_list():
    wl = []
    ydict = list_years(LISTDATA15_19)
    with open(BS_CORPUS, newline='', encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            row['listyears'] = str(ydict[row['id']])
            wl.append(row)
    return wl


def corpus_15_19(cwl):
    sel = []
    for book in cwl:
        for y in ['2015', '2016', '2017', '2018', '2019']:
            if y in book['listyears'] and book['category'] != 'NONFIC':
                sel.append(book)
                break
    return sel


def match_re_ind(regexs, name):
    for i in range(0, len(regexs)):
        if re.match(regexs[i], name):
            return i
    return -1


def sel_works_by_auth_re(regexs, cwl):
    sel_works = []
    for row in cwl:
        re_ind = match_re_ind(regexs, row[1].strip())
        if re.match('.*\\d\\d\\d', row[0].strip()) and re_ind != -1:
            sel_works.append(row)
    return sel_works


def doc_tokens(cfile):
    dt = []
    with open(cfile, newline='', encoding='utf-8') as infile:
        for line in infile:
            pcs = line.strip().split('\t')
            if len(pcs) == 10:
                dt.append(pcs)
    return dt


def doc_conll_tokens(cfile):
    toks = []
    with open(cfile, newline='', encoding='utf-8') as infile:
        ps = False
        for line in infile:
            pcs = line.strip().split('\t')
            if len(pcs) == 10:
                if pcs[1] == 'Paragseparation':
                    ps = True
                elif not ps:
                    toks.append(pcs)
                elif pcs[1] == '!':
                    ps = False
                else:
                    print(ps, 'Error in doc_conll_tokens: ' + line)
            elif len(line.strip()) > 0:
                print('Line not 10 comps in doc_conll_tokens:' + line)
    return toks


def add_udpaths(sent):
    for i in range(len(sent)):
        path = [sent[i][7]]
        parent = int(sent[i][6])
        while parent != 0:
            path = [sent[parent - 1][7]] + path
            parent = int(sent[parent - 1][6])
        sent[i].append(path)


def doc_conll_struct(cfile, add_ud_paths=False):
    parags = [[[]]]
    with open(cfile, newline='', encoding='utf-8') as infile:
        ps = False
        for line in infile:
            pcs = line.strip().split('\t')
            if len(pcs) == 10:
                if pcs[1] == 'Paragseparation':
                    ps = True
                    if parags[-1] != [[]]:
                        parags.append([[]])
                elif ps and pcs[1] == '!':
                    ps = False
                elif not ps and pcs[0] == '1':
                    if parags[-1][-1]:
                        parags[-1].append([pcs])
                    else:
                        parags[-1][-1].append(pcs)
                elif not ps:
                    parags[-1][-1].append(pcs)
                else:
                    print(ps, 'Error in doc_conll_struct: ' + line)
            elif len(line.strip()) > 0:
                print('Line not 10 comps in doc_conll_struct:' + line)
    if parags[-1] and not parags[-1][-1]:
        parags[-1] = parags[-1][:-1]
    if not parags[-1]:
        parags = parags[:-1]
    if add_ud_paths:
        for i in range(len(parags)):
            for sent in parags[i]:
                add_udpaths(sent)
    return parags


def toks_from_csv(csvfile):
    toks = []
    with open(csvfile, newline='', encoding='utf8') as csvf:
        csvreader = csv.reader(csvf)
        for tok in csvreader:
            toks.append(tok)
    return toks


def parag_sequence_from_csv(toks):
    parags = [[[]]]
    wc, sc, pc = 0, 0, 0
    for i, pcs in enumerate(toks):
        pcs.append(-1)
        pcs[8] = i
        wc += 1
        if str(pcs[0]) == '1' and pcs[1] == '§':
            pc += 1
            sc += 1
            if parags[-1] != [[]]:
                parags.append([[]])
        elif str(pcs[0]) == '1':
            sc += 1
            if parags[-1][-1]:
                parags[-1].append([pcs])
            else:
                parags[-1][-1].append(pcs)
        else:
            parags[-1][-1].append(pcs)
    if parags[-1] and not parags[-1][-1]:
        parags[-1] = parags[-1][:-1]
    if not parags[-1]:
        del parags[-1]
    return parags


def section_division(parag):
    if len(parag) > 1 or parag[0][0][1] in ['–', '”', '…', '(']:
        return False
    tlist = []
    for token in parag[0]:
        if re.match(r'[\w\d].*', token[1]):
            tlist.append(token[1].lower())
    if len(tlist) == 0:
        return True
    if len(tlist) == 1:
        if tlist[0] in ['i', 'tre', 'sex', 'sju', 'vi']:
            return True
        if re.match(NREGEX, tlist[0]):
            return True
        if re.match(r'[\d].*', tlist[0]):
            return True
        if re.match(r'(ii|iv|vii|ix|xi).*', tlist[0]):
            return True
        if tlist[0] in ['v', 'x']:
            return True
    if len(tlist) == 2 and tlist[1] in ['kapitlet']:
        return True
    if 0 < len(tlist) < 3 and tlist[0] in ['dag', 'del', 'kapitel']:
        return True
    return False


def list_years(csvfile):
    ydict = {}
    with open(csvfile, newline='', encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for bk in csvreader:
            years = ['na', 'na', 'na']
            fields = ['hb_year', 'pb_year', 'str_year']
            for i in range(0, 3):
                if re.match(r'\d\d\d\d.*', str(bk[fields[i]])):
                    years[i] = str(bk[fields[i]])[0: 4]
                else:
                    years[i] = str(bk[fields[i]])
            ydict[bk['id']] = years[0] + '_' + years[1] + '_' + years[2]
    return ydict

# if __name__ == '__main__':
