#Simon Ho/sho16

import string
#get Counter to count, get defaultdict to easily group mod&count pairs into a dict of lists.
from collections import Counter, defaultdict

# english frequencies found in wiki.
eng_frq = [ ('A', 0.08167),
  ('B', 0.01492),
  ('C', 0.02782),
  ('D', 0.04253),
  ('E', 0.12702),
  ('F', 0.02228),
  ('G', 0.02015),
  ('H', 0.06094),
  ('I', 0.06966),
  ('J', 0.00153),
  ('K', 0.00772),
  ('L', 0.04025),
  ('M', 0.02406),
  ('N', 0.06749),
  ('O', 0.07507),
  ('P', 0.01929),
  ('Q', 0.00095),
  ('R', 0.05987),
  ('S', 0.06327),
  ('T', 0.09056),
  ('U', 0.02758),
  ('V', 0.00978),
  ('W', 0.02360),
  ('X', 0.00150),
  ('Y', 0.01974),
  ('Z', 0.00074),]


#given a large string of stuff, return substrings
def find_substr(largestr, size):
  total_length = len(largestr)
  return [largestr[i:i+size] for i in range(total_length) if i+size<=total_length]

#shift character in a clockwise fashion.
def doshifts(achar, shift):
  shiftedchar = ord(achar)+shift

  #loop back cases
  if shiftedchar < ord('A'):
    shiftedchar = ord('Z') - (ord('A') - shiftedchar) + 1

  if shiftedchar > ord('Z'):
    shiftedchar = ord('A') + (shiftedchar - ord('Z')) - 1

  #return the char after shifting.
  return chr(shiftedchar)
  
#look at the list of substrings and measure distance between the similar elements.
def find_dist(substrings):
  distances = []         #keep distances in a tuple of substring,distance pairs.
  length = len(substrings)
  for i in range(length):
    for x in range(length):
      if substrings[i] == substrings[x] and i != x and i-x > 0:
        distances.append((substrings[i], i-x))
  return distances            

#Find the characters that appear with the most frequency.  
#Compare against wiki's eng frequency.
#Assuming plaintext is in English.  Look for characters that have similar
#                                          (least different) frequencies.
#Make a guess at the integer amount to shift by. 
def guess_shift(tryshift_chars):
  count = Counter(tryshift_chars)
  unknowns = [u for u in string.uppercase if u not in count]
  for u in unknowns: count[u] = 0
  total_chars = 0.0

  for u,c in count.most_common():total_chars += c
  # Find smallest differences btwn current and expected freqs
  differences = defaultdict(int)
  # Shift all the things.
  for r in range(len(eng_frq)):
    for u,f in eng_frq:
      shifted = doshifts(u, r)
      differences[r] += abs(f - count[shifted]/total_chars) 
  # The smallest difference is most likely the shift value
  smallest_dif = 0
  #iterate over the diff dict's pairs to find the smallest.
  for s,d in differences.iteritems():               
    if differences[s] < differences[smallest_dif]:
      smallest_dif = s
      #print(s)                      
  return smallest_dif

#performing the actual vigenere shift on a given ciphertext
#and a given amount to shift per char in key to get plain.
def vigenere(text, shift_col_amount):
  key_len = len(shift_col_amount)
  text = text.upper()
  vig_chars = []            #grab all the shifted vig shifted 
  for i in range(len(text)):
    shiftedchar = doshifts(text[i], -shift_col_amount[i%key_len])
    vig_chars.append(shiftedchar)
  return ''.join(vig_chars) #return the deciphered string!

#looks at the distances and mods until the given range is reached,
#counting when distance%modrange = 0.
#the counts are stored in a defaultdict counter.
def modcounter(distances, modrange):
  counts = defaultdict(int)
  for i in range(2, modrange):
    for n in distances:
      if n%i == 0:
        counts[i] += 1
  return counts

#main
def main():
  cipher_text = raw_input('input: \n')     #take in the cipher text from raw_input.
  substrings = find_substr(cipher_text, 4) #choose substrings (change if needed.)
                                     # --2 yields gibberish, 3 works and 4 confirms.
  distances = find_dist(substrings) #find distances between substrings
  #write counts...
  counts = modcounter(zip(*distances)[1], 25) #zip aggregates the tuples. 
                                              #(range can be changed if needed.)
  counts = [x for x in counts.iteritems()]
  counts.sort(key=lambda x: -x[1])            #key length sorted by most likely
  
  key_size = counts[0][0]                     #use most likely key for computation.
  print 'keylen:'                             # (will change manually if need)
  print (key_size)
  shift_col_amount = []                           #init values to shift.
  #shift_col_amount corresponds to the letter of the alphabet to shift (key)
  for i in range(key_size):
    tryshift_chars = [cipher_text[x] for x in range(len(cipher_text)) if x%key_size==i] 
    #do the even-randoms-would-have-similarities bit.....
    shift_col_amount.append(guess_shift(tryshift_chars))
    print(shift_col_amount)

  decrypted_text = vigenere(cipher_text, shift_col_amount)
  print('likely key: ')
  print(''.join([doshifts('A', c) for c in shift_col_amount])) #key as string
  print('output: ')
  print(decrypted_text)

#end 

# Call main
if __name__ == '__main__':
  main()

