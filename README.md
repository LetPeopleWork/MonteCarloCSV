# Monte Carlo CSV
![CI Workflow](https://github.com/letpeoplework/montecarlocsv/actions/workflows/publish.yml/badge.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/montecarlocsv)

## Introduction

This python package allows you to run a Monte Carlo Simulation (MCS) offline using a standard csv file as an input. Using this tool, any organisation can harness the power of MCS without relying on SaaS products or third-party tools.

Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into your pipeline. The true power of MCS comes when applied continuously. This tool is provided for free by [LetPeopleWork](https://letpeople.work). If you are curious about Flow Metrics, Kanban, #NoEstimates etc., feel free to reach out to us and [book a call](https://calendly.com/letpeoplework/)!

## Getting Started
To get started, follow the steps in **Installation** below.

For more information, check out our [Wiki](https://github.com/LetPeopleWork/MonteCarloCSV/wiki) and our [FAQ](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/FAQ).

If you have any further questions about using this tool, feel free to ask them in the [Discussion](https://github.com/huserben/MonteCarloCSV/discussions) tab.

## Installation
In order to run this tool, you will need python v3.9 at minimum on your machine.

### Installing python
1. To download python, please visit https://www.python.org/downloads/.
2. Install python on your machine.
3. Add python to your `PATH` variable.

Check if you have successfully installed python by entering `python --version` or `python3 --version` in your terminal window. If one of these commands works without error, you are ready to install MCS.

### Installing MCS

If you have installed python, you can download `montecarlocsv` via `pip` using the following terminal command:

`python -m pip install --upgrade montecarlocsv`

To test whether your installation is successful, run `montecarlocsv` in a terminal using the command line.

## Running montecarlocsv
When `montecarlocsv` is run without any parameters, it will use preset values and generate an `ExampleFile.csv` with dummy data to your current directory. 

**Note:** If you edit `ExampleFile.csv`, the application will take your data into account.

The application will use this `.csv` file as an input and runs a Monte Carlo simulation with an output similar to the one below:

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

If you can see an output like this, you are now ready to configure `montecarlocsv` and use the tool with your own data.

## Configuring MCS
To run Monte Carlo Simulations effectively, you need to provide a list of dates when your team completed work items. This data is to be provided in a `.csv` format. For more information, see the **Configuring the Done Data** section

There are three types of forecasts you can run with this application:

- To understand *how many* items could be completed until a deadline, you will need to specify a target date.
- To understand *when* a specific number of items could be completed by, you will need to specify the number of items to be resolved.
- To understand the probabilities of completing a specific number of items by a given deadline, you will need to specify both the target date and the number of items to be resolved.

For more information, see the **Configuring the Forecast** section.


### Configuring the Done Data
You need to provide a `.csv` file that includes the dates when items were closed. This file can contain other information as well but it will be disregarded when using `montecarlocsv`.

A sample input `.csv` file looks like the following:

```
Issue key,Summary,Resolved
TEAM-224,Issue summary,21/03/2024
TEAM-341,User story title,12/08/2024
TEAM-201,Bug 3,13/08/2024
TEAM-394,Task 5,13/08/2024
TEAM-84,Request 10,13/08/2024
TEAM-95,Task 7,14/08/2024
TEAM-408,Story10,14/08/2024
```

In the example above, the first two columns separated by comma (`,`) will be ignored, only the Done dates will be used by `montecarlocsv`.

We have created a tutorial to explain how to create the input `.csv` file using [Azure DevOps](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Azure-DevOps) and [Jira](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Jira). If you use a different work management system and have a way to export the CSV file as an input for MCS, reach out to us -- we're looking for [Contributors](https://github.com/LetPeopleWork/MonteCarloCSV#contributions).

There are multiple parameters you can use to customise the input `.csv` files. The parameters are as below:

Name | Description | Default | Notes |
--- | --- | --- | --- | 
`--FileName` | Name of the `.csv` file to be used for forecasting. File name can contain absolute or relative path (using `.`) | Empty. | For more information, see **Running montecarlocsv**. **Note**: It's recommended to give a descriptive name for your `.csv` files, such as *TeamName.csv* and use it as a parameter: `montecarlocsv --FileName "TeamName.csv"`.  |
`--Delimiter` | Delimiter used to separate values in the input `.csv` file. | `;` |
`--ClosedDateColumn` | Name of the column in the `.csv` file containing the dates when work items were closed. | `Closed Date` |
`--DateFormat` | Date format used for the `--ClosedDateColumn` parameter in the `.csv` file. Use [Python Dates](https://www.w3schools.com/python/python_datetime.asp) to specify the format you want to use (or ask ChatGPT). | "%m/%d/%Y %I:%M:%S %p" |
`--History` | How much "history" should be used for the simulation. Can be a fixed value to use a "rolling window" of the specified number of days. Or a date in the format "YYYY-MM-dd" (2024-08-19), then all data starting from the specified date will be included. | `30` | If this parameter isnot provided, delivery data older than 30 days will be disregarded.

### Configuring the Forecast

You can use the following parameters to configure the forecasts `montecarlocsv` is going to give you.

Name | Description | Default | Notes |
--- | --- | --- | --- | 
`--TargetDate` | Target date for the simulation. | `14` | If no `--TargetDate` is specified, `montecarlocsv` will use 14 days.
`--TargetDateFormat` | Date format used to specify the target date. Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) | "%d.%m.%Y" |
`--RemainingItems` | The number of items remaining in the Product Backlog for the simulation. | `10` |
`--SaveCharts` | Specifies whether to save charts with the forecast or not. If set to `true`, charts will be stored in the "Charts" subfolder. | `False` |

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
