import unicodedata

import numpy as np

from sinar_social_audit_2020.fields import FIELD_MAP


def cleanup(func):
    def inner(value, *args):
        return func(unicodedata.normalize("NFKD", value).strip(), *args)

    return inner


@cleanup
def field_name(field):
    return FIELD_MAP.get(field, field)


@cleanup
def employment_status(value):
    return (
        value.replace("Surirumah", "surirumah")
        .replace("Suri rumah", "surirumah")
        .replace("suri rumah", "surirumah")
        .replace("Suri Rumah", "surirumah")
        .replace("Freelance", "Bekerja sendiri/ pemilik perniagaan")
        .replace(
            "Tidak bkerja mjaga ank OKU",
            "Menganggur / tidak bekerja ( tiada kerja / sedang mencari kerja)",
        )
        .replace("Pos Malaysia", "Bekerja dengan bergaji (sepenuh masa/ separuh masa)")
    )


@cleanup
def essential_wishlist(value):
    normalized = (
        value.lower()
        .replace(
            "line telefon.tempat tinggal sekarang agak sukar mendapatkan line telefon",
            "telephony service",
        )
        .replace("sy xde laptop. teringin nak 1", "laptop")
        .replace(".", ",")
        .replace(" ,", ",")
        .replace("internet wifi", "wifi")
        .replace("kemudahan intenet percuma", "free internet")
        .replace("wifi percuma area kediaman", "free internet")
        .replace("kemudahan cetak/printer", "printer")
        .replace("kemudah cetak/printer", "printer")
        .replace("komputer/pc", "computer")
        .replace("/", ",")
        .replace("mesin cetak", "printer")
        .replace("my tv", "television")
        .replace("bantuan kewangan", "monetary assistance")
        .replace("kemudahan internet sangat terhad", "internet")
        .replace("kemudahan internet", "internet")
        .replace("internet", "internet service")
        .replace("broadband", "internet service")
        .replace("free internet service", "internet (free) service")
        .replace("unlimited internet service", "internet (unlimited) service")
        .replace("handphone", "cellphone")
        .replace("komputer desktop", "computer")
        .replace("komputer", "computer")
        .replace("pc", "computer")
        .replace("laptop belajar utuk anak", "laptop")
        .replace("telefon pintar untuk anak2", "smartphone")
        .replace("x", "")
        .replace("tiada", "")
        .replace("no", "")
        .replace(", ", ",")
        .replace(",", ", ")
    )

    return normalized or None


@cleanup
def income(value):
    normalized = (
        value.lower()
        .replace(",", "")
        .replace("rm", "")
        .replace("k", "000")
        .replace(" ", "")
        .replace("gross", "")
        .replace("bawah1000", "999")
        .replace("bawah1ribu", "999")
        .replace("tiada", "0")
        .strip()
    )

    return float(normalized) if normalized == 0 or normalized else np.nan


@cleanup
def value_integer(value):
    normalized = "".join(c for c in value if not c.isalpha()).strip().lstrip("0")
    return int(normalized) if normalized else np.nan
