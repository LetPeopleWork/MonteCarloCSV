from .WorkItem import WorkItem
from datetime import datetime, timedelta
import random
import csv

class CsvService:    
       
    def get_closed_items(self, file_path, delimeter, column_name, date_format):
        print("Loading Items from CSV File: '{0}'. Column Name '{1}' and Date Format '{2}'".format(file_path, column_name, date_format))
        work_items = []
        
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=delimeter)
            
            for row in csv_reader:
                closed_date_raw = row[column_name]

                if closed_date_raw:
                    closed_date = datetime.strptime(closed_date_raw, date_format)           
                    work_items.append(WorkItem(closed_date))
        
        print("Found {0} Items in the CSV".format(len(work_items)))

        return work_items

    def write_example_file(self, file_path, delimeter, column_name, history, date_format):
        print("Writing Example File with random values to {0}".format(file_path))
        
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=delimeter)
            field = [column_name]
            
            # Write Header
            writer.writerow(field)
            
            # Generate and write 100 random dates
            for _ in range(100):
                random_days_ago = random.randint(0, history)
                random_date = datetime.now() - timedelta(days=random_days_ago)
                formatted_date = random_date.strftime(date_format)
                writer.writerow([formatted_date])