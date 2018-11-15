# C7: gofuscated

- Category: Reverse

## Description

The very first settlers didn’t have a lot of confidence in their hand-assembled C6 system. They therefore built C7, an advanced defense system written in Golang.

Given the source code, can you find the correct input?

## The Main Idea

It helps if you have prior knowledge about [Google Go Language](https://golang.org/) but most of it should be quite recognizable with decent programming experience.  
The idea is to trace through the code starting from main() and figure out what goes on in each line.  
Thankfully, the code can be edited and run at our convenience and this makes it easier to analyze the code body.  
We should also note that failing any of the code checks would result in a [`panic`](https://gobyexample.com/panic) call.  
This means our goal is to find an `input` that is accepted by the function checks in the code before generating the flag successfully.  
  
To download Go on Debian-based systems like Ubuntu:
```
$ sudo apt-get install golang-go
```

## Code Analysis

Line 168: The code runs with one argument `input`.  
Line 169: panicIfInvalid is a function that checks if `input` is valid using the regex [a-zA-Z0-9]{26}; `input` must be alphanumeric and of length 26.  
Line 172: Generates the flag.  
Line 173: Sets flag content to the variable `h`.  
Line 189: Sets flag content in variable `h` to variable `flag`.  
Line 190: another_helper is another function check that is built from lines 154 to 162.  
Line 195: Flag content is printed out from variable `flag`.  

## My Solution

I first started off with "abc" as my `input`.  
Upon failing the first check at line 169, I discovered the regex check and changed `input` to "abcdefghijklmnopqrstuvwxyz".  
I then received another error on line 190.  
Apparently, my `input` variable was sort of jumbled up (in a deterministic way between lines 182 to 188) before this check was carried out.  
  
Two possible solutions:
- Comment out everything from lines 190 to 194 (the wonders of cient-side codes)  
- Find out the one-to-one mapping (details listed below) and provide a better `input` from the started  
  
Using the first solution, we can retrieve the flag content flag-705787f208e6eff63768ae166482125b.

## Misc. Details

For the one-to-one mapping I mentioned previously, I found out that by line 190 my `input` was "hstqcjvmiozdyanwgrkxpeublf" instead of "abcdefghijklmnopqrstuvwxyz".  
From there, I was able to find the mapping where:
- a -> h`
- b -> s
- c -> t
- and so on...  
  
I eventually mapped it back to "nxelvzqaifsyhojudrbcwgptmk" which would result in "abcdefghijklmnopqrstuvwxyz" by the time it reaches line 190.  
  
The runtime might take a few minutes because generating the flag takes 10000000000 iterations.
It is also not recommended to use online IDEs like [The Go Playground](https://play.golang.org/) because they might cut the program halfway through due to long runtime.