import streamlit as st


# 1. Konfigurasi Halaman (Wajib diletakkan paling atas)
# Mengatur tata letak web menjadi 'wide' agar lebih luas
st.set_page_config(page_title="Sistem Informasi PPC", page_icon="⚙️", layout="wide")

# ==========================================
# BAGIAN MENU NAVIGASI (SIDEBAR)
# ==========================================
st.sidebar.title("⚙️ Navigasi Utama")
st.sidebar.write("Silakan pilih menu aplikasi:")

# Membuat pilihan menu menggunakan tombol radio
menu = st.sidebar.radio("Daftar Menu", ["Kalkulator Bahan Baku", "Penjadwalan & Notifikasi WA","Penjadwalan Produksi"])

st.sidebar.divider()
st.sidebar.info("Dashboard ini dirancang untuk mendukung sistem Production Planning and Control (PPC).")

# ==========================================
# HALAMAN 1: KALKULATOR BAHAN BAKU
# ==========================================
if menu == "Kalkulator Bahan Baku":
    st.title("🏭 Kalkulator Kebutuhan Bahan Baku")
    st.write("Aplikasi ini digunakan untuk menghitung total bahan baku yang dibutuhkan berdasarkan target produksi.")
    st.divider()

    st.header("Tahap 1: Input Rencana Produksi")
    # Membatasi rentang nilai yang bisa diinput
    target_produksi = st.number_input("Berapa jumlah kursi yang ingin diproduksi?", min_value=0, value=50, step=1)

    # Logika Perhitungan (Bill of Materials untuk 1 Kursi)
    kayu_per_kursi = 2
    sekrup_per_kursi = 15
    cat_per_kursi = 0.5

    total_kayu = target_produksi * kayu_per_kursi
    total_sekrup = target_produksi * sekrup_per_kursi
    total_cat = target_produksi * cat_per_kursi

    st.divider()

    st.header("Tahap 2: Hasil Kebutuhan Bahan Baku")
    if target_produksi > 0:
        st.success(f"Untuk memproduksi **{target_produksi} kursi**, Anda harus menyiapkan bahan baku berikut:")
        
        # Menggunakan kolom agar tampilan rapi
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Kayu Solid", value=f"{total_kayu} Meter")
        with col2:
            st.metric(label="Sekrup", value=f"{total_sekrup} Pcs")
        with col3:
            st.metric(label="Cat Plitur", value=f"{total_cat} Liter")
    else:
        st.warning("Silakan masukkan jumlah produksi lebih dari 0 untuk melihat hasil.")


# ==========================================
# HALAMAN 2: PENJADWALAN & NOTIFIKASI WA
# ==========================================
elif menu == "Penjadwalan & Notifikasi WA":
    st.title("📅 Sistem Penjadwalan & Notifikasi Pekerja")
    st.write("Aplikasi untuk mengatur jadwal produksi dan mengirim pengingat shift otomatis via WhatsApp.")
    st.divider()

    st.header("Form Penjadwalan Shift")

    with st.form("form_jadwal"):
        nama_pekerjaan = st.text_input("Nama Pekerjaan / Shift", placeholder="Contoh: Shift 1 (08.00-16.00)")
        no_wa = st.text_input("Nomor WA Teknisi (Wajib pakai +62)", value="+62")
        
        st.write("Waktu Pengiriman Pesan (Gunakan format 24 Jam):")
        col1, col2 = st.columns(2)
        
        # Logika untuk mencari jam saat ini dan menambahkan 2 menit untuk testing

        with col1:
            jam_kirim = st.number_input("Jam (0-23)", min_value=0, max_value=23, value=jam_testing)
        with col2:
            menit_kirim = st.number_input("Menit (0-59)", min_value=0, max_value=59, value=menit_testing)
            
        pesan = st.text_area("Pesan Notifikasi", value="Halo, jadwal shift kamu besok adalah [Pekerjaan].")
        
        submitted = st.form_submit_button("Jadwalkan & Siapkan WA")
        
        if submitted:
            if nama_pekerjaan and no_wa != "+62" and len(no_wa) > 10:
                pesan_final = pesan.replace("[Pekerjaan]", nama_pekerjaan)
                st.info(f"⏳ Jadwal diproses! Sistem akan membuka WhatsApp Web secara otomatis pada pukul {jam_kirim:02d}:{menit_kirim:02d}. JANGAN tutup web ini atau mematikan komputer.")
                
                try:
                    st.success("✅ Pesan berhasil dikirim!")
                except Exception as e:
                    st.error(f"⚠️ Terjadi kesalahan pada sistem pengiriman: {e}")
            else:
                st.warning("⚠️ Mohon lengkapi Nama Pekerjaan dan pastikan Nomor WA sudah benar (minimal 10 angka).")

# ==========================================
# HALAMAN 3: PENJADWALAN PRODUKSI
# ==========================================

elif menu == "Penjadwalan Produksi":
    st.title("📊 Penjadwalan Produksi")
    st.write("Fitur ini akan segera hadir. Nantikan update selanjutnya!")
    st.divider()
    st.info("Fitur penjadwalan produksi akan memungkinkan Anda untuk mengatur timeline produksi, mengalokasikan sumber daya, dan memantau progres secara real-time.")       
