# Generate at_features.py which connects AT features with mile numbers with lat/lon.
# Script to translate the atdb.091015051935.ALL.csv file from www.sophiaknows.com/atdb/waypoints.php 
import csv
with open('./attracker_app/data/atdb.091015051935.ALL.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('./attracker_app/at_features.py', 'w') as pyfile:
        pyfile.write("#Source data for this file comes from atdb.091015051935.ALL.csv from www.sophiaknows.com/atdb/waypoints.php\n")
        pyfile.write("FEATURES = [\n")
        for row in reader:
            if row['lat'] and row['lon'] and (row['type'] != 'TOWN'):
                description = "Mile {0}: {1}: {2}/{3}".format(row['to spgr'], row['name'], row['lat'], row['lon'])
                text = '  {{"mile": {4}, "type": "{0}", "name": "{1}", "lat": {2}, "lon": {3}}},\n'.format( row['type'], description, row['lat'], row['lon'], row['to spgr'] )
                pyfile.write(text)
        pyfile.write("]\n")

