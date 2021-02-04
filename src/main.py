from pop_aux.exphelp import make_dir
from pop_exps.plotting_aux import scatter_raw
from pop_exps.dict_aux import mk_struct_stats, mk_lexrich_stats, \
    mk_corpus_check_art1, mk_gram_relfrqs
from pop_exps.lex_comparison import make_ranked_lists, make_comps
from pop_exps.lex_diversity import mk_lemma_freq_dict


def scatter_struct(dictcsv, wdir):
    make_dir(wdir)
    cc = ['frmt1', 'frmt2', 'category']
    title = 'Basic measures per book'
    for f, g in [('slm', 'ddm'), ('slm', 'plm')]:
        scatter_raw(dictcsv, f, g, wdir + 'strusts',
                    compcats=cc, title=title, axisfact=(0.001, 0.001))


def scatter_pos(dictcsv, wdir):
    make_dir(wdir)
    cc = ['frmt1', 'frmt2', 'category']
    title = 'POS rel. freqs., per book, in %'
    for f, g in [('p_nn', 'p_vb'), ('p_nn', 'p_jj'), ('p_vb', 'p_jj')]:
        scatter_raw(dictcsv, f, g, wdir + 'pos',
                    compcats=cc, title=title, axisfact=(0.0001, 0.0001))


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


def generate_comparisons(dicts_dir, res_dir):
    comps_dir = res_dir + 'comps/'
    make_dir(comps_dir)
    plots_dir = res_dir + 'comps/plots/'
    make_dir(comps_dir)
    rankedlists_dir = res_dir + 'comps/lists/'
    make_dir(rankedlists_dir)
    comparisons = [('frmt2', 'sell', 'strm', '', ''),
                   ('frmt2', 'sell', 'strm', 'category', 'CRIME_OTHER'),
                   ('frmt1', 'hb', 'pb', '', ''),
                   ('frmt2', 'sell', 'strm', 'category', 'CRIME'),
                   ('frmt2', 'sell', 'both', '', ''),
                   ('frmt2', 'sell', 'strm_both', '', ''),
                   ('frmt2', 'strm', 'both', '', ''),
                   ('frmt2', 'strm', 'sell_both', '', ''),
                   ('category', 'PRESTIGE', 'CRIME_OTHER', '', ''),
                   ('category', 'CRIME', 'PRESTIGE_OTHER', '', '')]
    dict_csvs = [dicts_dir + 'gram_relfrqs.csv',
                 dicts_dir + 'lexrich_stats.csv',
                 dicts_dir + 'struct_stats.csv']
    # Generate the comparisons
    make_comps(dict_csvs, comparisons, comps_dir)
    # Generate, for each measure, a list of the works ranked by that measure
    make_ranked_lists(dict_csvs, rankedlists_dir)
    # Generate scatter plots based on selected pairs of measures
    scatter_struct(dicts_dir + 'struct_stats.csv', plots_dir)
    # Generate scatter plots based on selected pairs of measures
    scatter_pos(dicts_dir + 'gram_relfrqs.csv', plots_dir)


if __name__ == '__main__':
    results_dir = '../results/'
    make_dir(results_dir)
    dicts_dir = results_dir + 'dicts/'
    make_dir(dicts_dir)
    # generate_data_from_corpus(dicts_dir) # requires corpus
    generate_comparisons(dicts_dir, results_dir)
