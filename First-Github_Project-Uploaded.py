import tkinter as tk
from tkinter import ttk
import requests

class CurrencyApp():
    def __init__(self):

        self.app_window = tk.Tk()
        self.app_window.title("Live Currency Converter")
        self.app_window.geometry("800x600")
        self.rates_status = tk.Label(self.app_window, font=("Arial", 12), text="")

        try:
            self.url = "https://api.exchangerate-api.com/v4/latest/USD"
            self.response = requests.get(self.url)
            self.data = self.response.json()
        except:
            self.data = {"rates": {}}
            self.rates_status.config(text="No Internet Connection")
        self.picker_values = list(self.data["rates"].keys())


        self.amount_entry = ttk.Entry(self.app_window, font=("Arial", 12), justify="center")
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        self.conversion_result = tk.Label(self.app_window, font=("Arial", 12), justify="center")
        self.conversion_result.grid(row=1, column=1)
        self.current_currency_var = tk.StringVar()
        self.current_currency_var.set("Set Currency")
        self.current_currency_dropdown = ttk.Combobox(self.app_window, font=("Arial", 12),
                                                      textvariable=self.current_currency_var,
                                                      values= self.picker_values,
                                                      state="readonly")
        self.current_currency_dropdown.grid(row=0, column=2, padx=5, pady=5)
        self.converting_currency_var = tk.StringVar()
        self.converting_currency_var.set("Set Currency")
        self.converting_currency_dropdown = ttk.Combobox(self.app_window, font=("Arial", 12),
                                                         textvariable=self.converting_currency_var,
                                                         values= self.picker_values,
                                                         state="readonly")
        self.converting_currency_dropdown.grid(row=1, column=2)
        self.refresh_button = tk.Button(self.app_window, font=("Arial", 12),
                                        text="Refresh", command=self.refresh_rates)
        self.refresh_button.grid(row=0, column=3)
        self.swap_currency_button = tk.Button(self.app_window, font=("Arial", 12),
                                              text="Swap Currencies", command=self.swap_currencies)
        self.swap_currency_button.grid(row=1, column=3, pady=5)

        self.rates_status.grid(row=0, column=4)

        self.amount_entry.bind("<KeyRelease>", lambda e: self.convert())
        self.current_currency_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: self.convert()
        )

        self.converting_currency_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: self.convert()
        )
        self.app_window.bind("<Escape>", lambda e: self.app_window.quit())
        self.app_window.mainloop()

    def swap_currencies(self):
        swapped_currency = self.current_currency_dropdown.get()
        self.current_currency_dropdown.set(self.converting_currency_dropdown.get())
        self.converting_currency_dropdown.set(swapped_currency)
        self.convert()
    def refresh_rates(self):
        try:
            response = requests.get(self.url)
            self.data = response.json()
            self.rates_status.config(text="Rates Updated")
            self.rates_status.after(3000, self.clear_status)
            self.convert()
        except:
            self.rates_status.config(text="Failed to update rates, Error: No Internet Connection")
            self.rates_status.after(3000, self.clear_status)
    def convert(self):
        current_currency_picked = self.current_currency_dropdown.get()
        converting_currency_picked = self.converting_currency_dropdown.get()

        if current_currency_picked not in self.data["rates"]:
            return
        current_rate = self.data["rates"][current_currency_picked]

        if converting_currency_picked not in self.data["rates"]:
            return
        converting_rate = self.data["rates"][converting_currency_picked]

        try:
            current_money = float(self.amount_entry.get())
        except:
            return 0

        amount_in_usd = current_money / current_rate
        converted_amount = amount_in_usd * converting_rate

        self.conversion_result.config(text=f"{converted_amount:.2f} {converting_currency_picked}")

    def clear_status(self):
        self.rates_status.config(text="")

CurrencyApp()

