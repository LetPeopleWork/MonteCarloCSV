# Monte Carlo CSV
![CI Workflow](https://github.com/letpeoplework/montecarlocsv/actions/workflows/publish.yml/badge.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/montecarlocsv)

This python package allows you to run a Monte Carlo Simulation (MCS) based on any csv file. It can be run offline, and all it needs is a csv file with the dates of the closure of the items. Our hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of MC Simulations.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of MC comes when applied continuously. You can use this for free, hope it helps.

This tool is provided for free by [LetPeopleWork](https://letpeople.work). If you are curious about Flow Metrics, Kanban, #NoEstimates etc., feel free to reach out to us and [book a call](https://calendly.com/letpeoplework/)!

## Wiki
You might have questions on how to use this. Please ask via the [Discussion](https://github.com/huserben/MonteCarloCSV/discussions) tab. However, you might want to check out the [Wiki](https://github.com/LetPeopleWork/MonteCarloCSV/wiki) first.
There we have an [FAQ](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/FAQ), so maybe your question was already answered.

On top, we do have some tutorials on how to create the CSV file with different work management systems. Right now we have one for [Azure DevOps](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Azure-DevOps) and [Jira](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Jira).
If you are using another one, we're looking for [Contributors](https://github.com/LetPeopleWork/MonteCarloCSV#contributions).

## Installation
Make sure you have python 3.9 or higher installed on your system and it's available via your PATH variable. You can check this by running `python --version` on your terminal. If it works without error, you have python installed and ready. If not, you can download it from the [official Python Website](https://www.python.org/downloads/).

**Important:** It can be that you have to use `python3 --version`. If this is the case, please use always `python3` instead of `python` in the following commands.

Once you have made sure python is installed, you can download `montecarlocsv` via pip:
`python -m pip install --upgrade montecarlocsv`

## Run montecarlocsv
If your installation was successfull, you can now run `montecarlocsv` via the commandline. When not supplied with any parameters (see below for details), it will use the default values and generate an `ExampleFile.csv` with dummy values to your current directory. Based on this, the MCS will be run and you should see the output in your commandline that looks something like this:

```
================================================================
Starting montecarlocsv with following Parameters
================================================================
FileName:
Delimiter: ;
ClosedDateColumn: Closed Date
DateFormat: %m/%d/%Y %I:%M:%S %p
TargetDate: 2024-06-23
History: 30
Save Charts: False
----------------------------------------------------------------
No csv file specified - generating example file with random values
Writing Example File with random values to C:\Users\benja\Downloads\montecarlocsvtest\ExampleFile.csv
Loading Items from CSV File: 'C:\Users\benja\Downloads\montecarlocsvtest\ExampleFile.csv'. Column Name 'Closed Date' and Date Format '%m/%d/%Y %I:%M:%S %p'
Found 30 Items in the CSV
Getting items that were done in the last 30 days...
Found 30 items that were closed in the last 30 days
--------------------------------
Running Monte Carlo Simulation - How Many items will be done till 2024-06-23
--------------------------------
50 Percentile: 13 Items
70 Percentile: 12 Items
85 Percentile: 10 Items
95 Percentile: 9 Items
--------------------------------
Running Monte Carlo Simulation - When will 10 items be done
--------------------------------
14 days to target date
50 Percentile: 10 days - Predicted Date: 2024-06-19
70 Percentile: 12 days - Predicted Date: 2024-06-21
85 Percentile: 14 days - Predicted Date: 2024-06-23
95 Percentile: 16 days - Predicted Date: 2024-06-25
Chance of hitting target date: 90.42
================================================================
Summary
================================================================
How many items will be done by 2024-06-23:
50%: 13
70%: 12
85%: 10
95%: 9
----------------------------------------
When will 10 items be done:
50%: 2024-06-19
70%: 2024-06-21
85%: 2024-06-23
95%: 2024-06-25
----------------------------------------
Chance of finishing the 10 remaining items till 2024-06-23: 90.42%



🛈 Want to learn more about how all of this works? Check out out website! 🛈
🔗 https://letpeople.work 🔗
```
You can now start to tweak the input parameters and replace the csv file according to your needs.
**Note**: It's recommended to name your csv files to something more meaningful (like *TeamName.csv*) and to specify this when running the tool: `montecarlocsv --FileName "TeamName.csv"`.

Read on to see details about how to configure `montecarlocsv`.

## "How Many" and "When"
To run the MC Simulations with `montecarlocsv`, you need various inputs. First and foremost, you need to provide a csv file that includes the date when an item was closed. The csv can contain other information, but it's not needed nor relevant for the MC Simulation. Then we need a target date to calculate *how many* items we manage till this date based on the past throughput. We can also calculate *when* a specific amount of items will be done. If we have both a target date and the remaining items we want to achieve till this date, we can also calculate the likelihood of managing those items till the target date.
To specify "how much history" should be used: Do you want to use the last 30 days or rather the last 90 days for your calculation?

## Parameters
You can specify several arguments to adjust `montecarlocsv` according to your needs. Below you find a table with the parameters, their description and the default values that are used when nothing else is supplied:

```
parser.add_argument("--FileName", default='ExampleFile.csv')
parser.add_argument("--ClosedDateColumn", default="Closed Date")
parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
parser.add_argument("--TargetDate", default="08.04.2024")
parser.add_argument("--TargetDateFormat", default="%d.%m.%Y")
parser.add_argument("--RemainingItems", default=78)
parser.add_argument("--History", default="90")
```
Name | Description | Default |
--- | --- | --- |
--FileName | The name of the csv file to be used for the simulation. Can be a relative path (using '.') or an absolute one | Empty. If nothing is provided, an example file is autogenerated with the name "ExampleFile.csv" that is matching all default parameters. You can overwrite other parameters and leave *FileName* empty, then the auto-generated file will take the other parameters into account. |
--Delimiter | The delimiter that is used in the file specified. | Default is ; |
--ClosedDateColumn | The name of the column in the csv file that contains the closed date. | Default is "Closed Date" |
--DateFormat | The format of the date in the csv file. Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) | Default is "%m/%d/%Y %I:%M:%S %p" |
--TargetDate | The target date for the simulation. It might be obvious, but that date should be in the future | If no Target Date is specified, it will take 14 days in the future |
--TargetDateFormat | The format of the target date. Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) | Default is "%d.%m.%Y" |
--RemainingItems | The number of remaining items for the simulation. | Default is 10 |
--History | The number of days of history to be used for the simulation. | Default is 30 |
--SaveCharts | If specified, the charts created during the MC Simulation will be stored in a subfolder called "Charts". | Default is False |

# Usage of montecarlocsv in other python scripts
We want to keep this project about running MCS with a CSV input. That said, it might make a lot of sense to directly integrate with your work tracking systems without the need for a CSV export. If you want to reuse `montecarlocsv` in your own python scripts, you can do so in two ways described below.

## Call with sys args
You can simply invoke the whole program and specify the parameters to use, by using `sys.argv`. You can find an example in the following file in the *Examples* folder: [call_via_sys.py](https://github.com/LetPeopleWork/MonteCarloCSV/blob/main/Examples/call_via_sys.py)

## Use Individual Services
If you don't want to call the full application, you can also call the different services.
In [use_individual_services.py](https://github.com/LetPeopleWork/MonteCarloCSV/blob/main/Examples/use_individual_services.py) in the *Examples* folder you can see how this could look like.

Using the [CsvService](https://github.com/LetPeopleWork/MonteCarloCSV/blob/main/MonteCarloCSV/CsvService.py) we first get a list of all our closed items. Then we generate the throughput history via the [MonteCarloService](https://github.com/LetPeopleWork/MonteCarloCSV/blob/main/MonteCarloCSV/MonteCarloService.py).

With this history, we then can run a  *When* and *How Many* simulation.

# Contributions
We're happy if you want to contribute. The following ways of contribution are possible:
- Do you have an idea for an additional feature? Share it with us in the [Discussions](https://github.com/huserben/MonteCarloCSV/discussions)
- Want to improve the code or extend the functionality? Feel free to create a Pull Request. However, please make sure to check first in the discussion if the feature is needed & wanted. We want to keep this generic and not make it overcomplicated, so we might intentionally leave some things out that you would get in other, full-blown SaaS tools.
- Contribute to our [Wiki](https://github.com/huserben/MonteCarloCSV/wiki) by sharing how-to's for your work tracking system or asking (or answering) frequently asked questions.
- If you have forked this repo and adjusted it to work directly with your work tracking system, why not keep that open-source and share it here, so we can link it.
