package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string
	var minusOrd int
	var shift int
	var cryptLetter_ord int

	ciphertext = ""

	keyword_ind := 0

	for ind := 0; ind < len(plaintext); ind++{
		if keyword[keyword_ind] >= 'A' && keyword[keyword_ind] <= 'Z'{
			minusOrd = 'A'
		}else{
			minusOrd = 'a'
		}

		shift = int(keyword[keyword_ind]) - minusOrd
		letter := plaintext[ind]

		if letter >= 'A' && letter <= 'Z'{
			cryptLetter_ord = 'A'
		}else if(letter >= 'a' && letter <= 'z'){
			cryptLetter_ord = 'a'
		}else{
			ciphertext += string(letter)
			continue
		}

		cryptLetter_ord += (int(letter) - cryptLetter_ord + shift) % 26
		ciphertext += string(cryptLetter_ord)
		keyword_ind = (keyword_ind + 1) % len(keyword)
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string
	var minusOrd int
	var shift int
	var encryptLetter_ord int

	plaintext = ""
	keyword_ind := 0
	
	for i := 0; i < len(ciphertext); i++{
		if keyword[keyword_ind] >= 'A' && keyword[keyword_ind] <= 'Z'{
			minusOrd = 'A'
		}else{
			minusOrd = 'a'
		}

		shift = int(keyword[keyword_ind]) - minusOrd
		cryptLetter := ciphertext[i]

		if cryptLetter >= 'A' && cryptLetter <= 'Z'{
			encryptLetter_ord = 'Z'
		}else if (cryptLetter >= 'a' && cryptLetter <= 'z'){
			encryptLetter_ord = 'z'
		}else{
			plaintext += string(cryptLetter)
			continue
		}

		encryptLetter_ord -= (encryptLetter_ord - int(cryptLetter) + shift) % 26
		plaintext += string(encryptLetter_ord)

		keyword_ind = (keyword_ind + 1) % len(keyword)

	}

	return plaintext
}
