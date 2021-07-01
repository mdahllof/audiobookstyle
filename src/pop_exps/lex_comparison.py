import csv
import re

from scipy.stats import mannwhitneyu

from expaux.bs_04_19 import METAFIELDS
from expaux.dataformatting import TermEntry, store_on_csv

ignore_feats = ['n', 'nNN', 'nJJ', 'nVB', 'tNN', 'tNN', 'tVB',
                'ddsd', 'slsd', 'slm', 'plsd',
                'r_punct', 'r_advmod', 'r_case', 'r_root', 'r_det',
                'r_amod', 'r_nmod', 'r_nmod:poss', 'r_nummod', 'r_obl',
                'r_compound:prt', 'r_flat:name', 'r_cc', 'r_conj']

abbdict1 = {'p_ma': 'sentence-terminal punctuation (mad)',
            'p_mi': 'intersentential punctuation (mid)',
            'p_pa': 'pairwise delimiter (pad)'}

abbdict = {'hb': 'hardback',
           'pb': 'paperback',
           'sell': 'bestseller',
           'strm': 'beststreamer',
           'both': 'crossover',
           'CRIME': 'crime',
           'PRESTIGE': 'prestige',
           'strm_both': 'other',
           'sell_both': 'other',
           'OTHER': 'middlebrow',
           'CRIME_OTHER': 'non-prestige',
           'PRESTIGE_OTHER': 'non-crime',
           'F': 'female',
           'M': 'male', 'p_pm': 'proper noun',
           'r_appos': 'appositional modifier',
           'wc': 'document length (word count)',
           'ddsd': 'dependency depth, standard deviation',
           'ddm': '(mean) dependency depth',
           'slm': 'sentence length (mean)',
           'slsd': 'sentence length (SD)',
           'plsd': 'paragraph length (SD)',
           'plm': '(mean) paragraph length',
           'ttrNN': 'type-token ratio, nouns',
           'ttrJJ': 'type-token ratio, adjectives',
           'ttrVB': 'type-token ratio, verbs',
           'rare': 'rare words',
           'r_obj': 'direct object',
           'r_iobj': 'indirect object',
           'r_orphan': 'orphan',
           'r_obl': 'prepositional complement/modifier',
           'r_acl': 'clausal modifier of noun',
           'r_conj': 'conjunct',
           'r_cop': 'copula',
           'r_punct': 'punctuation',
           'r_root': 'topmost node',
           'r_compound:prt': 'verb-particle relation',
           'r_fixed': 'multi-word expression relation',
           'r_aux': 'auxiliary',
           'r_aux:pass': 'passive auxiliary',
           'r_nsubj': 'nominal subject',
           'r_advcl': 'adverbial clause modifier',
           'r_advmod': 'adverbial modifier',
           'r_flat:name': 'name relation',
           'r_cc': 'conjunction-conjunct relation',
           'r_csubj:pass': 'clausal passive subject',
           'r_acl:relcl': 'relative clause modifier',
           'r_discourse': 'discourse element',
           'r_ccomp': 'clausal complement',
           'nJJ': 'adjective (first 10000)',
           'p_jj': 'adjective',
           'p_in': 'interjection',
           'p_hd': 'interrogative/relative determiner',
           'p_ha': 'WH-adverb',
           'p_hp': 'interrogative/relative pronoun',
           'p_hs': 'WH-possessive',
           'p_rg': 'cardinal numeral',
           'p_kn': 'conjunction',
           'p_sn': 'subordinating conjunction',
           'p_ab': 'adverb',
           'p_ma': 'sentence-terminal punctuation',
           'p_mi': 'intersentential punctuation',
           'p_nn': 'noun',
           'p_pn': 'pronoun',
           'p_pc': 'participle',
           'p_ro': 'ordinal numeral',
           'p_pl': '(verb) particle',
           'p_ps': 'possessive/genitive pronoun',
           'p_vb': 'verb',
           'p_uo': 'foreign language word',
           'r_nmod': 'prepositional modifier',
           'common': 'high frequency words',
           'r_nsubj:pass': 'passive nominal subject',
           'nVB': 'verb (first 10000)',
           'r_det': 'determiner (dependency relation)',
           'p_dt': 'determiner'}


def csv_data(csvfile):
    with open(csvfile, newline='', encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        return [bk for bk in csvreader]


def extr_vals(book_data, metr, cmpsn, ind):
    vals = []
    for bk0 in book_data:
        # ('frmt2', 'sell', 'strm', 'category', 'CRIME_OTHER')
        if (cmpsn[3] == '' or bk0[cmpsn[3]] in cmpsn[4]) and \
                bk0[cmpsn[0]] in cmpsn[ind]:
            vals.append(float(bk0[metr]))
    return vals


def check_feat(book_data, metr, cmpsn):
    v_c0, v_c1 = 0, 0
    vals0 = extr_vals(book_data, metr, cmpsn, 1)
    vals1 = extr_vals(book_data, metr, cmpsn, 2)
    # u1s, p1s = mannwhitneyu(vals0, vals1, alternative='less')
    u2s, p2s = mannwhitneyu(vals0, vals1, alternative='two-sided')
    # u2si, p2si = mannwhitneyu(vals1, vals0, alternative='two-sided')
    for v0 in vals0:
        for v1 in vals1:
            if v0 == v1:
                v_c0 += 0.5
                v_c1 += 0.5
            elif v0 > v1:
                v_c0 += 1
            else:
                v_c1 += 1
    return round((1000 * v_c0) / (v_c0 + v_c1)), len(vals0), len(vals1), \
           v_c0, v_c1, u2s, p2s  # u2si, p2si


def make_comps(datacsvs, comparisons, wd, latexf):
    # datacsv = 'C:/popres/gram_stats/gram_relfrqs2.csv'
    comparisons_double = []
    for c in comparisons:
        comparisons_double.append(c)
        comparisons_double.append((c[0], c[2], c[1]) + c[3:5])
    comps = []
    sel_comps = {}
    subset_sizes = {}
    smallest_or = 1000
    metrics_collected = []
    for cmpsn in comparisons_double:
        sel_comps[cmpsn] = []
    for datacsv in datacsvs:
        with open(datacsv, newline='', encoding='utf8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                metrics = row[len(METAFIELDS):]
                break
        # ydict = first_list_year(BS_LISTPLACES)
        book_data = csv_data(datacsv)
        for metr in metrics:
            if metr not in ignore_feats and not re.match(r'r_.*', metr):
                metrics_collected.append(metr)
                for cmpsn in comparisons_double:
                    val = check_feat(book_data, metr, cmpsn)
                    subset_sizes[cmpsn] = (str(val[1]), str(val[2]))
                    comps.append([str(val[0]),
                                  # '{:.15f}'.format(val[6]),
                                  metr] + list(cmpsn) +
                                 [str(val[1]), str(val[2]), str(val[3]),
                                  str(val[4]), str(val[5])])
                    if float(val[0]) >= 645: # and val[6] < 0.05:
                        smallest_or = min(float(val[0]), smallest_or)
                        trow = [str(val[0]), '{:.15f}'.format(val[6]),
                                metr, str(cmpsn), str(val[1]), str(val[2])]
                        sel_comps[cmpsn].append(TermEntry(trow, float(val[0])))
    store_on_csv(wd + 'cont_feats.csv', comps)
    table_latex(comparisons_double, sel_comps, subset_sizes, wd + latexf)
    print(smallest_or)
    store_on_csv(wd + 'metrics_collected.csv',
                 [[m] for m in metrics_collected])


def table_latex(comparisons, sel_comps, subset_sizes, filem):
    with open(filem, mode='w', newline=None, encoding='utf-8') as op:
        op.write('\\documentclass[11pt]{article}\n')
        op.write('\\usepackage{fontspec}\n')
        op.write('\\setmainfont{Arial}\n\n')
        op.write('\\begin{document}\n\n')
        op.write('\\noindent  Karl Berglund \\& Mats Dahllöf ' +
                 '\\hfill July 2021\n\n')
        op.write('\\noindent  \\textbf{Audiobook Stylistics: ' +
                 'Comparing Print and Audio in the Bestselling Segment}\n\n')
        op.write('\\section*{CLES comparison tables}\n\n')
        for cmpsn in comparisons:
            (n1, n2) = subset_sizes[cmpsn]
            cc = abbdict[cmpsn[1]] + ' (' + n1 + ') vs ' + \
                 abbdict[cmpsn[2]] + ' (' + n2 + ')'
            if cmpsn[4] != '':
                cc += ' (' + abbdict[cmpsn[4]] + ' only)'
            cc = cc[0:1].upper() + cc[1:]
            op.write('\\subsection*{' + cc + '}\n')
            op.write('')
            op.write('\\begin{tabular}{|lr|}\\hline\n')
            op.write('\\makebox[75mm][l]{\\textbf{Feature}} & ' +
                     '\\makebox[20mm][r]{\\textbf{CLES}}' +
                     '\\rule{0pt}{4mm}' +
                     # ' & \\makebox[20mm][r]{\\textbf{p-value}}' +
                     '\\\\\n')
            sel_comps[cmpsn].sort()
            for comp in sel_comps[cmpsn]:
                feat_row(comp.term, op)
            op.write('\\hline\n\\end{tabular}\n\n')
        op.write('\\end{document}\n')


def feat_row(comp, op):
    featl1 = re.sub('^p_', '(', comp[2])
    featl2 = re.sub('^r_', '(UD: ', featl1)
    featl = re.sub('_', '\\_', featl2)
    featl += ')'
    feat = abbdict.get(comp[2], featl) + ' ' + featl
    if featl[0] != '(':
        feat = abbdict.get(comp[2], featl)
    if comp[2] in abbdict1:
        feat = abbdict1[comp[2]]
    ccol = ''
    if float(comp[1]) > 0.05:
        ccol = '$\\ast$\\makebox[1mm]{}'
    orperc = float(comp[0]) / 10
    op.write(feat + ' & ' + str(orperc)
             # '\\% & ' + ccol +
             # '{\\footnotesize ' + '{:.2e}'.format(float(comp[1])) + '}'
             + '\\\\\n')


def make_ranked_lists(datacsvs, resdir):
    for datacsv in datacsvs:
        with open(datacsv, newline='', encoding='utf8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                metrics = row[len(METAFIELDS):]
                break
        book_data = csv_data(datacsv)
        for metr in metrics:
            if metr not in ignore_feats and not re.match(r'r_.*', metr):
                books = []
                for bk in book_data:
                    bkentry = [str(bk[k]) for k in METAFIELDS]
                    books.append(TermEntry(bkentry, int(bk[metr])))
                books.sort()
                metr_no_colon = re.sub('[:]', '_', metr)
                csvfile = resdir + 'list_' + metr_no_colon + '.csv'
                with open(csvfile, mode='w', newline='',
                          encoding='utf-8') as csvf:
                    csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow([metr] + METAFIELDS)
                    for bk in books:
                        csvwriter.writerow([bk.val] + bk.term)
