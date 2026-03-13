"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--mode", "-m", help="Validate or complete postcodes.", required=True
    )
    arg_parser.add_argument("postcode", help="The postcode to apply the operation to.")
    args = arg_parser.parse_args()
    postcode = args.postcode.upper().strip()
    validate = True if args.mode == "validate" else False
    if validate:
        if validate_postcode(postcode):
            print(f"{postcode} is a valid postcode.")
        else:
            print(f"{postcode} is not a valid postcode.")
    else:
        possible_postcodes = get_postcode_completions(postcode)
        if not possible_postcodes:
            print(f"No matches for {postcode}.")
        i = 0
        while i < min(len(possible_postcodes), 5):
            print(possible_postcodes[i].upper().strip())
            i += 1
