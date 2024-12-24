import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Misalkan Anda memiliki data dalam file CSV
day = pd.read_csv("dashboard/day.csv")

# Pastikan kolom 'date' adalah tipe datetime
day['dteday'] = pd.to_datetime(day['dteday'])

# Ekstrak bulan dari kolom 'date' dan simpan di kolom 'mnth'
day['mnth'] = day['dteday'].dt.month

# Kelompokkan berdasarkan bulan ('mnth') dan jumlahkan 'cnt'
jumlah_penyewa_perbulan = day.groupby('mnth')['cnt'].sum().reset_index()

# Ambil 12 bulan dengan jumlah penyewa terbanyak
top_12_months = jumlah_penyewa_perbulan.nlargest(n=12, columns='cnt')

# Tampilkan hasil
print(top_12_months)

# Judul aplikasi
st.title("Analisis Penyewaan Sepeda di Pecatu Bicycle")
st.sidebar.header("Pilihan Analisis")

# Radio button untuk memilih analisis
menu = st.sidebar.radio(
    "Pilih Analisis",
    options=[
        "Penyewaan Sepeda Per Bulan",
        "Perubahan Penyewaan Sepeda Per Tahun",
        "Pengaruh Hari Libur dan Akhir Pekan",
        "Pengaruh Musim terhadap Penyewaan"
    ]
)

if menu == "Penyewaan Sepeda Per Bulan":
    st.header("Analisis Penyewaan Sepeda Per Bulan")

    # Menghitung jumlah total penyewa sepeda per bulan
    jumlah_penyewa_perbulan = day.groupby('mnth')['cnt'].sum().reset_index().nlargest(n=12, columns='cnt')

    # Menampilkan tabel hasil
    st.write("Jumlah penyewa sepeda per bulan:")
    st.dataframe(jumlah_penyewa_perbulan)

    # Grafik batang
    fig, ax = plt.subplots()
    ax.bar(
        x=jumlah_penyewa_perbulan['mnth'],
        height=jumlah_penyewa_perbulan['cnt'],
        color='green'
    )
    ax.set_xticks(range(1, 13))
    ax.set_title('Banyaknya Penyewa Sepeda Setiap Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewa')
    st.pyplot(fig)

    # Menentukan bulan tertinggi dan terendah
    penyewa_bulan_terendah = jumlah_penyewa_perbulan.sort_values(by='cnt', ascending=True).head(1)
    st.write(f"Bulan dengan penyewa sepeda tertinggi adalah bulan {jumlah_penyewa_perbulan.iloc[0, 0]}.")
    st.write(f"Bulan dengan penyewa sepeda terendah adalah bulan {penyewa_bulan_terendah.iloc[0, 0]}.")

elif menu == "Perubahan Penyewaan Sepeda Per Tahun":
    st.header("Perubahan Penyewaan Sepeda Per Tahun")

    # Menghitung jumlah dan rata-rata penyewa per tahun
    jumlah_penyewa_per_tahun = day.groupby(by='yr')['cnt'].sum().reset_index()
    rata2_penyewa_per_tahun = day.groupby(by='yr')['cnt'].mean().reset_index()

    # Grafik jumlah penyewa
    fig, ax = plt.subplots()
    sns.barplot(data=jumlah_penyewa_per_tahun, x='yr', y='cnt', palette=['green', 'yellow'], ax=ax)
    ax.set_title('Jumlah Penyewa Sepeda Setiap Tahun')
    st.pyplot(fig)

    # Grafik rata-rata penyewa
    fig, ax = plt.subplots()
    sns.barplot(data=rata2_penyewa_per_tahun, x='yr', y='cnt', palette=['green', 'yellow'], ax=ax)
    ax.set_title('Rata-rata Penyewa Sepeda Per Tahun')
    st.pyplot(fig)

elif menu == "Pengaruh Hari Libur dan Akhir Pekan":
    st.header("Pengaruh Hari Libur dan Akhir Pekan")

    # Hari libur/akhir pekan vs hari kerja
    holiday = day[(day['holiday'] == 1) | (day['weekday'] == 0)]
    harikerja = day[day['workingday'] == 1]

    # Uji statistik ANOVA
    f_statistic, p_value = stats.f_oneway(holiday['cnt'], harikerja['cnt'])
    if p_value < 0.05:
        st.write('Terdapat perbedaan signifikan antara jumlah penyewa di hari libur/pekan dengan hari kerja.')
    else:
        st.write('Tidak ada perbedaan signifikan antara jumlah penyewa di hari libur/pekan dengan hari kerja.')

    # Rata-rata penyewa
    holiday_mean = holiday['cnt'].mean()
    harikerja_mean = harikerja['cnt'].mean()

    # Visualisasi
    dict = {
        'Jenis': ['Hari Libur/ Pekan', 'Hari Kerja'],
        'Rata-rata Penyewa': [holiday_mean, harikerja_mean]
    }
    new_df = pd.DataFrame(dict)

    fig, ax = plt.subplots()
    ax.bar(new_df['Jenis'], new_df['Rata-rata Penyewa'], color=['red', 'green'])
    ax.set_title('Rata-rata Penyewa Sepeda')
    ax.set_ylabel('Jumlah Penyewa')
    st.pyplot(fig)

elif menu == "Pengaruh Musim terhadap Penyewaan":
    st.header("Pengaruh Musim terhadap Penyewaan")

    # Diagram pai musim
    biggest_season = day.groupby('season')['cnt'].sum().reset_index()
    fig, ax = plt.subplots()
    colors = ['green', 'silver', 'red', 'yellow']
    ax.pie(
        biggest_season['cnt'],
        autopct='%1.1f%%',
        labels=['Winter', 'Spring', 'Summer', 'Fall'],
        shadow=True,
        explode=(0, 0, 0.1, 0),
        colors=colors
    )
    ax.set_title('Musim dengan Penyewa Sepeda Terbanyak')
    st.pyplot(fig)
