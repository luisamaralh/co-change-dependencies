import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt


def show_dist_categorical(in_df, col):
    '''
    '''
    df = in_df.copy()

    print(
        'Skewness: {0:.2f}\t\tKurtosis: {1:.2f}'
        .format(stats.skew(df[col]), stats.kurtosis(df[col]))
    )

    sns.set(
        style='whitegrid',
        palette="deep",
        font_scale=1.1,
        rc={"figure.figsize": [5, 3]}
    )

    sns.distplot(
        df[col].values,
        norm_hist=False,
        kde=False,
        bins=len(np.unique(df[col].values)),
        hist_kws={"alpha": 1}
    ).set(xlabel='Components Under Co-Change', ylabel='Count')

    # Get also the QQ-plot
    fig = plt.figure()
    res = stats.probplot(df[col], plot=plt)
    plt.show()
    # fig.show()


def show_barplot(in_df, col):
    '''
    '''
    df = in_df.copy()

    sns.set(
        style='whitegrid',
        palette="deep",
        font_scale=1.1,
        rc={"figure.figsize": [5, 3]}
    )

    sns.catplot(
        x=col,
        # y=df.groupby(col).count().iloc[:, 0],
        data=df,
        kind="count",
    )
