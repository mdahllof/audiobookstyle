import re
import csv

encoding_for_dictionary_files = 'utf-8-sig'
separator = '@'  # in word/number dictionary files
separCatSymb = '*'  # in word/number dictionary files


class TermEntry:
    """Used internally for frequency sorting."""

    def __init__(self, term, val):
        self.term = term
        self.val = val

    def __lt__(self, other):
        if self.val == other.val:
            return self.term < other.term
        return self.val > other.val

    def as_string(self):
        return self.term + separator + str(self.val)


class TermDict:
    """"For dictionaries of terms associated with numerical values, e.g. frequency."""

    def __init__(self, file=None):
        self._DCTN = {}
        if file is not None:
            line_nr = 0
            with open(file, encoding=encoding_for_dictionary_files) as infile:
                for line in infile:
                    (symb, _, fr) = line.partition(separator)
                    self._DCTN[symb] = int(fr)
                    line_nr = line_nr + 1
            print('TermDict from ' + file + ' (' + str(line_nr) + ' entries)')

    def __iter__(self):
        yield from self._DCTN.items()

    def __getitem__(self, key):
        if key in self._DCTN:
            return self._DCTN[key]
        return 0

    def __setitem__(self, key, val):
        self._DCTN[key] = val

    def put(self, key, val):
        self._DCTN[key] = val

    def keys(self):
        return self._DCTN.keys()

    def keylist(self):
        kl = list(self._DCTN.keys())
        kl.sort()
        return kl

    def keyset(self):
        ks = set(self._DCTN.keys())
        return ks

    def update_dict(self, key, val=1, lowercase=True):
        if lowercase:
            key = key.lower()
        if key in self._DCTN:
            self._DCTN[key] = self._DCTN[key] + val
        else:
            self._DCTN[key] = val

    def divide_all(self, divs):
        for key in self._DCTN:
            self._DCTN[key] = self._DCTN[key] / divs

    def add_dict(self, ddict):
        for key, value in ddict:
            self.update_dict(key, val=value)

    def get_top_scored(self, size): # Rather use the next method
        wordlist = [TermEntry(key, self._DCTN[key])
                    for key in self._DCTN.keys()]
        wordlist.sort()
        return [wordlist[i].term for i in range(0, min(size, len(wordlist)))]

    def top_scored_terms(self, size):
        wordlist = [TermEntry(key, self._DCTN[key])
                    for key in self._DCTN.keys()]
        wordlist.sort()
        return wordlist[0:size]

    def min_freq_terms(self, freq):
        trms = []
        for key in self._DCTN.keys():
            if self._DCTN[key] >= freq:
                trms.append(key)
        return trms

    def print(self):
        wordlist = [TermEntry(key, self._DCTN[key])
                    for key in self._DCTN.keys()]
        wordlist.sort()
        print([word.term + ':' + str(word.val) for word in wordlist])

    def store_dict_fr(self, file, min_fr=0):
        """For storing a dictionary, frequency sorted."""
        if not file[-4:] == '.txt':
            file = file + '.txt'
            print('Added txt extension to ' + file)
        w_lst = []
        for key in self._DCTN.keys():
            if self._DCTN[key] >= min_fr:
                w_lst.append(TermEntry(key, self._DCTN[key]))
        w_lst.sort()
        text_file = open(file, "w", encoding=encoding_for_dictionary_files)
        for i in range(len(w_lst)):
            text_file.write(w_lst[i].as_string() + '\n')
        text_file.close()

    def store_dict_csv(self, file):
        """For storing a dictionary, frequency sorted."""
        w_lst = []
        for key in self._DCTN.keys():
            w_lst.append(TermEntry(key, self._DCTN[key]))
        w_lst.sort()
        with open(file, mode='w', newline='', encoding='utf-8') as csvf:
            csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)
            for i in range(len(w_lst)):
                csvwriter.writerow([w_lst[i].term, w_lst[i].val])

    def store_dict_alpha(self, file, min_fr=0):
        """For storing a dictionary, alphabetically sorted."""
        w_lst = []
        for key in self._DCTN.keys():
            # if re.match('.*[aeiou].*', key) and self._DCTN[key] >= min_fr:
            if self._DCTN[key] >= min_fr:
                w_lst.append(key)
        w_lst.sort()
        text_file = open(file, "w", encoding=encoding_for_dictionary_files)
        for key in w_lst:
            text_file.write(key + separator + str(self._DCTN[key]) + "\n")
        text_file.close()

    def store_dict_year(self, file):
        w_lst = []
        for key in self._DCTN.keys():
            w_lst.append(key)
        w_lst.sort()
        with open(file + '.csv', mode='w', newline='', encoding='utf-8') as csvf:
            csvwriter = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(w_lst)):
                csvwriter.writerow([w_lst[i][0:4], w_lst[i][5:], self._DCTN[w_lst[i]]])

    def store_dict_csv_quot(self, file):
        """For storing a dictionary, frequency sorted."""
        w_lst = []
        for key in self._DCTN.keys():
            w_lst.append(TermEntry(key, self._DCTN[key]))
        w_lst.sort()
        with open(file, mode='w', newline='', encoding='utf-8') as csvf:
            csvwriter = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(w_lst)):
                stat = 'quot'
                if w_lst[i].val < 5:
                    stat = 'na'
                csvwriter.writerow([w_lst[i].term, stat, w_lst[i].val])
