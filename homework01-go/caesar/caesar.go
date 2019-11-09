package caesar

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string
	var firstLetter int

	for ind := 0; ind < len(plaintext); ind++{
		if plaintext[ind] >= 'a' && plaintext[ind] <= 'z'{
			firstLetter = 'a'
		}else if plaintext[ind] >= 'A' && plaintext[ind] <= 'Z'{
			firstLetter = 'A'
		}else{
			ciphertext = ciphertext + string(plaintext[ind])
			continue
		}

		ciphertext = ciphertext + string(firstLetter + (int(plaintext[ind]) - firstLetter + 3) % 26)
	}

	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string
	var lastLetter int

	for ind := 0; ind < len(ciphertext); ind++{
		if ciphertext[ind] >= 'a' && ciphertext[ind] <= 'z'{
			lastLetter = 'z'
		}else if ciphertext[ind] >= 'A' && ciphertext[ind] <= 'Z'{
			lastLetter = 'Z'
		}else{
			plaintext = plaintext + string(ciphertext[ind])
			continue
		}

		plaintext = plaintext + string(lastLetter - (lastLetter - int(ciphertext[ind]) + 3) % 26)
	}

	return plaintext
}
