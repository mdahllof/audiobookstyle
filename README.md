# Audiobook stylistics: Book format comparisons between print and audio in the bestselling segment

**Supplementary material for an article by Karl Berglund and Mats Dahllöf (Uppsala University)**

Exploing differences in stylistic properties (mainly among bestsellers and beststreamers).

Python code is located in `./src/` 

Use `main.py` to generate the analysis.
    
Metadata is located in ./meta/

Data generated from the corpus is located in `./results/dicts/`. The corpus itself is
protected by copyright, and cannot be shared. It is in conll format. The code for
processing it is however supplied.

Results (text comparisons) generated from the data in `./results/dicts/` are stored in
`./results/comps/`. The files there can be regenerated from the data in `./results/dicts/`
using `main.py`.

`./results/comps/lists/` contains for each measure, a list (csv) of the works ranked by that measure.

`./results/comps/plots/` contains a number of plots, of which a few appear as figures in the article.

`./results/comps/all_comparisons.csv` contains outranking ratios for all measures and
comparisons. Outranking ratios in permille.

`./results/comps/appendix1.tex` is LaTeX for Appendix 1 generated by `main.py`. It creates 
one table for each comparison showing the measures giving outranking ratios > 65.0%. 
A few of these tables appear in the article.

`./results/comps/appendix1.pdf` is the pdf generated using MikTeX/XeLaTex 
from `./results/comps/appendix1.tex`.



