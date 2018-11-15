# C1: Dot-n-dash

- Category: Programming
- URL: <https://squarectf.com/2018/dot-n-dash.html>

## Description

The instructions to disable C1 were considered restricted. As a result, they were stored only in encoded form.

The code to decode the instructions was regrettably lost due to cosmic radiation. However, the encoder survived.

Can you still decode the instructions to disable C1?

note: all the files we provide are compressed using `jar`. You should be able to decompress them on a command line (e.g. `jar xf dot-n-dash.jar`) or using a graphical decompression tool.

Your browser may warn you that "this type of file can harm your computer" because jar files typically contain Java code.

## JavaScript

Upon extracting the contents of the `.jar` file, we find a HTML file along with a single-line `instructions.txt` file that we have to decode.

The `_encode` function performs an encoding of an input string to a dot-n-dash format, which we will have to decode, since the implementation of `_decode` is empty:

```js
// Everything below this line was lost due to cosmis radiation. The engineer who knows
// where the backups are stored already left.
function _decode(input) {
  return '';
}
```

## Reversing the encoding

We can extract all of the relevant encoding to a separate JavaScript file and execute it with `node`, so that it's easier to manipulate input using the terminal.

We see that the encoding happens in 3 stages:

### 1. Encode charCode to binary bits

```js
let a = [];
for (let i = 0; i < input.length; i++) {
  let t = input.charCodeAt(i);
  for (let j = 0; j < 8; j++) {
    // if t >> j is odd
    if ((t >> j) & 1) {
      a.push(1 + j + (input.length - 1 - i) * 8);
    }
  }
}
```

After some head-scratching, we can see that the above code chunk encodes a single character from its ASCII value to a series of integers from 1 + (0 to 7 (modulo 8)).

An example would be clearer. With `A` with ASCII value 65 in decimal, we can generate a list of bitwise shifts for 0 to 7:

- 65 >> 0 = 65
- 65 >> 1 = 32
- 65 >> 2 = 16
- 65 >> 3 = 8
- 65 >> 4 = 4
- 65 >> 5 = 2
- 65 >> 6 = 1
- 65 >> 7 = 0

In essence, this encodes the binary digits of 65 where if `t >> j`, then the bit is `1`:

```
0100 0001

7654 3210
-x-- ---x   <-- `x` if t >> j is odd, `-` otherwise
```

We can ensure that this encoding is always reversible, since we are encoding both the value of the character, as well as its position (through `(input.length - 1 - i) * 8`).

### 2. Shuffle positions

```js
let b = [];
while (a.length) {
  const rand = Math.random();
  let t = (rand * a.length) | 0; // round down
  b.push(a[t]);
  a = a.slice(0, t).concat(a.slice(t + 1)); // remove a[t] from a
}
```

The next section essentially shuffles the position of the resultant encoded "bits". Since we have previously encoded the positions as well, we will have no problem restoring them to the correct positions later.

### 3. Convert values to dashes

```js
let r = '';
while (b.length) {
  let t = b.pop();
  r = r + '-'.repeat(t) + '.';
}
```

We can see that the number of dashes corresponds to the encoded value, and is delimited by dots.

## Decoding

With all that in mind, we simply have to perform the reverse process of encoding to obtain the decoded message. We can generate a reverse lookup table for each character by simply performing encoding every ASCII character.

While writing our decoder, we can pass in known plaintexts to be encoded, and check that it is being decoded as expected. The `exploit.js` script can help us to debug our code, like this:

```sh
node exploit.js encode < input.txt | node exploit.js decode
```

## Flag

```sh
$ cat instructions.txt | node encode.js decode
Instructions to disable C1:1. Open the control panel in building INM035.2. Hit the off switch.Congrats, you solved C1! The flag is flag-bd38908e375c643d03c6.
```
