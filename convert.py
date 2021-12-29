import os
import argparse

import pandas as pd
from pandas.core.frame import DataFrame
import re

import genanki
from genanki import builtin_models # standard models proposed by genanki

parser = argparse.ArgumentParser(description='convert a CSV to Anki flashcards')
parser.add_argument('--gui', action='store_true', default=False,
                    help='whether to open a gui to select the file') # open a GUI dialog to select file
parser.add_argument('file', metavar='F', type=str, nargs='?', default='test',
                    help='the path of the file to be converted')
parser.add_argument('deckname', metavar='N', type=str, nargs='?', default='',
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
if args.deckname=='': # if no deck name was provided by the user, use the name of the file
  deckname=filename
else: deckname = args.deckname

new_deck = genanki.Deck(
  2059400110,
  deckname)

print('Deck:', deckname)

## Create cards
card_counter = 0
for i in df.index: # iterate through lines of the df to define for each card: (1) values of the fields, and (2) model type
    q,a,r = str(df['Q'][i]), str(df['A'][i]), bool(df['R'][i]) # for each line, extract the question, answer, and whether it's a reverse card (True or False)
    if a == 'nan': # if there is no answer, then it's a cloze card
      model=builtin_models.CLOZE_MODEL
      fields=[q]
    elif r == False: # if there is an answer, its a basic card withoue reverse option...
        model=builtin_models.BASIC_MODEL
        fields=[q,a]
    else:
        model=builtin_models.BASIC_AND_REVERSED_CARD_MODEL # ...or a basic card with the reverse card option
        fields=[q,a]

    # create a card with the defined model and fields
    new_note = genanki.Note(
    model=model,
    fields=fields)
    new_deck.add_note(new_note) # add the card to the deck and continue the iteration with the next card
    card_counter += 1

print('-----Card Example:-----')
print(DataFrame({'field':['Front:','Back:','Reverse:','Type:'], 'value':[q,a,r,model.name]}).to_string(index=False,header=False))
print('-----------------------')

## Write file
genanki.Package(new_deck).write_to_file(output_file, None)

print('Conversion completed!\nNumber of cards in the new deck:',card_counter)

