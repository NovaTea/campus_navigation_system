import tkinter as tk
from src.ui import CampusNavigationUI 

def main():
    root = tk.Tk()
    app = CampusNavigationUI(root) 
    root.mainloop()

if __name__ == "__main__":
    main()
