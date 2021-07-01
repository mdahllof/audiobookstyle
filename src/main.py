import pandas as pd

from expaux.dataformatting import make_dir
from pop_exps.dict_aux import mk_corpus_check_art1, mk_gram_relfrqs, \
    mk_lexrich_stats, mk_struct_stats
from pop_exps.lex_comparison import make_comps, make_ranked_lists
from pop_exps.lex_diversity import mk_lemma_freq_dict
from pop_exps.plotting_style import scatter_raw2


def make_stylometric_scatter_plots(dicts_dir, wdir):
    make_dir(wdir)
    feats_csv1 = dicts_dir + 'gram_relfrqs.csv'
    feats_csv2 = dicts_dir + 'struct_stats.csv'
    datafr1 = pd.read_csv(feats_csv1, header=0, encoding='utf-8')
    datafr2 = pd.read_csv(feats_csv2, header=0, encoding='utf-8')
    datafr2 = datafr2.loc[:, 'wc':]
    datafr = pd.concat([datafr1, datafr2], axis=1)
    ofinterest1 = {'SvB_BS_188', 'SvB_BS_211', 'SvB_BS_212',
                   'SvB_BS_307', 'SvB_BS_300', 'SvB_BS_272',
                   'bstream_005', 'bstream_017', 'bstream_038',
                   'SvB_BS_300', 'SvB_BS_293', 'SvB_BS_202',
                   'bstream_031', 'bstream_051'}
    ofinterest2 = {'SvB_BS_300', 'SvB_BS_281', 'SvB_BS_184',
                   'SvB_BS_211', 'SvB_BS_212', 'SvB_BS_307',
                   'SvB_BS_197', 'SvB_BS_293', 'SvB_BS_273',
                   'SvB_BS_280', 'SvB_BS_256', 'bstream_031'}
    ofinterest3 = {'SvB_BS_300', 'SvB_BS_283', 'bstream_031', 'SvB_BS_307',
                   'SvB_BS_293', 'SvB_BS_264', 'SvB_BS_289',
                   'SvB_BS_156', 'SvB_BS_247', 'SvB_BS_171', 'SvB_BS_192',
                   'SvB_BS_244', 'SvB_BS_245', 'SvB_BS_252', 'SvB_BS_253',
                   'SvB_BS_293', 'SvB_BS_264', 'SvB_BS_289', 'bstream_002',
                   'SvB_BS_285', 'SvB_BS_292', 'bstream_031', 'bstream_006'}
    for cc, f, g, axf, unts, title, ofint, in \
            [('frmt2', 'ddm', 'p_pm', (0.001, 0.0001), ('', ' (%)'),
              'Basic measures per book', ofinterest1),
             ('frmt2', 'p_ma', 'p_nn', (0.0001, 0.0001), (' (%)', ' (%)'),
              'POS rel. freqs., per book, in %', ofinterest2),  # *
             ('frmt2', 'p_vb', 'p_jj', (0.0001, 0.0001), (' (%)', ' (%)'),
              'POS rel. freqs., per book, in %', ofinterest3)]:  # *
        scatter_raw2(datafr, f, g, wdir + 'strusts', compcats=[cc],
                     title=title, axisfact=axf, unts=unts, ofint=ofint)


def generate_data_from_corpus(dicts_dir):
    # These steps require that you have the corpus
    # which is protected by copyright.
    # Just listing the works
    mk_corpus_check_art1(dicts_dir + 'corpus_check_art1.csv')
    # Compile "structural" features
    mk_struct_stats(dicts_dir + 'struct_stats.csv')
    # Compile lemma (relative) frequencies
    mk_lemma_freq_dict(dicts_dir + 'lemma_freqs.csv')
    # Compile pos and UD relation relative frequencies (two steps/files)
    mk_gram_relfrqs(dicts_dir + 'gram_relfrqs')
    # Compile relative frequencies based on lexical diversity
    mk_lexrich_stats(dicts_dir + 'lemma_freqs.csv',
                     dicts_dir + 'lexrich_stats.csv')


def generate_comparisons_gend(dicts_dir, res_dir):
    comps_dir = res_dir + 'comps/'
    comparisons = [('author_gender', 'F', 'M', '', ''),
                   ('author_gender', 'F', 'M', 'frmt2', 'sell'),
                   ('author_gender', 'F', 'M', 'frmt2', 'strm'),
                   ('author_gender', 'F', 'M', 'category', 'PRESTIGE_OTHER'),
                   ('author_gender', 'F', 'M', 'category', 'CRIME')]
    dict_csvs = [dicts_dir + 'gram_relfrqs.csv',
                 dicts_dir + 'lexrich_stats.csv',
                 dicts_dir + 'struct_stats.csv']
    # Generate the comparisons
    make_comps(dict_csvs, comparisons, comps_dir, 'comps_gend.tex')


def generate_comparisons(dicts_dir, res_dir):
    comps_dir = res_dir + 'comps/'
    make_dir(comps_dir)
    plots_dir = res_dir + 'comps/plots/'
    make_dir(comps_dir)
    rankedlists_dir = res_dir + 'comps/lists/'
    make_dir(rankedlists_dir)
    comparisons = [('frmt2', 'sell', 'strm', '', ''),
                   ('frmt2', 'sell', 'strm', 'category', 'CRIME')]
    dict_csvs = [dicts_dir + 'gram_relfrqs.csv',
                 dicts_dir + 'lexrich_stats.csv',
                 dicts_dir + 'struct_stats.csv']
    # Generate the comparisons
    make_comps(dict_csvs, comparisons, comps_dir, 'cles_tables.tex')
    # Generate, for each measure, a list of the works ranked by that measure
    make_ranked_lists(dict_csvs, rankedlists_dir)
    # Generate scatter plots based on selected pairs of measures
    make_stylometric_scatter_plots(dicts_dir, plots_dir)


if __name__ == '__main__':
    results_dir = '../results/'
    make_dir(results_dir)
    dictionary_dir = results_dir + 'dicts/'
    make_dir(dictionary_dir)
    # generate_data_from_corpus(dictionary_dir)  # requires corpus
    # generate_comparisons_gend(dicts_dir, results_dir)
    generate_comparisons(dictionary_dir, results_dir)
