import tkinter as tk
import customtkinter as ctk
import math


def format_number(n):
    if n >= 10_000:
        return f"{n / 1_000:.1f}k"
    return f"{n:,}"


class RangeSlider(ctk.CTkFrame):
    def __init__(self, master, min_val=0, max_val=None, width=300, height=60, step=1, stepType="linear", *args, **kwargs):
        super().__init__(master, width=width, height=height, *args, **kwargs)
        self.pack_propagate(0)

        self.min_val = min_val
        self.max_val = max_val or 2 * 10**6
        self.addSign = max_val is None
        self.step = step
        self.width = width
        self.height = height
        self.knob_radius = 8
        self.slider_height = 4
        self.stepType = stepType

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg="#1E1E1E")
        self.canvas.pack(fill="both", expand=True)

        self.range_min = self.min_val
        self.range_max = self.max_val
        self.active_knob = None

        self.slider_y = height // 2 + 10

        self.slider_line = self.canvas.create_line(
            self.knob_radius, self.slider_y,
            width - self.knob_radius, self.slider_y,
            fill="#555", width=self.slider_height, capstyle="round"
        )

        self.range_line = self.canvas.create_line(0, 0, 0, 0, fill="#3B82F6", width=self.slider_height, capstyle="round")

        self.knob1 = self.canvas.create_oval(0, 0, 0, 0, fill="#FFFFFF", outline="#3B82F6", width=1)
        self.knob2 = self.canvas.create_oval(0, 0, 0, 0, fill="#FFFFFF", outline="#3B82F6", width=1)

        self.value_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3B82F6"
        )
        self.value_label.place(relx=0.5, rely=0.65, anchor="center")

        self.canvas.bind("<Button-1>", self.click_event)
        self.canvas.bind("<B1-Motion>", self.drag_event)

        self.update_knobs()

    def value_to_x(self, val):
        if self.stepType == "linear":
            return self.knob_radius + (val - self.min_val) / (self.max_val - self.min_val) * (self.width - 2 * self.knob_radius)
        elif self.stepType == "logarithmic":
            try:
                log_min = math.log10(self.min_val)
                log_max = math.log10(self.max_val)
                log_val = math.log10(val)
            except ValueError:
                log_min = 0
                log_max = math.log10(self.max_val) if self.max_val > 0 else 1
                log_val = 0
            return self.knob_radius + (log_val - log_min) / (log_max - log_min) * (self.width - 2 * self.knob_radius)

    def x_to_value(self, x):
        if self.stepType == "linear":
            val = self.min_val + (x - self.knob_radius) / (self.width - 2 * self.knob_radius) * (self.max_val - self.min_val)
        elif self.stepType == "logarithmic":
            log_min = math.log10(self.min_val)
            log_max = math.log10(self.max_val)
            ratio = (x - self.knob_radius) / (self.width - 2 * self.knob_radius)
            log_val = log_min + ratio * (log_max - log_min)
            val = 10 ** log_val
        return round(val / self.step) * self.step

    def click_event(self, event):
        x = event.x
        x1 = self.value_to_x(self.range_min)
        x2 = self.value_to_x(self.range_max)
        self.active_knob = 1 if abs(x - x1) < abs(x - x2) else 2
        self.drag_event(event)

    def drag_event(self, event):
        if self.active_knob is None:
            return
        x = max(self.knob_radius, min(self.width - self.knob_radius, event.x))
        val = self.x_to_value(x)
        if self.active_knob == 1:
            self.range_min = min(val, self.range_max)
        else:
            self.range_max = max(val, self.range_min)
        self.update_knobs()

    def update_knobs(self):
        x1 = self.value_to_x(self.range_min)
        x2 = self.value_to_x(self.range_max)

        if x1 == x2:
            x2 += 2 * self.knob_radius

        y = self.slider_y
        self.canvas.coords(self.knob1, x1 - self.knob_radius, y - self.knob_radius,
                           x1 + self.knob_radius, y + self.knob_radius)
        self.canvas.coords(self.knob2, x2 - self.knob_radius, y - self.knob_radius,
                           x2 + self.knob_radius, y + self.knob_radius)
        self.canvas.coords(self.range_line, x1, y, x2, y)

        label_min = format_number(int(self.range_min))
        label_max = format_number(int(self.range_max))
        if self.addSign and self.range_max == self.max_val:
            label_max = ">" + label_max
        self.value_label.configure(text=f"{label_min} - {label_max}")

    def get(self):
        return int(self.range_min), int(self.range_max)
