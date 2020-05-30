import argparse
import csv
import os
import random
import sys


debug = False


def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
	if debug:
		debug_hook(exception_type, exception, traceback)
	else:
		print(f'{exception_type.__name__}: {exception}')


sys.excepthook = exception_handler


class Model:

	def __init__(self):
		self.dict_ = {}
		self.output = None
		self.prefixes = []

	def gen_txt(self, max_len, num):
		output = open(self.output, 'w')

		for i in range(num):
			# Get a prefix, x, from the list of prefixes, where P(x) = occurrences of x / `len(prefixes)`.
			prefix = text = self.prefixes[random.randrange(len(self.prefixes))]

			# Add suffixes to the text until either the maximum length is reached or the prefix no longer matches any
			# key in the dictionary. Compute a new prefix each time a suffix is added.
			for j in range(text.count(' ') + 1, max_len):
				try:
					suffixes = self.dict_[prefix]  # Raises `KeyError` if `prefix` doesn't match any key.
					suffix = suffixes[random.randrange(len(suffixes))]  # Raises `ValueError` if `suffixes` is empty.
				except (KeyError, ValueError):
					break

				text += ' ' + suffix

				# Compute a new prefix.
				try:
					prefix = prefix[prefix.index(' ') + 1:] + ' ' + suffix
				except ValueError:
					prefix = suffix

			output.write(text + '\n')

		output.close()

	def train(self, file_, key_len):
		name = os.path.splitext(os.path.basename(file_))
		self.output = name[0] + '_output.txt'
		ext = name[1]

		if not (ext == '.csv' or ext == '.txt'):
			raise IOError(f'{ext} is not supported. Please use .csv or .txt.')

		with open(file_) as file:
			if ext == '.csv':
				lines = [' '.join(line[0].split()).rsplit(' ') for line in csv.reader(file)]
			elif ext == '.txt':
				lines = [' '.join(line.split()).rsplit(' ') for line in file]

		for line in [line for line in lines if len(line) >= key_len]:
			# Slide along the line, storing the first `key_len` words as a key and the following word as a value in the
			# dictionary.
			for i in range(len(line) - (key_len - 1)):
				key = line[i]
				for j in range(i + 1, i + key_len):
					key += ' ' + line[j]

				try:
					self.dict_.setdefault(key, []).append(line[i + key_len])
				except IndexError:
					self.dict_.setdefault(key, [])

				# Add the key to the list of prefixes if it is the line's prefix.
				if i == 0:
					self.prefixes.append(key)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	parser.add_argument(
		'-k',
		'--key_len',
		default=2,
		help='the order of the Markov chain - the number of past states each state depends upon. Default = 2',
		nargs='?',
		type=int
	)
	parser.add_argument(
		'-m',
		'--max_len',
		default=50,
		help='the maximum length of each generated message, in words. Default = 50',
		nargs='?',
		type=int
	)
	parser.add_argument(
		'-n',
		'--num',
		default=1000,
		help='the number of messages to generate. Default = 1000',
		nargs='?',
		type=int
	)

	args = parser.parse_args()

	if not args.key_len > 0:
		raise ValueError('`key_len` must be a positive integer.')
	if not args.max_len > 0:
		raise ValueError('`max_len` must be a positive integer.')
	if not args.num > 0:
		raise ValueError('`num` must be a positive integer.')

	model = Model()
	model.train(args.file, args.key_len)
	model.gen_txt(args.max_len, args.num)
