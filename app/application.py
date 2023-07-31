import json
import csv

# Internal function
# PARAMS: `component` - JSON object as dict, individual entry in `components`
#                       array in SBOM output file
# RETURNS: tuple of 5 strings, data to be written to single row in CSV
def __get_data(component):
    # For each category, return either its value or None if it is nonexistent
    try:
        bomref = component["bom-ref"]
    except:
        bomref = 'None'

    try:
        name = component["name"]
    except:
        name = 'None'

    try:
        hashes = component["hashes"][0]["alg"] + ": " + component["hashes"][0]["content"]
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

    try:
        commit = 'None'
        for prop in component['properties']:
            if prop['name'] == 'last_commit':
                commit = prop['value']
    except:
        commit = 'None'


    return bomref, name, hashes, mimetype, mode, commit

# Internal function
# PARAMS: `bomref` - string, the bom-ref (component ID) of the component to
#                    search for
#         `data` - JSON object as dict, the data that the function is searching
#                  within
# RETURNS: tuple containing information of the component with the bomref in
#          the `bomref` parameter
def __get_dep_data(bomref, data):

    # searching all components for the one that matches the bomref input
    for comp in data['components']:
        # if bomref matches, return name, type, and purl of component
        if comp['bom-ref'] == bomref:
            group = 'None'
            try:
                group = comp['group']
            except:
                group = 'None'
            try:
                hashes = comp["hashes"][0]["alg"] + ": " + comp["hashes"][0]["content"]
            except:
                hashes = 'None'
            return comp['name'], comp['type'], comp['purl'], hashes, group

    # if no bomref matches, check the component in metadata
    if data['metadata']['component']['bom-ref'] == bomref:
        try:
            group = data['metadata']['component']['group']
        except:
            group = 'None'

        try:
            hashes = data['metadata']['component']['hashes'][0]['alg'] + ': ' + data['metadata']['component']['hashes'][0]['alg']
        except:
            hashes = 'None'
        return data['metadata']['component']['name'], data['metadata']['component']['type'], data['metadata']['component']['purl'], hashes, group

    # finally, if nothing is found, return None as strings
    return 'None', 'None', 'None', 'None', 'None'

# Internal function
# PARAMS: `component` - JSON object as dict, individual entry in `components`
#                       array in SBOM output file
# RETURNS: tuple of (bomref, name, author, message, timestamp) about an
#          indivdual entry in `components`
def __get_git_data(component):
    bomref = component['bom-ref']
    name = component['name']
    author = 'None'
    message = 'None'
    timestamp = 'None'
    for property in component['properties']:
        if property['name'] == 'Author':
            author = property['value']
        elif property['name'] == 'Message':
            message = property['value']
        elif property['name'] == 'Timestamp':
            timestamp = property['value']

    return bomref, name, author, message, timestamp

# Internal function
# PARAMS: `sbom` - string, path to SBOM file
# RETURNS: boolean, whether SBOM file is correctly formatted as `CycloneDX`
def __format(sbom):
    f = open(sbom)

    data = json.load(f)

    if data['bomFormat'] == 'CycloneDX':
        return True
    else:
        return False

# PARAMS: `sbom` - string, path to sbom generated by valint
#         `write_file` - string, name of output file (csv format)
# RETURNS: void
def parse_sbom(sbom, write_file, append):
    # opening sbom
   f = open(sbom)

   # parsing json data from sbom into python dict
   data = json.load(f)

   if append == 'none':
       open_mode = 'w'
       write = write_file
   else:
       open_mode = 'a'
       write = append

   # opening `write_file` in write mode
   with open(write, open_mode, newline='') as csv_file:
      # defining cols
      csv_writer = csv.writer(csv_file)

      if open_mode != 'a':
        csv_writer.writerow(['bomref', 'name', 'hash', 'mimetype', 'mode', 'last-commit'])
      # populating each row with entry in components array
      for comp in data['components']:
        if comp['type'] == 'file':
            bomref, name, hashes, mimetype, mode, commit = __get_data(comp)
            csv_writer.writerow([bomref, name, hashes, mimetype, mode, commit])

   f.close()

# PARAMS: `sbom` - string, path to sbom file
# RETURNS: boolean representing whether sbom has dependencies
def dependencies(sbom):
    f = open(sbom)
    data = json.load(f)
    try:
        data['dependencies']
        ret = True
    except:
        ret = False

    return ret

# PARAMS: `sbom` - string, path to sbom generated by valint
#         `write_file` - string, name of output file (csv format)
# RETURNS: void
def parse_dependencies(sbom, write_file, append):
    # open file and load into dictionary
    f = open(sbom)
    data = json.load(f)

    if append == 'none':
       open_mode = 'w'
       write = write_file
    else:
       open_mode = 'a'
       write = append

    # create and open file to write to
    with open(write, open_mode, newline='') as csv_file:
        # writing column names (headers)
        csv_writer = csv.writer(csv_file)

        if open_mode != 'a':
            csv_writer.writerow(['depender-bom-ref', 'depender-name', 'depender-type', 'depender-purl', 'depender-hash', 'depender-group', 'dependee-bom-ref', 'dependee-name', 'dependee-type', 'dependee-purl', 'dependee-hash', 'dependee-group'])

        # search every depender in `dependencies`
        for depender in data['dependencies']:
            depender_bomref = depender['ref']
            # grab name, type, and purl of current depender
            depender_name, depender_type, depender_purl, depender_hash, depender_group = __get_dep_data(depender_bomref, data)

            # search all dependees of current depender
            for dependee in depender['dependsOn']:
                # grab name, type, and purl of current dependee
                dependee_name, dependee_type, dependee_purl, dependee_hash, dependee_group = __get_dep_data(dependee, data)
                # write a row with the current depender and dependee info
                csv_writer.writerow([depender_bomref, depender_name, depender_type, depender_purl, depender_hash, depender_group, dependee, dependee_name, dependee_type, dependee_purl, dependee_hash, dependee_group])

    # closing file
    f.close()

# PARAMS: `sbom` - string, path to SBOM file
#         `write_file` - string, path to desired output file (csv format)
# RETURNS: void
def parse_git_data(sbom, write_file, append):
    # Open and load JSON data
    f = open(sbom)
    data = json.load(f)

    if append == 'none':
       open_mode = 'w'
       write = write_file
    else:
       open_mode = 'a'
       write = append

    # Create file to write to
    with open(write, open_mode, newline='') as csv_file:
        # Initialize CSV writer object
        csv_writer = csv.writer(csv_file)

        if open_mode != 'a':
            # Write header row
            csv_writer.writerow(['bomref', 'type', 'name', 'commit-author', 'commit-message', 'commit-timestamp'])

        # Iterate through every component in the SBOM
        for component in data['components']:
            # Save the type
            type = component['type']

            # If it's a commit, write a row of the following information
            if type == 'commit':
                # Unpack commit info
                bomref, name, author, message, timestamp = __get_git_data(component)

                # Write commit info to file
                csv_writer.writerow([bomref, type, name, author, message, timestamp])

    # Close SBOM
    f.close()
