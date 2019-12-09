import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype


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
    # fig = plt.figure()
    # res = stats.probplot(df[col], plot=plt)
    # plt.show()
    # fig.show()


def show_barplot(in_df, col, y_logscale=False):
    '''
    '''
    df = in_df.copy()

    sns.set(
        style='whitegrid',
        palette="deep",
        font_scale=1.1
    )

    sns.catplot(
        x=col,
        # y=df.groupby(col).count().iloc[:, 0],
        data=df,
        kind="count",
        **{'log': y_logscale}
    )


def load_data(project_name: str):
    '''
    '''
    # temporarily loads data for all commits before running SZZ
    tmp =\
        pd.read_csv(
            '../assets/data/{0}/{0}_commits.csv'.format(project_name),
            # nrows=100,
            header=None
        )

    # transforms date column into datetime_index
    old_commits =\
        pd.Series(
            tmp[0].values,
            index=pd.DatetimeIndex(
                pd.to_datetime(
                    tmp[1].values,
                    infer_datetime_format=True,
                    utc=True
                )
            )
        )

    # removes temporary dataframe
    del tmp

    # --------------------------------------------------------------------
    # temporarily loads data for all commits after running SZZ
    tmp =\
        pd.read_csv(
            '../assets/data/{0}/new_{0}_commits.csv'.format(project_name),
            # nrows=100,
            header=None
        )

    # transforms date column into datetime_index
    new_commits =\
        pd.Series(
            tmp[0].values,
            index=pd.DatetimeIndex(
                pd.to_datetime(
                    tmp[1].values,
                    infer_datetime_format=True,
                    utc=True
                )
            )
        )

    # removes temporary dataframe
    del tmp

    # --------------------------------------------------------------------
    # loads data for cochange count of each commit
    cc_df =\
        pd.read_csv(
            '../assets/data/{0}/{0}-cochange.tsv'.format(project_name),
            header=None,
            # nrows=100,
            sep='\t'
        )[[2, 3, 6]]\
        .rename(
            columns={2: 'support_count', 3: 'confidence', 6: 'commit_hash'}
        )

    # transforms commit_hash into lists of hashes
    cc_df.commit_hash = cc_df.commit_hash.apply(lambda x: x.split(','))

    # transforms support_count into an ordinal categorical variable
    cc_df.support_count =\
        cc_df.support_count.astype(
            CategoricalDtype(categories=np.unique(
                cc_df.support_count.values),
                ordered=True
            )
        )

    # --------------------------------------------------------------------
    # loads commits that introduce bugs
    bic =\
        pd.read_csv(
            '../assets/data/szz_phaseII.csv',
            header=0,
            usecols=['bic', 'name']
        )

    bic =\
        bic[bic.name == project_name]\
        .drop(columns=['name']).squeeze('columns')\
        .reset_index(drop=True)

    # --------------------------------------------------------------------
    return old_commits, new_commits, cc_df, bic
