import random
from datetime import date, datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import pandas as pd

import os

class MonteCarloService:
    
    def __init__(self, history_in_days, today = date.today(), save_charts = False, trials=10000):
        self.trials = trials        
        self.history_in_days = history_in_days
        self.today = today
        
        self.percentile_50 = 0.5
        self.percentile_70 = 0.7
        self.percentile_85 = 0.85
        self.percentile_95 = 0.95

        # Save the plot as an image in the "Charts" folder next to the script
        self.charts_folder = os.path.join(os.getcwd(), 'Charts')
        self.save_charts = save_charts

        self.current_date = datetime.now().strftime('%d.%m.%Y')
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.png")
        self.logo = mpimg.imread(logo_path)
        
        if save_charts and not os.path.exists(self.charts_folder):
            os.makedirs(self.charts_folder)
        
    def create_closed_items_history(self, items):
        print("Getting items that were done in the last {0} days...".format(self.history_in_days))       
        time_delta = self.today - timedelta(self.history_in_days)
        df = pd.DataFrame.from_records([item.to_dict() for item in items])        
        
        closed_items = pd.DataFrame()
        
        closed_items = pd.concat([closed_items, df[df.closed_date >= time_delta]])
        
        closed_items_hist = closed_items["closed_date"].value_counts().to_dict()

        if self.save_charts:
            tp_run_chart_path = os.path.join(self.charts_folder, 'Throughput_Run_Chart.png')
            plt.figure(figsize=(15, 9))
            plt.gca().set_ylim(bottom=0)  
            
            print("Storing Chart at {0}".format(tp_run_chart_path))
            plt.bar(list(closed_items_hist.keys()), closed_items_hist.values(), color='b')
            
            self.add_timestamp(plt)
            self.add_logo(plt)
            
            plt.savefig(tp_run_chart_path)
        
        print("Found {0} items that were closed in the last {1} days".format(len(closed_items), self.history_in_days))
                    
        return closed_items_hist
    
    def how_many(self, target_date, closed_items_history):
        print("--------------------------------")
        print("Running Monte Carlo Simulation - How Many items will be done till {0}".format(target_date))
        print("--------------------------------")
        monte_carlo_simulation_results = self.__run_monte_carlo_how_many(target_date, closed_items_history)
        
        return self.__get_predictions_howmany(monte_carlo_simulation_results)
        
    def when(self, remaining_items, closed_items_history, target_date = None):
        print("--------------------------------")
        print("Running Monte Carlo Simulation - When will {0} items be done".format(remaining_items))
        print("--------------------------------")
        monte_carlo_simulation_results = self.__run_monte_carlo_when(remaining_items, closed_items_history)
        
        days_to_target_date = None
        if target_date:
            days_to_target_date = (target_date - self.today).days
            print("{0} days to target date".format(days_to_target_date))
        
        (predicted_date_50, predicted_70, predicted_date_85, predicted_date_95, target_date_likelyhood) = self.__get_predictions_when(monte_carlo_simulation_results, days_to_target_date)
        return (predicted_date_50, predicted_70, predicted_date_85, predicted_date_95, target_date_likelyhood)

    def __run_monte_carlo_when(self, remaining_items, closed_items_history):        
        time_delta = self.today - timedelta(self.history_in_days)
        monte_carlo_data = self.__prepare_monte_carlo_dataset(time_delta, closed_items_history)            
                
        mc_results = {}
                
        for i in range(self.trials):
            day_count = 0
            finished_item_count = 0
                    
            while finished_item_count < remaining_items:
                day_count += 1
                rand = random.randint(0, self.history_in_days - 1)
                finished_item_count += monte_carlo_data[rand]
                        
            if day_count in mc_results:
                mc_results[day_count] += 1
            else:
                mc_results[day_count] = 1
                
        return mc_results

    def __get_predictions_when(self, mc_results, days_to_target_date = None):        
        sorted_dict = {k:v for k,v in sorted(mc_results.items())}
                
        percentile_50_target = self.trials * 0.5
        percentile_70_target = self.trials * 0.7
        percentile_85_target = self.trials * 0.85
        percentile_95_target = self.trials * 0.95


        percentile_50 = 0
        percentile_70 = 0
        percentile_85 = 0
        percentile_95 = 0
        
        # Initialize trials in time with the number of trials - if we have 100% chance of hitting the target date, we don't need to calculate it
        trials_in_time = self.trials if days_to_target_date else -1
        
        count = 0
                    
        for key in sorted_dict:
            value = sorted_dict[key]

            count += value
                    
            if (percentile_50 == 0 and count >= percentile_50_target):
                percentile_50 = key
            elif (percentile_70 == 0 and count >= percentile_70_target):
                percentile_70 = key
            elif (percentile_85 == 0 and count >= percentile_85_target):
                percentile_85 = key
            elif (percentile_95 == 0 and count >= percentile_95_target):
                percentile_95 = key
                
            if trials_in_time == self.trials and key >= days_to_target_date:
                trials_in_time = count
                
        
        predicted_date_50 = self.today + timedelta(percentile_50)
        predicted_date_70 = self.today + timedelta(percentile_70)
        predicted_date_85 = self.today + timedelta(percentile_85)
        predicted_date_95 = self.today + timedelta(percentile_95)

        print("50 Percentile: {0} days - Predicted Date: {1}".format(percentile_50, predicted_date_50))
        print("70 Percentile: {0} days - Predicted Date: {1}".format(percentile_70, predicted_date_70))
        print("85 Percentile: {0} days - Predicted Date: {1}".format(percentile_85, predicted_date_85))
        print("95 Percentile: {0} days - Predicted Date: {1}".format(percentile_95, predicted_date_95))
        
        prediction_targetdate = 0
        if days_to_target_date:
            prediction_targetdate = (100 / self.trials) * trials_in_time
            print("Chance of hitting target date: {0}".format(prediction_targetdate))
        
        if self.save_charts:
            vertical_lines_data = [(percentile_50, '50th Percentile', "red"), (percentile_70, '70th Percentile', "orange"), (percentile_85, '85th Percentile', "lightgreen"), (percentile_95, '95th Percentile', "darkgreen")] 
            plt.figure(figsize=(15, 9))
            when_chart_path = os.path.join(self.charts_folder, 'MC_When.png')
            print("Storing Chart at {0}".format(when_chart_path))
            plt.bar(list(sorted_dict.keys()), sorted_dict.values(), color='g')

            for position, line_name, color in vertical_lines_data:
                plt.axvline(x=position, color=color, linestyle='--', label="{0} ({1})".format(line_name, position))

            plt.legend()
            plt.gca().set_ylim(bottom=0)  
            
            self.add_timestamp(plt)
            self.add_logo(plt)

            plt.savefig(when_chart_path)

        return (predicted_date_50, predicted_date_70, predicted_date_85, predicted_date_95, prediction_targetdate)

    def __run_monte_carlo_how_many(self, prediction_date, closed_items_hist):
        time_delta = self.today - timedelta(self.history_in_days)
        monte_carlo_data = self.__prepare_monte_carlo_dataset(time_delta, closed_items_hist)            
                
        mc_results = {}
        amount_of_days = (prediction_date - self.today).days
                
        for i in range(self.trials):
            day_count = 0
            finished_item_count = 0
                    
            while day_count < amount_of_days:
                day_count += 1
                rand = random.randint(0, self.history_in_days - 1)
                finished_item_count += monte_carlo_data[rand]
                        
            if finished_item_count in mc_results:
                mc_results[finished_item_count] += 1
            else:
                mc_results[finished_item_count] = 1
                
        return mc_results

    def __get_predictions_howmany(self, mc_results):        
        sorted_dict = {k:v for k,v in sorted(mc_results.items(), reverse=True)}
                
        percentile_50_target = self.trials * self.percentile_50
        percentile_70_target = self.trials * self.percentile_70
        percentile_85_target = self.trials * self.percentile_85
        percentile_95_target = self.trials * self.percentile_95
        
        percentile_50 = 0
        percentile_70 = 0
        percentile_85 = 0
        percentile_95 = 0
        
        count = 0
                
        for key in sorted_dict:
            value = sorted_dict[key]

            count += value
                    
            if (percentile_50 == 0 and count >= percentile_50_target):
                percentile_50 = key
            elif (percentile_70 == 0 and count >= percentile_70_target):
                percentile_70 = key
            elif (percentile_85 == 0 and count >= percentile_85_target):
                percentile_85 = key
            elif (percentile_95 == 0 and count >= percentile_95_target):
                percentile_95 = key
                
                
        print("50 Percentile: {0} Items".format(percentile_50))
        print("70 Percentile: {0} Items".format(percentile_70))
        print("85 Percentile: {0} Items".format(percentile_85))
        print("95 Percentile: {0} Items".format(percentile_95))

        if self.save_charts:
            vertical_lines_data = [(percentile_50, '50th Percentile', "red"), (percentile_70, '70th Percentile', "orange"), (percentile_85, '85th Percentile', "lightgreen"), (percentile_95, '95th Percentile', "darkgreen")] 

            plt.figure(figsize=(15, 9))
            how_many_chart_path = os.path.join(self.charts_folder, 'MC_HowMany.png')
            print("Storing Chart at {0}".format(how_many_chart_path))
            plt.bar(list(sorted_dict.keys()), sorted_dict.values(), color='g')
            
            for position, line_name, color in vertical_lines_data:
                plt.axvline(x=position, color=color, linestyle='--', label="{0} ({1})".format(line_name, position))

            plt.legend()
            
            self.add_timestamp(plt)
            self.add_logo(plt)

            plt.savefig(how_many_chart_path)
        
        return (percentile_50, percentile_70, percentile_85, percentile_95)

    def __prepare_monte_carlo_dataset(self, time_delta, closed_items_hist):
        monte_carlo_data = {}
        
        for i in range((self.today - time_delta).days):
            day = self.today - timedelta(days=i)
            monte_carlo_data[i] = 0

            if day in closed_items_hist:
                monte_carlo_data[i] = closed_items_hist[day]
                
        
        return monte_carlo_data       
    
    def add_timestamp(self, plt):
        plt.text(1, 1.02, f"Generated on {self.current_date}", transform=plt.gca().transAxes, fontsize=10, ha='right', va='top')
    
    def add_logo(self, plt):
        # Add logo
        imagebox = OffsetImage(self.logo, zoom=0.48)
        ab = AnnotationBbox(imagebox, (0.065, 1.08), xycoords='axes fraction', frameon=False, box_alignment=(1, 1))
        plt.gca().add_artist(ab)