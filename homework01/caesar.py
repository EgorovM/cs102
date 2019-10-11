def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    for letter in plaintext:
        if letter >= "A" and letter <= "Z":
            crypt_letterOrd = ord("A")
        elif letter >= "a" and letter <= "z":
            crypt_letterOrd = ord("a")
        else:
            ciphertext += letter
            continue

        crypt_letterOrd += (ord(letter) - crypt_letterOrd + 3) % 26
        ciphertext += chr(crypt_letterOrd)

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    for cryptLetter in ciphertext:
        if cryptLetter >= "A" and cryptLetter <= "Z":
            encrypt_letterOrd = ord("Z")
        elif cryptLetter >= "a" and cryptLetter <= "z":
            encrypt_letterOrd = ord("z")
        else:
            plaintext += cryptLetter
            continue

        encrypt_letterOrd -= (encrypt_letterOrd - ord(cryptLetter) + 3) % 26
        plaintext += chr(encrypt_letterOrd)

    return plaintext
