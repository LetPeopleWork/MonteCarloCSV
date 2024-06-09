from MonteCarloCSV.CsvService import CsvService
from MonteCarloCSV.MonteCarloService import MonteCarloService

from datetime import datetime, timedelta

history_in_days = 30
csv_service = CsvService()
monte_carlo_service = MonteCarloService(history_in_days, False)

csv_service.write_example_file("ExampleFile.csv", ";", "ClosedDate", 22, "%d.%m.%Y")
items = csv_service.get_closed_items("ExampleFile.csv", ";", "ClosedDate", "%d.%m.%Y")

# Get History
closed_items_history = monte_carlo_service.create_closed_items_history(items)

target_date = (datetime.now() + timedelta(days=14)).date()
(predictions_howmany_50, predictions_howmany_70, predictions_howmany_85, predictions_howmany_95) = monte_carlo_service.how_many(target_date, closed_items_history)

remaining_items = 12
(predictions_when_50, predictions_when_70, predictions_when_85, predictions_when_95, predictions_targetdate_likelyhood) = monte_carlo_service.when(remaining_items, closed_items_history, target_date)