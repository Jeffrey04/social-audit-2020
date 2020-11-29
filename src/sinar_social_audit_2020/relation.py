import numpy as np
import pandas as pd
from IPython.display import HTML, display
from scipy.stats import chi2, chi2_contingency, t


def distinct_vs_distinct(a, b, a_ranked):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for a_value in a_ranked:
        row = []
        for b_value in b.unique():
            _dfavalue = _df[_df[a.name] == a_value]
            row.append(_dfavalue[_dfavalue[b.name] == b_value].shape[0])

        data.append(row)

    result = pd.DataFrame(
        data,
        index=a_ranked,
        columns=pd.Series(b.unique(), name=b.name),
    )
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def distinct_vs_interval(a, b, a_ranked, b_interval_list):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for value in a_ranked:
        row = []
        for b_interval in b_interval_list:
            _dfavalue = _df[_df[a.name] == value]
            _dfbmax = _dfavalue[_dfavalue[b.name] <= b_interval.right]
            row.append(_dfbmax[b_interval.left < _dfbmax[b.name]].shape[0])

        data.append(row)

    result = pd.DataFrame(data, index=a_ranked, columns=b_interval_list)
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def distinct_vs_mcq(a, b, a_ranked):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for value in a_ranked:
        row = []
        for column in b.columns:
            _dfvalue = _df[_df[a.name] == value]
            row.append(_dfvalue[_dfvalue[column] == True].shape[0])

        data.append(row)

    result = pd.DataFrame(
        data,
        index=a_ranked,
        columns=pd.Series(b.columns),
    )
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def result_filter_zeros(result):
    return result.loc[:, (result != 0).any(axis=0)][(result.T != 0).any()]


def interval_vs_distinct(a, b, a_interval_list):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for interval in a_interval_list:
        row = []
        for value in b.unique():
            _dfmax = _df[_df[a.name] <= interval.right]
            _dfmin = _dfmax[interval.left < _dfmax[a.name]]
            row.append(_dfmin[_dfmin[b.name] == value].shape[0])

        data.append(row)

    result = pd.DataFrame(data, index=a_interval_list, columns=b.unique())
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def interval_vs_interval(a, b, a_interval_list, b_interval_list):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for a_interval in a_interval_list:
        row = []
        for b_interval in b_interval_list:
            _dfamax = _df[_df[a.name] <= a_interval.right]
            _dfamin = _dfamax[a_interval.left < _dfamax[a.name]]
            _dfbmax = _dfamin[_dfamin[b.name] <= b_interval.right]
            row.append(_dfbmax[b_interval.left < _dfbmax[b.name]].shape[0])

        data.append(row)

    result = pd.DataFrame(data, index=a_interval_list, columns=b_interval_list)
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def interval_vs_mcq(a, b, a_interval_list):
    _df = pd.merge(
        a,
        b,
        left_index=True,
        right_index=True,
    )

    data = []

    for interval in a_interval_list:
        row = []
        for column in b.columns:
            _dfmax = _df[_df[a.name] <= interval.right]
            _dfmin = _dfmax[interval.left < _dfmax[a.name]]
            row.append(_dfmin[_dfmin[column] == True].shape[0])

        data.append(row)

    result = pd.DataFrame(data, index=a_interval_list, columns=b.columns)
    display(HTML(result.to_html()))
    result.plot(kind="line")

    return result_filter_zeros(result)


def independence_check(data, alpha=0.05):
    test_stats, _, dof, _ = chi2_contingency(data)

    critical = chi2.ppf(1 - alpha, dof)

    independence = not independence_reject_hypothesis(test_stats, critical)

    if independence:
        print(
            f"Failed to reject H_0 at alpha={alpha} since test statistic chi2={abs(test_stats)} < {critical}"
        )
    else:
        print(
            f"H_0 is rejected at alpha={alpha} since test statistic chi2={abs(test_stats)} >= {critical}"
        )

    return independence


def independence_reject_hypothesis(test_stats, critical):
    return abs(test_stats) >= critical


def correlation_check(data, alpha=0.05, method="pearson"):
    _corr = (
        data.corrwith(
            pd.Series(
                range(len(data.index)) if method == "spearman" else data.index,
                index=data.index,
            ),
            method=method,
        )
        .rename("Correlation")
        .dropna()
    )
    display(HTML(_corr.to_frame().to_html()))

    critical = t.ppf(1 - alpha / 2, (len(_corr) - 2))

    for idx, rs in _corr.items():
        test_stats = rs * np.sqrt((len(_corr) - 2) / ((rs + 1.0) * (1.0 - rs)))

        print(
            f"The {(rs < 0) and 'negative ' or ''}correlation is {correlation_get_name(rs)} at rs={rs}."
        )

        if not correlation_reject_hypothesis(test_stats, critical):
            print(
                f"Failed to reject H_0 at alpha={alpha} since test statistic T={test_stats} and critical region=±{critical}. "
            )
            print(
                f"Hence, for {data.columns.name} at {idx}, the correlation IS NOT significant."
            )
        else:
            print(
                f"H_0 is rejected at alpha={alpha} since test statistic T={test_stats}, and critical region=±{critical}. "
            )
            print(
                f"Hence, for {data.columns.name} at {idx}, the correlation IS significant."
            )

        print()


def correlation_get_name(rs):
    result = None

    if abs(rs) == 1:
        result = "perfect"
    elif 0.8 <= abs(rs) < 1:
        result = "very high"
    elif 0.6 <= abs(rs) < 0.8:
        result = "high"
    elif 0.4 <= abs(rs) < 0.6:
        result = "some"
    elif 0.2 <= abs(rs) < 0.4:
        result = "low"
    elif 0.0 < abs(rs) < 0.2:
        result = "very low"
    elif abs(rs) == 0:
        result = "absent"
    else:
        raise Exception(f"Invalid rank at {rs}")

    return result


def correlation_reject_hypothesis(test_stats, critical):
    return abs(test_stats) > critical
