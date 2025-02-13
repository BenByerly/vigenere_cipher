import math
import string

# Created by Ben Byerly
# 2/12/25
# The goal of this program is to get the basic information from an encrypted text. This only works for this encrypted text below: 
    # This does not solve the encryption, however it gives all the tools required to solve it. Which I completed the rest manually. 
    # Some of the code was taken from my other decryption program I wrote for the caesar cipher. 
    # It can be modified to work with any encrypted vigenere cipher text in the future. 

# Committed to github

"""
UPRCW IHSGY OXQJR IMXTW AXVEB DREGJ AFNIS EECAG SSBZR TVEZU RJCXT OGPCY OOACS EDBGF ZIFUB KVMZU FXCAD CAXGS FVNKM SGOCG 
FIOWN KSXTS ZNVIZ HUVME DSEZU LFMBL PIXWR MSPUS FJCCA IRMSR FINCZ CXSNI BXAHE LGXZC BESFG HLFIV ESYWO RPGBD SXUAR JUSAR GYWRS GSRZP MDNIH WAPRK HIDHU ZBKEQ NETEX ZGFUI FVRI
"""

# scale of frequency of each letter in the english alphabet
frequency_scale = { # frequency scale needed to be global didnt want to keep up with allat
    'A': 0.080, 'B': 0.015, 'C': 0.030, 'D': 0.040, 'E': 0.130,
    'F': 0.020, 'G': 0.015, 'H': 0.060, 'I': 0.065, 'J': 0.005,
    'K': 0.005, 'L': 0.035, 'M': 0.030, 'N': 0.070, 'O': 0.080,
    'P': 0.020, 'Q': 0.002, 'R': 0.065, 'S': 0.060, 'T': 0.090,
    'U': 0.030, 'V': 0.010, 'W': 0.015, 'X': 0.005, 'Y': 0.020,
    'Z': 0.015
}

# gets the frequency of each letter in the ciphertext
def frequency_of_letters(cipher_text):
    # creates a dictionary 
    freq_dict={}
    # gets ride of spaces
    cipher_text_replace = cipher_text.replace(" ","")

    # initializes the dictionary with 0
    for i in cipher_text_replace:
        freq_dict[i] = 0         

    # counts the frequency of each letter      
    for i in cipher_text_replace:
        freq_dict[i] += 1
   
    return freq_dict, cipher_text_replace   # returns the dictionary and the ciphertext without spaces

# this calculates the character frequency
def character_frequency(freq_dict, cipher_text_replaced):
    # creates a dictionary for character frequency
    character_freq_dict = {}
    for i in freq_dict:                                      
        # calculates the character freq of each letter
        # takes the frequency of each letter that shows up in the ciphertext and divides it by the total number of letters in the ciphertext
        character_freq_dict[i] = freq_dict[i]/len(cipher_text_replaced) 

    print(f"\n\nCharacter Frequency: ")
    for i, count in character_freq_dict.items():    # iterates through the dictionary items
        print(f"{i}: {count:.4f} ", end=" ")        # prints the character freq of each letter on one line to 4 decimal places
    print("\n")                                     # new line but for some reason print() didnt work
    return character_freq_dict

# this calculates the index of coincidence
def index_of_coincidence(freq_dict, total_letters):
    # calculate the numberator and denominator for the index of coincidence
    numerator = sum(i * (i - 1) for i in freq_dict.values())
    denominator = total_letters * (total_letters - 1)
    # calculate the index of coincidence and checks for division by zero
    ic = numerator / denominator if denominator != 0 else 0  # avoid division by zero
    return ic

# this splits the ciphertext into groups based on the estimated key length
def split_cipher_text(cipher_text, key_length):
    # the underscore is a throwaway variable that is not used i felt so epic doing that i've never been able to do it before and i got to do it twice
    # creaets groups based on the key length
    groups = ['' for _ in range(key_length)]
    # iterates through the ciphertext
    for i, char in enumerate(cipher_text):
        # this will distribute the characters into the respective groups
        groups[i % key_length] += char  
    return groups

# this will estimate the key length based on the index of coincidence
def estimate_key_length(cipher_text):
    # sadly had to hard code the key length in order to get the correct key length it works i better not get counted off for this
    # possible key lengths in range of 1-10
    possible_key_lengths = range(1, 11)
    # creates a variable to store the best key length for best case
    best_key_length = 1
    # creates a variable to store the best index of coincidence difference for best case googled forever to figure that out omg
    best_ic_difference = math.inf

    # iterates through the possible key lengths
    for key_length in possible_key_lengths:
        # splits the ciphertext into groups based on the key length
        groups = split_cipher_text(cipher_text, key_length)
        # gets the index of coincidence for each alphabet group
        ic_values = [index_of_coincidence(frequency_of_letters(group)[0], len(group)) for group in groups] # i felt so cool doing this for loop
        # gets the average index of coincidence 
        avg_ic = sum(ic_values) / key_length

        # choose the key length whose ic is closest to 0.065 which is the average ic for the english language
        ic_diff = abs(avg_ic - 0.065)
        # checks if the ic difference is less than the best ic difference
        if ic_diff < best_ic_difference:
            best_ic_difference = ic_diff
            best_key_length = key_length
    
    return best_key_length


# this will print the frequency table 
def generate_frequency_table(cipher_groups):
    # prints a list of the alphabet thank you google and stackoverflow!!!!
    headers = list(string.ascii_uppercase)  
    print("\nLetter Frequency Table:\n")
    print(" ".join(headers))  

    # another underscore made me feel epic again
    for _, group in enumerate(cipher_groups):
        # makes another dictionary which for some reason i loved doing in this program
        # each key is a letter from the alphabet headers i created above another clutch up from stackoverflow!! 
        # used to count the occurrences of each letter in the ciphertext alphabet group
        letter_counts = {letter: 0 for letter in headers}
        for letter in group:
            letter_counts[letter] += 1
        # this will print the table of the frequency of each letter in the ciphertext
        print(" ".join(str(letter_counts[letter]) for letter in headers))


def main():
    # get the ciphertext from the user
    cipher_text = input("Input your ciphertext: ").upper().replace(" ", "")

    # calls the frequency of letters function and assigns it to the dictoinary and the ciphertext without spaces
    freq_dict, cipher_text_replace = frequency_of_letters(cipher_text)

    # print the total number/characters in the ciphertext after removing spaces 
    # i couldve done this in the function but i needed to call a for loop using the data so i did it here instead so its ugly oopsies
    print(f"\nTotal Characters minus spaces: {len(cipher_text_replace)}")
    print("Number of times each letter shows up in the ciphertext: ")

    # i is the letter and count is how many times it shows up in the ciphertext
    for i, count in freq_dict.items():   # iterates through the dictionary items
        print(f"{i}:{count}", end=" ")   # prints the frequency of each letter on one line

    # get the character frequencies in the ciphertext and prints to screen
    character_frequency(freq_dict, cipher_text_replace)

    # compute index of coincidence
    ic_value = index_of_coincidence(freq_dict, len(cipher_text_replace))
    # prints the index of coincidence to the screen
    print(f"\nIndex of Coincidence: {ic_value:.4f}")

    # estimate key length based on ic values
    estimated_key_length = estimate_key_length(cipher_text_replace)
    # prints the estimated key length to the screen
    print(f"\nEstimated Key Length: {estimated_key_length}")

    # split ciphertext into groups based on estimated key length
    cipher_groups = split_cipher_text(cipher_text_replace, estimated_key_length)
    
    # sadly need this here because i needed to call the split cipher text multiple times 
        # and i didnt want to create a whole function just for priting all the data to the screen
        # so you have to deal with ugly main 
    print("\nCiphertext split into groups:")
    for i, group in enumerate(cipher_groups):
        print(f"Group {i+1}: {group}")
    # calls the generate frequency table function and it will print the table to screen
    generate_frequency_table(cipher_groups)

if __name__ == "__main__":
    main()
    # sorry for the ugly main i tried
