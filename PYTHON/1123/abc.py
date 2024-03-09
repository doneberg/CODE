 def shift_barcode_focus(self, current_idx, *args):
    current_var = list(self.barcode_vars.values())[current_idx]
    if len(current_var.get()) == 6:
      next_entry = list(self.barcode_entries.values())[current_idx + 1]
      next_entry.focus()
