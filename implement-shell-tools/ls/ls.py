#!/usr/bin/env python3

import argparse
import locale
import os
import sys


def main():
    parser = argparse.ArgumentParser(add_help=False, usage="ls.py [-1] [-a] [path]")
    parser.add_argument("-1", dest="one_per_line", action="store_true")
    parser.add_argument("-a", dest="show_all", action="store_true")
    parser.add_argument("path", nargs="?", default=".")

    args = parser.parse_args()

    try:
        entries = os.listdir(args.path)
    except FileNotFoundError:
        print(f"ls: cannot access '{args.path}': No such file or directory", file=sys.stderr)
        sys.exit(1)
    except NotADirectoryError:
        print(os.path.basename(args.path))
        return

    if args.show_all:
        entries = entries + [".", ".."]
    else:
        entries = [name for name in entries if not name.startswith(".")]

    locale.setlocale(locale.LC_COLLATE, "")
    for entry in sorted(entries, key=locale.strxfrm):
        print(entry)


if __name__ == "__main__":
    main()
