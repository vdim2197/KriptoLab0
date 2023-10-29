#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Varga Dávid
SUNet: vdim2197

Replace this with a description of the program.
"""
import utils

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    encrypted_text = ""
    for character in plaintext:
        if character.isalpha():
            if ord(character) <= 87:
                new_character = chr(ord(character) + 3)
            else:
                new_character = chr(ord(character) - 26 + 3)
                print(ord(character) - 26 + 3)
            encrypted_text += new_character
        else:
            encrypted_text += character

    return encrypted_text
    #raise NotImplementedError  # Your implementation here


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    #raise NotImplementedError  # Your implementation here
    decrypted_text = ""
    for character in ciphertext:
        if character.isalpha():
            if ord(character) >= 68:
                new_character = chr(ord(character) - 3)
            else:
                new_character = chr(ord(character) + 26 - 3)
            decrypted_text += new_character
        else:
            decrypted_text += character

    return decrypted_text


# Vigenere Cipher

def creating_same_length_key(plaintext, keyword):
    same_length_key = ""
    length_text = len(plaintext)
    i = 0
    j = 0
    while i < length_text:
        j = 0
        while j < len(keyword) and i < length_text:
            same_length_key += keyword[j]
            j += 1
            i += 1
    return same_length_key

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    #raise NotImplementedError  # Your implementation here
    same_length_key = creating_same_length_key(plaintext, keyword)
    encrypted_text = ""
    for character_text,character_key in zip(plaintext, same_length_key):
        new_character = chr((ord(character_text) - 65 + ord(character_key) - 65) % 26 + 65)
        encrypted_text += new_character

    return encrypted_text



def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    #raise NotImplementedError  # Your implementation here
    same_length_key = creating_same_length_key(ciphertext, keyword)
    encrypted_text = ""
    for character_text,character_key in zip(ciphertext, same_length_key):
        decrypted_char = chr((ord(character_text) - ord(character_key) + 26) % 26 + 65)
        encrypted_text += decrypted_char

    return encrypted_text




# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

# Scytale Cipher
def fill_the_gap(plaintext, circumference):

    while(len(plaintext) % circumference != 0):
        plaintext += "_"

    return plaintext

def eliminate_the_gap(decrypted):
    newDecrypted = ""
    i = 0
    while decrypted[i] != "_":
        newDecrypted += decrypted[i]
        i = i + 1
    return newDecrypted

def encrypt_scytale(plaintext, circumference):

    #raise NotImplementedError  # Your implementation here
    plaintext = fill_the_gap(plaintext, circumference)
    encrypted = ""
    for i in range(circumference):
        j = i
        while j < len(plaintext):
            encrypted += plaintext[j]
            j = j + circumference

    return encrypted

def decrypt_scytale(ciphertext, circumference):

    steps = int(len(ciphertext)/circumference)
    decrypted = ""
    for i in range(steps):
        j = i
        while j < len(ciphertext):
            decrypted += ciphertext[j]
            j = j + steps
    return eliminate_the_gap(decrypted)

    #raise NotImplementedError  # Your implementation here