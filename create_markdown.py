# coding=utf-8

import sys  # reading command line arguments
import csv
from datetime import date
from distutils.util import strtobool

from pathlib import Path

if len(sys.argv) <= 1:
    print("No city given, Stopping script.")
    quit()
else:
    print("Plotting data for " + sys.argv[1])
    city = sys.argv[1]
    try:
        Path("hugo/content/kommunen/template.md").read_text()
        Path(f"data/{city}_data_source.md").read_text()
    except:
        print(
            f"File data/{city}_data_source.md not found (or error in file). Quitting",
        )
        quit()


with open('data/meta.csv', newline='') as csvfile:
  csv_reader = csv.DictReader(csvfile)
  for row in csv_reader:
    if row['city_machine'] == city:
      city_machine = row['city_machine']
      city_human = row['city_human']
      contact_name = row['contact_name']
      contact_mail = row['contact_mail']
      modules_exist = strtobool(row['modules'])
      break;

today = date.today().strftime("%d. %B %Y")

template = Path("hugo/content/kommunen/template.md").read_text()
new_text = template.replace("KOMMUNE_HUMAN", city_human)
new_text = new_text.replace("KOMMUNE_MACHINE", city_machine)

if (modules_exist):
  try:
    modules_text = Path(f"data/{city_machine}_sachstand_text.md").read_text()
  except:
    print(f"File data/{city_machine}_sachstand_text.md does not exist. It's needed and should contain the text for the modules plot. Quitting")
    quit()
  new_text = new_text.replace("MODULE", modules_text)
else:
  new_text = new_text.replace("MODULE", "")

new_text = new_text.replace("KONTAKTNAME", contact_name)
new_text = new_text.replace("KONTAKTEMAIL", contact_mail)
new_text = new_text.replace("DATENQUELLE", Path(f"data/{city_machine}_data_source.md").read_text())
new_text = new_text.replace("AKTUELLESDATUM", today)
new_text = new_text.replace("true", "false")
new_file = Path(f"hugo/content/kommunen/{city_machine}.md")
new_file.write_text(new_text)
