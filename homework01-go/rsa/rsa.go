package rsa

import (
    "math"
    "math/rand"
    "math/big"
    "errors"
)

type Key struct {
    key int
    n int
}

type KeyPair struct {
    Private Key
    Public Key
}

func isPrime(n int) bool {

    for factor := 2; factor < int(math.Sqrt(float64(n))) + 1; factor++{
        if n % factor == 0{
            return false
        }
    }

    return true
}


func gcd(a int, b int) int {
    // PUT YOUR CODE HERE
    if b == 0{
        return a
    }else{
        return gcd(b, a % b)
    }
}


func multiplicativeInverse(e int, phi int) int {
    var x int

    var history []int

    for e % phi > 0{
        history = append(history, int(e / phi))
        e, phi = phi, e % phi
    }

    x = 0
    y := 1

    for i := len(history)-1; i >= 0; i--{
        prev_x := x
        x = y
        y = prev_x - y * (history[i])
    }

    return x
}


func GenerateKeypair(p int, q int) (KeyPair, error) {
    var n int
    var phi int
    if !isPrime(p) || !isPrime(q) {
        return KeyPair{}, errors.New("Both numbers must be prime.")
    } else if  p == q {
        return KeyPair{}, errors.New("p and q can't be equal.")
    }

    n = p * q
    // PUT YOUR CODE HERE

    phi = (p-1)*(q-1)
    // PUT YOUR CODE HERE

    e := rand.Intn(phi - 1) + 1
    g := gcd(e, phi)

    for g != 1 {
        e = rand.Intn(phi - 1) + 1
        g = gcd(e, phi)
    }

    d := multiplicativeInverse(e, phi)

    return KeyPair{Key{e, n}, Key{d, n}}, nil
}


func Encrypt(pk Key, plaintext string) []int {
    cipher := []int{}
    n := new(big.Int)
    for _, ch := range plaintext {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        cipher = append(cipher, int(n.Int64()))
    }
    return cipher
}


func Decrypt(pk Key, cipher []int) string {
    plaintext := ""
    n := new(big.Int)
    for _, ch := range cipher {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        plaintext += string(rune(int(n.Int64())))
    }
    return plaintext
}
