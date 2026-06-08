#!/usr/bin/env python3

import argparse
import locale
import os
import sys


class LsArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"ls: {message}", file=sys.stderr)
        print("Usage: ls.py -1 [-a] [path]", file=sys.stderr)
        sys.exit(1)


def expand_combined_flags(args, valid_flags):
    expanded = []
    for arg in args:
        if arg == "-":
            expanded.append(arg)
            continue

        if arg.startswith("-") and not arg.startswith("--") and len(arg) > 2:
            flags = arg[1:]
            for flag in flags:
                if flag not in valid_flags:
                    print(f"ls: invalid option -- '{flag}'", file=sys.stderr)
                    sys.exit(1)
                expanded.append(f"-{flag}")
            continue

        expanded.append(arg)

    return expanded


def parse_args(args):
    parser = LsArgumentParser(add_help=False)
    parser.add_argument("-1", dest="one_per_line", action="store_true")
    parser.add_argument("-a", dest="show_all", action="store_true")
    parser.add_argument("path", nargs="?", default=".")

    expanded_args = expand_combined_flags(args, {"1", "a"})
    parsed = parser.parse_args(expanded_args)

    if not parsed.one_per_line:
        print("Usage: ls.py -1 [-a] [path]", file=sys.stderr)
        sys.exit(1)

    return parsed.show_all, parsed.path


def list_entries(path, show_all):
    try:
        entries = os.listdir(path)
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
        sys.exit(1)
    except NotADirectoryError:
        print(os.path.basename(path))
        return

    if show_all:
        entries = entries + [".", ".."]
    else:
        entries = [name for name in entries if not name.startswith(".")]

    locale.setlocale(locale.LC_COLLATE, "")
    entries = sorted(entries, key=locale.strxfrm)

    for entry in entries:
        print(entry)


def main():
    show_all, path = parse_args(sys.argv[1:])
    list_entries(path, show_all)


if __name__ == "__main__":
    main()
