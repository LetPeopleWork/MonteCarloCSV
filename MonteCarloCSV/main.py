import argparse
from datetime import datetime, timedelta
import os

from .MonteCarloService import MonteCarloService
from .CsvService import CsvService

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--FileName", default="")
    parser.add_argument("--Delimiter", default=None)
    parser.add_argument("--Delimeter", default=";")   # For backwards compatibility because I didn't know how to spell this :-)
    parser.add_argument("--ClosedDateColumn", default="Closed Date")
    parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
    parser.add_argument("--TargetDate", default="")
    parser.add_argument("--TargetDateFormat", default="%d.%m.%Y")
    parser.add_argument("--RemainingItems", default="10")
    parser.add_argument("--History", default="30")
    parser.add_argument("--Today", default=None)
    parser.add_argument("--SaveCharts", default=False, action=argparse.BooleanOptionalAction)

    return parser.parse_args()

def get_closed_items_history(csv_service, monte_carlo_service, file_name, delimiter, closed_date_column, date_format):    
    work_items = csv_service.get_closed_items(file_name, delimiter, closed_date_column, date_format)
    closed_items_history = monte_carlo_service.create_closed_items_history(work_items)
    return closed_items_history

def print_logo():
    logo = r"""
     /$$                 /$$           /$$$$$$$                           /$$                /$$      /$$                  /$$      
    | $$                | $$          | $$__  $$                         | $$               | $$  /$ | $$                 | $$      
    | $$       /$$$$$$ /$$$$$$        | $$  \ $$/$$$$$$  /$$$$$$  /$$$$$$| $$ /$$$$$$       | $$ /$$$| $$ /$$$$$$  /$$$$$$| $$   /$$
    | $$      /$$__  $|_  $$_/        | $$$$$$$/$$__  $$/$$__  $$/$$__  $| $$/$$__  $$      | $$/$$ $$ $$/$$__  $$/$$__  $| $$  /$$/
    | $$     | $$$$$$$$ | $$          | $$____| $$$$$$$| $$  \ $| $$  \ $| $| $$$$$$$$      | $$$$_  $$$| $$  \ $| $$  \__| $$$$$$/ 
    | $$     | $$_____/ | $$ /$$      | $$    | $$_____| $$  | $| $$  | $| $| $$_____/      | $$$/ \  $$| $$  | $| $$     | $$_  $$ 
    | $$$$$$$|  $$$$$$$ |  $$$$/      | $$    |  $$$$$$|  $$$$$$| $$$$$$$| $|  $$$$$$$      | $$/   \  $|  $$$$$$| $$     | $$ \  $$
    |________/\_______/  \___/        |__/     \_______/\______/| $$____/|__/\_______/      |__/     \__/\______/|__/     |__/  \__/
                                                                | $$                                                                
                                                                | $$                                                                
                                                                |__/                                                                
    """
    print(logo)

def check_if_file_exists(file_path, raise_if_not_found = False):
    if not os.path.isfile(file_path):
        if raise_if_not_found:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
        return False
    
    return True

def main():    
    try:
        args = parse_arguments()
        
        file_name = args.FileName
        
        today = args.Today
        if today is None:
            today = datetime.now().date()
            print("No custom date specified - using today ({0}) as end date".format(today))
        else:
            today = datetime.strptime(args.Today, "%Y-%m-%d").date()
            print("Custom Date for Today specified - using {0} as end date".format(today))
        
        history = try_parse_int(args.History)
        if history:
            print("Use rolling history of the last {0} days".format(history))
        else:
            history_start = datetime.strptime(args.History, "%Y-%m-%d").date()
            history = (today - history_start).days
            print("Using history with fixed start date {0} - History is {1} days".format(history_start, history))
        
        # Use the proper spelling if anything is defined. If not, we either use the old wrong spelling or we take the default (as it wasn't defined at all)
        delimiter = args.Delimiter if args.Delimiter else args.Delimeter
        closed_date_column = args.ClosedDateColumn
        date_format = args.DateFormat    
        
        remaining_items = int(args.RemainingItems)
        
        target_date = (today + timedelta(days=14))
        
        if args.TargetDate:        
            target_date = datetime.strptime(args.TargetDate, args.TargetDateFormat).date()
    
        csv_service = CsvService()
        monte_carlo_service = MonteCarloService(history, today, args.SaveCharts)

        print_logo()
        
        package_name = "montecarlocsv"
        current_version = version(package_name)
        
        print("================================================================")
        print("Starting {0}@{1} with following Parameters".format(package_name, current_version))
        print("================================================================")  
        print("FileName: {0}".format(file_name))
        print("Delimiter: {0}".format(delimiter))
        print("ClosedDateColumn: {0}".format(closed_date_column))
        print("DateFormat: {0}".format(date_format))
        print("TargetDate: {0}".format(target_date))
        print("History: {0}".format(history))        
        print("Today: {0}".format(today))        
        print("Save Charts: {0}".format(args.SaveCharts))
        print("----------------------------------------------------------------")
                
        if file_name == '':
            print("No csv file specified - generating example file with random values")
            file_name = os.path.join(os.getcwd(), "ExampleFile.csv")
            if not check_if_file_exists(file_name):
                csv_service.write_example_file(file_name, delimiter, closed_date_column, history, date_format, today)
            

        closed_items_history = get_closed_items_history(csv_service, monte_carlo_service, file_name, delimiter, closed_date_column, date_format)        
        if len(closed_items_history) < 1:
            print("No closed items - skipping prediction")
            exit()

        ## Run How Many Predictions via Monte Carlo Simulation for our specified target date
        predictions_howmany_50 = predictions_howmany_70 = predictions_howmany_85 = predictions_howmany_95 = 0
        if target_date:
            (predictions_howmany_50, predictions_howmany_70, predictions_howmany_85, predictions_howmany_95) = monte_carlo_service.how_many(target_date, closed_items_history)       


        ## Run When Predictions via Monte Carlo Simulation - only possible if we have specified how many items are remaining
        predictions_when_50 = predictions_when_70 = predictions_when_85 = predictions_when_95 = datetime.today()
        predictions_targetdate_likelyhood = None

        if remaining_items > 0:
            (predictions_when_50, predictions_when_70, predictions_when_85, predictions_when_95, predictions_targetdate_likelyhood) = monte_carlo_service.when(remaining_items, closed_items_history, target_date)

            
        print("================================================================")
        print("Summary")
        print("================================================================")

        print("How many items will be done by {0}:".format(target_date))
        print("50%: {0}".format(predictions_howmany_50))
        print("70%: {0}".format(predictions_howmany_70))
        print("85%: {0}".format(predictions_howmany_85))
        print("95%: {0}".format(predictions_howmany_95))
        print("----------------------------------------")

        if remaining_items != 0:
            print("When will {0} items be done:".format(remaining_items))
            print("50%: {0}".format(predictions_when_50.strftime(args.TargetDateFormat)))
            print("70%: {0}".format(predictions_when_70.strftime(args.TargetDateFormat)))
            print("85%: {0}".format(predictions_when_85.strftime(args.TargetDateFormat)))
            print("95%: {0}".format(predictions_when_95.strftime(args.TargetDateFormat)))
            print("----------------------------------------")
            print("Chance of finishing the {0} remaining items till {1}: {2}%".format(remaining_items, target_date, predictions_targetdate_likelyhood))
            
            
        print()
        
        print("================================================================")
        print("MonteCarloCSV is deprecated and will not receive any further updates.")
        print("Please consider using FlowPulse which supports CSV files as well as Jira and Azure DevOps.")
        print("You can find more details at https://letpeople.work#flowpulse")
        print("================================================================")
        
    except Exception as exception:
        print("Error while executing montecarloscsv:")
        print(exception)
        
        print("🪲 If the problem cannot be solved, consider opening an issue on GitHub: https://github.com/LetPeopleWork/MonteCarloCSV/issues 🪲")

def try_parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None



if __name__ == "__main__":    
    main()