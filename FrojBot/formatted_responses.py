import os
from typing import Dict, Optional
from response_utils import load_json, base_dir

_lookup_data_cache: Optional[Dict[str, dict]] = {}


# You could make an equivilent function to this one that calls the other 2 simpler functions.
def get_lookup_data(prefix: str, lookup_type: str) -> Dict[str, dict]:
    "Get relevant lookup data for the given prefix and lookup type (entries or outlines)"
    global _lookup_data_cache
    # Ensure that we load data only once for the given letter
    if lookup_type not in _lookup_data_cache:
        _lookup_data_cache[lookup_type] = {}

    if prefix not in _lookup_data_cache[lookup_type]:
        # Lazy load the corresponding file based on the letter and lookup type
        file_path = os.path.join(base_dir, "preprocessed_dictionaries", f"{lookup_type}_starting_{prefix}.json")
        if os.path.exists(file_path):
            _lookup_data_cache[lookup_type][prefix] = load_json(file_path)
        else:
            _lookup_data_cache[lookup_type][prefix] = {}  # Empty if not found

    # After lookup, clear the cache
    result = _lookup_data_cache[lookup_type][prefix]
    _lookup_data_cache[lookup_type].pop(prefix, None)  # Remove this entry from cache after use
    if not _lookup_data_cache[lookup_type]:  # Clean up cache if it's empty
        _lookup_data_cache.pop(lookup_type, None)

    return result


def giveChordsColours(theory_rules, colours):
    coloured_letters = []

    # Iterate through each theory rule
    for i, theory_rule in enumerate(theory_rules):
        # Get the colour for this rule
        colour = "\033[2;" + colours[i % len(colours)] + "m"
        folding_colour = "\033[2;35m"
        end_colour = "\033[0m"

        # List to hold each character with its respective colour
        chord_coloured = []

        number_of_spaces = 5
        if "fold" in theory_rule['chord']:
            for character in theory_rule['chord']:
                if character in ("/STKPWHRAO-*EUFRPBLGTSDZ"):
                    chord_coloured.append([folding_colour, character, end_colour])
                    number_of_spaces -= 1
        else:
            # Iterate through the chord characters in the rule
            for character in theory_rule['chord']:
                if character in ("/STKPWHRAO-*EUFRPBLGTSDZ"):
                    chord_coloured.append([colour, character, end_colour])

                    number_of_spaces -= 1

        spaces = ""
        for i in range(number_of_spaces):
            spaces += " "

        # Store the coloured chord back into the theory_rule
        # The chord is now a string with its full colour coding
        theory_rule['chord'] = spaces + ''.join([x[0] + x[1] + x[2] for x in chord_coloured])

        # Also append the coloured version of the chord to coloured_letters
        coloured_letters.extend(chord_coloured)

    return theory_rules, coloured_letters


def colour_the_outline(uncoloured_outline, coloured_letters):
    coloured_outline = ""

    # Iterate through each character in the uncoloured outline
    for character in uncoloured_outline:
        # Flag to check if the character is found and coloured
        found = False

        # Check if the character matches any of the coloured letters
        for i, coloured_letter in enumerate(coloured_letters):
            if character == coloured_letter[1]:
                coloured_outline += "".join(coloured_letters.pop(i))  # Apply colour to the character
                found = True  # Set flag to True if a match is found
                break

        # If no match was found, apply the grey and normal colour
        if not found:
            coloured_outline += "\033[2;30m" + character + "\033[0m"  # Grey colour for uncoloured characters

    return coloured_outline


def colour_the_outline_with_chords(outline, theory_rules):
    colours = [
        "32",  # green
        "34",  # blue
        "33",  # yellow
        "36",  # cyan
    ]

    coloured_theory_rules, coloured_letters = giveChordsColours(theory_rules, colours)

    coloured_outline = colour_the_outline(outline, coloured_letters)

    return coloured_outline, coloured_theory_rules


# Function to print the smallest stroke count per ambiguity level, ensuring more ambiguous strokes only show if shorter than previous ones
def formatted_word_lookup(word, word_lookup_data, annotation_level):
    "Returns the formatted ANSI discord word lookup guy"
    output = ""
    ambiguity = word_lookup_data.get("ambiguity", {})

    number_of_best_entries = 0

    total_number_of_entries = sum(
        len(ambiguity[amb]["number of strokes"][stroke_count])

        for amb in ambiguity
        for stroke_count in ambiguity[amb]["number of strokes"]
        for stroke_count in ambiguity[amb]["number of strokes"]
    )

    # Sort ambiguity levels by their numeric value (e.g., "2", "5")
    sorted_ambiguities = sorted(ambiguity.keys(), key=int)

    # Keep track of the smallest stroke count encountered
    smallest_stroke_count = float('inf')  # Initialize to infinity, so the first stroke will always be considered

    too_big = ""

    for amb in sorted_ambiguities:
        entries = ambiguity[amb]["number of strokes"]

        # Sort the stroke counts for the ambiguity level to pick the smallest first
        sorted_stroke_counts = sorted(entries.keys(), key=int)

        for stroke_count in sorted_stroke_counts:

            if not annotation_level == "summarise all":
                # Only consider this stroke if it's smaller than the smallest stroke count so far
                if int(stroke_count) >= smallest_stroke_count:
                    break
            steno_entries = entries[stroke_count]
            for entry in steno_entries:
                raw_steno = entry['raw steno outline']
                plain_raw_steno = entry['raw steno outline']

                theory_rule_breakdown = ""
                if annotation_level == "annotate best":

                    set_theory_colour = "\033[2;30m"
                    remove_colour = "\033[0m"
                    set_theory_colour = "\033[2;30m"
                    remove_colour = "\033[0m"

                    raw_steno, theory_rules = colour_the_outline_with_chords(raw_steno, entry['explanation'])
                    for theory_rule in theory_rules:
                        linker = " ┐ " if "/" in theory_rule['chord'] else " │ "
                    raw_steno, theory_rules = colour_the_outline_with_chords(raw_steno, entry['explanation'])
                    for theory_rule in theory_rules:

                        linker = " ┐ " if "/" in theory_rule['chord'] else " │ "

                        theory_rule_breakdown += f"\n{set_theory_colour}{theory_rule['theory'].ljust(8)}{remove_colour}{theory_rule['chord']}{linker}{theory_rule['description']}"
                        theory_rule_breakdown += (
                            f"\n{set_theory_colour}{theory_rule['theory'].ljust(8)}{remove_colour}{theory_rule['chord']}{linker}{theory_rule['description']}")

                if len(output) > 1200:
                    too_big = "Too big for Discord, stopped early. Try `:>`"
                    number_of_best_entries += 1
                    break

                chunk_to_add = ("```Ansi\n\n")

                if len(plain_raw_steno.split("/")) < 3:
                    list_of_all_spellings = return_list_of_all_spellings(plain_raw_steno,
                                                                         get_lookup_data(plain_raw_steno[:3].lower().replace("/","_"),
                                                                                         "entries")[plain_raw_steno])
                    if not word == list_of_all_spellings[0]:
                        chunk_to_add += (f"{raw_steno} → {list_of_all_spellings[0]}/\033[2;31m{'/'.join(list_of_all_spellings[1:])}\033[0m")

                    elif len(list_of_all_spellings) > 1:
                        chunk_to_add += (f"{raw_steno} → \033[2;32m{list_of_all_spellings[0]}\033[0m/\033[2;31m{'/'.join(list_of_all_spellings[1:])}\033[0m")
                    else:
                        chunk_to_add += (f"{raw_steno} → {word}")
                else:
                    chunk_to_add += (f"{raw_steno} → {word}")

                chunk_to_add += (theory_rule_breakdown)
                chunk_to_add += ("```")

                # Update the smallest stroke count to this one, since it's smaller
                smallest_stroke_count = int(stroke_count)
                number_of_best_entries += 1

                if len(chunk_to_add) + len(output) > 1200:
                    too_big = "Too big for Discord, stopped early. Try `:>`"
                    number_of_best_entries += 1
                    break
                output += chunk_to_add

                if not annotation_level == "summarise all":
                    break  # Only print the smallest number of strokes for this ambiguity level
            if not annotation_level == "summarise all":
                break  # Stop at the first entry (smallest strokes for this level)
    if annotation_level == "summarise all":
        output = f"Showing `{number_of_best_entries}`/`{total_number_of_entries}` outlines for `{word}` in Tadpole theory\n{output}{too_big}"
    else:
        output = f"Here's the best {number_of_best_entries}/{total_number_of_entries} entries in Tadpole theory\n{output}{too_big}"

    return output


def return_list_of_all_spellings(outline, spellings):
    ambiguity = spellings.get("ambiguity", {})
    sorted_ambiguities = sorted(ambiguity.keys(), key=int)
    list_of_all_spellings = []

    for amb in sorted_ambiguities:
        outlines = ambiguity[amb]
        for outline in outlines:
            spelling = outline['spelling']
            if not spelling in list_of_all_spellings:
                list_of_all_spellings.append(spelling)

    return list_of_all_spellings


def best_entries(outline, spellings, complexity):
    if not complexity == "annotate best":
        list_of_all_spellings = return_list_of_all_spellings(outline, spellings)

        return f"Found {len(list_of_all_spellings)} matches for `{outline}` in Tadpole theory\n`{outline}` → `{'`/`'.join(list_of_all_spellings)}`"

    output = ""
    ambiguity = spellings.get("ambiguity", {})

    total_number_of_spellings = sum(
        len(ambiguity[amb]) for amb in ambiguity
    )

    # Sort ambiguity levels by their numeric value (e.g., "2", "5")
    sorted_ambiguities = sorted(ambiguity.keys(), key=int)

    too_big = ""
    initial_raw_steno = outline
    raw_steno = outline
    number_of_best_entries = 0
    list_of_all_spellings = []

    for amb in sorted_ambiguities:
        outlines = ambiguity[amb]
        for outline in outlines:

            spelling = outline['spelling']
            if not spelling in list_of_all_spellings:
                list_of_all_spellings.append(spelling)
            theory_rule_breakdown = ""
            if complexity == "annotate best":

                set_theory_colour = "\033[2;30m"
                remove_colour = "\033[0m"

                raw_steno, theory_rules = colour_the_outline_with_chords(initial_raw_steno, outline['explanation'])

                for theory_rule in theory_rules:
                    linker = " ┐ " if "/" in theory_rule['chord'] else " │ "

                    theory_rule_breakdown += (
                        f"\n{set_theory_colour}{theory_rule['theory'].ljust(8)}{remove_colour}{theory_rule['chord']}{linker}{theory_rule['description']}")

                chunk_to_add = ("```Ansi\n\n")
                chunk_to_add += (f"{raw_steno} → {spelling}")
                chunk_to_add += (theory_rule_breakdown)
                chunk_to_add += ("```")

                if len(chunk_to_add) + len(output) > 1200:
                    too_big = "Too big for Discord, stopped early. Try `:>`"
                    break
                output += chunk_to_add

    output = f"Here's the {total_number_of_spellings} entries for `{initial_raw_steno}` in Tadpole theory (best first)\n{output}\n{too_big}"

    return output


