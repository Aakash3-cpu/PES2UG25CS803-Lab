
import pytest
from marathon_registration import entry_fee, start_wave, finisher_status


# ENTRY FEE TESTS

def test_unknown_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("100k", 25, False, False)


def test_age_below_12():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_half_marathon_under_18():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)


def test_full_marathon_under_18():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 16, False, False)


def test_standard_fee():
    assert entry_fee("10k", 30, False, False) == 800


def test_early_bird_discount():
    assert entry_fee("5k", 25, True, False) == 375


def test_senior_discount():
    assert entry_fee("10k", 65, False, False) == 400


def test_tshirt_charge():
    assert entry_fee("5k", 25, False, True) == 800


def test_all_fee_discounts():
    assert entry_fee("5k", 65, True, True) == 487


# START WAVE TESTS

def test_first_timer_wave():
    assert start_wave(None, "full") == "D"


def test_full_race_wave_a():
    assert start_wave(180, "full") == "A"


def test_full_race_wave_b():
    assert start_wave(200, "full") == "B"


def test_full_race_wave_c():
    assert start_wave(241, "full") == "C"


def test_other_race_wave_a():
    assert start_wave(90, "10k") == "A"


def test_other_race_wave_b():
    assert start_wave(100, "10k") == "B"


def test_other_race_wave_c():
    assert start_wave(121, "10k") == "C"


# FINISHER STATUS TESTS

def test_disqualified_runner():
    assert finisher_status(100, "full", 1) == "DSQ"


def test_full_marathon_finisher():
    assert finisher_status(360, "full", 0) == "finisher"


def test_full_marathon_dnf():
    assert finisher_status(361, "full", 0) == "DNF"


def test_half_marathon_finisher():
    assert finisher_status(180, "half", 0) == "finisher"


def test_half_marathon_dnf():
    assert finisher_status(181, "half", 0) == "DNF"


def test_other_race_finisher():
    assert finisher_status(90, "5k", 0) == "finisher"


def test_other_race_dnf():
    assert finisher_status(91, "5k", 0) == "DNF"
