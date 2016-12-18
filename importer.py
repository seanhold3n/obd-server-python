import db
import glob
import json
import os
from psycopg2 import IntegrityError

path = ''

files_count = 0
readings_count = 0
err_count = 0

# For each JSON file...
for filename in glob.glob(os.path.join(path, '*.json')):

    files_count += 1

    with open(filename) as f:
        # Read data
        data_str = f.read()

        # Replace 'vin' with 'vehicleid' (column names)
        data_str = data_str.replace("\"vin\":", "\"vehicleid\":")

        # Now load the modified string as a JSON document
        data = json.loads(data_str)

        # For each JSON element...
        for element in data:

            readings_count += 1

            try:
                db.put(element)
            except IntegrityError:
                err_count += 1
                db.getConn().rollback()
            except Exception, e:
                print "Error on element {}".format(element)
                raise e

print "Processed {} readings across {} files with {} errors.".format(readings_count, files_count, err_count)
