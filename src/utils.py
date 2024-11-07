import csv
from tkinter import messagebox

def validate_csv(file_path, required_columns):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        missing_columns = [col for col in required_columns if col not in reader.fieldnames]
        if missing_columns:
            raise ValueError(f"CSV is missing required columns: {missing_columns}")
        return True
    
def format_path(path):
    return " -> ".join(path)

def show_error(message):
    messagebox.showerror("Error", message)
    