# sdate clone
A Python clone of the Eternal September `sdate` for all those recent Linux distros whose Rust-based `core-utils` can't run `sdate` natively.

## Installation

1. Save the scrit to your user directory (e.g. `~/sdate.py`)
2. Make it executable
```bash
chmod +x ~/sdate.py
```
3. (Optional) Alias it in your shell config file (`~/.bashrc`):
```bash
alias sdate="~/sdate.py"
```
4. Reload your environment
```bash
source ~/.bashrc
```
5. ???
6. It should work exactly like `sdate`, so much so you can leave the original installed in case you don't want to lose the `man` pages.