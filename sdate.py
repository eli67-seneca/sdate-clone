#!/usr/bin/env python3

import sys
import datetime
import time
import argparse

def main():
    args, positional = parse_args()

    if args.help:
        print("Usage: sdate [-e YYYY-MM] | --covid] [FORMAT | COMMAND]")
        print("  -e, --epoch      Set custom epoch month (default: 1993-03)")
        print("  --covid          Shortcut for Neverending March 2020 epoch")
        sys.exit(0)

    # Establish target epoch date
    if args.covid:
        epoch_year, epoch_month = 2020, 3
    elif args.epoch:
        try:
            epoch_year, epoch_month = map(int, args.epoch.split('-'))
        except ValueError:
            print("Error: Epoch format must be YYYY-MM", file=sys.stderr)
            sys.exit(1)
    else:
        epoch_year, epoch_month = 1993, 9   # That's Eternal September!

    # Process positional elements
    fmt_string = None
    if positional:
        # If user passes an arbitrary command wrapper like `sdate date` or `sdate bash`
        if not positional[0].startswith('+') and positional[0] not in ['date', 'bash']:
            fmt_string = " ".join(positional)
        elif positional[0].startswith('+'):
            # Strip leading '+'
            fmt_string = positional[0][1:]

    # Time calculations
    epoch_start = datetime.date(epoch_year, epoch_month, 1)
    today = datetime.date.today()
    days_passed = (today - epoch_start).days + 1

    now = datetime.datetime.now()
    weekday = now.strftime("%a")
    time_str = now.strftime("%H:%M:%S")
    tz_str = time.tzname[time.daylight]

    # Handle custom format tokens
    if fmt_string:
        # Swap out custom date tokens so Python's strftime doesn't blow past them
        res = fmt_string.replace('%d', str(days_passed))
        res = res.replace('%m', f"{epoch_month:02d}")
        res = res.replace('%B', now.replace(month=epoch_month).strftime('%B'))
        res = res.replace('%b', now.replace(month=epoch_month).strftime('%b'))
        res = res.replace('%Y', str(epoch_year))
        res = res.replace('%y', str(epoch_year)[-2:])

        # Render remaining tokens like standard (like %H, %M, %S, etc)
        # This is the thing that actually prints out the time
        print(now.strftime(res))
    else:
        # Fallback to classic default terminal string output
        month_name = now.replace(month=epoch_month).strftime('%b')
        print(f"{weekday} {month_name} {days_passed:,} {time_str} {tz_str} {epoch_year}")

def parse_args():
    # Setup parser to mimick the original sdate
    parser = argparse.ArgumentParser(
        description="sdate: Neverending September date tool clone",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-e", "--epoch", type=str, help="Epoch month (YYYY-MM)")
    parser.add_argument("-c", "--covid", action="store_true", help="Use Neverending COVID-19 March 2020 epoch")

    # Capture all unknown args (formatting tags or nested commands)
    args, unknown = parser.parse_known_args()
    return args, unknown

if __name__ == "__main__":
    main()