import streamlit as st

# 1. Mengatur konfigurasi halaman web (UI/UX)
st.set_page_config(page_title="Kalkulator Bahan Baku", page_icon="🏭")

# 2. Membuat Judul dan Deskripsi
st.title("🏭 Kalkulator Kebutuhan Bahan Baku")
st.write("Aplikasi ini digunakan untuk menghitung total bahan baku yang dibutuhkan berdasarkan target produksi.")

st.divider() # Membuat garis pembatas

# 3. Bagian Input Pengguna
st.header("Tahap 1: Input Rencana Produksi")
# Membuat kolom input angka. Nilai minimal 0, nilai awal (default) 50.
target_produksi = st.number_input("Berapa jumlah kursi yang ingin diproduksi?", min_value=0, value=50)

# 4. Logika Perhitungan (Contoh: Bill of Materials untuk 1 Kursi)
# Asumsi 1 kursi butuh: 2 meter kayu, 15 buah sekrup, dan 0.5 liter cat
kayu_per_kursi = 2
sekrup_per_kursi = 15
cat_per_kursi = 0.5

total_kayu = target_produksi * kayu_per_kursi
total_sekrup = target_produksi * sekrup_per_kursi
total_cat = target_produksi * cat_per_kursi

st.divider()

# 5. Bagian Output Hasil
st.header("Tahap 2: Hasil Kebutuhan Bahan Baku")

if target_produksi > 0:
    st.success(f"Untuk memproduksi **{target_produksi} kursi**, Anda harus menyiapkan bahan baku berikut:")
    
    # Menggunakan fitur 'columns' agar tampilan metrik sejajar ke samping (UI/UX bagus)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Kayu Solid", value=f"{total_kayu} Meter")
    with col2:
        st.metric(label="Sekrup", value=f"{total_sekrup} Pcs")
    with col3:
        st.metric(label="Cat Plitur", value=f"{total_cat} Liter")
else:
    st.warning("Silakan masukkan jumlah produksi lebih dari 0 untuk melihat hasil.")