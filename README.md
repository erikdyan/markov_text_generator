# Markov Text Generator
Python script that uses a Markov chain to generate text.
## Installation
Clone this repository:
```
$ git clone https://github.com/erikdyan/markov_text_generator.git
```
## Usage
Run the script from the command line:
```
$ python3 generate_text.py [-k [KEY_LEN]] [-m [MAX_LEN]] [-n [NUM]] file
```
With no optional flags set, this script will use a second order Markov chain trained on the contents of the specified file to generate 1000 messages, each with a maximum length of 50 words. The messages will be written to `<file>_output.txt`, with one message stored on each line.
### Optional Flags
* `-k [KEY_LEN], --key_len [KEY_LEN]`: the order of the Markov chain - the number of past states each state depends upon. Smaller orders will generate more random text, whereas larger orders will generate text that more closely resembles the training data. Default = 2
* `-m [MAX_LEN], --max_len [MAX_LEN]`: the maximum length of each generated message, in words. Default = 50
* `-n [NUM], --num [NUM]`: the number of messages to generate. Default = 1000
