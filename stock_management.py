import csv
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Create a dictionary to store the stock data, organized by product code, renk, and color code
stock = {}

# Create a dictionary to map English month names to Turkish
month_translation = {
    "January": "Ocak",
    "February": "Şubat",
    "March": "Mart",
    "April": "Nisan",
    "May": "Mayıs",
    "June": "Haziran",
    "July": "Temmuz",
    "August": "Ağustos",
    "September": "Eylül",
    "October": "Ekim",
    "November": "Kasım",
    "December": "Aralık"
}

# Function to format the date with Turkish month names
def format_turkish_date(date_str):
    for eng_month, tr_month in month_translation.items():
        date_str = date_str.replace(eng_month, tr_month)
    return date_str

# Function to add stock
def add_stock():
    product_code = product_code_entry.get()
    renk = renk_entry.get()
    color_code = color_code_entry.get()
    stock_amount = stock_amount_entry.get()

    if not product_code or not color_code or not renk or not stock_amount:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    try:
        stock_amount = int(stock_amount)
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir stok miktarı girin.")
        return

    current_time = datetime.datetime.now()
    current_date = format_turkish_date(current_time.strftime("%d %B %Y"))
    current_time_str = current_time.strftime("%H:%M")

    if product_code in stock:
        if renk in stock[product_code]:
            if color_code in stock[product_code][renk]:
                stock[product_code][renk][color_code]['stok_adet_gelen'] += stock_amount
            else:
                stock[product_code][renk][color_code] = {
                    'stok_adet_gelen': stock_amount,
                    'date': current_date,
                    'time': current_time_str
                }
        else:
            stock[product_code][renk] = {
                color_code: {
                    'stok_adet_gelen': stock_amount,
                    'date': current_date,
                    'time': current_time_str
                }
            }
    else:
        stock[product_code] = {
            renk: {
                color_code: {
                    'stok_adet_gelen': stock_amount,
                    'date': current_date,
                    'time': current_time_str
                }
            }
        }

    display_stock()

# Function to display the current stock
def display_stock():
    tree.delete(*tree.get_children())  # Clear the treeview

    for product_code, renk_data in stock.items():
        for renk, color_data in renk_data.items():
            for color_code, details in color_data.items():
                tree.insert("", "end", values=(product_code, renk, color_code, details['stok_adet_gelen'], details['date'], details['time']))

# Function to save stock data to a CSV file
def save_stock_to_csv():
    with open('stock_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Ürün Kodu", "Renk", "Renk Kodu", "Gelen Stok Adeti", "Eklenen Tarih", "Eklenen Saat"])
        for product_code, renk_data in stock.items():
            for renk, color_data in renk_data.items():
                for color_code, details in color_data.items():
                    writer.writerow([product_code, renk, color_code, details['stok_adet_gelen'], details['date'], details['time']])

    messagebox.showinfo("Başarı", "Stok verileri stock_data.csv dosyasına kaydedildi")

# Function to search for a product by product code, renk, color code, or date
def search_product(query):
    results = []
    for product_code, renk_data in stock.items():
        for renk, color_data in renk_data.items():
            for color_code, details in color_data.items():
                if query.lower() in product_code.lower() or query.lower() in renk.lower() or query.lower() in color_code.lower() or query.lower() in details['date'].lower():
                    results.append((product_code, renk, color_code, details['stok_adet_gelen'], details['date'], details['time']))

    if results:
        display_search_results(results)
    else:
        messagebox.showinfo("Sonuç Yok", "Eşleşen ürün bulunamadı.")

# Function to display search results in a new window
def display_search_results(results):
    search_results_window = tk.Toplevel(root)
    search_results_window.title("Arama Sonuçları")

    search_tree = ttk.Treeview(search_results_window, columns=("Ürün Kodu", "Renk", "Renk Kodu", "Gelen Stok Adeti", "Eklenen Tarih", "Eklenen Saat"), show="headings")
    search_tree.heading("Ürün Kodu", text="Ürün Kodu")
    search_tree.heading("Renk", text="Renk")
    search_tree.heading("Renk Kodu", text="Renk Kodu")
    search_tree.heading("Gelen Stok Adeti", text="Gelen Stok Adeti")
    search_tree.heading("Eklenen Tarih", text="Eklenen Tarih")
    search_tree.heading("Eklenen Saat", text="Eklenen Saat")

    # Set column alignment to center for all columns
    for col in ("Ürün Kodu", "Renk", "Renk Kodu", "Gelen Stok Adeti", "Eklenen Tarih", "Eklenen Saat"):
        search_tree.column(col, anchor="center")

    for result in results:
        search_tree.insert("", "end", values=result)

    search_tree.pack(padx=10, pady=10, fill="both", expand=True)

def update_logo_position():
    # Logo görüntüsünün güncel konumu ve boyutu
    logo_x = 0.9 * root.winfo_width()  # Örnek bir oranla x koordinatı hesaplaması
    logo_y = 10  # Y koordinatı
    logo_width = 100  # Logo genişliği
    logo_height = 100  # Logo yüksekliği

    # Logo görüntüsünün konumunu ve boyutunu güncelle
    logo_label.place(x=logo_x, y=logo_y, width=logo_width, height=logo_height)



# Create the main application window
root = tk.Tk()
root.title("Vostro Çanta Stok Yönetim Paneli")

# Create a frame for adding stock
add_stock_frame = ttk.Frame(root)
add_stock_frame.pack(padx=10, pady=10, anchor="w")

# Add stock entry fields and labels
product_code_label = ttk.Label(add_stock_frame, text="Ürün Kodu:")
product_code_label.grid(row=0, column=0, padx=5, pady=5)

product_code_entry = ttk.Entry(add_stock_frame)
product_code_entry.grid(row=0, column=1, padx=5, pady=5)

renk_label = ttk.Label(add_stock_frame, text="Renk:")
renk_label.grid(row=0, column=2, padx=5, pady=5)

renk_entry = ttk.Entry(add_stock_frame)
renk_entry.grid(row=0, column=3, padx=5, pady=5)

color_code_label = ttk.Label(add_stock_frame, text="Renk Kodu:")
color_code_label.grid(row=1, column=0, padx=5, pady=5)

color_code_entry = ttk.Entry(add_stock_frame)
color_code_entry.grid(row=1, column=1, padx=5, pady=5)

stock_amount_label = ttk.Label(add_stock_frame, text="Gelen Stok Adeti:")
stock_amount_label.grid(row=1, column=2, padx=5, pady=5)

stock_amount_entry = ttk.Entry(add_stock_frame)
stock_amount_entry.grid(row=1, column=3, padx=5, pady=5)

add_stock_button = ttk.Button(add_stock_frame, text="Stok Ekle", command=add_stock)
add_stock_button.grid(row=2, columnspan=4, pady=10)

# Create and configure the treeview widget for displaying stock data
tree = ttk.Treeview(root, columns=("Ürün Kodu", "Renk", "Renk Kodu", "Gelen Stok Adeti", "Eklenen Tarih", "Eklenen Saat"), show="headings")
tree.heading("Ürün Kodu", text="Ürün Kodu")
tree.heading("Renk", text="Renk")
tree.heading("Renk Kodu", text="Renk Kodu")
tree.heading("Gelen Stok Adeti", text="Gelen Stok Adeti")
tree.heading("Eklenen Tarih", text="Eklenen Tarih")
tree.heading("Eklenen Saat", text="Eklenen Saat")

# Set column alignment to center for all columns
for col in ("Ürün Kodu", "Renk", "Renk Kodu", "Gelen Stok Adeti", "Eklenen Tarih", "Eklenen Saat"):
    tree.column(col, anchor="center")

# Create a scrollbar for the treeview
tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scrollbar.set)

# Pack the treeview and scrollbar
tree.pack(padx=10, pady=10, fill="both", expand=True)
tree_scrollbar.pack(side="right", fill="y")

# Load the logo image
logo_image = Image.open("logo.JPG")
logo_image = ImageTk.PhotoImage(logo_image)

# Create a label to display the logo
logo_label = ttk.Label(root, image=logo_image)
logo_label.place(x=1110, y=1, width=100, height=100)  # Adjust width and height as needed

# Ensure that the image reference is not garbage collected
logo_label.image = logo_image



# Create menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Dosya", menu=file_menu)
file_menu.add_command(label="Stok Verilerini Kaydet (CSV)", command=save_stock_to_csv)
file_menu.add_separator()
file_menu.add_command(label="Çıkış", command=root.destroy)

search_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Ara", menu=search_menu)
search_menu.add_command(label="Ürün Ara", command=lambda: search_product(search_entry.get()))

search_frame = ttk.Frame(root)
search_frame.pack(padx=10, pady=10, anchor="ne")

search_label = ttk.Label(search_frame, text="Arama:")
search_label.grid(row=0, column=0, padx=5, pady=5)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Ara", command=lambda: search_product(search_entry.get()))
search_button.grid(row=0, column=2, padx=5, pady=5)


root.bind("<Configure>", lambda event: update_logo_position()) # call the function when the screen size changes

update_logo_position()  # begining place of the logo

# Main program loop
root.mainloop()
