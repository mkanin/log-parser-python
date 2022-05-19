"""The main module of application."""

import argparse

from services import calc_events_per_second
from services import calc_less_frequent_ip
from services import calc_most_frequent_ip
from services import calc_size_total_amount
from services import read_and_save_to_db
from services import read_from_directory
from services import write_json


def register_arguments():
    """Parses the input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input-files-list", nargs="+", default=[])
    parser.add_argument("-d", "--input-directory")
    parser.add_argument("-o", "--output-file", default="output.json")
    parser.add_argument("-op", "--operation", default="most-frequent-ip")
    args = vars(parser.parse_args())
    return args


def main():
    """The main method of the application."""
    args = register_arguments()
    if args.get("input_files_list"):
        read_and_save_to_db(args.get("input_files_list"))
    elif args.get("input_directory"):
        read_from_directory(args.get("input_directory"))

    res = ""
    if args.get("operation") == "most-frequent-ip":
        res = calc_most_frequent_ip()
    elif args.get("operation") == "less-frequent-ip":
        res = calc_less_frequent_ip()
    elif args.get("operation") == "calc-events":
        res = calc_events_per_second()
    elif args.get("operation") == "total-amount-ex":
        res = calc_size_total_amount()

    output_filename = args.get("output_file")
    write_json(output_filename, res)


if __name__ == "__main__":
    main()
