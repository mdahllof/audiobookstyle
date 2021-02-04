import re

from pop_aux.bs_04_19 import corpus_file_name_dict


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


add_paragsep()