def encrypt_caesar(plaintext, shift):
    ciphertext = ""

    for letter in plaintext:
        if letter >= "A" and letter <= "Z":
            cryptLetterOrd = ord("A")
        elif letter >= "a" and letter <= "z":
            cryptLetterOrd = ord("a")
        else:
            ciphertext += letter
            continue

        cryptLetterOrd += (ord(letter) - firstLetterOrd + shift) % 26
        ciphertext += chr(cryptLetterOrd)

    return ciphertext


def decrypt_caesar(ciphertext, shift):
    plaintext = ""

    for cryptLetter in ciphertext:
        if cryptLetter >= "A" and cryptLetter <= "Z":
            encryptLetterOrd = ord("Z")
        elif cryptLetter >= "a" and cryptLetter <= "z":
            encryptLetterOrd = ord("z")
        else:
            plaintext += cryptLetter
            continue

        encryptLetterOrd -= (lastLetterOrd - ord(cryptLetter) + shift) % 26
        plaintext += chr(encryptLetterOrd)

    return plaintext
