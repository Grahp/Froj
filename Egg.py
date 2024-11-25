"""
questions for professor
why is pancake pang+cake
but suncream sun+cream not sung+cream

huh? why is it "sh == n" and not "== sh n"?
starting_root  l  i  .  k  w  I2  =.=  f  a  k  .  sh  ==  n ",
  "word_boundaries": "lique==fact==ion",



  
I've found missing pronunciations for "lithe"
HRAO*EUT seems to be the most common
HR*EUT https://youtu.be/CTgk5pGOe1g?si=MwXHGoLloZJcPXFq&t=517
(8:37)
HRAO*ET https://youtu.be/-5FEgL-BkIk?si=1XSGHabJnnN6g-fg&t=10239
(2:50:40)

I've also found voiced and unvoiced versions for "lithe", but I don't know of any steno theory that makes a distinction so that doesn't interest me




Going based off word boundaries instead of the spelling means there's no difference between downy and downie
"""
import multiprocessing
import json

from convert_unilex_into_readable_lists import (
    full_entry_pattern,
    make_boundaries_into_list,
    make_target_pronunciation_into_string,
    make_target_spelling_into_string)

from map_steno_chords_to_keysymbols import generate_write_outs








def make_input_into_dictionary_entry(input):
    word = full_entry_pattern.fullmatch(input).groupdict()

    word['pronunciation'           ] = make_target_pronunciation_into_string(make_boundaries_into_list(word['pronunciation']))
    word['word_boundaries'         ] = make_target_spelling_into_string(make_boundaries_into_list(word['word_boundaries']))
    #print(word)
    word['number of entries'   ] = (0)
    word['steno stuff'         ] = generate_write_outs(word)
    word['number of entries'   ] = len(word['steno stuff'])

    #print(word)



    word['pronunciation'           ] = str(word['pronunciation'])
    word['word_boundaries'           ] = str(word['word_boundaries'])
    return word
    return {word['word']: (word)}
    return {word['word']:word}


with (open("big.txt", "r", encoding="utf-8")) as txt_dictionary:
    outlines = txt_dictionary.readlines()



#for outline in outlines:
#    results = make_input_into_dictionary_entry(outline)



with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:

    results = pool.map(make_input_into_dictionary_entry, outlines)

with open("Egg_output.json", "w") as outfile:
    json.dump(results, outfile, indent=1)

#print(results)


"""
Example of an entry:

dictionary['["seriously"],["RB"]'] = [

            #phonetics
            [[[["s"] ["*"] ["ir"] ["."] ["r"] ["ii"] ["@"] ["s"]],["root"]],[["l iy"],["suffix"]]],

            #orthography
            [[["serious"],["root"]],          [["ly"],["suffix"]]],

            #write outs
            ["SAOER/KWRAOE/KWRUS/HREU" 1],

            #briefing within word boundaries
            ["SAOER/KWHUS/HREU" 1, "SAO*ERD/KWRUS/HREU" 2,"SAOERS/HREU" 3],

            #briefing between word boundaries
            ["SAOER/KWRAOE/KWRULS" 2, "SAOER/KWHULS" 3, "SAO*ERD/KWRULS" 3,"SAOER/KWRULS" 4,"SAO*ERLSZ" 5, "SAOERLS" 5,"SHRAOERLS" 6]]
"""
