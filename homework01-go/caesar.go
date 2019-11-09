package main

import (
	"fmt"
)

func main() {
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

	fmt.Println(plaintext)
}
