import numpy as np
import os
import japanize_matplotlib
import math
import matplotlib.pyplot as plt
from composeexample.settings import BASE_DIR

def make_hist(scores: list, max_score: float, positive: str):
    if positive == "positive":
        plotcol = 'darkorange'
        backcol = '#fff0df'
    else:
        plotcol = 'darkcyan'
        backcol = '#e5f0ff'

    fig = plt.figure(facecolor= backcol)
    plt.hist(scores, bins= 50, rwidth= 0.8, color= plotcol)
    ax = plt.gca()
    ax.set_facecolor(backcol)

    axcol = 'dimgray'
    ax.spines['top'].set_color(axcol)
    ax.spines['bottom'].set_color(axcol)
    ax.spines['left'].set_color(axcol)
    ax.spines['right'].set_color(axcol)

    ax.tick_params(axis = 'x', colors =axcol)
    ax.tick_params(axis = 'y', colors = axcol)

    ax.xaxis.label.set_color(axcol)
    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)

    return fig


def make_chart(scores: list, positive: str) -> str:
    scores = np.asarray(scores)
    pos_neg = [np.sum(scores > 0.1), np.sum(scores <= 0.1)]

    backcol = '#fff0df' if positive == "positive" else '#e5f0ff'
    fig = plt.figure(facecolor= backcol)
    pathes, labels, pcts = plt.pie(pos_neg, labels= ['ポジティブ', 'ネガティブ'], colors= ['darkorange', 'darkcyan'],
                                   autopct= "%.1f%%", labeldistance= 0.5, rotatelabels= False, pctdistance= 0.65,
                                   radius= 1.5, startangle= 90, shadow= True,
                                   wedgeprops={'linewidth': 2, 'edgecolor':"white"},
                                   textprops={'color': "white", 'weight': "bold"})

    for i, l, p in zip(range(len(labels)), labels, pcts):
        l.set_horizontalalignment('center')
        l.set_size(max(32 * pos_neg[i] / sum(pos_neg), 16))

        p.set_horizontalalignment('center')
        p.set_size(max(28 * pos_neg[i] / sum(pos_neg), 14))
        co = l.get_position()
        p.set_position([co[0], co[1]-0.2])


    if positive:
        pathes[0].set_alpha(0.8)
    else:
        pathes[1].set_alpha(0.8)

    fname = os.path.join(BASE_DIR, "static/img/piechart.png")
    plt.savefig(fname)
    plt.close()

    return fname


def make_maghist(magnitudes: list, positive: str) -> str:
    f = make_hist(magnitudes, max(magnitudes), positive)

    plt.xlim(0, math.ceil(max(magnitudes)))
    plt.xlabel('熱 意', fontsize= 15)

    fname = os.path.join(BASE_DIR, 'static/img/magnitude.png')
    plt.savefig(fname)
    plt.close()

    return fname


def make_scorehist(scores: list, positive: bool) -> str:
    f = make_hist(scores, 1.0, positive)

    plt.xlim(-1, 1)
    plt.xlabel('評 価', fontsize= 15)

    fname = os.path.join(BASE_DIR, 'static/img/score.png')
    plt.savefig(fname)
    plt.close()

    return fname
