from tkinter import *
from math import *

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label_function = Label(self, text="Function:")
        self.label_function.grid(row=0, column=0)
        self.function = Entry(self)
        self.function.grid(row=0, column=1)

        self.label_start_x = Label(self, text="Start x:")
        self.label_start_x.grid(row=1, column=0)
        self.start_x = Entry(self)
        self.start_x.grid(row=1, column=1)

        self.label_start_y = Label(self, text="Start y:")
        self.label_start_y.grid(row=2, column=0)
        self.start_y = Entry(self)
        self.start_y.grid(row=2, column=1)

        self.label_end_x = Label(self, text="End x:")
        self.label_end_x.grid(row=3, column=0)
        self.end_x = Entry(self)
        self.end_x.grid(row=3, column=1)

        self.label_step = Label(self, text="Step size:")
        self.label_step.grid(row=4, column=0)
        self.step = Entry(self)
        self.step.grid(row=4, column=1)

        self.label_decimal = Label(self, text="Decimal places:")
        self.label_decimal.grid(row=5, column=0)
        self.decimal = Entry(self)
        self.decimal.grid(row=5, column=1)

        self.label_toggle = Label(self, text="Select method:")
        self.label_toggle.grid(row=6, column=0)
        self.method_toggle = IntVar()
        self.radiobutton_toggle_euler = Radiobutton(self, text="Euler", value=1, variable=self.method_toggle)
        self.radiobutton_toggle_euler.grid(row=6, column=1, sticky=W)
        self.radiobutton_toggle_improved_euler = Radiobutton(self, text="Improved Euler", value=2, variable=self.method_toggle)
        self.radiobutton_toggle_euler.select()
        self.radiobutton_toggle_improved_euler.grid(row=7, column=1, sticky=W)
        self.radiobutton_toggle_runge_kutta = Radiobutton(self, text="Runge Kutta", value=3, variable=self.method_toggle)
        self.radiobutton_toggle_runge_kutta.grid(row=8, column=1, sticky=W)

        self.button_calculate = Button(self, text="Calculate", command=self.calculate)
        self.button_calculate.grid(row=9, column=0)

        self.button_close = Button(self, text="Close", fg="red", command=root.destroy)
        self.button_close.grid(row=9, column=1, sticky=W)

        self.label_result = Label(self)
        self.label_result.grid(row=0, column=2, rowspan=9, columnspan=2)
    
    def calculate(self):
        option = self.method_toggle.get()
        function = self.function.get()
        start_x = float(self.start_x.get())
        start_y = float(self.start_y.get())
        end_x = float(self.end_x.get())
        step = float(self.step.get())
        decimal = int(self.decimal.get())

        if option == 1:
            result = self.euler_method(function, start_x, start_y, end_x, step, decimal)
            self.display_result(result)
        elif option == 2:
            result = self.improved_euler_method(function, start_x, start_y, end_x, step, decimal)
            self.display_result(result)
        else:
            result = self.runge_kutta_method(function, start_x, start_y, end_x, step, decimal)
            self.display_result(result)

    def clear_result(self):
        self.label_result["text"] = ""

    def display_result(self, list):
        self.clear_result()
        for element in list:
            self.label_result["text"] = self.label_result["text"] + \
            " ".join(map(str, element)) + "\n"

    def euler_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "f(xn, yn)", "yn+1"]]
        n = 0
        while start_x < end_x:
            x, y = start_x, start_y
            func_val = eval(function)
            next_y = start_y + step * func_val
            result.append([n, round(start_x, 2), round(start_y, decimal), round(func_val, decimal), round(next_y, decimal)])
            n += 1
            start_x += step
            start_y = next_y
        return result

    def improved_euler_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "f(xn, yn)", "y*n+1", "f(xn+1, y*n+1)", "yn+1"]]
        n = 0

        while start_x < end_x:
            x, y = start_x, start_y
            init_estimate = eval(function)
            next_init_estimate = start_y + step * init_estimate
            x, y = start_x + step, next_init_estimate
            func_val = eval(function)
            next_y = start_y + step * (init_estimate + func_val) / 2
            result.append([n, round(start_x, 2), round(start_y, decimal), round(init_estimate, decimal), round(next_init_estimate, decimal), round(func_val, decimal), round(next_y, decimal)])
            n += 1
            start_x += step
            start_y = next_y
        return result

    def runge_kutta_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "k1", "k2", "k3", "k4", "yn+1"]]
        n = 0

        while start_x < end_x:
            x, y = start_x, start_y
            k1 = eval(function)
            x, y = start_x + 0.5*step, start_y + 0.5*step*k1
            k2 = eval(function)
            y = start_y + 0.5*step*k2
            k3 = eval(function)
            x, y = start_x + step, start_y + step*k3
            k4 = eval(function)
            next_y = start_y + step/6*(k1 + 2*k2 + 2*k3 + k4)
            result.append([n, round(start_x, 2), round(start_y, decimal), round(k1, decimal), round(k2, decimal), round(k3, decimal), round(k4, decimal), round(next_y, decimal)])
            n += 1
            start_x += step
            start_y = next_y
        return result

root = Tk()
root.title("Numerical Solver of Differential Equations")
root.geometry("700x275")

app = Application(root)
app.mainloop()