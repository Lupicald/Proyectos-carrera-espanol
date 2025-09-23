"""
Calculator GUI using Tkinter
"""
import tkinter as tk
from tkinter import messagebox

class CalculatorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("320x400")
        self.window.resizable(False, False)
        
        # Calculator variables
        self.current = "0"
        self.previous = ""
        self.operation = ""
        self.should_reset = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Display frame
        display_frame = tk.Frame(self.window, bg="black", height=80)
        display_frame.pack(fill="x", padx=5, pady=5)
        display_frame.pack_propagate(False)
        
        # Display label
        self.display = tk.Label(display_frame, text="0", 
                               font=("Arial", 24, "bold"), 
                               bg="black", fg="white", 
                               anchor="e", padx=10)
        self.display.pack(fill="both", expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create buttons
        self.create_buttons(buttons_frame)
    
    def create_buttons(self, parent):
        # Button configuration
        btn_config = {
            'font': ('Arial', 16, 'bold'),
            'width': 5,
            'height': 2
        }
        
        # Row 0: Clear and operations
        tk.Button(parent, text="C", command=self.clear, 
                 bg="orange", fg="white", **btn_config).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(parent, text="÷", command=lambda: self.operation_pressed("÷"), 
                 bg="gray", fg="white", **btn_config).grid(row=0, column=3, padx=2, pady=2)
        
        # Row 1: 7, 8, 9, ×
        tk.Button(parent, text="7", command=lambda: self.digit_pressed("7"), 
                 bg="lightgray", **btn_config).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(parent, text="8", command=lambda: self.digit_pressed("8"), 
                 bg="lightgray", **btn_config).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(parent, text="9", command=lambda: self.digit_pressed("9"), 
                 bg="lightgray", **btn_config).grid(row=1, column=2, padx=2, pady=2)
        tk.Button(parent, text="×", command=lambda: self.operation_pressed("×"), 
                 bg="gray", fg="white", **btn_config).grid(row=1, column=3, padx=2, pady=2)
        
        # Row 2: 4, 5, 6, -
        tk.Button(parent, text="4", command=lambda: self.digit_pressed("4"), 
                 bg="lightgray", **btn_config).grid(row=2, column=0, padx=2, pady=2)
        tk.Button(parent, text="5", command=lambda: self.digit_pressed("5"), 
                 bg="lightgray", **btn_config).grid(row=2, column=1, padx=2, pady=2)
        tk.Button(parent, text="6", command=lambda: self.digit_pressed("6"), 
                 bg="lightgray", **btn_config).grid(row=2, column=2, padx=2, pady=2)
        tk.Button(parent, text="-", command=lambda: self.operation_pressed("-"), 
                 bg="gray", fg="white", **btn_config).grid(row=2, column=3, padx=2, pady=2)
        
        # Row 3: 1, 2, 3, +
        tk.Button(parent, text="1", command=lambda: self.digit_pressed("1"), 
                 bg="lightgray", **btn_config).grid(row=3, column=0, padx=2, pady=2)
        tk.Button(parent, text="2", command=lambda: self.digit_pressed("2"), 
                 bg="lightgray", **btn_config).grid(row=3, column=1, padx=2, pady=2)
        tk.Button(parent, text="3", command=lambda: self.digit_pressed("3"), 
                 bg="lightgray", **btn_config).grid(row=3, column=2, padx=2, pady=2)
        tk.Button(parent, text="+", command=lambda: self.operation_pressed("+"), 
                 bg="gray", fg="white", **btn_config).grid(row=3, column=3, padx=2, pady=2)
        
        # Row 4: 0 and =
        tk.Button(parent, text="0", command=lambda: self.digit_pressed("0"), 
                 bg="lightgray", **btn_config).grid(row=4, column=0, columnspan=2, 
                                                   padx=2, pady=2, sticky="ew")
        tk.Button(parent, text="=", command=self.equals_pressed, 
                 bg="orange", fg="white", **btn_config).grid(row=4, column=2, columnspan=2, 
                                                            padx=2, pady=2, sticky="ew")
        
        # Configure grid weights
        for i in range(4):
            parent.columnconfigure(i, weight=1)
    
    def digit_pressed(self, digit):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        
        if self.current == "0":
            self.current = digit
        else:
            self.current += digit
        
        self.update_display()
    
    def operation_pressed(self, op):
        if self.operation and not self.should_reset:
            self.equals_pressed()
        
        self.previous = self.current
        self.operation = op
        self.should_reset = True
    
    def equals_pressed(self):
        if self.operation and self.previous:
            try:
                # Convert display symbols to Python operators
                if self.operation == "×":
                    result = float(self.previous) * float(self.current)
                elif self.operation == "÷":
                    if float(self.current) == 0:
                        messagebox.showerror("Error", "Cannot divide by zero!")
                        return
                    result = float(self.previous) / float(self.current)
                elif self.operation == "+":
                    result = float(self.previous) + float(self.current)
                elif self.operation == "-":
                    result = float(self.previous) - float(self.current)
                
                # Format result
                if result == int(result):
                    self.current = str(int(result))
                else:
                    self.current = str(round(result, 8))
                
                self.update_display()
                self.operation = ""
                self.previous = ""
                self.should_reset = True
                
            except Exception as e:
                messagebox.showerror("Error", "Invalid calculation!")
                self.clear()
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operation = ""
        self.should_reset = False
        self.update_display()
    
    def update_display(self):
        # Limit display length
        display_text = self.current[:12]
        self.display.config(text=display_text)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = CalculatorGUI()
    calculator.run()
