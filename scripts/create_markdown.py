# coding=utf-8

import sys  # reading command line arguments
import csv
from datetime import date
import locale
from distutils.util import strtobool
import os

from pathlib import Path

if len(sys.argv) <= 1:
  print("No city given, Stopping script.")
  quit()
else:
  city = sys.argv[1]
  # FIXME: not nice but it works: https://stackoverflow.com/questions/7974849/how-can-i-make-one-python-file-run-another
  os.system(f"python scripts/generate_plots.py {city}")
  print("Plots are generated")
  print("Generating markdown page for " + sys.argv[1])
  try:
    Path("hugo/content/kommunen/template.md").read_text()
  except:
    print("hugo/content/kommunen/template.md not found (or error in file). Quitting")
    quit()

with open('data/meta.csv', newline='') as csvfile:
  csv_reader = csv.DictReader(csvfile)
  for row in csv_reader:
    if row['city_machine'] == city:
      city_machine = row['city_machine']
      city_human = row['city_human']
      contact_name = row['contact_name']
      contact_mail = row['contact_mail']
      data_source = row['data_source']
      modules_exist = strtobool(row['modules'])
      break;

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
today = date.today().strftime("%d. %B %Y")

template = Path("hugo/content/kommunen/template.md").read_text()
new_text = template.replace("KOMMUNE_HUMAN", city_human)
new_text = new_text.replace("KOMMUNE_MACHINE", city_machine)

if (modules_exist):
  new_text = new_text.replace("MODULE", "## Umsetzung Klimaschtzkonzept\nTODO: HIER MUSS NOCH MANUELL EIN TEXT ZU DEM FOLGENDEN PLOT ERGÄNZT WERDEN! {{< modules_" + city_machine + ">}}")
else:
  new_text = new_text.replace("MODULE", "")

new_text = new_text.replace("KONTAKTNAME", contact_name)
new_text = new_text.replace("KONTAKTEMAILUMGEKEHRT", contact_mail[::-1]) # [::-1] reverses the string (spam protection; it's reversed back for humans)
new_text = new_text.replace("DATENQUELLE", data_source)
new_text = new_text.replace("AKTUELLESDATUM", today)
new_text = new_text.replace("true", "false")
new_file = Path(f"hugo/content/kommunen/{city_machine}.md")
new_file.write_text(new_text)

hugoconfigfile = Path("hugo/config.toml")
updated_config = hugoconfigfile.read_text().replace("#NEUEKOMMUNE", f'     [[params.klimawatch.kommunen]]\n        name = "{city_human}"\n        slug = "{city_machine}"\n#NEUEKOMMUNE')
hugoconfigfile.write_text(updated_config)

print("---------------------------------------------------------------")
print(f"Markdown file is generated. Now run 'hugo server' in the hugo directory, proof-read at 'localhost:1313' and correct any errors in the file 'hugo/content/kommunen/{city_machine}.md")
print("If everything looks good, create a merge request with the following files:")
print(f"  hugo/config.toml")
print(f"  hugo/content/kommunen/{city_machine}.md")
print(f"  hugo/data/you_draw_it_{city_machine}.json")
print(f"  hugo/layouts/shortcodes/paris_{city_machine}.html")
if (modules_exist):
  print(f"  hugo/layouts/shortcodes/modules_{city_machine}.html")
print(f"  data/{city_machine}.csv")

