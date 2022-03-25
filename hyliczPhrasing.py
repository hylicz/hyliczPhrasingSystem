import re

LONGEST_KEY = 1
 


def lookup(chord):
    
    chord = list(chord)
    for i in range(len(chord)):
        chord[i] = list(chord[i])

        if any(k in chord[i] for k in "1234506789"):  # if chord contains a number
            numbers = ["O", "S", "T", "P", "H", "A", "F", "P", "L", "T"]
            for character in range(len(chord[i])):
                if chord[i][character].isnumeric():
                    chord[i][character] = numbers[int(chord[i][character])]
                     


            chord[i].insert(0, "#")
        chord[i] = "".join(chord[i])

    chord = tuple(chord)

    
    match = re.fullmatch(r'(#?)([STKPWHR]*)([AO]*)([*-]?)([EU]*)([FRPBLGTS]*)(D?)(Z?)', chord[0])
    
    if match is None:
        raise KeyError
    (emph, pronoun, ao, negation, eu, verb, tense, extra) = match.groups()
    modalverb = ao + eu


    # Pronouns
    # First number: 1 for first person, 2 for second person, 3 for third person
    # Second number: 1 for singular, 2 for plural
    pronouns = {
        "SWR"       : ["I",     1, 1],
        "KPWR"      : ["you",   2, 1],
        "KWHR"      : ["he",    3, 1],
        "SKWHR"     : ["she",   3, 1],
        "KPWH"      : ["it",    3, 1],
        "TWR"       : ["we",    1, 2],
        "TWH"       : ["they",  3, 2],    
        "STKPWHR"   : ["",      1, 1]
    }


    # Modal verbs
    # Forms: Normal, third person singular, past tense, negative normal, negative third person singular, negative past tense.
    modalverbs = {

        ""          : ["", "", "", "", "", ""],
        "A"         : ["can","can","could", "can't", "", "couldn't"],
        "O"         : ["have", "has", "had", "haven't", "hasn't", "hadn't"],
        "E"         : ["do","does","did", "don't", "doesn't", "didn't"],
        "U"         : ["must","must", "must have", "must not", "", "must not have"],
        "AO"        : ["want to", "wants to", "wanted to", "don't want to", "doesn't want to", "didn't want to"],
        "AE"        : ["really don't", "really doesn't", "really didn't"],
        "AU"        : ["ought to", "ought to", "ought to have", "ought not to", "", "ought not to have"],
        "OE"        : ["don't","doesn't","didn't"], 
        "OU"        : ["would", "would", "would have"],
        "EU"        : ["will", "will", "will have"],
        "AOE"       : ["don't even","doesn't even", "didn't even"],
        "AOU"       : ["do", "does", "did"],
        "AEU"       : ["think you should", "thinks you should", "think you should have", "don't think you should", "doesn't think you should", "don't think you should have"],
        "OEU"       : ["don't really","doesn't really", "didn't really"],
        "AOEU"      : ["like to", "likes to", "liked to"]
    }

    # Regular Verbs & Final Words
    # First form: present tense
    # Second form: past tense
    # Third form: extra word!
    verbs = {
        ""          : ["","",""],
        "P"         : ["want", "wanted", "to"],
        "PBT"       : ["need", "needed", "to"],
        "BLG"       : ["like", "liked", "to"],
        "RL"        : ["recall", "recalled", "that"],
        "PBG"       : ["think", "thought", "that"],
        "FL"        : ["feel", "felt", "that"],
        "BL"        : ["believe", "believed", "that"],
        "RPL"       : ["remember", "remembered", "that"],
        "RBG"       : ["care", "cared", "about"],
        "GT"        : ["get", "got", "to"],
        "LG"        : ["love", "loved", "to"],
        "FRB"       : ["wish", "wished", "to"],
        "PGT"       : ["expect", "expected", "to"],
        "RPBT"      : ["understand", "understood", "that"],
        "BS"        : ["say", "said", "to"],
        "PLG"       : ["imagine", "imagined", "that"],
        "PBLG"      : ["just", "just", "about"],

    }

    # Irregular verbs
    irregularverbs = {
        "R"         : ["be", "am", "are", "is", "been", "was", "were", "the"],
        "F"         : ["have", "have", "have", "has", "had", "had", "had", "the"],
        "T"         : ["do", "do", "do", "does", "done", "did", "did", "the"],
        "PB"        : ["know", "know", "know", "knows", "known", "knew", "knew", "that"]
    }

    # Alternative starters
    # Type 1 defined in the dictionary
    # Type 2 points to a verb in the verbs dictionary
    altstarters = {
        "WHA"       : ["what", 1],
        "STHA"      : ["that", 1],
        "STPA"      : ["if",   1],
        "STKA"      : ["AOU",  2], # Do
        "SKPW"      : ["OE",   2], # Don't
        "SWH"       : ["when", 1],
    }

    emphasis = "really"




    if pronoun not in pronouns and pronoun+ao not in altstarters:
        raise KeyError

    assert len(chord) <= LONGEST_KEY

    ### Defining variables
    modalverbvalue = 0

    requirealt = False
    negate = False
    pasttense = False
    modal = False
    modalhashave = False
    thirdsingular = False
    addemphasis = False
    addextra = False
    irregularverb = False
    

    ### Performing checks
    # If the pronoun is third person and singular, it's a third person singular pronoun.
    if pronouns[pronoun][1] == 3 and pronouns[pronoun][2] == 1: thirdsingular = True 

    # If we need to add emphasis
    if "#" in emph: addemphasis = True

    # If we're using an alt starter instead of a pronoun
    if pronoun+ao in altstarters: requirealt = True
    
    # If a modal verb is to be added
    if modalverb in modalverbs and modalverb != "": modal = True
    
    # Check if modal verb contains aux verb "have" 
    if "have" in modalverbs[modalverb][2]: modalhashave = True

    # If -D is pressed, the verb must be in the past tense.
    if "D" in tense: pasttense = True
    
    # Checking if the modal verb should be negated
    if "*" in negation: modalverbvalue +=3

    # Checking if needs to add extra word
    if "Z" in extra: addextra = True

    # Checking if the verb is irregular
    if verb in irregularverbs:
        irregularverb = True
        

    ###########################################
    # Welcome, my son. Welcome to The Machine.#
    ###########################################
    output = []

    if requirealt:
        pass 


    else:
        # Pronouns
        output.append(pronouns[pronoun][0])

        # Emphasis
        if addemphasis: output.append(emphasis)


        # Verbs
        if  irregularverb:
            if pasttense:
                if modal:    
                    if modalhashave:
                        output.append(modalverbs[modalverb][modalverbvalue+2]) 
                        output.append(irregularverbs[verb][4])
                    else:
                        output.append(modalverbs[modalverb][modalverbvalue+2]) 
                        output.append(irregularverbs[verb][0])
                else:    
                    if pronouns[pronoun][1] == 1 and pronouns[pronoun][2] == 1:
                        output.append(irregularverbs[verb][5])
                    elif pronouns[pronoun][1] == 3 and pronouns[pronoun][2] == 1:
                        output.append(irregularverbs[verb][5])
                    else:
                        output.append(irregularverbs[verb][6])

            else:
                if modal:
                    if thirdsingular:
                        output.append(modalverbs[modalverb][modalverbvalue+1])
                        output.append(irregularverbs[verb][0])
                    else:
                        output.append(modalverbs[modalverb][modalverbvalue]) 
                        output.append(irregularverbs[verb][0])
                else:
                    if pronouns[pronoun][2] == 2:
                        output.append(irregularverbs[verb][2])
                    else:
                        output.append(irregularverbs[verb][pronouns[pronoun][1]])
                    


              




        else:
            if pasttense:
                if modal:
                    if modalhashave:
                        output.append(modalverbs[modalverb][modalverbvalue+2]) 
                        output.append(verbs[verb][1])
                    else:
                        output.append(modalverbs[modalverb][modalverbvalue+2]) 
                        output.append(verbs[verb][0])
                else:
                    output.append(verbs[verb][1])
            
            else:
                if modal:
                    if thirdsingular:
                        output.append(modalverbs[modalverb][modalverbvalue+1]) 
                        output.append(verbs[verb][0])
                    else:
                        output.append(modalverbs[modalverb][modalverbvalue]) 
                        output.append(verbs[verb][0])
                else:
                    if thirdsingular:
                        output.append(verbs[verb][0] + "s")
                    else:
                        output.append(verbs[verb][0])

    # Handling present perfect tense
    if modalverbs[modalverb][0] == "have":
        output.pop()
        if irregularverb: output.append(irregularverbs[verb][4])
        else: output.append(verbs[verb][1])

    # Add optional extra word if required
    if addextra:
        if irregularverb: output.append(irregularverbs[verb][7])
        else: output.append(verbs[verb][2])

    return " ".join(output)