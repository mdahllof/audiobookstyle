import csv
import re

from expaux.bs_04_19 import bests_file_name_dict, corpus_file_name_dict


def norm_paragr(pstring):
    pstring = re.sub('[«»"“]', '”', pstring)
    pstring = re.sub('[‘‹›]', '’', pstring)
    pstring = re.sub('[—]', '–', pstring)
    pstring = re.sub('[_▷↵→•·♥]', '', pstring)
    return pstring


def add_paragsep():
    ddir = [None, None]
    filedict = [None, None]
    ddir[0] = 'C:/corpuspop/bs_all_2004-2019/'
    filedict[0] = corpus_file_name_dict(ddir[0], 7, 10)
    ddir[1] = 'C:/corpuspop/bstream/'
    filedict[1] = corpus_file_name_dict(ddir[1], 8, 11)
    filepref = ['SvB_BS_', 'bstream_']
    for i in [0, 1]:
        for fid in filedict[i]:
            parags = []
            with open(ddir[i] + filedict[i][fid], 'r', encoding='utf8') as ins:
                for line in ins:
                    tln = line.strip()
                    if len(tln) > 0:
                        parags.append(tln)
            with open('C:/corpuspop/textprepro1/' + filepref[i] + fid + '.txt',
                      'w', encoding='utf8') as outs:
                for line in parags:
                    outs.write(norm_paragr(line))
                    outs.write('\n\n')
                    outs.write('Paragseparation!')
                    outs.write('\n\n')


def zzz_align_titles_filenames():
    filedict = bests_file_name_dict('C:/corpuspop/bs_all_2004-2019/')
    with open('C:/corpuspop/bs_all_2004-2019/bestsellers20042019.csv',
              newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0][7:10] in filedict:
                print(filedict[row[0][7:10]] + ' ' + row[1] + ' ' + row[2])
                print('')


def zzz_add_paragsep():
    filedict = bests_file_name_dict('C:/corpuspop/bs_all_2004-2019/')
    with open('C:/corpuspop/bs_all_2004-2019/bestsellers20042019.csv',
              newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0][7:10] in filedict:
                parags = []
                ddir = 'C:/corpuspop/bs_all_2004-2019/'
                with open(ddir + filedict[row[0][7:10]], 'r',
                          encoding='utf8') \
                        as ins:
                    for line in ins:
                        tln = line.strip()
                        if len(tln) > 0:
                            parags.append(tln)
                print(str(len(parags)) + ' ' + row[1] + ' ' + row[2])
                with open('C:/corpuspop/bsallstep1/SvB_BS_' +
                          row[0][7:10] + '.txt', "w", encoding='utf8') as outs:
                    for line in parags:
                        outs.write(norm_paragr(line))
                        outs.write('\n\n')
                        outs.write('Paragseparation!')
                        outs.write('\n\n')


def zzz_mod_tagged():
    filedict = bests_file_name_dict('C:/corpuspop/bsallstep2/', fext='.tag')
    with open('C:/corpuspop/bs_all_2004-2019/bestsellers20042019.csv',
              newline='', encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0][7:10] in filedict:
                tagtokens = []
                with open('C:/corpuspop/bsallstep2/' + filedict[row[0][7:10]],
                          'r', encoding='utf8') as ins:
                    for line in ins:
                        line = line.strip()
                        ls = line.split('\t')
                        if line == '':
                            if not (tagtokens[-1] == 'PARAGEND' or
                                    tagtokens[-1] == 'SENTEND'):
                                tagtokens.append('SENTEND')
                        elif len(ls) == 4 and ls[0] == 'Paragseparation':
                            if tagtokens[-1] == 'SENTEND':
                                tagtokens[-1] = 'PARAGEND'
                            elif tagtokens[-1] != 'PARAGEND':
                                tagtokens.append('PARAGEND')
                        elif len(ls) == 4 and ls[0] == '!' and \
                                tagtokens[-1] == 'PARAGEND':
                            pass
                        elif len(ls) == 4:
                            tagtokens.append(line)
                        elif len(ls) > 0:
                            print('UNEXPECTED: ' + line + row[0][7:10] +
                                  row[1] + ' ' + row[2])
                print(str(len(tagtokens)) + ' ' + row[1] + ' ' + row[2])
                with open('C:/corpuspop/bsallstep3/SvB_BS_' +
                          row[0][7:10] + '.txt', "w", encoding='utf8') as outs:
                    for line in tagtokens:
                        outs.write(line + '\n')



# add_paragsep()

# add_paragsep()

# mod_tagged()

#list_csv()