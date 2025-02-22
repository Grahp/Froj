
import json
import re

with open("../Froj_theories/Froj_Harri_theory/best_of_word_to_entry_lookup.json", "r") as f:
    best_words = json.load(f)
with open("../Froj_theories/Froj_Harri_theory/all_word_to_entry_lookup.json", "r") as f:
    all_words = json.load(f)
with open("../Froj_theories/Froj_Harri_theory/Froj_Plover_dictionary.json", "r") as f:
    entries = json.load(f)
with open("../Froj_theories/Froj_Harri_theory/Froj_verbose_lookup.json", "r") as f:
    verbose_entries = json.load(f)

is_raw_steno = re.compile(r'(S?T?K?P?W?H?R?A?O?\*?E?U?F?R?P?B?L?G?T?S?D?Z?)(/S?T?K?P?W?H?R?A?O?\*?E?U?F?R?P?B?L?G?T?S?D?Z?)*')


def get_response( user_input:str) -> str:
    word_to_find = user_input


    if ":>>> " in word_to_find:
        word_to_find=word_to_find.replace(":>>> ","")
        complexity = 'very complex'
    elif ":>>> " in word_to_find:
        word_to_find=word_to_find.replace(":>>> ","")
        complexity = 'very complex'

    elif ":>> " in word_to_find:
        word_to_find=word_to_find.replace(":>> ","")
        complexity = 'complex'
    elif ":>>" in word_to_find:
        word_to_find=word_to_find.replace(":>>","")
        complexity = 'complex'

    elif ":> " in word_to_find:
        word_to_find=word_to_find.replace(":> ","")
        complexity = 'simple'
    elif ":>" in word_to_find:
        word_to_find=word_to_find.replace(":>","")
        complexity = 'simple'
    
    else:
        return


    if word_to_find == '':
        return 'you can do :> for lookup, :>> for complex lookup'


    if is_raw_steno.match(user_input):
        if user_input in entries:
            if complexity == 'simple':
                return entries[user_input]
            else:
                return verbose_entries[user_input]


    elif 'hello' in word_to_find:
        return f"Hi friend (ΘoΘ )"
    elif 'froj' in word_to_find:
        return f"That's me! How can I help?"
    elif 'shrimp' in word_to_find:
        return "🦐"
    elif 'crazy' in word_to_find:
        return "I was crazy once"
    elif f"{word_to_find}:" in best_words:

        #if complexity == 'very complex':


        response = ""
        response+= f'found `{word_to_find}`'

        if best_words[word_to_find+':']['text'] == "showing the best 0 out of 0 entries":
            return "Sorry, Harri hasn't written all the rules to make that word. Removing suffixes *might* help"

        response+= f"\n{best_words[word_to_find+':']['text']}"

        for entry in reversed(best_words[word_to_find+':']['entries']):
            response+=f"```"

            thingie = (entry['raw steno']
                   .replace('Z*','*Z')
                   .replace('D*','*D')
                   .replace('S*','*S')
                   .replace('T*','*T')
                   .replace('G*','*G')
                   .replace('L*','*L')
                   .replace('B*','*B')
                   .replace('P*','*P')
                   .replace('R*','*R')
                   .replace('F*','*F')
                   .replace('U*','*U')
                   .replace('E*','*E')
                   .replace('-*','*'))

            response+= (f"\n{thingie}")
            if complexity == 'complex':
                for chord in entry['explanation']:
                    response+= f"\n\t{chord}"
            response+= f"```"

        return response
        return f"Found {word_to_find}\n{best_words[word_to_find+':']['text']}\n{best_words[word_to_find+':']['entries']}"
        #,{words['{word_to_find}:']['text']}"
        return best_words["{word_to_find}:"]
    else:
        return "Sorry, I'm missing the pronunciation data for that word :("



