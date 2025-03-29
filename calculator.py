import tkinter as tk

# Function to update the entry box when a button is clicked
def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + value)

# Function to evaluate the expression
def evaluate():
    try:
        result = eval(entry.get())  # Using eval to evaluate the mathematical expression
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Function to clear the entry box
def clear():
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.config(bg="lightblue")  # Set background color of the window

# Create an entry widget to display the input and output
entry = tk.Entry(root, width=16, font=('Arial', 34), borderwidth=2, relief='solid', justify='right', bg="lightyellow", fg="blue")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15)

# Button layout with colors
buttons = [
    ('7', 1, 0, "#FFB6C1"), ('8', 1, 1, "#FFB6C1"), ('9', 1, 2, "#FFB6C1"), ('/', 1, 3, "#FFA500"),
    ('4', 2, 0, "#FFB6C1"), ('5', 2, 1, "#FFB6C1"), ('6', 2, 2, "#FFB6C1"), ('*', 2, 3, "#FFA500"),
    ('1', 3, 0, "#FFB6C1"), ('2', 3, 1, "#FFB6C1"), ('3', 3, 2, "#FFB6C1"), ('-', 3, 3, "#FFA500"),
    ('0', 4, 0, "#FFB6C1"), ('C', 4, 1, "#FF6347"), ('=', 4, 2, "#32CD32"), ('+', 4, 3, "#FFA500")
]

# Add buttons to the grid with specified colors
for (text, row, col, color) in buttons:
    if text == "=":
        tk.Button(root, text=text, width=6, height=3, font=('Arial', 18), bg=color, command=evaluate).grid(row=row, column=col)
    elif text == "C":
        tk.Button(root, text=text, width=6, height=3, font=('Arial', 18), bg=color, command=clear).grid(row=row, column=col)
    else:
        tk.Button(root, text=text, width=6, height=3, font=('Arial', 18), bg=color, command=lambda value=text: button_click(value)).grid(row=row, column=col)

# Run the Tkinter event loop
root.mainloop()
