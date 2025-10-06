
# Tasks 2025-10-04

First, list out all of the functions that I want to convert from Javascript to python

Majority of it will be just JSON Functions and some other utilities

all input will be based on using file based input, meaning we store it in a text file, preferably, tmp.txt and then execute it

The output will be console.log, so that we may pipe it to another command
Otherwise we may add an argument, so that it will generate an output text file

Should we modify in place? I think this will be better

Convert Logs into Test Cases

## Features

- [x] Join Lines
- [x] Make into Array
- [x] Make into JSON
- [x] Get JSON Key and Value
- [x] Epoch ISO Converter
- [x] Convert JSON to YAML
- [x] Convert JSON to CSV
- [x] Convert JSON to SQL
  - [x] Convert to Insert Statement
  - [x] Convert to Update Statement
  - [x] Convert to Select Statement
- [ ] JSON Comments Parser
- [ ] Function to Sort Both List via Column Specific Key
  - [ ] First Input will be Function Keys, in the preferred Order
  - [ ] Second will be a CSV

- [x] Grep Lines
  - [x] `grep -E 'birthday' datakit.txt | sed -E 's/.*"birthday": "(.*)"/\1/'`

## 2025-10-06

- [ ] Add Class For Conversion
  - [ ] Forward and Backward Conversion

## What I want

I want to make all of this into IDE agnostic, so that I won't be stuck using vscode all the time

What does a text editor for me needs?

1. Ability to run code snippets
2. Ability to run tasks.json, meaning I have a shortcut to execute all the command I want
3. Ability to execute code command into terminal
4. Ability to copy terminal command back into buffer

## Thought Process III

Come up with a catalog of commonly used variable Names, so that I may reference to
Also clear up my phone storage

## Thoughts Process II

List all Functions Available
Execute Command Function

## Thought Process

What am I Stuck at? How do I make a CLI Program??

Think of some sample CLI Commands

`python snip.py -m join_lines`

`python snip.py -m join_lines -i input.txt -o gay.txt`
