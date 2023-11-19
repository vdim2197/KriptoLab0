import random
from sympy import isprime


def steps(card_deck):

    number_of_cards = len(card_deck)
    # Megkeressuk a feher dzsokert
    white_joker_pos = card_deck.index(53)
    if white_joker_pos < number_of_cards-1:  # kicseréljük az alatta levo kártyalappal
        card_deck[white_joker_pos], card_deck[white_joker_pos +
                                              1] = card_deck[white_joker_pos+1], card_deck[white_joker_pos]
    else:  # Ha a fehér dzsóker a pakli legalsó kártyalapja
        for i in range(0, number_of_cards):
            card_deck[white_joker_pos-i] = card_deck[white_joker_pos-i-1]
        card_deck[1] = 53  # akkor beszúrjuk felülrol az elso kártyalap után.

    # Megkeressük a fekete dzsókert
    black_joker_pos = card_deck.index(54)
    if black_joker_pos < number_of_cards-2:  # két kártyalappal lennebb szúrjukbe a pakliba
        card_deck[black_joker_pos], card_deck[black_joker_pos +
                                              1] = card_deck[black_joker_pos+1], card_deck[black_joker_pos]
        card_deck[black_joker_pos+1], card_deck[black_joker_pos +
                                                2] = card_deck[black_joker_pos+2], card_deck[black_joker_pos+1]
    elif black_joker_pos == 53:  # Ha a fekete dzsóker a legalsó kártyalap
        for i in range(0, number_of_cards-3):
            # felülrol a második kártyalap után szúrjuk be
            card_deck[black_joker_pos-i] = card_deck[black_joker_pos-i-1]
        card_deck[2] = 54
    else:  # Ha a fekete dzsóker a pakli alján az utolsó elotti kártyalap
        for i in range(0, number_of_cards-2):
            # legfelso kártyalap alá kerül
            card_deck[black_joker_pos-i] = card_deck[black_joker_pos-i-1]
        card_deck[1] = 54

    # mostantol kezde nem szamit a dzsokerek szine tehat mind a ket dzsoker 53as lesz
    # Cseréljük fel az elso dzsóker elotti kártyalapokat a második dzsóker utáni kártyalapokkal.
    # black_joker_pos = card_deck.index(54)
    # card_deck[black_joker_pos] = 53
    # print(card_deck)

    first_joker_pos = card_deck.index(53)
    # for i in range(first_joker_pos+1, 54):
    #     if card_deck[i] == 53:
    #         second_joker_pos = i
    second_joker_pos = card_deck.index(54)
    first_part = card_deck[0:first_joker_pos]
    middle_part = card_deck[first_joker_pos:second_joker_pos+1]
    last_part = card_deck[second_joker_pos+1:number_of_cards]

    new_card_deck = last_part + middle_part + first_part
    card_deck = new_card_deck
    # print(card_deck)

    # Megnezzuk a legalso kartyalapot
    last_card = card_deck[number_of_cards-1]
    if last_card != 53 or last_card != 54:  # csak akkor modosul ha az utolso kartya nem dzsoker
        first_part = card_deck[0:last_card]
        second_part = card_deck[last_card:number_of_cards]
        # print(first_part)
        # print(second_part)

        new_card_deck = second_part[0:len(
            second_part)-1] + first_part + [last_card]
        card_deck = new_card_deck

    # print(card_deck)
    # Felülrol annyi kártyalapot számlálunk le, amennyi a legfelso kártyalap számértéke
    first_card = card_deck[0]
    if first_card > number_of_cards - 1:
        next_card = card_deck[(first_card % number_of_cards) + 1]
    else:
        next_card = card_deck[first_card]
    # card_deck.remove(next_card)
    return next_card, card_deck


def solitaire(n):
    key = []
    # az egyszeruseg kedveert a feher dzsoker 53 es a fekete 54
    card_deck = list(range(1, 55))
    random.shuffle(card_deck)
    for i in range(0, n):

        key_value, new_deck = steps(card_deck)
        while key_value == 53:  # hogy ha a kulcsfolyam pontosan az egyik dzsoker kartya erteke ujra csinaljuk az egeszet
            key_value, new_deck = steps(card_deck)
        new_deck.remove(key_value)
        card_deck = new_deck
        key.append(key_value)

    return key


def generate_large_prime():
    while True:
        # Generaljunk egy nagy primet
        prime_candidate = random.randrange(5000,10000)

        # Ellenorizzuk, hogy a prim a kivant tulajdonsagokkal rendelkezik-e
        if prime_candidate % 4 == 3 and isprime(prime_candidate):
            return prime_candidate


def blum_blum_shub(numbers):
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    s = random.randrange(1, n)
    x = []
    x.append((s*s)%n)
    z = []
    for i in range(1,numbers):
        x.append((x[i-1] * x[i-1]) % n)
        z.append(x[i] % 2)
    return z


def generate_one_time_key(size):
    key = solitaire(size)
    print(key)
    return key


def stream_encrypt(data, key):
    if len(data) > len(key):
        raise ValueError("Error: the key is to short")

    ciphertext = bytes(x ^ y for x, y in zip(data, key))
    return ciphertext


def stream_decrypt(ciphertext, key):
    if len(ciphertext) > len(key):
        raise ValueError("Ciphertext is longer than the key")

    plaintext = bytes(x ^ y for x, y in zip(ciphertext, key))
    return plaintext


data = b"Az eredeti bytes sorozat."
key_size = len(data)
key = generate_one_time_key(key_size)
encrypted_data = stream_encrypt(data, key)
decrypted_data = stream_decrypt(encrypted_data, key)

print(f"Original data: {data}")
print(f"Key: {key}")
print(f"Encrypted data: {encrypted_data}")
print(f"Decrypted data: {decrypted_data}")

key2 = blum_blum_shub(key_size * 8)
encrypted_data = stream_encrypt(data, key2)
decrypted_data = stream_decrypt(encrypted_data, key2)
print(f"Original data: {data}")
print(f"Key: {key2}")
print(f"Encrypted data: {encrypted_data}")
print(f"Decrypted data: {decrypted_data}")

