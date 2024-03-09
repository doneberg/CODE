large_font = ('Arial', 12)
   
tk.Label(self.master, text="Plate", font=large_font).grid(row=0, column=0, padx=10, pady=10)
tk.Label(self.master, text="Barcode", font=large_font).grid(row=0, column=1, padx=10, pady=10)

self.barcode_entries = {}
self.barcode_vars = {}

non_nan_index = 0 # This will track our non-NaN index
for index, plate in enumerate(self.unique_plates):
  if pd.isna(plate): # Skip NaN values
    continue

tk.Label(self.master, text=plate, font=large_font).grid(row=non_nan_index+1, column=0, padx=10, pady=10)

barcode_var = StringVar()
self.barcode_vars[plate] = barcode_var
entry = tk.Entry(self.master, textvariable=barcode_var, font=large_font)
entry.grid(row=non_nan_index+1, column=1, padx=10, pady=10)
self.barcode_entries[plate] = entry

# If not the last non-NaN barcode entry, add a trace to shift focus
if non_nan_index < len(self.barcode_vars) - 1:
  callback = lambda *args, idx=non_nan_index: self.shift_barcode_focus(idx)
  barcode_var.trace("w", callback)

non_nan_index += 1

btn_submit = tk.Button(self.master, text="Submit Barcodes", command=self.store_barcodes, font=large_font)
btn_submit.grid(row=non_nan_index+2, column=0, columnspan=2, padx=10, pady=10)

# Center the tkinter window
self.master.update()
width = self.master.winfo_width()
height = self.master.winfo_height()
screenwidth = self.master.winfo_screenwidth()
screenheight = self.master.winfo_screenheight()
x = (screenwidth // 2) - (width // 2)
y = (screenheight // 2) - (height // 2)
self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))



def shift_barcode_focus(self, current_idx, *args):
current_var = list(self.barcode_vars.values())[current_idx]
if len(current_var.get()) == 6:
  next_entry = list(self.barcode_entries.values())[current_idx + 1]
  next_entry.focus()

