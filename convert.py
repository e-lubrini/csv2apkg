import os

from cached_property import cached_property
from numpy import NaN
#os.system('/bin/bash --rcfile venv/bin/activate')
os.system('source venv/bin/activate')
import genanki
import sys
from genanki import deck, model, builtin_models
import pandas as pd
import re

program_name = sys.argv[0]
arguments = sys.argv[1:]
filename=arguments[0]
# optional deck name (if none, filename is used)
deck_name=arguments[-1]

## TODO add argument convert all

input_path = os.path.join('data','input')
output_path = os.path.join('data','output')
try: 
    os.mkdir(output_path) 
except OSError as error: 
    pass  

input_file = os.path.join(input_path,filename+'.csv')
if not os.path.isfile(input_file):
  input_file = os.path.join(input_path,'Anki - '+filename+'.csv')
print(input_file)

output_file = str(os.path.join(output_path, filename+'.apkg'))

new_deck = genanki.Deck(
  2059400110,
  deck_name)


## INPUT

colnames=['Q','A','R']
df = pd.read_csv(input_file, index_col=False, names=colnames)

print('Card Example:')
print(df.iloc[0])

for i in df.index:
    q,a,r = str(df['Q'][i]), str(df['A'][i]), str(df['R'][i])
    if a == 'nan':
      model=builtin_models.CLOZE_MODEL
      fields=[q]
      print(type(model))
      print(a,'cloze')
    elif r == True:
        model=builtin_models.BASIC_AND_REVERSED_CARD_MODEL
        fields=[q,a]
        print(type(model))
        print(a,'basic_and_reversed')
    else:
        model=builtin_models.BASIC_MODEL
        fields=[q,a]
        print(type(model))
        print(a,'basic')
      
    new_note = genanki.Note(
    model=model,
    fields=fields)
    new_deck.add_note(new_note)

genanki.Package(new_deck).write_to_file(output_file, None)

print('\nSUCCESS!')
