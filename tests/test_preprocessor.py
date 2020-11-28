import numpy as np
import sinar_social_audit_2020.preprocessor as p


def test_income():
    assert p.income("2000") == 2000
    assert p.income("Rm2000") == 2000
    assert p.income("RM2500") == 2500
    assert p.income("3600 gross") == 3600
    assert p.income("bawah rm 1 ribu") == 999
    assert p.income("5k") == 5000
    assert p.income("Rm 1500") == 1500
    assert p.income("RM3000.00") == 3000.0
    assert p.income("RM 3000.00") == 3000.0
    assert p.income("Tiada") == 0
    assert p.income("2,500") == 2500
    assert p.income("RM 3,500") == 3500


def test_employment_status():
    assert p.employment_status("Surirumah") == "surirumah"
    assert p.employment_status("Suri rumah") == "surirumah"
    assert p.employment_status("surirumah") == "surirumah"
    assert p.employment_status("suri rumah") == "surirumah"
    assert p.employment_status("Suri Rumah") == "surirumah"
    assert p.employment_status("Freelance") == "Bekerja sendiri/ pemilik perniagaan"
    assert (
        p.employment_status("Tidak bkerja mjaga ank OKU")
        == "Menganggur / tidak bekerja ( tiada kerja / sedang mencari kerja)"
    )
    assert (
        p.employment_status("Pos Malaysia")
        == "Bekerja dengan bergaji (sepenuh masa/ separuh masa)"
    )


def test_essential_wishlist():
    assert p.essential_wishlist("Bantuan kewangan") == "monetary assistance"
    assert p.essential_wishlist("Broadband") == "internet service"
    assert p.essential_wishlist("Handphone") == "cellphone"
    assert p.essential_wishlist("Internet") == "internet service"
    assert (
        p.essential_wishlist("Internet, komputer,printer")
        == "internet service, computer, printer"
    )
    assert p.essential_wishlist("KEMUDAHAN INTERNET") == "internet service"
    assert p.essential_wishlist("Kemudahan cetak/printer") == "printer"
    assert p.essential_wishlist("Komputer") == "computer"
    assert (
        p.essential_wishlist("Komputer desktop, kemudah cetak/printer, WIFI")
        == "computer, printer, wifi"
    )
    assert p.essential_wishlist("Laptop") == "laptop"
    assert p.essential_wishlist("Laptop belajar utuk anak") == "laptop"
    assert (
        p.essential_wishlist("Laptop/komputer/printer") == "laptop, computer, printer"
    )
    assert p.essential_wishlist("Mesin cetak") == "printer"
    assert p.essential_wishlist("My tv") == "television"
    assert p.essential_wishlist("No") is None
    assert p.essential_wishlist("Pc") == "computer"
    assert p.essential_wishlist("Printer") == "printer"
    assert p.essential_wishlist("Smart tv") == "smart tv"
    assert p.essential_wishlist("Speaker") == "speaker"
    assert p.essential_wishlist("Sy xde laptop. Teringin nak 1") == "laptop"
    assert p.essential_wishlist("TIADA") is None
    assert p.essential_wishlist("Telefon pintar untuk anak2") == "smartphone"
    assert p.essential_wishlist("Tiada") is None
    assert p.essential_wishlist("Unlimited internet") == "internet (unlimited) service"
    assert p.essential_wishlist("Wifi") == "wifi"
    assert p.essential_wishlist("X") is None
    assert p.essential_wishlist("internet wifi") == "wifi"
    assert p.essential_wishlist("laptop") == "laptop"
    assert (
        p.essential_wishlist(
            "line telefon.tempat tinggal sekarang agak sukar mendapatkan line telefon"
        )
        == "telephony service"
    )
    assert p.essential_wishlist("") is None
    assert (
        p.essential_wishlist("printer . komputer . kemudahan internet sangat terhad")
        == "printer, computer, internet service"
    )
    assert (
        p.essential_wishlist("printer, komputer/pc, kemudahan intenet percuma")
        == "printer, computer, internet (free) service"
    )
    assert p.essential_wishlist("tiada") is None
    assert (
        p.essential_wishlist("wifi percuma area kediaman") == "internet (free) service"
    )


def test_value_integer():
    assert p.value_integer("42") == 42
    assert p.value_integer("03") == 3
    assert np.isnan(p.value_integer(""))


def test_value_integer_age():
    assert p.value_integer("41") == 41
    assert p.value_integer("45TH") == 45
    assert p.value_integer("43 tahun") == 43
    assert p.value_integer("38 TAHUN") == 38
    assert p.value_integer("17 Tahun") == 17
    assert p.value_integer("30an") == 30


def test_value_integer_family_size():
    assert p.value_integer("7 orang") == 7
    assert p.value_integer("5orang") == 5
    assert p.value_integer("5 Org") == 5
    assert p.value_integer("7org") == 7
    assert p.value_integer("6 org") == 6
    assert p.value_integer("7 Orang") == 7
