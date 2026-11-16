
import pytest
from marathon_registration import entry_fee, start_wave, finisher_status


# ENTRY FEE BRANCH TESTS

def test_unknown_race():
    with pytest.raises(ValueError):
        entry_fee("100k", 25, False, False)


def test_age_below_12():
    with pytest.raises(ValueError):
        entry_fee("5k", 11, False, False)


def test_valid_age_above_12():
    assert entry_fee("5k", 12, False, False) == 500


def test_half_marathon_under_18():
    with pytest.raises(ValueError):
        entry_fee("half", 17, False, False)


def test_half_marathon_adult():
    assert entry_fee("half", 18, False, False) == 1200


def test_full_marathon_under_18():
    with pytest.raises(ValueError):
        entry_fee("full", 17, False, False)


def test_full_marathon_adult():
    assert entry_fee("full", 18, False, False) == 1800


def test_early_bird():
    assert entry_fee("5k", 25, True, False) == 375


def test_no_early_bird():
    assert entry_fee("5k", 25, False, False) == 500


def test_senior_discount():
    assert entry_fee("10k", 65, False, False) == 400


def test_non_senior():
    assert entry_fee("10k", 64, False, False) == 800


def test_tshirt_required():
    assert entry_fee("5k", 25, False, True) == 800


def test_no_tshirt():
    assert entry_fee("5k", 25, False, False) == 500


# START WAVE BRANCH TESTS

def test_none_time():
    assert start_wave(None, "full") == "D"


def test_full_wave_a():
    assert start_wave(180, "full") == "A"


def test_full_wave_b():
    assert start_wave(200, "full") == "B"


def test_full_wave_c():
    assert start_wave(241, "full") == "C"


def test_other_wave_a():
    assert start_wave(90, "10k") == "A"


def test_other_wave_b():
    assert start_wave(100, "10k") == "B"


def test_other_wave_c():
    assert start_wave(121, "10k") == "C"


# FINISHER STATUS BRANCH TESTS

def test_disqualified():
    assert finisher_status(100, "full", 1) == "DSQ"


def test_not_disqualified():
    assert finisher_status(300, "full", 0) == "finisher"


def test_full_finisher():
    assert finisher_status(360, "full", 0) == "finisher"


def test_full_dnf():
    assert finisher_status(361, "full", 0) == "DNF"


def test_half_finisher():
    assert finisher_status(180, "half", 0) == "finisher"


def test_half_dnf():
    assert finisher_status(181, "half", 0) == "DNF"


def test_other_race_finisher():
    assert finisher_status(90, "5k", 0) == "finisher"


def test_other_race_dnf():
    assert finisher_status(91, "5k", 0) == "DNF"
