import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from datetime import datetime 

# Navigasi sidebar
with st.sidebar:
    selected = st.sidebar.radio("NIO FARM", 
                           ['Profile', 'Data Transaksi', 'Data Persediaan', 'Data Beban', 'Data Modal', 'Neraca Saldo Periode Sebelumnya', 'Jurnal Umum', 'Buku Besar', 'Neraca Saldo', 'Laporan Laba Rugi', 'Laporan Perubahan Modal', 'Laporan Posisi Keuangan', 'Jurnal Penutup', 'Neraca Saldo Setelah Penutup'],  # Pilihan menu
                            )


if selected == 'Profile':
        st.subheader('Profile')
        st.write("""Nio Farm adalah usaha rumah tangga yang bergerak di bidang produksi susu kambing yang telah berdiri sejak 2020. Kambing di Nio Farm senantiasa dipastikan kesehatan, kualitas pakan, serta kebersihan kandangnya. Setiap tetes susu yang dihasilkan adalah hasil dari perawatan alami dan proses yang bersih sehingga menghasilkan susu kambing yang segar, aman dikonsumsi, dan baik bagi kesehatan.""")
        st.write('Jl. Pamongan Sari No.90, Pedurungan Lor, Kec. Pedurungan, Kota Semarang, Jawa Tengah 50192')

    # Halaman Data Transaksi
elif selected == 'Data Transaksi':
    st.subheader('Data Transaksi')
    st.markdown('Periode 30 April 2025')

    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_transaksi" not in st.session_state:
        st.session_state.df_data_transaksi = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_transaksi", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input("Tanggal Transaksi", format="DD/MM/YYYY")
        nama_akun = st.text_input("Nama Akun")
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
        
        with col1:
            tambah = st.form_submit_button("Tambah Transaksi")
        with col2:
            reset = st.form_submit_button("Reset Data")

        if tambah:
            if nama_akun.strip() == "" or nominal == 0:
                st.warning("Nama akun wajib diisi dan nilai nominal tidak boleh nol.")
            else:
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),
                    "Nama Akun": nama_akun,
                    "Nominal (Rp)": nominal if nominal > 0 else None,
                }
                st.session_state.df_data_transaksi = pd.concat(
                    [st.session_state.df_data_transaksi, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_transaksi = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_transaksi.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_data_transaksi)
        gb.configure_default_column(editable=True)
        gb.configure_column("Tanggal", editable=True)
        grid_options = gb.build()

        st.markdown("Tabel Data Transaksi")
        grid_response = AgGrid(
            st.session_state.df_data_transaksi,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_data_transaksi = pd.DataFrame(updated_data)

        # Ubah ke datetime dan urutkan tanggal
        st.session_state.df_data_transaksi["Nominal (Rp)"] = pd.to_numeric(
            st.session_state.df_data_transaksi["Nominal (Rp)"], errors="coerce"
        ).fillna(0)

        st.session_state.df_data_transaksi["Tanggal"] = pd.to_datetime(
            st.session_state.df_data_transaksi["Tanggal"], dayfirst=True, errors="coerce"
        )

        # Urutkan berdasarkan tanggal
        st.session_state.df_data_transaksi = st.session_state.df_data_transaksi.sort_values(
            by="Tanggal"
        )

        # Format kembali tanggal ke dd/mm/yyyy setelah pengurutan
        st.session_state.df_data_transaksi["Tanggal"] = st.session_state.df_data_transaksi["Tanggal"].dt.strftime('%d/%m/%Y')

        # Tambahkan total
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": st.session_state.df_data_transaksi["Nominal (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_data_transaksi,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Nominal (Rp)": "Rp {:,.0f}",
            })
        )

        if reset:
            st.session_state.df_data_transaksi = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")


    # Halaman Data Persediaan
elif selected == 'Data Persediaan':
    st.subheader('Data Persediaan')
    st.markdown('Periode 30 April 2025')
        
    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_persediaan" not in st.session_state:
        st.session_state.df_data_persediaan = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_persediaan", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input ("Tanggal Transaksi",format="DD/MM/YYYY")
        nama_akun = st.text_input("Nama Akun")
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
    with col1:
        tambah = st.form_submit_button("Tambah Transaksi")
    with col2:
        reset = st.form_submit_button("Reset Data")


        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or nominal == 0:
                st.warning("Nama akun wajib diisi dan nilai nominal tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),
                    "Nama Akun": nama_akun,
                    "Nominal (Rp)": nominal if nominal > 0 else None,
                }
                # Update DataFrame di session_state
                st.session_state.df_data_persediaan = pd.concat(
                    [st.session_state.df_data_persediaan, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_persediaan= pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_persediaan.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_data_persediaan)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("Tanggal", editable=True)  # Kolom "Tanggal" bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Data Transaksi")
        grid_response = AgGrid(
            st.session_state.df_data_persediaan,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_data_persediaan = pd.DataFrame(updated_data)

        st.session_state.df_data_persediaan["Nominal (Rp)"] = pd.to_numeric(st.session_state.df_data_persediaan["Nominal (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_data_persediaan["Tanggal"] = pd.to_datetime(
        st.session_state.df_data_persediaan["Tanggal"], errors="coerce"
    ).dt.strftime('%d/%m/%Y')

        # Tambahkan total Nominal
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": st.session_state.df_data_persediaan["Nominal (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_data_persediaan,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Nominal (Rp)": "Rp {:,.0f}",
            })
        )

        if reset:
            st.session_state.df_data_persediaan = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Halaman Data Beban
elif selected == 'Data Beban':
    st.subheader('Data Beban') 
    st.markdown('Periode 30 April 2025')
        
    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_beban" not in st.session_state:
        st.session_state.df_data_beban = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_beban", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input ("Tanggal Transaksi",format="DD/MM/YYYY")
        nama_akun = st.text_input("Nama Akun")
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
    with col1:
        tambah = st.form_submit_button("Tambah Transaksi")
    with col2:
        reset = st.form_submit_button("Reset Data")


        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or nominal == 0:
                st.warning("Nama akun wajib diisi dan nilai nominal tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),
                    "Nama Akun": nama_akun,
                    "Nominal (Rp)": nominal if nominal > 0 else None,
                }
                # Update DataFrame di session_state
                st.session_state.df_data_beban = pd.concat(
                    [st.session_state.df_data_beban, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_beban= pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_beban.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_data_beban)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("Tanggal", editable=True)  # Kolom "Tanggal" bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Data Transaksi")
        grid_response = AgGrid(
            st.session_state.df_data_beban,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_data_beban = pd.DataFrame(updated_data)

        st.session_state.df_data_beban["Nominal (Rp)"] = pd.to_numeric(st.session_state.df_data_beban["Nominal (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_data_beban["Tanggal"] = pd.to_datetime(
        st.session_state.df_data_beban["Tanggal"], errors="coerce"
    ).dt.strftime('%d/%m/%Y')
        
        # Tambahkan total Nominal
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": st.session_state.df_data_beban["Nominal (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_data_beban,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Nominal (Rp)": "Rp {:,.0f}",
            })
        )

        if reset:
            st.session_state.df_data_beban = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")
           
    # Halaman Data Modal
elif selected == 'Data Modal':
    st.subheader('Data Modal') 
    st.markdown('Periode 30 April 2025')
        
    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_modal" not in st.session_state:
        st.session_state.df_data_modal = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_modal", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input ("Tanggal Transaksi",format="DD/MM/YYYY")
        nama_akun = st.text_input("Nama Akun")
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
    with col1:
        tambah = st.form_submit_button("Tambah Transaksi")
    with col2:
        reset = st.form_submit_button("Reset Data")


        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or nominal == 0:
                st.warning("Nama akun wajib diisi dan nilai nominal tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),
                    "Nama Akun": nama_akun,
                    "Nominal (Rp)": nominal if nominal > 0 else None,
                }
                # Update DataFrame di session_state
                st.session_state.df_data_modal = pd.concat(
                    [st.session_state.df_data_modal, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_modal= pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_modal.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_data_modal)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("Tanggal", editable=True)  # Kolom "Tanggal" bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Data Transaksi")
        grid_response = AgGrid(
            st.session_state.df_data_modal,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_data_modal = pd.DataFrame(updated_data)

        st.session_state.df_data_modal["Nominal (Rp)"] = pd.to_numeric(st.session_state.df_data_modal["Nominal (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_data_modal["Tanggal"] = pd.to_datetime(
        st.session_state.df_data_modal["Tanggal"], errors="coerce"
    ).dt.strftime('%d/%m/%Y')
        
        # Tambahkan total Nominal
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": st.session_state.df_data_modal["Nominal (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_data_modal,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Nominal (Rp)": "Rp {:,.0f}",
            })
        )

        if reset:
            st.session_state.df_data_modal = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Halaman Neraca Saldo Periode Sebelumnya
elif selected == 'Neraca Saldo Periode Sebelumnya':
    st.subheader('Neraca Saldo Periode Sebelumnya')
    st.markdown('Periode 31 Maret 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Inisialisasi DataFrame di session_state jika belum ada
    if "df_neraca_saldo_periode_sebelumnya" not in st.session_state:
        st.session_state.df_neraca_saldo_periode_sebelumnya = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_neraca_saldo_periode_sebelumnya", clear_on_submit=True):
        st.write("Tambah Transaksi")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        
        col1, col2 = st.columns(2) 
    with col1:
        tambah = st.form_submit_button("Tambah Transaksi")  
    with col2:
        reset = st.form_submit_button("Reset Data")

    # Logika untuk tombol tambah
    if tambah:
        if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
            st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
        else:
            # Tambahkan data baru ke DataFrame
            nomor = len(st.session_state.df_neraca_saldo_periode_sebelumnya) + 1
            row = {
                "No": nomor,
                "Nama Akun": nama_akun,
                "Debit (Rp)": debit,
                "Kredit (Rp)": kredit
            }
            st.session_state.df_neraca_saldo_periode_sebelumnya = pd.concat(
                [st.session_state.df_neraca_saldo_periode_sebelumnya, pd.DataFrame([row])],
                ignore_index=True
            )
            st.success("Transaksi berhasil ditambahkan.")

    # Logika untuk tombol reset
    if reset:
        st.session_state.df_neraca_saldo_periode_sebelumnya = pd.DataFrame(columns=columns)
        st.info("Data berhasil direset.")

    # Menampilkan tabel
    if st.session_state.df_neraca_saldo_periode_sebelumnya.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        # Konfigurasi tabel dengan AgGrid
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_neraca_saldo_periode_sebelumnya)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("### Tabel Neraca Saldo")
        grid_response = AgGrid(
            st.session_state.df_neraca_saldo_periode_sebelumnya,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True
        )

        # Perbarui DataFrame dari hasil AgGrid
        updated_data = grid_response["data"]
        st.session_state.df_neraca_saldo_periode_sebelumnya = pd.DataFrame(updated_data)

        # Pastikan kolom debit dan kredit bertipe numerik
        st.session_state.df_neraca_saldo_periode_sebelumnya["Debit (Rp)"] = pd.to_numeric(
            st.session_state.df_neraca_saldo_periode_sebelumnya["Debit (Rp)"], errors="coerce"
        ).fillna(0)
        st.session_state.df_neraca_saldo_periode_sebelumnya["Kredit (Rp)"] = pd.to_numeric(
            st.session_state.df_neraca_saldo_periode_sebelumnya["Kredit (Rp)"], errors="coerce"
        ).fillna(0)

        # Tambahkan baris total ke dalam DataFrame untuk ditampilkan
        total_row = {
            "No": "",
            "Nama Akun": "Total",
            "Debit (Rp)": st.session_state.df_neraca_saldo_periode_sebelumnya["Debit (Rp)"].sum(skipna=True),
            "Kredit (Rp)": st.session_state.df_neraca_saldo_periode_sebelumnya["Kredit (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_neraca_saldo_periode_sebelumnya,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan DataFrame dengan styling
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

# Halaman Jurnal Umum
elif selected == 'Jurnal Umum':
    st.subheader('Jurnal Umum')
    st.markdown('Periode 30 April 2025')

    columns = ["Tanggal", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_jurnal_umum" not in st.session_state:
        st.session_state.df_jurnal_umum = pd.DataFrame(columns=columns)

    if "buku_besar" not in st.session_state:
        st.session_state.buku_besar = pd.DataFrame(columns=["Nama Akun", "Tanggal", "Keterangan", "Debit (Rp)", "Kredit (Rp)", "Saldo (Rp)"])

    daftar_akun = [
        "Kas", "Persediaan", "Perlengkapan", "Peralatan", "Penjualan",
        "Beban Gaji", "Beban Transportasi", "Beban Listrik dan Air", "Modal", "Aset Biologis"
    ]

    def update_buku_besar(jurnal_df):
        grouped = []
        saldo_dict = {}
        for _, row in jurnal_df.iterrows():
            nama_akun = row["Nama Akun"]
            tanggal = row["Tanggal"]
            debit = row["Debit (Rp)"]
            kredit = row["Kredit (Rp)"]

            if nama_akun not in saldo_dict:
                saldo_dict[nama_akun] = 0
            saldo_dict[nama_akun] += debit - kredit

            grouped.append({
                "Nama Akun": nama_akun,
                "Tanggal": tanggal,
                "Keterangan": "Transaksi",
                "Debit (Rp)": debit,
                "Kredit (Rp)": kredit,
                "Saldo (Rp)": saldo_dict[nama_akun]
            })

        return pd.DataFrame(grouped)

    with st.form("form_tambah_transaksi_jurnal_umum", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input("Tanggal Transaksi", format="DD/MM/YYYY")
        nama_akun = st.selectbox("Nama Akun", daftar_akun)
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
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),  # Format tanggal saat input
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0,
                }
                st.session_state.df_jurnal_umum = pd.concat(
                    [st.session_state.df_jurnal_umum, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.session_state.buku_besar = update_buku_besar(st.session_state.df_jurnal_umum)
                st.success("Transaksi berhasil ditambahkan dan Buku Besar diperbarui.")

        if reset:
            st.session_state.df_jurnal_umum = pd.DataFrame(columns=columns)
            st.session_state.buku_besar = pd.DataFrame(columns=["Nama Akun", "Tanggal", "Keterangan", "Debit (Rp)", "Kredit (Rp)", "Saldo (Rp)"])
            st.info("Data berhasil direset.")

    if st.session_state.df_jurnal_umum.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_jurnal_umum)
        gb.configure_default_column(editable=True)
        gb.configure_column("Tanggal", editable=True)
        grid_options = gb.build()

        st.markdown("Tabel Jurnal Umum")
        grid_response = AgGrid(
            st.session_state.df_jurnal_umum,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True
        )

        # Ambil data dari hasil edit tabel
        updated_data = grid_response["data"]
        st.session_state.df_jurnal_umum = pd.DataFrame(updated_data)

        # Format tanggal ulang agar selalu konsisten dd/MM/yyyy
        st.session_state.df_jurnal_umum["Tanggal"] = pd.to_datetime(
            st.session_state.df_jurnal_umum["Tanggal"], dayfirst=True, errors="coerce"
        ).dt.strftime('%d/%m/%Y')

        # Pastikan kolom angka tetap valid
        st.session_state.df_jurnal_umum["Debit (Rp)"] = pd.to_numeric(
            st.session_state.df_jurnal_umum["Debit (Rp)"], errors="coerce"
        ).fillna(0)
        st.session_state.df_jurnal_umum["Kredit (Rp)"] = pd.to_numeric(
            st.session_state.df_jurnal_umum["Kredit (Rp)"], errors="coerce"
        ).fillna(0)

        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Debit (Rp)": st.session_state.df_jurnal_umum["Debit (Rp)"].sum(),
            "Kredit (Rp)": st.session_state.df_jurnal_umum["Kredit (Rp)"].sum(),
        }

        df_tampil = pd.concat(
            [st.session_state.df_jurnal_umum, pd.DataFrame([total_row])],
            ignore_index=True
        )

        st.dataframe(
            df_tampil.fillna("").style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

    #Halaman Buku Besar
elif selected == 'Buku Besar':
    st.subheader("Buku Besar")
    st.markdown("Periode 30 April 2025")

    if "buku_besar" not in st.session_state:
        st.session_state.buku_besar = pd.DataFrame(columns=["Nama Akun", "Tanggal", "Keterangan", "Debit (Rp)", "Kredit (Rp)", "Saldo (Rp)"])

    if st.session_state.buku_besar.empty:
        st.info("Buku Besar masih kosong. Tambahkan transaksi di Jurnal Umum.")
    else:
        # Bersihkan data Nama Akun dari spasi & seragamkan kapital
        st.session_state.buku_besar["Nama Akun"] = st.session_state.buku_besar["Nama Akun"].str.strip().str.title()

        akun_unik = st.session_state.buku_besar["Nama Akun"].dropna().unique()

        for akun in akun_unik:
            st.markdown(f"### Akun: {akun}")
            df_akun = st.session_state.buku_besar[st.session_state.buku_besar["Nama Akun"] == akun]
            st.dataframe(
                df_akun.style.format({
                    "Debit (Rp)": "Rp {:,.0f}",
                    "Kredit (Rp)": "Rp {:,.0f}",
                    "Saldo (Rp)": "Rp {:,.0f}"
                })
            )

    # Halaman Neraca Saldo
elif selected == 'Neraca Saldo':
    st.subheader('Neraca Saldo')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]


    if "df_neraca_saldo" not in st.session_state:
        st.session_state.df_neraca_saldo = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_neraca_saldo", clear_on_submit=True):
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
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                nomor = len(st.session_state.df_neraca_saldo) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                # Update DataFrame di session_state
                st.session_state.df_neraca_saldo = pd.concat(
                    [st.session_state.df_neraca_saldo, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_neraca_saldo = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_neraca_saldo.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_neraca_saldo)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("### Tabel Neraca Saldo")
        grid_response = AgGrid(
            st.session_state.df_neraca_saldo,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_neraca_saldo = pd.DataFrame(updated_data)

        st.session_state.df_neraca_saldo["Debit (Rp)"] = pd.to_numeric(st.session_state.df_neraca_saldo["Debit (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_neraca_saldo["Kredit (Rp)"] = pd.to_numeric(st.session_state.df_neraca_saldo["Kredit (Rp)"], errors="coerce").fillna(0)

        # Tambahkan total debit dan kredit
        total_row = {
            "No": "",
            "Nama Akun": "Total",
            "Debit (Rp)": st.session_state.df_neraca_saldo["Debit (Rp)"].sum(skipna=True),
            "Kredit (Rp)": st.session_state.df_neraca_saldo["Kredit (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_neraca_saldo,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

        if reset:
            st.session_state.df_neraca_saldo = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

            # Halaman Laporan Laba Rugi
elif selected == 'Laporan Laba Rugi':
    st.subheader('Laporan Laba Rugi')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_laporan_laba_rugi" not in st.session_state:
        st.session_state.df_laporan_laba_rugi = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_laporan_laba_rugi", clear_on_submit=True):
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
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                nomor = len(st.session_state.df_laporan_laba_rugi) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                # Update DataFrame di session_state
                st.session_state.df_laporan_laba_rugi = pd.concat(
                    [st.session_state.df_laporan_laba_rugi, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_laporan_laba_rugi = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_laporan_laba_rugi.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_laporan_laba_rugi)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Laporan Laba Rugi")
        grid_response = AgGrid(
            st.session_state.df_laporan_laba_rugi,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_laporan_laba_rugi = pd.DataFrame(updated_data)

        st.session_state.df_laporan_laba_rugi["Debit (Rp)"] = pd.to_numeric(st.session_state.df_laporan_laba_rugi["Debit (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_laporan_laba_rugi["Kredit (Rp)"] = pd.to_numeric(st.session_state.df_laporan_laba_rugi["Kredit (Rp)"], errors="coerce").fillna(0)

        df_tampil = pd.concat([
            st.session_state.df_laporan_laba_rugi,
        ], ignore_index=True)
       # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

        if reset:
            st.session_state.df_laporan_laba_rugi = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

            # Halaman Laporan Perubahan Modal
elif selected == 'Laporan Perubahan Modal':
    st.subheader('Laporan Perubahan Modal')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_laporan_perubahan_modal" not in st.session_state:
        st.session_state.df_laporan_perubahan_modal = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_laporan_perubahan_modal", clear_on_submit=True):
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
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                nomor = len(st.session_state.df_laporan_perubahan_modal) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                # Update DataFrame di session_state
                st.session_state.df_laporan_perubahan_modal = pd.concat(
                    [st.session_state.df_laporan_perubahan_modal, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_laporan_perubahan_modal= pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_laporan_perubahan_modal.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_laporan_perubahan_modal)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Laporan Laba Rugi")
        grid_response = AgGrid(
            st.session_state.df_laporan_perubahan_modal,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_laporan_perubahan_modal = pd.DataFrame(updated_data)

        st.session_state.df_laporan_perubahan_modal["Debit (Rp)"] = pd.to_numeric(st.session_state.df_laporan_perubahan_modal["Debit (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_laporan_perubahan_modal["Kredit (Rp)"] = pd.to_numeric(st.session_state.df_laporan_perubahan_modal["Kredit (Rp)"], errors="coerce").fillna(0)


        df_tampil = pd.concat([
            st.session_state.df_laporan_perubahan_modal,
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

        if reset:
            st.session_state.df_laporan_perubahan_modal = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

            # Halaman Laporan Posisi Keuangan
elif selected == 'Laporan Posisi Keuangan':
    st.subheader('Laporan Posisi Keuangan')
    st.markdown('Periode 30 April 2025')

    # Definisi kolom untuk DataFrame
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Inisialisasi DataFrame dalam session_state jika belum ada
    if "df_laporan_posisi_keuangan" not in st.session_state:
        st.session_state.df_laporan_posisi_keuangan = pd.DataFrame(columns=columns)

    # Form untuk menambahkan transaksi
    with st.form("form_tambah_transaksi_laporan_posisi_keuangan", clear_on_submit=True):
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
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                nomor = len(st.session_state.df_laporan_posisi_keuangan) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0
                }
                st.session_state.df_laporan_posisi_keuangan = pd.concat(
                    [st.session_state.df_laporan_posisi_keuangan, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_laporan_posisi_keuangan = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Tampilkan tabel jika ada data
    if st.session_state.df_laporan_posisi_keuangan.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        # Konfigurasi tabel menggunakan AgGrid
        from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode

        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_laporan_posisi_keuangan)
        gb.configure_default_column(editable=True)
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Laporan Posisi Keuangan")
        grid_response = AgGrid(
            st.session_state.df_laporan_posisi_keuangan,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        # Update DataFrame di session_state berdasarkan perubahan di AgGrid
        updated_data = grid_response["data"]
        st.session_state.df_laporan_posisi_keuangan = pd.DataFrame(updated_data)

        # Pastikan kolom debit/kredit memiliki tipe data numerik
        st.session_state.df_laporan_posisi_keuangan["Debit (Rp)"] = pd.to_numeric(
            st.session_state.df_laporan_posisi_keuangan["Debit (Rp)"], errors="coerce"
        ).fillna(0)
        st.session_state.df_laporan_posisi_keuangan["Kredit (Rp)"] = pd.to_numeric(
            st.session_state.df_laporan_posisi_keuangan["Kredit (Rp)"], errors="coerce"
        ).fillna(0)

        # Tampilkan tabel dengan format Rupiah
        st.dataframe(
            st.session_state.df_laporan_posisi_keuangan.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

            # Halaman Jurnal Penutup
elif selected == 'Jurnal Penutup':
    st.subheader('Jurnal Penutup')
    st.markdown('Periode 30 April 2025')

    columns = ["Tanggal", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Inisialisasi session_state untuk tabel jika belum ada
    if "df_jurnal_penutup" not in st.session_state:
        st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_jurnal_penutup", clear_on_submit=True):
        st.write("Tambah Transaksi")
        tanggal = st.date_input("Tanggal Transaksi", format="DD/MM/YYYY")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
        with col1:
            tambah = st.form_submit_button("Tambah Transaksi")
        with col2:
            reset = st.form_submit_button("Reset Data")

        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambahkan transaksi ke DataFrame di session_state
                row = {
                    "Tanggal": tanggal.strftime('%d/%m/%Y'),
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0,
                }
                st.session_state.df_jurnal_penutup = pd.concat(
                    [st.session_state.df_jurnal_penutup, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            # Reset tabel
            st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Tampilkan tabel
    if st.session_state.df_jurnal_penutup.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_jurnal_penutup)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("Tanggal", editable=False)  # Kolom "Tanggal" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Jurnal Penutup")
        grid_response = AgGrid(
            st.session_state.df_jurnal_penutup,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True
        )

        # Ambil data yang diperbarui dari tabel
        updated_data = grid_response["data"]
        st.session_state.df_jurnal_penutup = pd.DataFrame(updated_data)

        # Konversi kolom nominal ke numerik
        st.session_state.df_jurnal_penutup["Debit (Rp)"] = pd.to_numeric(
            st.session_state.df_jurnal_penutup["Debit (Rp)"], errors="coerce"
        ).fillna(0)
        st.session_state.df_jurnal_penutup["Kredit (Rp)"] = pd.to_numeric(
            st.session_state.df_jurnal_penutup["Kredit (Rp)"], errors="coerce"
        ).fillna(0)

        # Hitung total debit dan kredit
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Debit (Rp)": st.session_state.df_jurnal_penutup["Debit (Rp)"].sum(),
            "Kredit (Rp)": st.session_state.df_jurnal_penutup["Kredit (Rp)"].sum(),
        }

        # Gabungkan data utama dengan baris total
        df_tampil = pd.concat(
            [st.session_state.df_jurnal_penutup, pd.DataFrame([total_row])],
            ignore_index=True
        )

        # Tampilkan tabel akhir dengan total
        st.dataframe(
            df_tampil.fillna("").style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

            # Halaman Neraca Saldo Setelah Penutup    
elif selected == 'Neraca Saldo Setelah Penutup':
    st.subheader('Neraca Saldo Setelah Penutup')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    if "df_neraca_saldo_setelah_penutup" not in st.session_state:
        st.session_state.df_neraca_saldo_setelah_penutup = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_neraca_saldo_setelah_penutup", clear_on_submit=True):
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
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Tambah transaksi ke DataFrame di session_state
                nomor = len(st.session_state.df_neraca_saldo_setelah_penutup) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
                # Update DataFrame di session_state
                st.session_state.df_neraca_saldo_setelah_penutup = pd.concat(
                    [st.session_state.df_neraca_saldo_setelah_penutup, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_neraca_saldo_setelah_penutup= pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_neraca_saldo_setelah_penutup.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df_neraca_saldo_setelah_penutup)
        gb.configure_default_column(editable=True)  # Semua kolom bisa diedit
        gb.configure_column("No", editable=False)  # Kolom "No" tidak bisa diedit
        grid_options = gb.build()

        st.markdown("Tabel Neraca Saldo Setelah Penutup")
        grid_response = AgGrid(
            st.session_state.df_neraca_saldo_setelah_penutup,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            fit_columns_on_grid_load=True    
        )

        updated_data = grid_response["data"]
        st.session_state.df_neraca_saldo_setelah_penutup = pd.DataFrame(updated_data)

        st.session_state.df_neraca_saldo_setelah_penutup["Debit (Rp)"] = pd.to_numeric(st.session_state.df_neraca_saldo_setelah_penutup["Debit (Rp)"], errors="coerce").fillna(0)
        st.session_state.df_neraca_saldo_setelah_penutup["Kredit (Rp)"] = pd.to_numeric(st.session_state.df_neraca_saldo_setelah_penutup["Kredit (Rp)"], errors="coerce").fillna(0)

        # Tambahkan total debit dan kredit
        total_row = {
            "No": "",
            "Nama Akun": "Total",
            "Debit (Rp)": st.session_state.df_neraca_saldo_setelah_penutup["Debit (Rp)"].sum(skipna=True),
            "Kredit (Rp)": st.session_state.df_neraca_saldo_setelah_penutup["Kredit (Rp)"].sum(skipna=True)
        }

        df_tampil = pd.concat([
            st.session_state.df_neraca_saldo_setelah_penutup,
            pd.DataFrame([total_row])
        ], ignore_index=True)

        # Tampilkan tabel
        st.dataframe(
            df_tampil.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            })
        )

        if reset:
            st.session_state.df_neraca_saldo_setelah_penutup = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")