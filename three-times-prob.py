# Probability of seeing same character right after/right before
#    a real unit, just due to random chance.   Mostly these are
#    frequent characters
# Computation is for a single string location, e.g. just the position
#    right before the start of our extracted word.   So double it to
#    get the chance of seeing an extra letter either before or after.

# Margaret Fleck, 2023

import argparse

#  English letter frequencies
#  https://en.wikipedia.org/wiki/Letter_frequency

letters = {"A": 8.2, "B": 1.5, "C": 2.8, "D": 4.3, "E": 12.7, "F": 2.2, 
           "G": 2.0, "H": 6.1, "I": 7.0, "J": 0.15, "K": 0.77, "L": 4.0, 
           "M": 2.4, "N": 6.7, "O": 7.5, "P": 1.9, "Q": 0.095, "R": 6.0, 
           "S": 6.3, "T": 9.1, "U": 2.8, "V": 0.98, "W": 2.4, "X": 0.15, 
           "Y": 2.0, "Z": 0.074}	
 
# Do they sum to 1.0?
def total_probs(letters):
    sum = 0
    for letter in letters:
        sum += letters[letter]
#    print(sum)
    return sum

# find probabilty of seeing duplicate letters k times
# denominator is what the values in letters sum to (e.g. 100 rather than 1.0)
def duplicate_prob(letters,k,denominator):
    sum = 0
    for letter in letters:
        prob = letters[letter]/denominator
        sum += prob**k
    print(f"Probability of seeing letter {k} times is {sum}")
    print(f"This is about 1 time in {round(1/sum)}")

def main(k):
    global letters
    sum = total_probs(letters)
    duplicate_prob(letters,k,sum)

# Top-level entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='three-times-prob k')
    parser.add_argument('k')
    args = parser.parse_args()
    main(int(args.k))
    
