import json
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm untuk progress bar

# Fungsi untuk mengonversi harga ke dalam bentuk angka
def convert_price(price_str):
    # Menghapus 'Rp' dan karakter non-numerik, lalu mengubahnya menjadi integer
    return int(price_str.replace('Rp', '').replace('.', '').strip())

# Fungsi untuk memfilter produk berdasarkan kata kunci
def filter_by_keyword(products, keyword):
    return [product for product in products if keyword.lower() in product['name'].lower()]

# Nama file HTML di direktori yang sama
file_name = "input.html"

# Meminta pengguna untuk memasukkan kata kunci
keyword = input("Masukkan kata kunci produk yang ingin ditampilkan: ").strip()

# Membuka file HTML
with open(file_name, "r", encoding="utf-8") as file:
    html = file.read()

# Parsing HTML dengan BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Ambil semua elemen produk
produk_elements = soup.find_all('a', class_='contents')  # Ganti dengan selector yang sesuai jika berbeda

# Daftar untuk menyimpan produk dan harga
produk_list = []

# Menggunakan tqdm untuk progress bar saat iterasi
for produk in tqdm(produk_elements, desc="Scraping Produk", unit="produk"):
    # Ambil nama produk
    product_name = produk.select_one('.line-clamp-2').get_text(strip=True)
    
    # Ambil harga produk
    price = produk.find('span', class_='text-base/5').get_text(strip=True)
    
    # Ambil link produk
    product_link = produk['href']
    
    # Konversi harga ke angka untuk sorting
    price_int = convert_price(price)
    
    # Menyimpan data produk dalam list
    produk_list.append({
        'name': product_name,
        'price': price_int,
        'link': 'https://shopee.co.id' + product_link,
    })

# Filter produk berdasarkan kata kunci
filtered_produk_list = filter_by_keyword(produk_list, keyword)

# Menampilkan jumlah produk yang sesuai
jumlah_produk = len(filtered_produk_list)
print(f"Jumlah produk yang sesuai dengan kata kunci '{keyword}': {jumlah_produk}")

# Jika tidak ada produk yang cocok
if not filtered_produk_list:
    print(f"Tidak ada produk yang cocok dengan kata kunci '{keyword}'.")
else:
    # Urutkan produk berdasarkan harga (dari yang terendah)
    produk_list_sorted = sorted(filtered_produk_list, key=lambda x: x['price'])

    # Menyimpan hasil ke dalam file JSON
    output_filename = f"produk_{keyword}.json"
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(produk_list_sorted, json_file, ensure_ascii=False, indent=4)

    print(f"Hasil scraping telah disimpan dalam file: {output_filename}")
    
    # Tampilkan produk yang sudah disimpan
    for produk in produk_list_sorted:
        print('Nama Produk:', produk['name'])
        print('Harga Produk: Rp', format(produk['price'], ',d'))  # Format harga agar lebih rapi
        print('Link Produk:', produk['link'])
        print('-' * 40)  # Pembatas antar produk
