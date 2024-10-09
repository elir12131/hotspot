import tkinter as tk
from tkinter import messagebox, Toplevel, ttk  # Changed from `tk.Entry` to `ttk.Combobox` for suggestions
from fpdf import FPDF
import os
import json

# Constants for file paths
DATA_FILE = "customer_orders.json"
INVOICE_DIR = "invoices"

# Ensure the invoice directory exists
if not os.path.exists(INVOICE_DIR):
    os.makedirs(INVOICE_DIR)

# Load existing customer data or create an empty dictionary
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            customer_orders = json.load(f)
    except json.JSONDecodeError:
        customer_orders = {}
else:
    customer_orders = {}

class ProduceOrderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Poppy's Produce Order Entry")
        self.root.geometry("800x600")
        self.root.configure(bg='#DCE6F0')

        # Font settings
        self.font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 10)

        # Collapsible Sidebar Frame for Orders
        self.sidebar_expanded = True
        self.sidebar_frame = tk.Frame(root, bg="#FFFFFF", width=300, padx=10, pady=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)

        # Search bar for orders
        self.search_entry = tk.Entry(self.sidebar_frame, font=self.font, bg="#FFFFFF", fg="#000000")
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_orders)

        # Orders Listbox in Sidebar
        self.order_listbox = tk.Listbox(self.sidebar_frame, bg="#FFFFFF", fg="#000000", font=self.font)
        self.order_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.order_listbox.bind('<<ListboxSelect>>', self.on_order_select)

        # Main content Frame
        self.main_frame = tk.Frame(root, bg="#DCE6F0")
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Customer name entry
        self.customer_label = tk.Label(self.main_frame, text="Customer Name:", font=self.font, bg="#DCE6F0", fg="#000000")
        self.customer_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.customer_var = tk.StringVar()
        self.customer_entry = ttk.Combobox(self.main_frame, textvariable=self.customer_var, font=self.font, background="#FFFFFF", foreground="#000000")
        self.customer_entry.grid(row=0, column=1, padx=10, pady=10)
        self.customer_entry.bind("<KeyRelease>", self.suggest_customer_names)

        # Item, quantity, and price entry
        self.item_label = tk.Label(self.main_frame, text="Item:", font=self.font, bg="#DCE6F0", fg="#000000")
        self.item_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.item_entry = tk.Entry(self.main_frame, font=self.font, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="flat")
        self.item_entry.grid(row=1, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(self.main_frame, text="Quantity:", font=self.font, bg="#DCE6F0", fg="#000000")
        self.quantity_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.quantity_entry = tk.Entry(self.main_frame, font=self.font, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="flat")
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        self.price_label = tk.Label(self.main_frame, text="Price (Optional):", font=self.font, bg="#DCE6F0", fg="#000000")
        self.price_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.price_entry = tk.Entry(self.main_frame, font=self.font, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="flat")
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        self.view_button = tk.Button(self.main_frame, text="View Past Orders", command=self.view_past_orders, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.view_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.add_button = tk.Button(self.main_frame, text="Add to Order", command=self.add_to_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.add_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        self.save_button = tk.Button(self.main_frame, text="Save", command=self.save_all, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.save_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.pdf_button = tk.Button(self.main_frame, text="Save as PDF", command=self.save_as_pdf, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.pdf_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.email_button = tk.Button(self.main_frame, text="Email Order", command=self.email_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.email_button.grid(row=7, column=2, padx=10, pady=10, sticky="ew")

        self.print_button = tk.Button(self.main_frame, text="Print Order", command=self.print_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.print_button.grid(row=7, column=3, padx=10, pady=10, sticky="ew")

        self.new_order_button = tk.Button(self.main_frame, text="New Order", command=self.new_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        self.new_order_button.grid(row=8, column=0, columnspan=4, pady=10, sticky="ew")

        # Initialize orders
        self.order_list_data = []
        self.current_invoice_file = None

        # Update sidebar
        self.update_sidebar()

    def on_order_select(self, event):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            selected_order = self.order_list_data[selected_index[0]]
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, selected_order[0])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, selected_order[1])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, selected_order[2])
            self.open_price_window(selected_order)

    def open_price_window(self, order):
        price_window = Toplevel(self.root)
        price_window.title("Edit Price & Export")
        price_window.configure(bg="#DCE6F0")

        price_label = tk.Label(price_window, text="Enter Price:", font=self.font, bg="#DCE6F0", fg="#000000")
        price_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        price_entry = tk.Entry(price_window, font=self.font, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="flat")
        price_entry.grid(row=0, column=1, padx=10, pady=10)

        def save_price_and_export():
            new_price = price_entry.get().strip()
            if new_price:
                order[2] = new_price
                self.update_sidebar()
                self.save_as_pdf()  # Update PDF with the new price

                # Provide export options
                export_frame = tk.Frame(price_window, bg="#DCE6F0")
                export_frame.grid(row=2, column=0, columnspan=2, pady=10)

                email_button = tk.Button(export_frame, text="Email Order", command=self.email_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
                email_button.grid(row=0, column=0, padx=5, pady=5)

                pdf_button = tk.Button(export_frame, text="Save as PDF", command=self.save_as_pdf, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
                pdf_button.grid(row=0, column=1, padx=5, pady=5)

                print_button = tk.Button(export_frame, text="Print Order", command=self.print_order, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
                print_button.grid(row=0, column=2, padx=5, pady=5)

            price_window.destroy()

        save_button = tk.Button(price_window, text="Save Price & Export", command=save_price_and_export, font=self.button_font, bg="#0066CC", fg="#ffffff", relief="flat")
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def update_sidebar(self):
        self.order_listbox.delete(0, tk.END)
        self.order_list_data = []

        for order in customer_orders.get(self.customer_var.get(), []):
            if len(order) >= 2:
                self.order_list_data.append(order)
                self.order_listbox.insert(tk.END, f"{order[0]} - Qty: {order[1]} - Price: {order[2] if len(order) > 2 else 'N/A'}")

    def suggest_customer_names(self, event):
        current_text = self.customer_var.get()
        customer_names = list(customer_orders.keys())
        suggestions = [name for name in customer_names if name.lower().startswith(current_text.lower())]
        self.customer_entry['values'] = suggestions

    def add_to_order(self):
        item = self.item_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()
        customer_name = self.customer_var.get().strip()

        if not customer_name:
            messagebox.showerror("Error", "Customer name cannot be empty!")
            return

        if not item or not quantity:
            messagebox.showerror("Error", "Item and quantity cannot be empty!")
            return

        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        quantity = int(quantity)
        order_data = [item, quantity, price if price else "N/A"]

        if customer_name not in customer_orders:
            customer_orders[customer_name] = []

        customer_orders[customer_name].append(order_data)
        self.save_all()
        self.update_sidebar()

        self.item_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def view_past_orders(self):
        customer_name = self.customer_var.get().strip()

        if customer_name not in customer_orders:
            messagebox.showinfo("No Orders", f"No past orders found for {customer_name}.")
            return

        orders = customer_orders[customer_name]
        orders_window = Toplevel(self.root)
        orders_window.title(f"{customer_name}'s Past Orders")
        orders_window.configure(bg="#DCE6F0")

        for idx, order in enumerate(orders):
            order_text = f"{order[0]} - Qty: {order[1]} - Price: {order[2]}"
            tk.Label(orders_window, text=order_text, font=self.font, bg="#DCE6F0", fg="#000000").pack(padx=10, pady=5)

    def new_order(self):
        self.customer_var.set("")
        self.item_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.update_sidebar()

    def save_all(self):
        with open(DATA_FILE, "w") as f:
            json.dump(customer_orders, f, indent=4)
        messagebox.showinfo("Saved", "All data saved successfully.")

    def save_as_pdf(self):
        customer_name = self.customer_var.get().strip()
        if customer_name not in customer_orders:
            messagebox.showerror("Error", "No orders found for this customer!")
            return

        if not self.order_list_data:
            messagebox.showerror("Error", "No orders to save as PDF!")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice for {customer_name}", ln=True, align='C')

        for order in self.order_list_data:
            pdf.cell(200, 10, txt=f"{order[0]} - Qty: {order[1]} - Price: {order[2]}", ln=True)

        file_name = f"{customer_name.replace(' ', '_')}_invoice.pdf"
        file_path = os.path.join(INVOICE_DIR, file_name)
        pdf.output(file_path)

        messagebox.showinfo("Saved", f"PDF saved as {file_path}")

    def email_order(self):
        messagebox.showinfo("Not Implemented", "Email functionality not implemented yet.")

    def print_order(self):
        messagebox.showinfo("Not Implemented", "Print functionality not implemented yet.")

    def search_orders(self, event):
        search_text = self.search_entry.get().lower()
        self.order_listbox.delete(0, tk.END)

        for order in self.order_list_data:
            if search_text in order[0].lower():
                self.order_listbox.insert(tk.END, f"{order[0]} - Qty: {order[1]} - Price: {order[2]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProduceOrderApp(root)
    root.mainloop()
