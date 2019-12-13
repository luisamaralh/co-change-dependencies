import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
# import matplotlib.pyplot as plt
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


def load_data(project_name: str, kind=None, nrows=None) -> tuple:
    '''
    Receives a project name and a, optionally, the kind of data to fetch
    Kind can be:
        any combination of ['old', 'new', 'cochange', 'bic']
    Returns all data if no 'kind' is specified
    Otherwise returns a tuple with the specified data in order:
        old_commits, new_commits, cc_df, bic
    '''
    if (not kind or 'old' in kind):
        # temporarily loads data for all commits before running SZZ
        try:
            tmp =\
                pd.read_csv(
                    'assets/data/{0}/{0}_commits.csv'.format(project_name),
                    nrows=nrows,
                    header=None
                )
        except UnicodeDecodeError:
            tmp =\
                pd.read_csv(
                    'assets/data/{0}/{0}_commits.csv'.format(project_name),
                    nrows=nrows,
                    header=None,
                    encoding='utf-16'
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
        old_commits.name = project_name

        # removes temporary dataframe
        del tmp

    # --------------------------------------------------------------------
    if (not kind or 'new' in kind):
        # temporarily loads data for all commits after running SZZ
        try:
            tmp =\
                pd.read_csv(
                    'assets/data/{0}/new_{0}_commits.csv'.format(project_name),
                    nrows=nrows,
                    header=None
                )
        except UnicodeDecodeError:
            tmp =\
                pd.read_csv(
                    'assets/data/{0}/new_{0}_commits.csv'.format(project_name),
                    nrows=nrows,
                    header=None,
                    encoding='utf-16'
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
        new_commits.name = project_name

        # removes temporary dataframe
        del tmp

    # --------------------------------------------------------------------
    if (not kind or 'cochange' in kind):
        # loads data for cochange count of each commit
        cc_df =\
            pd.read_csv(
                'assets/data/{0}/{0}-cochange.mdg'.format(project_name),
                header=None,
                nrows=nrows,
                sep='\t'
            )[[2, 3, 6]]\
            .rename(
                columns={
                    2: 'support_count',
                    3: 'confidence',
                    6: 'commit_hash'
                }
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
    if (not kind or 'bic' in kind):
        # loads commits that introduce bugs
        bic =\
            pd.read_csv(
                'assets/data/szz_phase2.csv',
                header=0,
                usecols=['bic', 'name']
            )

        bic =\
            bic[bic.name == project_name]\
            .drop(columns=['name'])\
            .squeeze('columns')\
            .reset_index(drop=True)

        bic.name = project_name

    # --------------------------------------------------------------------
    if not kind:
        return old_commits, new_commits, cc_df, bic

    else:
        result = []

        try:
            result.append(old_commits)

        except NameError:
            pass

        try:
            result.append(new_commits)

        except NameError:
            pass

        try:
            result.append(cc_df)

        except NameError:
            pass

        try:
            result.append(bic)

        except NameError:
            pass

        return tuple(result)


def _get_multiIndex(
    incoming: (pd.Series or pd.DataFrame),
    project: str
) -> pd.MultiIndex:
    '''
    '''
    # if type(incoming) == pd.Series:
    #     incoming = pd.Series(incoming)

    # else:
    #     incoming = pd.DataFrame(incoming)

    return\
        pd.MultiIndex.from_tuples(
            [
                (project, x) for x in incoming.index
            ]
        )


def _melt_data(
    project_name: list,
    kind: str,
    nrows=None
) -> (pd.Series or pd.DataFrame):
    '''
    Recursively concatenates Pandas Series for all projects in 'project_name'
    Returns Multi-level indexed Pandas Series (project, created_at)
    '''
    try:
        [incoming] = load_data(
            ''.join(project_name[0]),
            kind=kind,
            nrows=nrows
        )

        incoming.index =\
            _get_multiIndex(
                incoming,
                project_name[0]
            )

        return\
            pd.concat(
                [
                    incoming,
                    _melt_data(
                        project_name[1:],
                        kind, nrows=nrows
                    )
                ],
                sort=False
            )

    except IndexError:
        if kind == 'cochange':
            return pd.DataFrame()

        else:
            return pd.Series()

    except UnicodeDecodeError as e:
        error_codec, error_f, error_msg, error_pos, _ = tuple(e.args)
        custom_msg =\
            'Error while loading file "{0}" for project "{1}"'\
            .format(kind, project_name[0])

        raise UnicodeDecodeError(
            error_codec, error_f, error_msg, error_pos, custom_msg
        )


def load_data_all(exception=[], nrows=None) -> [
    pd.Series,
    pd.Series,
    pd.DataFrame,
    pd.Series
]:
    '''
    '''
    all_proj =\
        [
            project for project
            in os.listdir('assets/data/')
            if (project not in exception) and ('szz' not in project)
        ]

    # try:
    return\
        _melt_data(all_proj, 'old', nrows=nrows),\
        _melt_data(all_proj, 'new', nrows=nrows),\
        _melt_data(all_proj, 'cochange', nrows=nrows),\
        _melt_data(all_proj, 'bic', nrows=nrows)

    # except UnicodeDecodeError:
    #     return []


# if __name__ == "__main__":
#     old, new, cochange, bic = load_data_all(nrows=100)
