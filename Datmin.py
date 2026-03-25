import kagglehub
import pandas as pd
import os

print("Memeriksa dan menyiapkan dataset...")
# 1. Download dataset dan simpan lokasinya di variabel 'dataset_path'
dataset_path = kagglehub.dataset_download("dnkumars/industrial-equipment-monitoring-dataset")
print(f"Lokasi folder dataset: {dataset_path}")

# 2. Menggabungkan lokasi folder dengan nama file CSV
# Pastikan nama file CSV sesuai dengan yang ada di dataset Kaggle tersebut
file_path = os.path.join(dataset_path, "equipment_anomaly_data.csv")

# 3. Membaca data ke dalam tabel Pandas (DataFrame)
df = pd.read_csv(file_path)

# 4. Menampilkan 5 baris pertama untuk memastikan data terbaca
print("\n--- 5 Baris Pertama Data ---")
print(df.head())

# 5. Mengecek informasi kolom
print("\n--- Informasi Dataset ---")
df.info()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, classification_report

print("\n--- Memulai Proses Data Mining ---")

# 1. Pengecekan dan Penghapusan Data Kosong (Missing Values)
jumlah_kosong_awal = df.isnull().sum().sum()
df.dropna(inplace=True)
print(f"-> Tahap 1: {jumlah_kosong_awal} baris data kosong telah dihapus.")

# 2. Drop kolom 'location' dan Encoding data teks
# ALASAN DROP: Lokasi (location) biasanya tidak memiliki korelasi langsung secara fisik 
# terhadap kerusakan mesin. Memasukkan lokasi justru berisiko membuat model menjadi bias 
# (misal: menganggap mesin di kota A pasti rusak) padahal yang menentukan kerusakan 
# adalah metrik fisik seperti suhu, getaran, dll.
if 'location' in df.columns:
    df.drop('location', axis=1, inplace=True)
    print("-> Tahap 2: Kolom 'location' berhasil dihapus karena tidak relevan secara fisik.")

# Encoding kolom teks lain (misalnya 'equipment' atau jenis mesin) menjadi angka
encoder = LabelEncoder()
# Ganti 'equipment' dengan nama kolom yang berisi teks jenis mesin jika berbeda
if 'equipment' in df.columns:
    df['equipment'] = encoder.fit_transform(df['equipment'])
    print("-> Tahap 2: Kolom 'equipment' berhasil diubah menjadi angka (Encoding).")

# 3. Memisahkan Fitur (X) dan Target (y)
# Asumsi nama kolom target adalah 'faulty' (0 = normal, 1 = rusak)
# Sesuaikan jika nama kolom target di dataset aslinya berbeda
X = df.drop('faulty', axis=1)
y = df['faulty']
print("-> Tahap 3: Fitur (X) dan Target (y) berhasil dipisahkan.")

# Pembagian data latih (80%) dan data uji (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# WAJIB UNTUK KNN: Standarisasi Data (Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Pemodelan dengan K-Nearest Neighbors (KNN)
# Kita mulai dengan K=5 (mencari 5 tetangga terdekat)
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_scaled, y_train)
print("-> Tahap 4: Model KNN selesai dilatih.")

# Melakukan prediksi pada data uji
y_pred = knn_model.predict(X_test_scaled)

# 5. Evaluasi dengan Precision dan Recall
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print("\n--- Hasil Evaluasi Model KNN ---")
print(f"Precision : {precision:.2f} (Dari semua yang diprediksi rusak, berapa persen yang benar-benar rusak?)")
print(f"Recall    : {recall:.2f} (Dari semua mesin yang aslinya rusak, berapa persen yang berhasil ditebak model?)")

print("\nLaporan Lengkap (Classification Report):")
print(classification_report(y_test, y_pred))


import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

print("\n--- Membuat Visualisasi Confusion Matrix ---")

# 1. Menghitung matriks konfusi (angka mentah)
cm = confusion_matrix(y_test, y_pred)

# 2. Mengatur ukuran dan estetika gambar grafik
plt.figure(figsize=(8, 6)) # Ukuran gambar (lebar, tinggi) dalam inci
sns.set(font_scale=1.2) # Mengatur ukuran font agar mudah dibaca

# 3. Membuat Heatmap (peta panas) dengan Seaborn
# annot=True: Menampilkan angka di dalam kotak
# fmt='g': Menampilkan angka format standar (bukan notasi ilmiah)
# cmap='Blues': Memberikan tema warna biru (makin gelap makin tinggi angkanya)
ax = sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', cbar=False)

# 4. Memberikan Label dan Judul Grafik agar informatif
ax.set_title('Visualisasi Confusion Matrix (Model KNN)', fontsize=16, pad=20)
ax.set_xlabel('Hasil Prediksi Model', fontsize=14)
ax.set_ylabel('Kondisi Sebenarnya (Aktual)', fontsize=14)

# Mengubah label angka 0/1 menjadi Normal/Faulty agar mudah dipahami
ax.xaxis.set_ticklabels(['✅ Normal', '⚠️ Faulty'])
ax.yaxis.set_ticklabels(['✅ Normal', '⚠️ Faulty'])

# Menambahkan sedikit rotasi agar label tidak tumpang tindih
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# Menyesuaikan tata letak agar tidak terpotong
plt.tight_layout()

# 5. Menampilkan grafik ke layar
print("-> Grafik Confusion Matrix sedang dimuat... (Mohon tutup jendela grafik untuk lanjut ke tahap input manual)")
plt.show()


# ==========================================
# 6. Simulasi Input Pengguna untuk Prediksi
# ==========================================
print("\n" + "="*50)
print("SISTEM PREDIKSI KONDISI MESIN (MANUAL INPUT)")
print("="*50)

# Menampilkan panduan kode 'equipment' jika kolom tersebut ada
# Agar pengguna tahu harus mengetik angka berapa untuk jenis mesin tertentu
if 'equipment' in X.columns:
    print("Panduan Kode 'equipment':")
    for i, kelas in enumerate(encoder.classes_):
        print(f"- Ketik {i} untuk mesin jenis: {kelas}")
    print("-" * 30)

# Membuat dictionary untuk menyimpan input dari terminal
data_input = {}

# Looping otomatis meminta input berdasarkan kolom yang dipakai model
print("\nSilakan masukkan parameter metrik mesin saat ini:")
for col in X.columns:
    while True:
        try:
            # Meminta input dan langsung mengubahnya menjadi angka desimal (float)
            nilai = float(input(f"Masukkan nilai untuk {col}: "))
            data_input[col] = [nilai] # Disimpan dalam bentuk list agar mudah jadi DataFrame
            break # Keluar dari loop jika input valid berupa angka
        except ValueError:
            print("⚠️ Error: Harap masukkan angka yang valid!")

# Mengubah input dictionary menjadi Pandas DataFrame
df_input = pd.DataFrame(data_input)

# WAJIB: Melakukan Scaling pada data input baru menggunakan scaler dari tahap training
# Perhatikan kita menggunakan .transform(), bukan .fit_transform()
df_input_scaled = scaler.transform(df_input)

# Meminta model melakukan prediksi
hasil_prediksi = knn_model.predict(df_input_scaled)

# Menampilkan hasil prediksi ke layar
print("\n" + "="*50)
print("HASIL ANALISIS MESIN")
print("="*50)

if hasil_prediksi[0] == 1.0:
    print("⚠️ STATUS: MESIN BERPOTENSI RUSAK (FAULTY)!")
    print("Tindakan: Segera jadwalkan inspeksi teknisi dan hentikan operasi jika perlu.")
else:
    print("✅ STATUS: MESIN NORMAL / SEHAT.")
    print("Tindakan: Lanjutkan operasi sesuai jadwal standar.")
print("="*50 + "\n")