# Monte Carlo CSV
This is a script that runs an MC Simulation based on any csv file. It can be run offline, and all it needs is a csv file with the dates of the closure of the items. My hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of MC Simulations.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of MC comes when applied continuously. You can use this for free, hope it helps.

If you like it and use the script, I'm happy if I can mention you/your company in the readme or for an attribution on [LinkedIn](https://www.linkedin.com/in/huserben/).

## Download Files
In order to run the scripts, you need to download all the files in this repository. There are dependencies between the files so you cannot just download a single file. Please always use the full folder structure.

## Install Prerequisites
Make sure you have python 3.x installed on your system and it's available via your PATH variable.

Then run `python -m pip install -r .\requirements.txt` from this directory to install the packages.

## Run Monte Carlo (MC) Simulations
To run the MC Simulations with this script, you need various inputs. First and foremost, you need to provide a csv file that includes the date when an item was closed. The csv can contain other information, but it's not needed nor relevant for the MC Simulation. Then we need a target date to calculate *how many* items we manage till this date based on the past throughput. We can also calculate *when* a specific amount of items will be done. If we have both a target date and the remaining items we want to achieve till this date, we can also calculate the likelihood of managing those items till the target date.
To specify "how much history" should be used: Do you want to use the last 30 days or rather the last 90 days for your calculation?

### Run using the example values
The repo comes with an example configuration including an example csv file.
Simply run `python .\MonteCarlo.py` to run the forecasts. This will use the Throughput provided from *ExampleFile.csv* and run the Monte Carlo Simulation using the last 90 days. It will calculate how many items be done till 08.04.2024 and assumes there are 78 items pending.

## Configuration Options
In `MonteCarlo.py` the following default values are defined:

```
parser.add_argument("--FileName", default=".\\ExampleFile.csv")
parser.add_argument("--ClosedDateColumn", default="Closed Date")
parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
parser.add_argument("--TargetDate", default="08.04.2024")
parser.add_argument("--TargetDateFormat", default="%d.%m.%Y")
parser.add_argument("--RemainingItems", default=78)
parser.add_argument("--History", default="90")
```

You can overwrite them either by changing the python file or by supplying specific options via command line: `python .\MonteCarlo.py --History 30`
I would recommend to change the values that don't change often (for example the file name) in code, while for others like Target Date or History to supply them via command line, so you can easily rerun it with different configurations.

### Arguments
Name | Description |
--- | --- |
--FileName | The name of the csv file to be used for the simulation. Default is ".\\ExampleFile.csv". Can be a relative path (using '.') or an absolute one |
--ClosedDateColumn | The name of the column in the csv file that contains the closed date. Default is "Closed Date". |
--DateFormat | The format of the date in the csv file. Default is "%m/%d/%Y %I:%M:%S %p". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--TargetDate | The target date for the simulation. Default is "08.04.2024". It might be obvious, but that date should be in the future |
--TargetDateFormat | The format of the target date. Default is "%d.%m.%Y". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--RemainingItems | The number of remaining items for the simulation. Default is 78. |
--History | The number of days of history to be used for the simulation. Default is "90". |