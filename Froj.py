"""
where's matte

questions for professor
why is pancake pang+cake
but suncream sun+cream not sung+cream

huh? why is it "sh == n" and not "== sh n"?
starting_root  l  i  .  k  w  I2  =.=  f  a  k  .  sh  ==  n ",
  "word_boundaries": "lique==fact==ion",

I wanna stick a w in here, you know where
  "pronunciation": " starting_root  s  p  i  r  i  t  suffix  y  uu  @  l ",

the first morpheme is {able} and not {abile}, I get it :(
ability::NN: { @ . b * i l $}.> @ . t iy > :{able}>ity>:14435

"word": "abrasive:",
  this is just nasty
  "word_boundaries": "abradeive",
  abrasive::JJ: { @ . b r * ee s $}.> i v > :{abrade}>ive>:221

  
the suffix is just y, but the spelling has 2 'l's?
  "pronunciation": " starting_root  a  b  d  o  m  i2  n  l  suffix  iy ",
  "word_boundaries": "abdominally",


there's just no way there's a single suffix in all of this?
  indefatigability::NN: { ~ i n =.= d i . f ~ a . t i . g @ . b * i l $}.> @ . t iy > :{in==defatigable}>ity>:1


would be much more useful if medical terms were in here like buccinator, random body parts
  
parallelepiped


what does "(@r/~ e)" mean? I thought it was my bad formatting but it's not
  
in my accent, the 'air r' in Aaron is different to the 'air r' in aerate.


this is the only word with ai1... why bother giving it an entire keysymbol?
acetylcholine::NN: { @ . s ~ ii . t [ai1] l . k * ou . l ii n } :{acetylcholine}:304



tissue::NN: { t * i . s y iu3 } :{tissue}:3260???????????
No alternative spellings?


is this really not using the suffix ize??
  "word": "accessorized:",

  
why is
clowned::VBD/VBN/JJ: { k l * ow n }> d > :{clown}>ed>:4
but


why is absence with e50, but absenses no vowel at all?


uu/uu????????????
acumen::NN: { [*] A . k y [*1] uu/uu . m E n } :{acumen}:293

t        = T
t [y]    = T
t  y     = KH
   y  uu = W

and without it being explicitly defined:
t  y  uu = TW
amazing!

`ABG/TWAL` → `actual` (I use BG for c)



there's a word which is one vowel followed by 5 consonants??? (6 if you include a glottal stop after the n)
  "word": "accents:1",
  "word_class": "NNS",
  "pronunciation": " starting_root  a  k  s  [e1]  n  t  suffix  s ",

  
I've found missing pronunciations for "lithe"
HRAO*EUT seems to be the most common
HR*EUT https://youtu.be/CTgk5pGOe1g?si=MwXHGoLloZJcPXFq&t=517
(8:37)
HRAO*ET https://youtu.be/-5FEgL-BkIk?si=1XSGHabJnnN6g-fg&t=10239
(2:50:40)

I've also found voiced and unvoiced versions for "lithe", but I don't know of any steno theory that makes a distinction so that doesn't interest me


The word "outworkings" is missing,

abdication, I think I say with an y... so should be d [y] ?

I say "assume" with sh, but I don't say "pseudo" with a sh

Going based off word boundaries instead of the spelling means there's no difference between downy and downie

mum says fact with an unaspirated c, and dad hears it as "fat"



suffix sh n versus sh suffix n

  "word": "accreditation:",
  "pronunciation": " starting_prefix  @  root  k  r  e  d  i2  t  suffix  ee  suffix  sh  n ",

  "word": "accreditations:",
  "word_class": "NNS",
  "pronunciation": " starting_prefix  @  root  k  r  e  d  i2  t  suffix  ee  sh  suffix  n  suffix  z ",


I say 'sh' but I hear 's' lots
species:2:NNS: { s p * ii . sh ii z } ::11014


This says 'z' but I say zh, so I'd at least expect   z y
ambrosial::JJ: { a m . b r * ou . z ii @ }> l > ::94


you separate k and g, but not s and s?
background::NN: { b * a k }.{ g r - ow n d } ::13149

@ in thm?
algorithm::NN: { * a l . g @r . r ~ i . dh @ m } ::250



 {
  "word": "aux:",
  "word_class": "FW",
  "pronunciation": " starting_root  ou ",
  "word_boundaries": "aux",
  "frequency": "74",
  "number of entries": 0,
  "steno stuff": {}
 },

"""
import multiprocessing
import json

from convert_unilex_into_readable_lists import (
    full_entry_pattern,
    make_boundaries_into_list,
    make_target_pronunciation_into_string,
    make_target_spelling_into_string)

from map_steno_chords_to_keysymbols import generate_write_outs

from chord_definitions import steno_chords_and_their_meanings

def make_input_into_dictionary_entry(input, user_chords):
    word = full_entry_pattern.fullmatch(input).groupdict()
    #print(word)

    word['pronunciation'    ] = make_target_pronunciation_into_string(make_boundaries_into_list(word['pronunciation']))
    #word['word_boundaries'  ] = make_target_spelling_into_string(make_boundaries_into_list(word['word_boundaries']))
    word['word_boundaries'  ] = word["word"].split(":")[0]
    #print(word['word_boundaries'])
    word['number of entries'] = (0)
    word['steno stuff'      ] = generate_write_outs(word, user_chords)
    word['number of entries'] = len(word['steno stuff'])
    word['pronunciation'    ] = str(word['pronunciation'])
    word['word_boundaries'  ] = str(word['word_boundaries'])
    return word


with (open("most.txt", "r", encoding="utf-8")) as txt_dictionary:
    outlines = txt_dictionary.readlines()

#for outline in outlines:
#   results = make_input_into_dictionary_entry(outline, steno_chords_and_their_meanings)

#using multiple inputs
with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
    results = pool.starmap(make_input_into_dictionary_entry, [(outline, steno_chords_and_their_meanings) for outline in outlines])

with open("11_02_25 most Froj.json", "w") as outfile:
    json.dump(results, outfile, indent=1)
