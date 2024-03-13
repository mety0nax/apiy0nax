import random
import string
import argparse

arg_parser = argparse.ArgumentParser(
  prog = 'Key Generator',
  description = 'General Purpouse Key Generator'
)

arg_parser.add_argument(
  '--keyN', type = int, metavar = '', required = True,
  help = 'Amount of Keys to Generate'
)

arg_parser.add_argument(
  '--keyL', type = int, metavar = '', required = True,
  help = 'Length of One Key'
)

arg_parser.add_argument(
  '--file', type = str, metavar = '', required = True,
  help = 'File Where to Save Generated Keys'
)

cmdl_args = arg_parser.parse_args( )
symbols = ''.join([
  string.ascii_lowercase,
  string.ascii_uppercase,
  string.digits,
])

keys = [ ''.join([random.choice(symbols) for y in range(cmdl_args.keyL)]) for x in range(cmdl_args.keyN) ]
with open(cmdl_args.file, 'w') as f:
  for k in keys:
    f.write(k + '\n')
print(f'{cmdl_args.keyN} Keys Were Generated')