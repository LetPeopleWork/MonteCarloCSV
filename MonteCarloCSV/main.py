import argparse
from datetime import datetime, timedelta
import os

from .MonteCarloService import MonteCarloService
from .CsvService import CsvService

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--FileName", default="")
    parser.add_argument("--Delimeter", default=";")
    parser.add_argument("--ClosedDateColumn", default="Closed Date")
    parser.add_argument("--DateFormat", default="%m/%d/%Y %I:%M:%S %p")
    parser.add_argument("--TargetDate", default="")
    parser.add_argument("--TargetDateFormat", default="%d.%m.%Y")
    parser.add_argument("--RemainingItems", default="10")
    parser.add_argument("--History", default="30")
    parser.add_argument("--SaveCharts", default=False, action=argparse.BooleanOptionalAction)

    return parser.parse_args()

def get_closed_items_history(csv_service, monte_carlo_service, file_name, delimeter, closed_date_column, date_format):    
    work_items = csv_service.get_closed_items(file_name, delimeter, closed_date_column, date_format)
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
        history = int(args.History)
        delimeter = args.Delimeter
        closed_date_column = args.ClosedDateColumn
        date_format = args.DateFormat    
        
        remaining_items = int(args.RemainingItems)
        
        target_date = (datetime.now() + timedelta(days=14)).date()
        
        if args.TargetDate:        
            target_date = datetime.datetime.strptime(args.TargetDate, args.TargetDateFormat).date()
    
        csv_service = CsvService()
        monte_carlo_service = MonteCarloService(history, args.SaveCharts)

        print_logo()
        
        print("================================================================")
        print("Starting montecarlocsv with following Parameters")
        print("================================================================")  
        print("FileName: {0}".format(file_name))
        print("Delimeter: {0}".format(delimeter))
        print("ClosedDateColumn: {0}".format(closed_date_column))
        print("DateFormat: {0}".format(date_format))
        print("TargetDate: {0}".format(target_date))
        print("History: {0}".format(history))        
        print("Save Charts: {0}".format(args.SaveCharts))
        print("----------------------------------------------------------------")
                
        if file_name == '':
            print("No csv file specified - generating example file with random values")
            file_name = os.path.join(os.getcwd(), "ExampleFile.csv")
            if not check_if_file_exists(file_name):
                csv_service.write_example_file(file_name, delimeter, closed_date_column, history, date_format)
            

        closed_items_history = get_closed_items_history(csv_service, monte_carlo_service, file_name, delimeter, closed_date_column, date_format)        
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
            print("50%: {0}".format(predictions_when_50))
            print("70%: {0}".format(predictions_when_70))
            print("85%: {0}".format(predictions_when_85))
            print("95%: {0}".format(predictions_when_95))
            print("----------------------------------------")
            print("Chance of finishing the {0} remaining items till {1}: {2}%".format(remaining_items, target_date, predictions_targetdate_likelyhood))
            
            
        print()
        print()
        print()
        print("🛈 Want to learn more about how all of this works? Check out out website! 🛈")
        print("🔗 https://letpeople.work 🔗")
        
    except Exception as exception:
        print("Error while executing montecarloscsv:")
        print(exception)
        
        print("🪲 If the problem cannot be solved, consider opening an issue on GitHub: https://github.com/LetPeopleWork/MonteCarloCSV/issues 🪲")

if __name__ == "__main__":    
    main()