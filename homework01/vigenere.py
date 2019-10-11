def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    keyword_ind = 0

    for letter in plaintext:
        if keyword[keyword_ind] >= "A" and keyword[keyword_ind] <= "Z":
            minusOrd = ord("A")
        else:
            minusOrd = ord("a")

        shift = ord(keyword[keyword_ind]) - minusOrd

        if letter >= "A" and letter <= "Z":
            cryptLetter_ord = ord("A")
        elif letter >= "a" and letter <= "z":
            cryptLetter_ord = ord("a")
        else:
            ciphertext += letter
            continue

        cryptLetter_ord += (ord(letter) - cryptLetter_ord + shift) % 26
        ciphertext += chr(cryptLetter_ord)

        keyword_ind = (keyword_ind + 1) % len(keyword)

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    keyword_ind = 0

    for cryptLetter in ciphertext:
        if keyword[keyword_ind] >= "A" and keyword[keyword_ind] <= "Z":
            minusOrd = ord("A")
        else:
            minusOrd = ord("a")

        shift = ord(keyword[keyword_ind]) - minusOrd

        if cryptLetter >= "A" and cryptLetter <= "Z":
            encryptLetter_ord = ord("Z")
        elif cryptLetter >= "a" and cryptLetter <= "z":
            encryptLetter_ord = ord("z")
        else:
            plaintext += cryptLetter
            continue

        encryptLetter_ord -= (encryptLetter_ord - ord(cryptLetter) + shift) % 26
        plaintext += chr(encryptLetter_ord)

        keyword_ind = (keyword_ind + 1) % len(keyword)

    return plaintext
