# C2: Flipping bits

- Category: Cryptology
- URL: <https://squarectf.com/2018/flipping_bits.html>

## Description

Disabling C2 requires cracking a RSA message. You have two ciphertexts. The public key is (e1, n).

Fortunately (this time), space rabiation caused some bit flibs and the second ciphertext was encrypted with a faulty public key (e2, n). Can you recover the plaintexts?

## Common Modulus Attack

From the given instructions, we are given two separate ciphertexts, two different exponents (albeit with a single bit difference) and a single modulus. It is given that the two public keys used for `ct1` and `ct2` are `(e1, n)` and `(e2, n)` respectively.

On the basis of this alone, we can exploit the weakness using a **Common Modulus Attack**. This [StackExchange post](https://crypto.stackexchange.com/questions/16283/how-to-use-common-modulus-attack) explains it pretty well.

Essentially, since both `e1` and `e2` are coprime (their GCD is 1), we make use of [Bézout's identity](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity), which states that:

> Let _a_ and _b_ be integers with greatest common divisor _d_. Then, there exist integers _x_ and _y_ such that _ax + by = d_. More generally, the integers of the form _ax + by_ are exactly the multiples of _d_.

We can thus write the following:

```
GCD(e1, e2) = 1
=> e1s1 * e2s2 = 1, for some s1, s2 (by Bézout's identity)

c1^s1 * c2^s2 mod N
= (m^e1)^s1 * (m^e2)^s2 mod N
= m^(e1s1+e2s2) mod N
= m mod N
```

As such, by finding some `s1` and `s2` that fulfils the given properties, we can recover the plaintext.

## Exploit

For the exploit, we can write it in Python using [`libnum`](https://github.com/hellman/libnum), a useful package for crypto CTF challenges.

We first find `s1` and `s2` using the [Extended Euclidean Algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm), inverting any negative results as necessary (by modulus). The plaintext `m` can be found by taking `c1^s1 * c2^s2 mod N`, and finally converting the decimal number into a string.

See [`exploit.py`](./exploit.py) for the complete Python script.

## Flag

```sh
$ python exploit.py
flag-54d3db5c1efcd7afa579c37bcb560ae0
```
