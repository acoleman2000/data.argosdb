import json, csv
import argparse
import jsonschema
from jsonschema import validate
import sys
__version__ = "1.1.0"
__status__ = "Production"

def usr_args():
    """
    functional arguments for process
    https://stackoverflow.com/questions/27529610/call-function-based-on-argparse
    """

    parser = argparse.ArgumentParser()

    # set usages options
    parser = argparse.ArgumentParser(
        prog='argosdb',
        usage='%(prog)s [options]')

    # version
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + __version__)

    parser.add_argument('-c', '--csv',
                                help="CSV file to create.")

    parser.add_argument('-s', '--schema',
                                required=True,
                                # type = argparse.FileType('r'),
                                help="Root json schema to parse")

    # Print usage message if no args are supplied.
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    options = parser.parse_args()
    return options

def get_schema(options):
    """
        This function loads the given schema available
    """
    with open(options.schema, 'r') as file:
        schema = json.load(file)
    return schema

def make_csv(options, schema): 
    """
        make csv
    """
    if options.csv: 
        csv_file = options.csv
    else: 
        csv_file = 'test.csv'
    csv_columns = ['property', '$id', 'title', 'description', 'type', 'default', 'examples', 'pattern', 'required']
    required = schema['required']
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for key in schema['properties']:
            row = [key]
            for item in schema['properties'][key]:
                row.append(schema['properties'][key][item])
            if row[0] in required:
                row.append('required')
            else: 
                row.append('optional')
            writer.writerow(row)


def main():
    """
    Main function
    """

    options = usr_args()
    schema = get_schema(options)
    make_csv(options, schema)

#______________________________________________________________________________#
if __name__ == "__main__":
    main()