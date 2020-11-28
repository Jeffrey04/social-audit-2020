import pandas as pd
from IPython.display import HTML, display

from sinar_social_audit_2020 import preprocessor


def mcq(df, field, title, options, processor=None):
    normalized = (
        df[field].copy().apply(processor if processor else lambda x: x).to_frame(field)
    )

    counts = [0 for _ in options]

    for idx, option in enumerate(options):
        normalized[option] = normalized[field].str.contains(option, regex=False)

        counts[idx] = normalized[normalized[option] == True][option].count()

    summary = pd.DataFrame(
        data=counts, index=options, columns=("Frequency",)
    ).rename_axis(title)

    display(HTML(summary.to_html()))

    summary.plot(kind="bar")

    return normalized[[*options]], summary


def number(df, field, title, bins, processor=None):
    normalized = pd.Series(
        df[field].copy().apply(processor if processor else preprocessor.value_integer)
    )

    summary = (
        normalized.value_counts(bins=bins)
        .to_frame("Frequency")
        .rename_axis(title)
        .sort_index()
    )

    display(HTML(summary.to_html()))

    normalized.hist(bins=bins)

    return normalized, summary


def distinct(df, field, title, processor=None):
    normalized = df[field].copy().apply(processor if processor else lambda x: x)
    normalized[normalized == ""] = "not captured"

    summary = (
        normalized.value_counts().to_frame("Frequency").rename_axis(title).sort_index()
    )
    display(HTML(summary.to_html()))
    summary.plot(kind="bar")

    return normalized, summary


def ranking(df, field_names, options):
    values = {
        field: [df[df[field] == option][field].shape[0] for option in options]
        for field in field_names
    }

    summary = pd.DataFrame(values, index=options)

    display(HTML(summary.to_html()))

    return df[[*field_names]], summary
