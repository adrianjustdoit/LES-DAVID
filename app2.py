import streamlit as st
import pywhatkit as kit
import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Sistem PPC & Notifikasi", page_icon="🏭")

st.title("🏭 Sistem Penjadwalan & Notifikasi Pekerja")
st.write("Aplikasi untuk mengatur jadwal produksi dan mengirim pengingat shift otomatis via WhatsApp.")

st.divider()

# 2. Antarmuka Web (UI)
st.header("Form Penjadwalan Shift")

with st.form("form_jadwal"):
    # Input data pekerjaan
    nama_pekerjaan = st.text_input("Nama Pekerjaan / Shift", placeholder="Contoh: Shift 1 (08.00-16.00)")
    no_wa = st.text_input("Nomor WA Teknisi (Wajib pakai +62)", value="+62")
    
    st.write("Waktu Pengiriman Pesan:")
    # Membagi kolom agar UI rapi
    col1, col2 = st.columns(2)
    
    # Otomatis mengisi nilai default dengan jam saat ini + 2 menit untuk kemudahan testing
    waktu_sekarang = datetime.datetime.now()
    menit_testing = (waktu_sekarang.minute + 2) % 60
    jam_testing = waktu_sekarang.hour if waktu_sekarang.minute + 2 < 60 else (waktu_sekarang.hour + 1) % 24

    with col1:
        jam_kirim = st.number_input("Jam (0-23)", min_value=0, max_value=23, value=jam_testing)
    with col2:
        menit_kirim = st.number_input("Menit (0-59)", min_value=0, max_value=59, value=menit_testing)
        
    # Input Pesan (bisa diedit di web)
    pesan = st.text_area("Pesan Notifikasi", value="Halo, jadwal shift kamu besok adalah [Pekerjaan].")
    
    # Tombol eksekusi
    submitted = st.form_submit_button("Jadwalkan & Siapkan WA")
    
    # 3. Logika Pengiriman pywhatkit
    if submitted:
        if nama_pekerjaan and no_wa != "+62":
            # Ganti teks [Pekerjaan] dengan inputan user
            pesan_final = pesan.replace("[Pekerjaan]", nama_pekerjaan)
            
            st.info(f"⏳ Jadwal diproses! Sistem akan membuka WhatsApp Web pada pukul {jam_kirim:02d}:{menit_kirim:02d}. JANGAN tutup web ini atau mematikan komputer.")
            
            try:
                # Menjalankan pywhatkit
                # wait_time=15: Waktu tunggu agar WA Web selesai loading
                # tab_close=True: Menutup tab WA otomatis setelah 2 detik pesan terkirim
                kit.sendwhatmsg(no_wa, pesan_final, jam_kirim, menit_kirim, wait_time=15, tab_close=True, close_time=2)
                
                st.success("✅ Pesan berhasil dikirim!")
            except Exception as e:
                st.error(f"⚠️ Terjadi kesalahan: {e}")
        else:
            st.warning("⚠️ Mohon lengkapi Nama Pekerjaan dan pastikan Nomor WA sudah benar.")