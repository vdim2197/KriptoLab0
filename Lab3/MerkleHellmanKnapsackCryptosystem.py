import random
import numpy as np
import utils


def coprime(m, n):
    c = 0
    for i in range(1, m + 1):
        if m % i == 0:
            for j in range(1, n+1):
                if n % j == 0:
                    if i == j:
                        c = c + 1
    if c == 1:
        return True
    return False


def create_bit_list(n, characters):
    powers_of_two = []
    bits = np.zeros(n)
    element = 1
    for i in range(n):
        powers_of_two.append(element)
        element *= 2

    bits_list = []
    for character in characters:
        number_for_character = character
        powers_of_two.reverse()

        i = 0
        while number_for_character > 0:
            if number_for_character >= powers_of_two[i]:
                number_for_character -= powers_of_two[i]
                bits[i] = 1
            else:
                bits[i] = 0
            i += 1

        bits_list.extend(bits)

    return bits_list


def key_generation():
    beta, w, q, r = generate_key_components()
    public_key = beta
    private_key = w
    private_key.append(q)
    private_key.append(r)
    return public_key, private_key


def generate_key_components():
    n = 8
    w, total = generate_superincreasing_sequence(n)
    q = random.randint(total+1, 2*total)
    ok = 0
    r = random.randint(2, q-1)
    while coprime(q, r) is False:
        r = random.randint(2, q-1)
    beta = []
    for element in w:
        beta.append((r * element) % q)
    return beta, w, q, r


def generate_superincreasing_sequence(n):
    w = []
    first_element = random.randint(2, 10)
    total = first_element
    w.append(first_element)
    for i in range(1, n):
        new_element = random.randint(total + 1, 2 * total)
        w.append(new_element)
        total += new_element
    return w, total


def encrypt_mh(message, public_key):
    chunk_size = len(public_key)
    encrypted_message = []

    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        print(bytearray"a")
        print("a")
        encrypted_chunk = sum(a * b for a, b in zip(create_bit_list(8, chunk), public_key))
        encrypted_message.append(encrypted_chunk)

    return encrypted_message


def byte_to_bits(byte):
    """Convert a byte to a list of its 8 bits."""
    return [(byte >> i) & 1 for i in range(7, -1, -1)]

def string_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return [int(bit) for bit in binary_message]


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - (a // b) * y


def modinv(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise ValueError("The modular inverse does not exist")
    return x % m


def decrypt_mh(ciphertext, private_key):
    w = private_key[0:(len(private_key)-2)]
    q = private_key[len(private_key)-2]
    r = private_key[len(private_key)-1]

    s = modinv(r, q)

    c_prime = (ciphertext * s) % q

    alpha = []

    for w_i in reversed(w):
        if w_i <= c_prime:
            alpha.insert(0, 1)
            c_prime -= w_i
        else:
            alpha.insert(0, 0)

    return alpha


public_key, private_key = key_generation()
message = "vhjdsfvjshadvfhjsvdhjfvjhasdvjfhvjhgsdvfj"
binary_message = string_to_binary(message)
encrypted_message = encrypt_mh(binary_message, public_key)
print(encrypted_message)

decrypted_message = decrypt_mh(encrypted_message[0], private_key)
print(decrypted_message)
