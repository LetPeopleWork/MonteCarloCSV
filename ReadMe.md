# Monte Carlo CSV
This is a script that runs an MC Simulation based on any csv file. It can be run offline, and all it needs is a csv file with the dates of the closure of the items. My hope is that this will allow organizations that don't want to rely on any SaaS products or third party tools to still harness the power of MC Simulations.
Feel free to check out the code, propose improvements and also make it your own by adjusting it to your context and potentially integrating it into some kind of pipeline of yours. The true power of MC comes when applied continuously. You can use this for free, hope it helps.

If you like it and use the script, I'm happy if I can mention you/your company in the readme or for an attribution on [LinkedIn](https://www.linkedin.com/in/huserben/).

## Wiki
You might have questions on how to use this. Please ask (you can use the [Discussion](https://github.com/huserben/MonteCarloCSV/discussions) tab to ask us. However, you might want to check out the [Wiki](https://github.com/LetPeopleWork/MonteCarloCSV/wiki) first.
There we have an [FAQ](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/FAQ), so maybe your question was already answered.

On top, we do have some tutorials on how to create the CSV file with different work management systems. Right now we have one for [Azure DevOps](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Azure-DevOps) and [Jira](https://github.com/LetPeopleWork/MonteCarloCSV/wiki/Jira).
If you are using another one, we're looking for [Contributors](https://github.com/LetPeopleWork/MonteCarloCSV#contributions).

## Download Files
In order to run the scripts, you need to download all the files in this repository. There are dependencies between the files so you cannot just download a single file. Please always use the full folder structure.

## Install Prerequisites
Make sure you have python 3.x installed on your system and it's available via your PATH variable. You can check this by running `python --version` on your terminal. If it works without error, you have python installed and ready. If not, you can download it from the [official Python Website](https://www.python.org/downloads/).

**Important:** It can be that you have to use `python3 --version`. If this is the case, please use always `python3` instead of `python` in the following commands.

Once you have made sure python is installed, you can fetch the required python packages:
Run `python -m pip install -r .\requirements.txt` from the directory that contains the scripts.

**Important:** If you are on Linux or MacOS, the paths work differently. Use "/" instead of "\" for all the commands that follow. So the above command would look like this for MacOS/Linux:
`python -m pip install -r ./requirements.txt`

## Run Monte Carlo (MC) Simulations
To run the MC Simulations with this script, you need various inputs. First and foremost, you need to provide a csv file that includes the date when an item was closed. The csv can contain other information, but it's not needed nor relevant for the MC Simulation. Then we need a target date to calculate *how many* items we manage till this date based on the past throughput. We can also calculate *when* a specific amount of items will be done. If we have both a target date and the remaining items we want to achieve till this date, we can also calculate the likelihood of managing those items till the target date.
To specify "how much history" should be used: Do you want to use the last 30 days or rather the last 90 days for your calculation?

### Run using the example values
The repo comes with an example configuration including an example csv file.
Simply run `python .\MonteCarlo.py` to run the forecasts. This will use the Throughput provided from *ExampleFile.csv* and run the Monte Carlo Simulation using the last 90 days. It will calculate how many items be done till 08.04.2024 and assumes there are 78 items pending.

## Configuration Options
In `MonteCarlo.py` the following default values are defined:

```
parser.add_argument("--FileName", default='ExampleFile.csv')
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
--FileName | The name of the csv file to be used for the simulation. Default is 'ExampleFile.csv'. Can be a relative path (using '.') or an absolute one |
--Delimeter | The delimeter that is used in the file specified. Default is ; |
--ClosedDateColumn | The name of the column in the csv file that contains the closed date. Default is "Closed Date". |
--DateFormat | The format of the date in the csv file. Default is "%m/%d/%Y %I:%M:%S %p". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--TargetDate | The target date for the simulation. Default is "08.04.2024". It might be obvious, but that date should be in the future |
--TargetDateFormat | The format of the target date. Default is "%d.%m.%Y". Check [Python Dates](https://www.w3schools.com/python/python_datetime.asp) for the options you have (or ask ChatGPT) |
--RemainingItems | The number of remaining items for the simulation. Default is 78. |
--History | The number of days of history to be used for the simulation. Default is "90". |
--SaveCharts | If specified, the charts created during the MC Simulation will be stored in a subfolder called "Charts". |

# Direct Integration into Work Tracking Systems
We want to keep this project about running MCS with a CSV input. That said, it might make a lot of sense to directly integrate with your work tracking systems without the need for a CSV export. Following is a list of where this was done. You might still want to gain some experience using the CSV, but feel free to check out the other repositories:
- [AzureDevOpsFlowScripts](https://github.com/LetPeopleWork/AzureDevOpsFlowScripts)

# Contributions
We're happy if you want to contribute. The following ways of contribution are possible:
- Do you have an idea for an additional feature? Share it with us in the [Discussions](https://github.com/huserben/MonteCarloCSV/discussions)
- Want to improve the code or extend the functionality? Feel free to create a Pull Request. However, please make sure to check first in the discussion if the feature is needed & wanted. We want to keep this generic and not make it overcomplicated, so we might intentionally leave some things out that you would get in other, full-blown SaaS tools.
- Contribute to our [Wiki](https://github.com/huserben/MonteCarloCSV/wiki) by sharing how-to's for your work tracking system or asking (or answering) frequently asked questions.
- If you have forked this repo and adjusted it to work directly with your work tracking system, why not keep that open-source and share it here, so we can link it.
