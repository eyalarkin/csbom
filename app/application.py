import json
import csv

def get_data(component):
    try:
        bomref = component["bom-ref"]
    except:
        bomref = 'None'

    try:
        name = component["name"]
    except:
        name = 'None'

    try:
        hashes = component["hashes"][0]["content"]
    except:
        hashes = 'None'

    try:
        mimetype = component["mime-type"]
    except:
        mimetype = 'None'

    try:
        mode = component["mode"]
    except:
        mode = 'None'


    return bomref, name, hashes, mode, mimetype


def parse_sbom(sbom, write_file):
    # opening sbom
   f = open(sbom)

   # parsing json data in sbom into python dict
   data = json.load(f)

   # defining file name for csv as 'name-version'
   # write_file = data['metadata']['component']['name'] + '-' + data['metadata']['component']['version'] + '.csv'

   # opening write_file in write mode
   with open(write_file, 'w', newline='') as csv_file:
      # defining cols
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow(['bomref', 'name', 'hash', 'mimetype', 'mode'])
      for comp in data["components"]:

         bomref, name, hashes, mode, mimetype = get_data(comp)
         csv_writer.writerow([bomref, name, hashes, mode, mimetype])

   f.close()

