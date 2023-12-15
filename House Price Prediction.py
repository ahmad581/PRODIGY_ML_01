# import os
import joblib
import pandas as pd
import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog

# file_path = os.getenv('FILE_PATH')
model = joblib.load('House_Price_Pridiction.pkl')
csv_data = None

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()


def predict_price(sender, app_data):
    ids = csv_data['Id']
    new_data = csv_data.select_dtypes(include=['float64', 'int64'])
    model_prediction = model.predict(new_data)
    if model_prediction is not None:
        result = pd.DataFrame({'Id': ids, 'PredictedPrice': model_prediction})
        result = result.values.tolist()
        for i in range(len(result)):
            with dpg.table_row(parent="Result"):
                dpg.add_text(result[i][0])  # ID
                dpg.add_text(result[i][1])  # Predicted Price


def read_file(sender, app_data):
    file_path = dpg.get_value("File_Path")
    if file_path:
        try:
            global csv_data
            csv_data = pd.read_csv(file_path)
            dpg.set_value("Status", f"Loaded {len(csv_data)} rows successfully.")
        except Exception as e:
            dpg.set_value("Status", f"Error: {str(e)}")
    else:
        dpg.set_value("Status", "Please provide a valid file path.")


def browse_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        dpg.set_value("File_Path", file_path)
    else:
        print('ERROR')


with dpg.window(label="Price Prediction", width=400, height=200):
    dpg.add_text("Enter The Path Of The File:")
    dpg.add_input_text(label="File Path", tag="File_Path", width=400)
    dpg.add_button(label="Browse", callback=browse_file)
    dpg.add_button(label="Load File", callback=read_file)
    dpg.add_text(label="", tag="Status")
    dpg.add_button(label="Display Predicted Prices", callback=predict_price)
    with dpg.table(tag="Result"):
        dpg.add_table_column(label='ID')
        dpg.add_table_column(label='Predicted Price')


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
