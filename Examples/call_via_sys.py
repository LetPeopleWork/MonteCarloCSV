import sys
from MonteCarloCSV.main import main

config_file_path = 'ExampleConfig.json'

sys.argv = ['montecarlocsv', '--Delimiter', ',', '--DateFormat', '%d.%m.%Y', '--RemainingItems', '15']

main()