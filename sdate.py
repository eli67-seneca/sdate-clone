#!/usr/bin/env python3
# Author: eli67 (Enoch Li)
# Description: A Python clone of `sdate`, the Eternal September date counter.
# Disclaimer: By running this utility, you choose to accept that Python runs quite
# a lot slower than C. So don't go complaining to me about performance issues if
# you choose to use this thing to timestamp all your backups.

import sys
import datetime
import time
import argparse
import subprocess

def main() -> None:
	args, positional = parse_args()

	if args.help:
		print("Usage: sdate [-e YYYY-MM] | --covid] [FORMAT | COMMAND]")
		print("  -e, --epoch	  Set custom epoch month (default: 1993-03)")
		print("  --covid		  Shortcut for Neverending March 2020 epoch")
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
	is_command = False

	if positional:
		# If user passes an arbitrary command wrapper like `sdate date` or `sdate bash`
		if not positional[0].startswith('+') and positional[0] not in ['date', 'bash']:
			fmt_string = " ".join(positional)
		elif positional[0].startswith('+'):
			# Strip leading '+'
			fmt_string = positional[0][1:]
		else:
			is_command = True

	# Time calculations
	epoch_start = datetime.date(epoch_year, epoch_month, 1)
	today = datetime.date.today()
	days_passed = (today - epoch_start).days + 1 - args.offset

	now = datetime.datetime.now()
	weekday = now.strftime("%a")
	time_str = now.strftime("%H:%M:%S")

	# Extract timezone name
	try:
		tz_str = time.tzname[time.daylight]
	except IndexError:
		# Fall back to the default name of current timezone (presumably; I didn't check)
		tz_str = time.tzname[0]

	# Create safe fallback date object to extract calendar string in case this thing
	# is run at the end of a month whose number of days isn't exactly 30.
	month_date = datetime.date(epoch_year, epoch_month, 1)

	# Handle custom format tokens
	if fmt_string:
		# Swap out custom date tokens so Python's strftime doesn't blow past them
		res = fmt_string.replace('%d', str(days_passed))
		res = res.replace('%m', f"{epoch_month:02d}")
		res = res.replace('%B', month_date.strftime('%B'))
		res = res.replace('%b', month_date.strftime('%b'))
		res = res.replace('%Y', str(epoch_year))
		res = res.replace('%y', str(epoch_year)[-2:])
		# Explicit support for high-resolution system clock microseconds because...why not?
		res = res.replace('%f', f"{now.microsecond:06d}")

		# Render remaining tokens like standard (like %H, %M, %S, etc)
		output_str = now.strftime(res)
	else:
		# Fallback to classic default terminal string output
		month_name = month_date.strftime('%b')
		output_str = f"{weekday} {month_name} {days_passed:,} {time_str} {tz_str} {epoch_year}"

	# Parse command if there is one
	if is_command:
		print(output_str)
		try:
			sys.exit(subprocess.run(positional).returncode)
		except FileNotFoundError:
			print(f"sdate: {positional}: command not found.", file=sys.stderr)
			sys.exit(127)
		except KeyboardInterrupt:
			sys.exit(130)
	else:
		# This is the thing that actually prints the output
		print(output_str)

def parse_args() -> tuple[argparse.Namespace, list[str]]:
	# Setup parser to mimick the original sdate
	parser = argparse.ArgumentParser(
		description="sdate: Neverending September date tool clone",
		add_help=False
	)
	parser.add_argument("-h", "--help", action="store_true")
	parser.add_argument("-e", "--epoch", type=str, help="Epoch month (YYYY-MM)")
	parser.add_argument("-c", "--covid", action="store_true", help="Use Neverending COVID-19 March 2020 epoch")

	# Undocumented offset argument for when you want to use your birthdate as an epoch
	parser.add_argument("-o", "--offset", type=int, default=0, help=argparse.SUPPRESS)

	# Capture all unknown args (formatting tags or nested commands)
	args, unknown = parser.parse_known_args()
	return args, unknown

if __name__ == "__main__":
	main()