import customtkinter as ctk
import tkinter as tk
import customWidgets as cW

filters = {
    'Race': {"Type": "multiselect", "Options": ["Asian", "Black", "Hispanic", "White", "Other"]},
    'Gender': {"Type": 'multiselect', "Options": ["Male", "Female", "Other"]},
    'GPA': {"Type": "range", "Options": {"Min": 0, "Max": 100, "Input_Method": "linear", "Step": 1}},
    'Income': {"Type": "range", "Options": {"Min": 1000, "Max": None, "Input_Method": "logarithmic", "Step": 1000}},
    "Focus": {"Type": 'textinput', "Options": None},
    "Graduating Year": {"Type": 'multiselect', "Options": list(range(2026, 2030))},
    "Community Service Requirement": {'Type': 'singleselect', "Options": ["Very High", "High", "Medium", "Low", "None"]},
    "Scholarship_Description": {"Type": 'textinput', "Options": None},
}


class Search_Page(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Search for students")
        self.geometry("600x600")

        self.vars = {}  # Store variables for all inputs here

        self.container = ctk.CTkScrollableFrame(self, width=580, height=500)
        self.container.pack(padx=10, pady=10, fill="both", expand=True)

        for filter_name, filter_info in filters.items():
            ctk.CTkLabel(self.container, text=filter_name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 0))
            f_type = filter_info["Type"]
            opts = filter_info["Options"]

            if f_type == "multiselect":
                frame = ctk.CTkFrame(self.container)
                frame.pack(anchor="w", pady=5)
                vars_dict = {}
                for option in opts:
                    var = tk.BooleanVar(value=False)
                    cb = ctk.CTkCheckBox(frame, text=str(option), variable=var)
                    cb.pack(anchor="w")
                    vars_dict[option] = var
                self.vars[filter_name] = vars_dict

            elif f_type == "singleselect":
                var = tk.StringVar(value=opts[0] if opts else "")
                dropdown = ctk.CTkOptionMenu(self.container, values=opts, variable=var)
                dropdown.pack(anchor="w", pady=5)
                self.vars[filter_name] = var

            elif f_type == "range":
                min_val = opts["Min"]
                max_val = opts["Max"] # Arbitrary large number for max
                range_slider = cW.RangeSlider(self.container, min_val=min_val, max_val=max_val, step=opts["Step"], stepType=opts["Input_Method"])
                range_slider.pack(anchor="w", pady=5)
                self.vars[filter_name] = {"min": range_slider.range_min, "max": range_slider.range_max}

            elif f_type == "textinput":
                var = tk.StringVar()
                entry = ctk.CTkEntry(self.container, textvariable=var, width=200)
                entry.pack(anchor="w", pady=5)
                self.vars[filter_name] = var

        btn = ctk.CTkButton(self, text="Print Filters", command=self.print_filters)
        btn.pack(pady=10)

    def print_filters(self):
        print("Current filter selections:")
        for key, val in self.vars.items():
            if isinstance(val, dict):
                if all(isinstance(v, tk.BooleanVar) for v in val.values()):
                    selected = [k for k, v in val.items() if v.get()]
                    print(f"{key}: {selected}")
                else:
                    try: 
                        print(f"{key}: Min={int(val['min'].get())}, Max={int(val['max'].get())}")
                    except AttributeError:
                        print(f"{key}: Min={val['min']}, Max={val['max']}")
            elif isinstance(val, tk.StringVar):
                print(f"{key}: {val.get()}")
            else:
                print(f"{key}: {val}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = Search_Page()
    app.mainloop()
