import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
from io import BytesIO
import openpyxl 

def export_to_excel():
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Export standar
        export_list = {
            "df_data_transaksi": "Data Transaksi",
            "df_data_persediaan": "Data Persediaan",
            "df_data_beban": "Data Beban",
            "df_data_modal": "Data Modal",
            "df_neraca_saldo_periode_sebelumnya": "Neraca Saldo Periode Sebelumnya",
            "df_jurnal_umum": "Jurnal Umum",
            "df_buku_besar": "Buku Besar",
            "df_neraca_saldo": "Neraca Saldo",
            "df_laporan_laba_rugi": "Laporan Laba Rugi",
            "df_laporan_perubahan_modal": "Laporan Perubahan Modal",
            "df_laporan_posisi_keuangan": "Laporan Posisi Keuangan",
            "df_jurnal_penutup": "Jurnal Penutup",
            "df_neraca_saldo_setelah_penutup": "Neraca Saldo Setelah Penutup"
        }

        for key, sheet_name in export_list.items():
            if key in st.session_state and not st.session_state[key].empty:
                st.session_state[key].to_excel(writer, sheet_name=sheet_name, index=False)

        if "df_buku_besar" in st.session_state and not st.session_state.df_buku_besar.empty:
            df_buku_besar = st.session_state.df_buku_besar

            daftar_akun = [
                "kas", "persediaan", "perlengkapan", "aset biologis", "peralatan",
                "modal", "penjualan", "beban listrik dan air", "beban transportasi", "beban gaji"
            ]

            for akun in daftar_akun:
                df_akun = df_buku_besar[df_buku_besar["Nama Akun"].str.lower() == akun.lower()]
                if not df_akun.empty:
                    nama_sheet = akun[:31].replace('/', ' ').replace('\\', ' ').replace('*', ' ')\
                        .replace('[', ' ').replace(']', ' ').replace(':', ' ').replace('?', ' ')
                    df_akun.to_excel(writer, sheet_name=nama_sheet, index=False)

    buffer.seek(0)
    return buffer



def update_buku_besar():
    df_jurnal = st.session_state.get("df_jurnal_umum", pd.DataFrame())
    df_saldo_awal = st.session_state.get("df_neraca_saldo_periode_sebelumnya", pd.DataFrame())

    data = pd.concat([df_saldo_awal, df_jurnal], ignore_index=True)
    data["Debit (Rp)"] = data["Debit (Rp)"].fillna(0)
    data["Kredit (Rp)"] = data["Kredit (Rp)"].fillna(0)

    buku_besar = data.groupby("Nama Akun")[["Debit (Rp)", "Kredit (Rp)"]].sum().reset_index()
    buku_besar["Saldo (Rp)"] = buku_besar["Debit (Rp)"] - buku_besar["Kredit (Rp)"]

    st.session_state.df_buku_besar = buku_besar

    df_akun_template = pd.DataFrame({"Nama Akun": [
        "Kas", "Persediaan", "Perlengkapan", "Aset biologis", "Peralatan",
        "Penjualan", "Modal", "Beban listrik dan air", "Beban transportasi", "Beban gaji"]})

    neraca = df_akun_template.merge(buku_besar, on="Nama Akun", how="left").fillna(0)

    neraca_final = []
    for _, row in neraca.iterrows():
        debit = row["Debit (Rp)"] if row["Saldo (Rp)"] >= 0 else 0
        kredit = -row["Saldo (Rp)"] if row["Saldo (Rp)"] < 0 else 0
        neraca_final.append({"Nama Akun": row["Nama Akun"], "Debit (Rp)": debit, "Kredit (Rp)": kredit})

    df_neraca_saldo = pd.DataFrame(neraca_final)
    df_neraca_saldo.insert(0, "No", range(1, len(df_neraca_saldo)+1))

    total_debit = df_neraca_saldo["Debit (Rp)"].sum()
    total_kredit = df_neraca_saldo["Kredit (Rp)"].sum()
    total_row = {"No": "", "Nama Akun": "Total", "Debit (Rp)": total_debit, "Kredit (Rp)": total_kredit}
    df_neraca_saldo = pd.concat([df_neraca_saldo, pd.DataFrame([total_row])], ignore_index=True)

    st.session_state.df_neraca_saldo = df_neraca_saldo

def hitung_laba_rugi(df_jurnal):
    kategori = {
        "Pendapatan": ["Penjualan"],
        "Beban": ["Beban listrik dan air", "Beban kendaraan", "Beban gaji"]
    }

    df_jurnal = df_jurnal.copy()
    df_jurnal["Debit (Rp)"] = df_jurnal["Debit (Rp)"].fillna(0)
    df_jurnal["Kredit (Rp)"] = df_jurnal["Kredit (Rp)"].fillna(0)

    pendapatan = df_jurnal[df_jurnal["Nama Akun"].isin(kategori["Pendapatan"])]
    beban = df_jurnal[df_jurnal["Nama Akun"].isin(kategori["Beban"])]

    total_pendapatan = pendapatan["Kredit (Rp)"].sum()
    total_beban = beban["Debit (Rp)"].sum()
    laba_bersih = total_pendapatan - total_beban

    return total_pendapatan, total_beban, laba_bersih

def hitung_perubahan_modal(laba_bersih, modal_awal):
    perubahan_modal = {
        "Modal Awal 31 Maret": modal_awal,
        "Laba Bersih": laba_bersih,
        "Penambahan Modal": 0,
        "Modal Akhir 30 April": modal_awal + laba_bersih
    }
    return pd.DataFrame.from_dict(perubahan_modal, orient="index", columns=["Nilai (Rp)"])

def hitung_posisi_keuangan(df_buku_besar):
    akun_aset_lancar = ["Kas", "Persediaan", "Perlengkapan"]
    akun_aset_tidak_lancar = ["Peralatan", "Aset biologis"]
    akun_liabilitas = ["Utang gaji", "Utang bank"]
    akun_ekuitas = ["Modal"]

    def total_akun(akun_list, kategori):
        df = df_buku_besar[df_buku_besar["Nama Akun"].isin(akun_list)]
        df = df.groupby("Nama Akun")["Saldo (Rp)"].last().reset_index()
        df["Kategori"] = kategori
        return df

    aset_lancar = total_akun(akun_aset_lancar, "Aset Lancar")
    aset_tidak_lancar = total_akun(akun_aset_tidak_lancar, "Aset Tidak Lancar")
    liabilitas = total_akun(akun_liabilitas, "Liabilitas")
    ekuitas = total_akun(akun_ekuitas, "Ekuitas")

    posisi = pd.concat([aset_lancar, aset_tidak_lancar, liabilitas, ekuitas], ignore_index=True)

    # Tambahkan total per kategori
    total_df = posisi.groupby("Kategori")["Saldo (Rp)"].sum().reset_index()
    total_df["Nama Akun"] = "Total " + total_df["Kategori"]
    posisi = pd.concat([posisi, total_df[["Nama Akun", "Saldo (Rp)", "Kategori"]]], ignore_index=True)

    # Tambahkan Total Aset dan Total Liabilitas + Ekuitas secara terpisah
    total_aset_value = total_df[total_df["Kategori"].isin(["Aset Lancar", "Aset Tidak Lancar"])]
    total_liab_eq_value = total_df[total_df["Kategori"].isin(["Liabilitas", "Ekuitas"])]

    total_rows = pd.DataFrame([
        {"Nama Akun": "\nTotal Aset", "Saldo (Rp)": total_aset_value["Saldo (Rp)"].sum(), "Kategori": "Ringkasan"},
        {"Nama Akun": "\nTotal Liabilitas dan Ekuitas", "Saldo (Rp)": total_liab_eq_value["Saldo (Rp)"].sum(), "Kategori": "Ringkasan"}
    ])

    posisi = pd.concat([posisi, total_rows], ignore_index=True)

    return posisi

    # user data
if "users" not in st.session_state:
    # Data default untuk user yang sudah terdaftar
    st.session_state.users = {
        "admin": "admin123",
        "nio": "nio2025"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

    # LOGIN & REGIST
if not st.session_state.logged_in:
    st.title("🔐 Autentikasi Nio Farm")

    tab_login, tab_register = st.tabs(["Login", "Registrasi"])

    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Selamat datang, {username}!")
                st.session_state.logged_in = True  
                st.session_state.username = username
                st.stop()  
            else:
                st.error("Username atau password salah.")

    with tab_register:
        new_user = st.text_input("Username Baru", key="reg_user")
        new_pass = st.text_input("Password Baru", type="password", key="reg_pass")
        confirm_pass = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")

        if st.button("Daftar"):
            if new_user.strip() == "" or new_pass.strip() == "":
                st.warning("Username dan password tidak boleh kosong.")
            elif new_user in st.session_state.users:
                st.error("Username sudah terdaftar.")
            elif new_pass != confirm_pass:
                st.error("Password dan konfirmasi tidak cocok.")
            else:
                # Daftarkan user baru
                st.session_state.users[new_user] = new_pass
                st.success("Registrasi berhasil! Silakan login.")

    # regist login berhasil
    st.stop()

# menu login regist
with st.sidebar:
    if "username" in st.session_state:
        st.markdown(f"👤 Login sebagai {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)  # Hapus username
        st.stop()  # Stop eksekusi dan tampilkan halaman logout

# Navigasi sidebar
with st.sidebar:
    selected = st.sidebar.radio("NIO FARM 🐐", 
                           ['Profile', 'Neraca Saldo Periode Sebelumnya', 'Jurnal Umum', 'Buku Besar', 'Neraca Saldo', 'Laporan Laba Rugi', 'Laporan Perubahan Modal', 'Laporan Posisi Keuangan', 'Jurnal Penutup', 'Neraca Saldo Setelah Penutup', 'Unduh Laporan Keuangan'],  # Pilihan menu
                            )


if selected == 'Profile':
        st.subheader('Profile 🐐')
        st.write("""Nio Farm adalah usaha rumah tangga yang bergerak di bidang produksi susu kambing yang telah berdiri sejak 2020. Kambing di Nio Farm senantiasa dipastikan kesehatan, kualitas pakan, serta kebersihan kandangnya. Setiap tetes susu yang dihasilkan adalah hasil dari perawatan alami dan proses yang bersih sehingga menghasilkan susu kambing yang segar, aman dikonsumsi, dan baik bagi kesehatan.""")
        st.write('Jl. Pamongan Sari No.90, Pedurungan Lor, Kec. Pedurungan, Kota Semarang, Jawa Tengah 50192')

    # Halaman Neraca Saldo Periode Sebelumnya
elif selected == 'Neraca Saldo Periode Sebelumnya':
    st.subheader('Neraca Saldo Periode Sebelumnya 🧾')
    st.markdown('Periode 31 Maret 2025')

    if "df_neraca_saldo_periode_sebelumnya" not in st.session_state:
        st.session_state.df_neraca_saldo_periode_sebelumnya = pd.DataFrame(
            columns=["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]
        )

    with st.form("form_tambah_transaksi_neraca_saldo_periode_sebelumnya", clear_on_submit=True):
        nama_akun = st.selectbox("Nama Akun", ["Kas", "Persediaan", "Perlengkapan", "Aset biologis", "Peralatan", "Modal"])
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        tambah = st.form_submit_button("Tambah Transaksi")

        if tambah:
            if debit == 0 and kredit == 0:
                st.warning("Isi salah satu nilai Debit atau Kredit.")
            else:
                nomor = len(st.session_state.df_neraca_saldo_periode_sebelumnya) + 1
                row = {"No": nomor, "Nama Akun": nama_akun, "Debit (Rp)": debit, "Kredit (Rp)": kredit}
                st.session_state.df_neraca_saldo_periode_sebelumnya = pd.concat([
                    st.session_state.df_neraca_saldo_periode_sebelumnya, pd.DataFrame([row])
                ], ignore_index=True)
                update_buku_besar()

    st.dataframe(st.session_state.df_neraca_saldo_periode_sebelumnya, use_container_width=True)

    # Halaman Jurnal Umum
elif selected == "Jurnal Umum":
    st.subheader("Jurnal Umum 📓")
    st.markdown("Periode April 2025")
    with st.form("form_jurnal", clear_on_submit=True):

        # Input lainnya
        if "df_jurnal_umum" not in st.session_state:
            st.session_state.df_jurnal_umum = pd.DataFrame(
            columns=["No", "Tanggal", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]
        )

    with st.form("form_tambah_jurnal", clear_on_submit=True):
        tanggal = st.date_input("Tanggal")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        tambah = st.form_submit_button("Tambah")

        if tambah:
            nomor = len(st.session_state.df_jurnal_umum) + 1
            row = {"No": nomor, "Tanggal": tanggal, "Nama Akun": nama_akun, "Debit (Rp)": debit, "Kredit (Rp)": kredit}
            st.session_state.df_jurnal_umum = pd.concat([
                st.session_state.df_jurnal_umum, pd.DataFrame([row])
            ], ignore_index=True)
            update_buku_besar()

    st.dataframe(st.session_state.df_jurnal_umum, use_container_width=True)


    # Halaman Buku Besar
elif selected == "Buku Besar":
    st.subheader("Buku Besar 📚")
    
    # Update buku besar berdasarkan jurnal umum terbaru
    update_buku_besar()

    # Ambil data dari session_state
    neraca_saldo_awal = st.session_state.get("neraca_saldo_periode_sebelumnya", {})
    jurnal_umum = st.session_state.get("jurnal_umum", pd.DataFrame())
    
    # Inisialisasi buku besar jika belum ada
    if "buku_besar" not in st.session_state:
        st.session_state["buku_besar"] = {}
    
    buku_besar = st.session_state["buku_besar"]

    # Gabungkan akun dari neraca saldo periode sebelumnya dan jurnal umum
    akun_saldo = set(neraca_saldo_awal.keys())
    akun_jurnal = set(jurnal_umum['Akun'].unique()) if not jurnal_umum.empty else set()
    semua_akun = akun_saldo.union(akun_jurnal)

    # Siapkan struktur awal untuk buku besar per akun
    for akun in semua_akun:
        if akun not in buku_besar:
            buku_besar[akun] = []

    # Tambahkan Saldo Awal dari neraca saldo periode sebelumnya
    for akun, saldo in neraca_saldo_awal.items():
        buku_besar[akun].insert(0, {
            "Tanggal": "Saldo Awal",
            "Keterangan": "",
            "Debit": saldo if saldo > 0 else 0,
            "Kredit": abs(saldo) if saldo < 0 else 0,
            "Saldo": saldo
        })

    # Tambahkan transaksi dari jurnal umum
    if not jurnal_umum.empty:
        for akun in semua_akun:
            # Ambil saldo awal dari entri pertama, default ke 0
            saldo = next((entry['Saldo'] for entry in buku_besar[akun] if entry['Tanggal'] == "Saldo Awal"), 0)
            
            # Ambil semua transaksi jurnal untuk akun ini
            transaksi_akun = jurnal_umum[jurnal_umum["Akun"] == akun]

            for _, row in transaksi_akun.iterrows():
                debit = row["Debit"]
                kredit = row["Kredit"]
                saldo += debit - kredit

                buku_besar[akun].append({
                    "Tanggal": row["Tanggal"],
                    "Keterangan": row["Keterangan"],
                    "Debit": debit,
                    "Kredit": kredit,
                    "Saldo": saldo
                })

    # Simpan kembali buku besar yang sudah diperbarui
    st.session_state["buku_besar"] = buku_besar

    # Tampilkan Buku Besar per akun
    if buku_besar:
        for akun, transaksi in buku_besar.items():
            st.subheader(f"Akun: {akun}")
            st.dataframe(pd.DataFrame(transaksi))
    else:
        st.info("Buku Besar kosong. Tambahkan transaksi terlebih dahulu.")
    
    # Halaman Neraca Saldo
elif selected == "Neraca Saldo":
    st.subheader("Neraca Saldo 📋")
    update_buku_besar()
    df_neraca = st.session_state.get("df_neraca_saldo", pd.DataFrame())
    st.dataframe(df_neraca.style.format({
        "Debit (Rp)": "Rp {:,.0f}",
        "Kredit (Rp)": "Rp {:,.0f}"
    }), use_container_width=True)

            # Halaman Laporan Laba Rugi
elif selected == "Laporan Laba Rugi":
    st.subheader("Laporan Laba Rugi 📊")
    df_jurnal = st.session_state.get("df_jurnal_umum", pd.DataFrame())
    pendapatan, beban, laba_bersih = hitung_laba_rugi(df_jurnal)
    st.metric("Pendapatan", f"Rp {pendapatan:,.0f}")
    st.metric("Beban", f"Rp {beban:,.0f}")
    st.metric("Laba Bersih", f"Rp {laba_bersih:,.0f}")

         # Halaman Laporan Perubahan Modal
elif selected == "Laporan Perubahan Modal":
    st.subheader("Laporan Perubahan Modal 🔄")
    df_jurnal = st.session_state.get("df_jurnal_umum", pd.DataFrame())
    df_saldo = st.session_state.get("df_neraca_saldo", pd.DataFrame())
    _, _, laba_bersih = hitung_laba_rugi(df_jurnal)
    modal_awal = df_saldo[df_saldo["Nama Akun"] == "Modal"]["Kredit (Rp)"].sum()
    df_modal = hitung_perubahan_modal(laba_bersih, modal_awal)
    st.dataframe(df_modal, use_container_width=True)

        # Halaman Laporan Posisi Keuangan
elif selected == "Laporan Posisi Keuangan":
    st.subheader("Laporan Posisi Keuangan 💰")
    df_buku_besar = st.session_state.get("df_buku_besar", pd.DataFrame())
    df_posisi = hitung_posisi_keuangan(df_buku_besar)
    st.dataframe(df_posisi, use_container_width=True)

        # Halaman Jurnal Penutup
elif selected == 'Jurnal Penutup':
    st.subheader('Jurnal Penutup 🛑')
    st.markdown('Periode 30 April 2025')

    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_jurnal_penutup" not in st.session_state:
        st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_jurnal_penutup", clear_on_submit=True):
        st.write("Tambah Transaksi")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)

        with col1:
            tambah = st.form_submit_button("Tambah Transaksi")
        with col2:
            reset = st.form_submit_button("Reset Data")

        if tambah:
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                nomor = len(st.session_state.df_jurnal_penutup) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                st.session_state.df_jurnal_penutup = pd.concat(
                    [st.session_state.df_jurnal_penutup, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_jurnal_penutup.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        df = st.session_state.df_jurnal_penutup.copy()

        st.markdown("### Edit Jurnal Penutup")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        edited_df["Debit (Rp)"] = pd.to_numeric(edited_df["Debit (Rp)"], errors="coerce").fillna(0)
        edited_df["Kredit (Rp)"] = pd.to_numeric(edited_df["Kredit (Rp)"], errors="coerce").fillna(0)

        st.session_state.df_jurnal_penutup = edited_df

        total_row = {
            "No": "",
            "Nama Akun": "Total",
            "Debit (Rp)": edited_df["Debit (Rp)"].sum(),
            "Kredit (Rp)": edited_df["Kredit (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Neraca Saldo (dengan Total)")
        st.dataframe(
            df_total.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

            # Halaman Neraca Saldo Setelah Penutup    
elif selected == 'Neraca Saldo Setelah Penutup':
    st.subheader('Neraca Saldo Setelah Penutup ✅') 
    st.markdown('Periode 30 April 2025')

    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_neraca_saldo_setelah_penutup" not in st.session_state:
        st.session_state.df_neraca_saldo_setelah_penutup = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_setelah_penutup", clear_on_submit=True):
        st.write("Tambah Transaksi")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)

        with col1:
            tambah = st.form_submit_button("Tambah Transaksi")
        with col2:
            reset = st.form_submit_button("Reset Data")

        if tambah:
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                nomor = len(st.session_state.df_neraca_saldo_setelah_penutup) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                st.session_state.df_neraca_saldo_setelah_penutup = pd.concat(
                    [st.session_state.df_neraca_saldo_setelah_penutup, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_neraca_saldo_setelah_penutup = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_neraca_saldo_setelah_penutup.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        df = st.session_state.df_neraca_saldo_setelah_penutup.copy()

        st.markdown("### Edit Data Neraca Saldo Setelah Penutup")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        edited_df["Debit (Rp)"] = pd.to_numeric(edited_df["Debit (Rp)"], errors="coerce").fillna(0)
        edited_df["Kredit (Rp)"] = pd.to_numeric(edited_df["Kredit (Rp)"], errors="coerce").fillna(0)

        st.session_state.df_neraca_saldo_setelah_penutup = edited_df

        total_row = {
            "No": "",
            "Nama Akun": "Total",
            "Debit (Rp)": edited_df["Debit (Rp)"].sum(),
            "Kredit (Rp)": edited_df["Kredit (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Neraca Saldo Setelah Penutup(dengan Total)")
        st.dataframe(
            df_total.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

        
        # Halaman Unduh Laporan Keuangan
elif selected == 'Unduh Laporan Keuangan':
    st.subheader('Unduh Laporan Keuangan') 
    st.markdown("Pada halaman ini, Anda dapat mengunduh laporan keuangan dalam bentuk file Excel.")

    try:
        import xlsxwriter
        st.success("Modul berhasil diimpor!")
        buffer = export_to_excel()

        # Tombol unduh
        st.download_button(
            label="📥 Unduh Semua Data Laporan (Excel)",
            data=buffer,
            file_name="laporan_keuangan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except ModuleNotFoundError:
        st.error("Modul xlsxwriter tidak ditemukan. Silakan instal dengan menjalankan: pip install xlsxwriter")