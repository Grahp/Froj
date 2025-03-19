# Froj 
Shorthand dictionary generator
![Froj diagram](images/Froj_diagram.png)

Froj converts Edinburgh's pronunciation dictionary into stenography outlines using theory rules and brute force

Every rule depends on four things:
- Spelling
- Phonetics
- previous keys
- Prefixes/roots/compounds/suffixes

Every rule outputs three things:
- chord
- ambiguity (for conflict resolution)
- description (for FrojBot)

# Tadpole theory
Tadpole theory is my collection of 400 rules from various other theories/people

Designed to work with any accent, once you've labelled which vowels you use (is the 'e' in 'zebra' long or short?) you can then generate your dictionary with Froj

# FrojBot
FrojBot is the annotated lookup tool for a Froj theory running via a Discord bot


## :> unannotated summary
If you feed it a word, it summarises the best ways to write it, and what conflicts there could be
![Unannotated lookup for the word 'summary'](images/Unannotated_summary_for_the_word_summary.png)

If you feed it raw steno, it will find what possible matches there are, showing the best fit first
![Unannotated lookup for the steno 'PAEUR'](images/Unannotated_summary_for_the_steno_PAEUR.png)

## :>> annotated summary
Given a word or raw steno, will describe each theory rule used to make that outline
![Annotated lookup for the word 'Harlow'](images/Annotated_summary_for_the_word_Harlow.png)

Red to highlight that steno order has been folded
![Annotated lookup for the raw steno 'TO*ERGT'](images/Annotated_summary_for_the_steno_TO*ERGT.png)

## :>> unannotated show all
If you want to see all the ways you could write a word
![Unannotated lookup for the word 'read'](images/Unannotated_complete_outlines_for_the_word_read.png)