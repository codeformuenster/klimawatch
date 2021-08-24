# coding=utf-8

#import json  # writing json
#import os  # possibility to delete files
#import sys  # reading command line arguments
#import textwrap  # wrapping long lines

#import numpy as np  # make it easier with numeric values
import csv
from datetime import date
#import plotly.graph_objects as go  # plots
#from scipy.stats import linregress  # for computing the trend


from pathlib import Path

city = "bonn"

with open('data/meta.csv', newline='') as csvfile:
  csv_reader = csv.DictReader(csvfile)
  for row in csv_reader:
    if row['city_machine'] == city:
      city_human = row['city_human']
      contact_name = row['contact_name']
      contact_mail = row['contact_mail']
      data_source = row['data_source']
      break;

today = date.today().strftime("%d. %B %Y")

template = Path("hugo/content/kommunen/template.md").read_text()
new_text = template.replace("KOMMUNE", city_human)
new_text = new_text.replace("KONTAKTNAME", contact_name)
new_text = new_text.replace("KONTAKTEMAIL", contact_mail)
new_text = new_text.replace("DATENQUELLE", data_source)
new_text = new_text.replace("AKTUELLESDATUM", today)
new_text = new_text.replace("true", "false")
new_file = Path(f"hugo/content/kommunen/{city}.md")
new_file.write_text(new_text)
