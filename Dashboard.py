import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="white", height=10000, padx=10, pady=10)
        self.pack_propagate(False)

        # Placeholder statistics
        statistics_label = ttk.Label(self, text="Dashboard Statistics", style='TLabel', font=("Arial", 16))
        statistics_label.pack(pady=10)

        # Placeholder table
        table_label = ttk.Label(self, text="Table Data", style='TLabel', font=("Arial", 14))
        table_label.pack(pady=5)

        # Create a Treeview for displaying a table
        columns = ("Column 1", "Column 2", "Column 3")
        table_tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            table_tree.heading(col, text=col)
        table_tree.pack(pady=10)

        # Insert some placeholder data into the table
        for i in range(5):
            table_tree.insert("", "end", values=(f"Value {i+1}", f"Value {i+2}", f"Value {i+3}"))

        # Placeholder pie chart
        pie_chart_label = ttk.Label(self, text="Pie Chart", style='TLabel', font=("Arial", 14))
        pie_chart_label.pack(pady=5)

        # Create a placeholder pie chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # Pie Chart
        ax1.pie([25, 30, 45], labels=["Category A", "Category B", "Category C"], autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Bar Chart
        categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
        values = [10, 20, 15, 25, 30]
        ax2.bar(categories, values, color='skyblue')

        # Embed the charts in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(pady=10)