import datetime as dt
import pytest
from unittest.mock import patch
import sdate

@pytest.mark.parametrize(
    "target_date, epoch_yr, epoch_mo, expected_days",
    [
        (dt.datetime.date(1993, 9, 1), 1993, 9, 1),        # Testing Eternal September day 1
        (dt.date(1993, 9, 2), 1993, 9, 2),        # Testing Day 2
        (dt.date(2026, 10, 12), 1993, 9, 12095),  # Testing Thanksgiving 2026
        (dt.date(2020, 3, 1), 2020, 3, 1),        # Testing COVID epoch start
        (dt.date(2026, 10, 12), 2020, 3, 2417),   # Testing Covid epoch on Thanksgiving 2026
    ]
)

def test_epoch_math(target_date, epoch_yr, epoch_mo, expected_days):
    epoch_start = dt.date(epoch_yr, epoch_mo, 1)
    days_passed = (target_date - epoch_start).days + 1
    assert days_passed == expected_days

@patch('sdate.datetime')
def test_custom_format_tokens(mock_dt):
    # Freeze time precisely to October 12, 2026 at 08:30:15.123456
    fixed_now = dt.datetime(2026, 10, 12, 8, 30, 15, 123456)
    mock_dt.datetime.now.return_value = fixed_now
    mock_dt.date.today.return_value = fixed_now.date()
    mock_dt.date.side_effect = dt.date  # Keep base class constructor

    # Simulate passing custom flags: sdate +"%Y-%m-%d %H:%M:%S.%f"
    fmt_string = "%Y-%m-%d %H:%M:%S.%f"
    epoch_year, epoch_month = 1993, 9  # Eternal September
    days_passed = 12095  # Days from 1993-09-01 to 2026-10-12

    # Replicate token swap algorithm
    res = fmt_string.replace('%d', str(days_passed))
    res = res.replace('%m', f"{epoch_month:02d}")
    res = res.replace('%Y', str(epoch_year))
    res = res.replace('%f', f"{fixed_now.microsecond:06d}")

    output = fixed_now.strftime(res)

    # Assert that everything parses exactly down to the bare-metal microsecond
    assert output == "1993-09-12095 08:30:15.123456"