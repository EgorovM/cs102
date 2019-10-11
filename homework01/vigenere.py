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
            cryptLetterOrd = ord("A")
        elif letter >= "a" and letter <= "z":
            cryptLetterOrd = ord("a")
        else:
            ciphertext += letter
            continue

        cryptLetterOrd += (ord(letter) - cryptLetterOrd + shift) % 26
        ciphertext += chr(cryptLetterOrd)

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
            encryptLetterOrd = ord("Z")
        elif cryptLetter >= "a" and cryptLetter <= "z":
            encryptLetterOrd = ord("z")
        else:
            plaintext += cryptLetter
            continue

        encryptLetterOrd -= (encryptLetterOrd - ord(cryptLetter) + shift) % 26
        plaintext += chr(encryptLetterOrd)

        keyword_ind = (keyword_ind + 1) % len(keyword)

    return plaintext
