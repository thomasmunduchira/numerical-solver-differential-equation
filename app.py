from tkinter import *

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_function = Label(self, text="Function:").pack()
        self.function = Entry(self).pack()

        self.label_start_x = Label(self, text="Start x:").pack()
        self.start_x = Entry(self).pack()

        self.label_start_y = Label(self, text="Start y:").pack()
        self.start_y = Entry(self).pack()

        self.label_end_x = Label(self, text="End x:").pack()
        self.end_x = Entry(self).pack()

        self.label_step = Label(self, text="Step size:").pack()
        self.step = Entry(self).pack()

        self.label_decimal = Label(self, text="Decimal places:").pack()
        self.decimal = Entry(self).pack()

        self.label_toggle = Label(self, text="Select method:").pack()
        self.method_toggle = IntVar()
        self.radiobutton_toggle_euler = Radiobutton(self, text="Euler", value=1, variable=self.method_toggle).pack(anchor=W)
        self.radiobutton_toggle_improved_euler = Radiobutton(self, text="Improved Euler", value=2, variable=self.method_toggle).pack(anchor=W)
        self.radiobutton_toggle_runge_kutta = Radiobutton(self, text="Runge Kutta", value=3, variable=self.method_toggle).pack(anchor=W)

        self.button_calculate = Button(self, text="Calculate", command=self.calculate).pack()

        self.label_result = Label(self)

        self.button_close = Button(self, text="Close", fg="red", command=root.destroy).pack(side="bottom")
    
    def calculate(self):
        option = self.method_toggle.get()
        function = self.function.get()
        start_x = self.start_x.get()
        start_y = self.start_y.get()
        end_x = self.end_x.get()
        step = self.step.get()
        decimal = self.decimal.get()

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
        self.label_result.delete(0, END)

    def display_result(self, list):
        self.clear_result()
        for element in list:
            self.label_result.insert(END, element)

    def euler_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "f(xn, yn)", "yn+1"]]
        n = 0
        while start_x < end_x:
            x, y = start_x, start_y
            func_val = round(eval(function), decimal)
            next_y = round(start_y + step * func_val, decimal)
            result.append([n, start_x, start_y, func_val, next_y])
            n += 1
            n = round(n, 2)
            start_x += step
            start_x = round(start_x, 2)
            start_y = next_y
        return result

    def improved_euler_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "f(xn, yn)", "y*n+1", "f(xn+1, y*n+1)", "yn+1"]]
        n = 0

        while start_x < end_x:
            x, y = start_x, start_y
            init_estimate = round(eval(function), decimal)
            next_init_estimate = round(start_y + step * init_estimate, decimal)
            x, y = start_x + step, next_init_estimate
            func_val = round(eval(function), decimal)
            next_y = round(start_y + step * (init_estimate + func_val) / 2, decimal)
            result.append([n, start_x, start_y, init_estimate, next_init_estimate, func_val, next_y])
            n += 1
            n = round(n, 2)
            start_x += step
            start_x = round(start_x, 2)
            start_y = next_y
        return result

    def runge_kutta_method(self, function, start_x, start_y, end_x, step, decimal):
        result = [["n", "xn", "yn", "k1", "k2", "k3", "k4", "yn+1"]]
        n = 0

        while start_x < end_x:
            x, y = start_x, start_y
            k1 = round(eval(function), decimal)
            x, y = start_x + 0.5*step, start_y + 0.5*step*k1
            k2 = round(eval(function), decimal)
            y = start_y + 0.5*step*k2
            k3 = round(eval(function), decimal)
            x, y = start_x + step, start_y + step*k3
            k4 = round(eval(function), decimal)
            next_y = round(start_y + step/6*(k1 + 2*k2 + 2*k3 + k4), decimal)
            result.append([n, start_x, start_y, k1, k2, k3, k4, next_y])
            n += 1
            n = round(n, 2)
            start_x += step
            start_x = round(start_x, 2)
            start_y = next_y
        return result    

root = Tk()
root.title("Numerical Solution Calculator of Ordinary Differential Equations")
root.geometry("500x500")

app = Application(root)
app.mainloop()