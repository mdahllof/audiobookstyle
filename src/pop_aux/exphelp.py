import os
import csv


def make_dir(newdir):
    if not os.path.exists(newdir):
        os.makedirs(newdir)
        print('Made directory:', newdir)
    else:
        print('Will use existing directory:', newdir)


def store_on_csv(filen, rows):
    with open(filen, mode='w', newline='', encoding='utf-8') as csvf:
        csvwriter = csv.writer(csvf, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        for csvrow in rows:
            csvwriter.writerow(csvrow)
