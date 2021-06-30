import math

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from expaux.dataformatting import TermDict, TermEntry
from pop_exps.lex_comparison import abbdict

matplotlib.use('Agg')

colordict = {'CRIME': 'red', 'OTHER': 'blue', 'NONFIC': 'grey',
             'strm': 'red', 'sell': 'blue', 'both': 'gainsboro',
             'hb': 'red', 'pb': 'blue', 'no': 'gray',
             'na': 'gainsboro', 'undefined': 'gainsboro'}

adict = {'Paris': 'Paris', 'Westover': 'Westover', 'Hjorth': 'Hjorth',
         'Ferrante': 'Ferrante', 'Guillou': 'Guillou', 'Roslund': 'Roslund',
         'Adler-Olsen': 'Adler-Olsen', 'Gerhardsen': 'Gerhardsen',
         'Flynn': 'Flynn', 'Hawkins': 'Hawkins',
         'Läckberg': 'Läckberg', 'Kepler': 'Kepler',
         'Finn': 'Finn', 'Yanagihara': 'Yanagihara'}


class PointAppearance:

    def __init__(self, point_cats):
        self.clabels = list(set(point_cats))
        self.clabels.sort()
        self.color = ['blue', 'red', 'green', 'goldenrod', 'magenta', 'maroon',
                      'lime', 'darkgray', 'purple', 'yellow', 'black', 'blue',
                      'red', 'green', 'goldenrod', 'magenta', 'maroon', 'lime',
                      'darkgray', 'purple', 'yellow']
        self.marker = ['o', 'o', 'o', 'o', '.', '.', '.', '.', '.', '.', '.',
                       '.',
                       '<', '>', 'o', 'o', '^', 'o', '^', 'o', '^', 'o', '^',
                       'o', '^', 'o', '^', 'o', '^', 'o', '^', 'o']

    def col(self, cat):
        if cat in colordict:
            return colordict[cat]
        return self.color[self.clabels.index(cat)]

    def mrkr(self, cat):
        if cat == 'undefined':
            return 'o'
        return self.marker[self.clabels.index(cat)]


def scatter2dim(x, transf, point_cats, point_labels, imgfile, axis_lbls=[],
                title=''):
    trnsfd = transf.transf(x, point_cats)
    plt.figure(figsize=(9, 5))
    subfig, ax = plt.subplots()
    if len(axis_lbls) > 1:
        plt.xlabel(axis_lbls[0], fontsize=8)
        plt.ylabel(axis_lbls[1], fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=5)
    ax.tick_params(axis='both', which='minor', labelsize=5)
    pa = PointAppearance(point_cats)
    cat_count = TermDict()
    # regions(point_cats, trnsfd, pa)
    # boundary(point_cats, trnsfd, 7, ax)
    for i in range(len(trnsfd)):
        cat_count.update_dict(point_cats[i], lowercase=False)
        ax.scatter(trnsfd[i][0], trnsfd[i][1], marker=pa.mrkr(point_cats[i]),
                   s=6, c=pa.col(point_cats[i]))
        opx = -2 * len(point_labels[i])
        ax.annotate(point_labels[i], (trnsfd[i][0], trnsfd[i][1]),
                    fontsize=6, color='black', textcoords='offset points',
                    xytext=(opx, 3))
    cathandles = []
    cat_sort = []
    for ct in cat_count.keys():
        cat_sort.append(TermEntry(ct, cat_count[ct]))
    cat_sort.sort()
    for ctw in cat_sort:
        clabel = abbdict.get(ctw.term, ctw.term) + ' [' + str(ctw.val) + ']'
        cathandles.append(
            Line2D([0], [0], label=clabel, marker=pa.mrkr(ctw.term), color='w',
                   markerfacecolor=pa.col(ctw.term), markersize=5))
    plt.legend(handles=cathandles, prop={'size': 5})
    plt.title(title)
    plt.savefig(imgfile + '.png', dpi=600, bbox_inches='tight')
    print('SAVED: ' + imgfile + '.png')
    plt.close(subfig)
    plt.close()


class NoTransf:
    def __init__(self, f1, f2, fact=(1.0, 1.0)):
        self.f1 = f1
        self.f2 = f2
        self.fact = fact

    def transf(self, x, y):
        f1 = [float(val) * self.fact[0] for val in x[self.f1]]
        f2 = [float(val) * self.fact[1] for val in x[self.f2]]
        return [(f1[i], f2[i]) for i in range(len(f1))]


def scatter_raw2(datafr, ix, iy, im_file, compcats=['sex', 'genre'],
                 axis_lbls=None, title='', axisfact=(0.001, 0.001),
                 unts=('', ''), ofint=[]):
    for col in compcats:
        # datafr.query(col + ' != "na"', inplace=True)
        x = datafr.loc[:, [ix, iy]]
        if not axis_lbls:
            ixl, iyl = abbdict.get(ix, ix), abbdict.get(iy, iy)
            axis_lbls = [ixl + unts[0], iyl + unts[1]]
        title2 = axis_lbls[0] + ' vs ' + axis_lbls[1]
        labs = datafr[col].to_list()
        # albs = [val[0:5] for val in datafr['author1']]
        # tlbs = [val[0:5] for val in datafr['title']]
        # plabels = [albs[i] + tlbs[i] for i in range(len(albs))]
        # auths = [adict.get(val.split(",")[0], '') for val in datafr['author1']]
        ids = [val for val in datafr['id']]
        auths = [val.split(",")[0] for val in datafr['author1']]
        auths2 = [val for val in datafr['author2']]
        for i in range(len(ids)):
            if ids[i] in ofint:
                print(ids[i] + ' & ' + auths[i])
                if isinstance(auths2[i], str) and auths2[i] != '':
                    print(auths2[i])
                    auths[i] = auths[i] + ' & ' + auths2[i].split(" ")[1]
            else:
                auths[i] = ''
                # plabels = ['' for _ in datafr['author1']]
        for i in range(0, len(labs)):
            if labs[i] == 'na':
                auths[i] = ''
        scatter2dim(x, NoTransf(ix, iy, fact=axisfact), labs, auths,
                    im_file + '_' + ix + '_' + iy + '_' + col,
                    axis_lbls=axis_lbls, title=title2)
