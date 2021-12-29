import os
import argparse

import pandas as pd
from pandas.core.frame import DataFrame
import re

import genanki
from genanki import builtin_models # standard models proposed by genanki

parser = argparse.ArgumentParser(description='convert a CSV to Anki flashcards')
parser.add_argument('--gui', action='store_true', default=False,
                    help='whether to open a gui to select the file')
parser.add_argument('file', metavar='F', type=str, nargs='?', default='test',
                    help='the path of the file to be converted')
parser.add_argument('deckname', metavar='N', type=str, nargs='?', default='new_deck',
                    help='the name of the flashcard deck')

args = parser.parse_args()

if args.gui == True:
  from tkinter import Tk 
  from tkinter.filedialog import askopenfilename

  Tk().withdraw()
  filepath = askopenfilename()
  input_file = os.path.join(filepath)
  output_file = str(os.path.join(filepath[:-4]+'.apkg'))
else:
  input_path = os.path.join('data','input')
  output_path = os.path.join('data','output')
  try: os.mkdir(output_path) 
  except OSError as error: pass  

  filename = args.file

  input_file = os.path.join(input_path,filename+'.csv')
  output_file = str(os.path.join(output_path, filename+'.apkg'))

## Load file
print('File:', input_file)

colnames=['Q','A','R']
df = pd.read_csv(input_file, index_col=False, names=colnames)

## Create deck
deckname = args.deckname
new_deck = genanki.Deck(
  2059400110,
  deckname)

print('Deck:', deckname)

## Create cards
for i in df.index:
    q,a,r = str(df['Q'][i]), str(df['A'][i]), bool(df['R'][i])
    if a == 'nan':
      model=builtin_models.CLOZE_MODEL
      fields=[q]
    elif r == True:
        model=builtin_models.BASIC_AND_REVERSED_CARD_MODEL
        fields=[q,a]
    else:
        model=builtin_models.BASIC_MODEL
        fields=[q,a]
      
    new_note = genanki.Note(
    model=model,
    fields=fields)
    new_deck.add_note(new_note)

print('-----Card Example:-----')
print(DataFrame({'field':['Front:','Back:','Reverse:','Type:'], 'value':[q,a,r,model.name]}).to_string(index=False,header=False))
print('-----------------------')

## Write file
genanki.Package(new_deck).write_to_file(output_file, None)

print('Conversion completed!')
