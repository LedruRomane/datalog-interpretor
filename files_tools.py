import argparse

# Import datalog from file
def importFile():
   # Create object ArgumentParser
    parser = argparse.ArgumentParser()

    # Add argument
    parser.add_argument('-f', '--file', help='Fichier à analyser')

    # Analyse arguments from command line
    args = parser.parse_args()

    return args.file

def exportFile(path, content):
    with open(path, 'w') as file:
        file.write(content)