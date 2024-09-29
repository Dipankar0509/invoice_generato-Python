import tkinter
from tkinter import ttk
import datetime
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import mysql.connector

# Generate a random bill number


# Function to create a PDF invoice
def create_pdf_invoice(name, phone, invoice_list, subtotal, salestax, total):
    num = random.sample(range(10), 4)
    bill_no = ''.join(map(str, num))
    
    pdf_file_name = f"{bill_no}__{name}.pdf"
    c = canvas.Canvas(pdf_file_name, pagesize=letter)
    
    

    # Set font styles
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Invoice for: {name}")

    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Phone: {phone}")
    c.drawString(100, 710, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, 690, f"Invoice No: {bill_no}")

    # Draw a horizontal line
    c.line(100, 680, 500, 680)

    # Table headers
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 640, "Qty")
    c.drawString(200, 640, "Description")
    c.drawString(300, 640, "Unit Price")
    c.drawString(400, 640, "Total")

    # Draw a horizontal line for headers
    c.line(100, 630, 500, 630)

    # Reset font for the body
    c.setFont("Helvetica", 12)
    y = 610
    for item in invoice_list:
        c.drawString(100, y, str(item[0]))
        c.drawString(200, y, item[1])
        c.drawString(300, y, f"${item[2]:.2f}")
        c.drawString(400, y, f"${item[3]:.2f}")
        y -= 20  # Move to the next line

    # Draw a horizontal line after the last item
    c.line(100, y, 500, y)

    # Add subtotal, tax, and total
    y -= 20  # Adjust Y position for subtotal
    c.drawString(300, y, "Subtotal:")
    c.drawString(400, y, f"${subtotal:.2f}")

    y -= 20  # Adjust Y position for sales tax
    c.drawString(300, y, f"Sales Tax ({salestax * 100:.0f}%):")
    c.drawString(400, y, f"${subtotal * salestax:.2f}")

    y -= 20  # Adjust Y position for total
    c.drawString(300, y, "Total:")
    c.drawString(400, y, f"${total:.2f}")

    # Save the PDF
    c.save()

    messagebox.showinfo("Invoice Complete", f"Invoice saved as: {pdf_file_name}")
    
    # Save invoice to MySQL
    save_invoice_to_db(name,bill_no,phone,total)
    
    new_invoice()

# Function to save invoice to the MySQL database name, phone, invoice_list, subtotal, salestax, total, bill_no
def save_invoice_to_db(name, bill_no,phone,total):
    
        # Establish a database connection
        mydb = mysql.connector.connect(
            host='localhost',  # e.g., 'localhost'
            database='trial',  # your database name
            user='root',  # your username
            password='Dip@2005'  # your password
        )
        
        mycursor=mydb.cursor()
        name = first_name_entry.get()
        inv_no = bill_no
    
        
        sql = "INSERT INTO cust (name, bill_no,phone,total) VALUES (%s, %s,%s,%s)"
        val = (name,inv_no,phone,total)
        mycursor.execute(sql, val)
        mydb.commit()   

# Function to clear item entry fields
def clear_item():
    qty_spinbox.delete(0, tkinter.END)
    qty_spinbox.insert(0, "1")
    desc_entry.delete(0, tkinter.END)
    price_spinbox.delete(0, tkinter.END)
    price_spinbox.insert(0, "0.0")

# Global list to store invoice items
invoice_list = []

# Function to add item to the invoice
def add_item():
    qty = int(qty_spinbox.get())
    desc = desc_entry.get()
    price = float(price_spinbox.get())
    line_total = qty * price
    invoice_item = [qty, desc, price, line_total]
    tree.insert('', 0, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)

# Function to create a new invoice
def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())
    invoice_list.clear()

# Function to generate the invoice
def generate_invoice():
    name = first_name_entry.get() + " " + last_name_entry.get()
    phone = phone_entry.get()
    subtotal = sum(item[3] for item in invoice_list)
    salestax = 0.1
    total = subtotal * (1 + salestax)

    create_pdf_invoice(name, phone, invoice_list, subtotal, salestax, total)

# Create the main window
window = tkinter.Tk()
window.title("Invoice Generator Form")

frame = tkinter.Frame(window)
frame.pack(padx=20, pady=10)

# Create labels and entries for first name, last name, and phone
first_name_label = tkinter.Label(frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(frame)
last_name_entry = tkinter.Entry(frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

phone_label = tkinter.Label(frame, text="Phone")
phone_label.grid(row=0, column=2)
phone_entry = tkinter.Entry(frame)
phone_entry.grid(row=1, column=2)

# Create labels and entries for quantity, description, and unit price
qty_label = tkinter.Label(frame, text="Qty")
qty_label.grid(row=2, column=0)
qty_spinbox = tkinter.Spinbox(frame, from_=1, to=100)
qty_spinbox.grid(row=3, column=0)

desc_label = tkinter.Label(frame, text="Description")
desc_label.grid(row=2, column=1)
desc_entry = tkinter.Entry(frame)
desc_entry.grid(row=3, column=1)

price_label = tkinter.Label(frame, text="Unit Price")
price_label.grid(row=2, column=2)
price_spinbox = tkinter.Spinbox(frame, from_=0.0, to=500, increment=0.5)
price_spinbox.grid(row=3, column=2)

# Button to add items to the invoice
add_item_button = tkinter.Button(frame, text="Add Item", command=add_item)
add_item_button.grid(row=4, column=2, pady=5)

# Create a treeview to display the invoice items
columns = ('qty', 'desc', 'price', 'total')
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('qty', text='Qty')
tree.heading('desc', text='Description')
tree.heading('price', text='Unit Price')
tree.heading('total', text="Total")
tree.grid(row=5, column=0, columnspan=3, padx=20, pady=10)

# Button to generate the invoice
save_invoice_button = tkinter.Button(frame, text="Generate Invoice", command=generate_invoice)
save_invoice_button.grid(row=6, column=0, columnspan=3, sticky="news", padx=20, pady=5)

# Button to create a new invoice
new_invoice_button = tkinter.Button(frame, text="New Invoice", command=new_invoice)
new_invoice_button.grid(row=7, column=0, columnspan=3, sticky="news", padx=20, pady=5)

# Run the main event loop
window.mainloop()
