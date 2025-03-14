import re
import os
from typing import Dict
from response_utils import load_json, base_dir
from formatted_responses import formatted_word_lookup

messages = {"not in edinburgh": "Sorry, Tad does not have pronunciation data for that word :(",
            "not in tad": "Sorry, Tad does not cover that word :(",
            "help": "You can do :> for lookup, and :>> for annotated lookup!"}


def first_three_letters(input: str) -> str:
    "Returns the first 3 letters of input for lookup."
    return input[:3].lower().replace("/", "_")


def get_outline_lookup_data(outline: str) -> Dict[str, dict]:
    "Get entry lookup data from a given outline."
    prefix = first_three_letters(outline)
    file_path = os.path.join(base_dir, "preprocessed_dictionaries", f"entries_starting_{prefix}.json")
    lookup_data = load_json(file_path)
    if outline in lookup_data:
        return lookup_data[outline]


def get_word_lookup_data(word: str) -> Dict[str, dict]:
    "Get outline lookup data for word, or None if word is not present."
    prefix = first_three_letters(word)
    file_path = os.path.join(base_dir, "preprocessed_dictionaries", f"outlines_starting_{prefix}.json")
    lookup_data = load_json(file_path)
    if word in lookup_data:
        return lookup_data[word]


message_prefix_annotation_levels = {":>>>": "summarise all",
                                    ":>>": "annotate best",
                                    ":>": "summarise best"}


def message_annotation_level(prefix: str):
    """Returns the annotation level of input, None if not present.
    See `message_prefix_meanings`"""
    if prefix in message_prefix_annotation_levels:
        return message_prefix_annotation_levels[prefix]


def split_input(input: str) -> tuple:
    "Splits input into tuple of :>+ and the rest of the input."
    return re.match(r"(:>+)\s*(.*)", input).groups()


def lookup_entry(entry: str, annotation_level):
    return "entry"


def is_in_edinburg(word: str):
    file_path = os.path.join(base_dir,
                             "preprocessed_dictionaries",
                             "words_that_Edinburgh_has.txt")
    with open(file_path) as file:
        for line in file:
            if line.strip() == word:
                return True
    return False


def lookup_word(word: str, annotation_level):
    "Looks up word. If Tad doesn't cover word, returns a message stating that."
    if not is_in_edinburg(word):
        return messages["not in edinburgh"]

    lookup_data = get_word_lookup_data(word)
    if lookup_data:
        return formatted_word_lookup(word, lookup_data, annotation_level)
    else:
        return messages["not in tad"]


raw_steno_regex = re.compile(
            r'^(S?T?K?P?W?H?R?[AO*\-EU]+F?R?P?B?L?G?T?S?D?Z?)(/S?T?K?P?W?H?R?[AO*\-EU]+F?R?P?B?L?G?T?S?D?Z?)*$')


def is_raw_steno(input: str):
    return re.match(raw_steno_regex, input)


def lookup(input: str, annotation_level):
    "Looks up the appropriate response for the (validated) user input."
    return (lookup_entry(input, annotation_level)
            if is_raw_steno(input)
            else lookup_word(input.lower(), annotation_level))


def is_valid_input(input: str):
    "Returns whether input is valid."
    return bool(re.match(r"(:>|:>>|:>>>)\s*[^:>\s]+", input))


def get_response(user_input: str) -> str:
    "Returns the appropriate response for user input."
    if is_valid_input(user_input):
        prefix, input = split_input(user_input)
        annotation_level = message_annotation_level(prefix)
        return lookup(input, annotation_level)
    else:
        return messages["help"]


# Remove
get_response(":> TKOG")
