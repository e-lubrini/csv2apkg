import genanki
import sys
import os
import pandas as pd

program_name = sys.argv[0]
arguments = sys.argv[1:]
filename=arguments[0]
# optional deck name (if none, filename is used)
deck_name=arguments[-1]

input_path = os.path.join('data','input')
output_path = os.path.join('data','output')
try: 
    os.mkdir(output_path) 
except OSError as error: 
    pass  

input_file = os.path.join(input_path,filename+'.csv')
output_file = str(os.path.join(output_path, filename+'.apkg'))

my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

new_deck = genanki.Deck(
  2059400110,
  deck_name)

colnames=['Q','A']
df = pd.read_csv(input_file, names=colnames)

for i in df.index:
    q,a = df['Q'][i], df['A'][i]
    new_note = genanki.Note(
    model=my_model,
    fields=[str(q),str(a)])
    new_deck.add_note(new_note)

genanki.Package(new_deck).write_to_file(output_file, None)