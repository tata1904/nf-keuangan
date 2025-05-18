import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime 

def update_buku_besar():
    df_bb = pd.DataFrame(columns=["Tanggal", "Nama Akun", "Debit (Rp)", "Kredit (Rp)", "Saldo (Rp)"])
    saldo_per_akun = {}

    # Neraca Saldo
    for _, row in st.session_state.df_neraca_saldo.iterrows():
        nama_akun = row["Nama Akun"]
        debit = row["Debit (Rp)"]
        kredit = row["Kredit (Rp)"]
        saldo = saldo_per_akun.get(nama_akun, 0) + debit - kredit
        saldo_per_akun[nama_akun] = saldo
        df_bb = pd.concat([df_bb, pd.DataFrame([{
            "Tanggal": "31/03/2025",
            "Nama Akun": nama_akun,
            "Debit (Rp)": debit,
            "Kredit (Rp)": kredit,
            "Saldo (Rp)": saldo
        }])], ignore_index=True)

    # Jurnal Umum
    for _, row in st.session_state.df_jurnal_umum.iterrows():
        nama_akun = row["Nama Akun"]
        debit = row["Debit (Rp)"]
        kredit = row["Kredit (Rp)"]
        tanggal = row["Tanggal"]
        saldo = saldo_per_akun.get(nama_akun, 0) + debit - kredit
        saldo_per_akun[nama_akun] = saldo
        df_bb = pd.concat([df_bb, pd.DataFrame([{
            "Tanggal": tanggal,
            "Nama Akun": nama_akun,
            "Debit (Rp)": debit,
            "Kredit (Rp)": kredit,
            "Saldo (Rp)": saldo
        }])], ignore_index=True)

    st.session_state.df_buku_besar = df_bb

if "df_neraca_saldo" not in st.session_state:
    st.session_state.df_neraca_saldo = pd.DataFrame(columns=["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"])

if "df_jurnal_umum" not in st.session_state:
    st.session_state.df_jurnal_umum = pd.DataFrame(columns=["No", "Tanggal", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"])

if "df_buku_besar" not in st.session_state:
    st.session_state.df_buku_besar = pd.DataFrame(columns=["Nama Akun", "Debit (Rp)", "Kredit (Rp)", "Saldo (Rp)"])


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
    st.markdown('Periode April 2025')

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
                    "Nominal (Rp)": nominal,
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
        df = st.session_state.df_data_transaksi.copy()

        # Ubah ke datetime lalu sort
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/%m/%Y", errors="coerce")
        df = df.sort_values(by="Tanggal")

        # Format ulang ke string
        df["Tanggal"] = df["Tanggal"].dt.strftime('%d/%m/%Y')

        st.markdown("### Edit Data Transaksi")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Validasi dan konversi nominal
        edited_df["Nominal (Rp)"] = pd.to_numeric(edited_df["Nominal (Rp)"], errors="coerce").fillna(0)

        # Simpan hasil edit ke session state
        st.session_state.df_data_transaksi = edited_df

        # Tambahkan total di akhir
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": edited_df["Nominal (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Data Transaksi (dengan Total)")
        st.dataframe(
            df_total.style.format({
                "Nominal (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

     # Halaman Data Persediaan
elif selected == 'Data Persediaan':
    st.subheader('Data Persediaan')
    st.markdown('Periode April 2025')

    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_persediaan" not in st.session_state:
        st.session_state.df_data_persediaan = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_persediaan", clear_on_submit=True):
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
                    "Nominal (Rp)": nominal,
                }
                st.session_state.df_data_persediaan = pd.concat( 
                    [st.session_state.df_data_persediaan, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_persediaan = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_persediaan.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        df = st.session_state.df_data_persediaan.copy()

        # Ubah ke datetime lalu sort
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/%m/%Y", errors="coerce")
        df = df.sort_values(by="Tanggal")

        # Format ulang ke string
        df["Tanggal"] = df["Tanggal"].dt.strftime('%d/%m/%Y')

        st.markdown("### Edit Data Transaksi")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Validasi dan konversi nominal
        edited_df["Nominal (Rp)"] = pd.to_numeric(edited_df["Nominal (Rp)"], errors="coerce").fillna(0)

        # Simpan hasil edit ke session state
        st.session_state.df_data_persediaan = edited_df

        # Tambahkan total di akhir
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": edited_df["Nominal (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Data Transaksi (dengan Total)")
        st.dataframe(
            df_total.style.format({
                "Nominal (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )


     # Halaman Data Beban
elif selected == 'Data Beban':
    st.subheader('Data Beban')
    st.markdown('Periode April 2025')

    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_beban" not in st.session_state:
        st.session_state.df_data_beban = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_beban", clear_on_submit=True):
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
                    "Nominal (Rp)": nominal,
                }
                st.session_state.df_data_beban = pd.concat(
                    [st.session_state.df_data_beban, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_beban = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_beban.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        df = st.session_state.df_data_beban.copy()

        # Ubah ke datetime lalu sort
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/%m/%Y", errors="coerce")
        df = df.sort_values(by="Tanggal")

        # Format ulang ke string
        df["Tanggal"] = df["Tanggal"].dt.strftime('%d/%m/%Y')

        st.markdown("### Edit Data Transaksi")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Validasi dan konversi nominal
        edited_df["Nominal (Rp)"] = pd.to_numeric(edited_df["Nominal (Rp)"], errors="coerce").fillna(0)

        # Simpan hasil edit ke session state
        st.session_state.df_data_beban = edited_df

        # Tambahkan total di akhir
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": edited_df["Nominal (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Data Transaksi (dengan Total)")
        st.dataframe(
            df_total.style.format({
                "Nominal (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

       
    # Halaman Data Modal 
elif selected == 'Data Modal':
    st.subheader('Data Modal')
    st.markdown('Periode April 2025')

    columns = ["Tanggal", "Nama Akun", "Nominal (Rp)"]

    if "df_data_modal" not in st.session_state:
        st.session_state.df_data_modal = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
    with st.form("form_tambah_transaksi_data_modal", clear_on_submit=True):
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
                    "Nominal (Rp)": nominal,
                }
                st.session_state.df_data_modal = pd.concat(
                    [st.session_state.df_data_modal, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        if reset:
            st.session_state.df_data_modal = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    if st.session_state.df_data_modal.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        df = st.session_state.df_data_modal.copy()

        # Ubah ke datetime lalu sort
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], format="%d/%m/%Y", errors="coerce")
        df = df.sort_values(by="Tanggal")

        # Format ulang ke string
        df["Tanggal"] = df["Tanggal"].dt.strftime('%d/%m/%Y')

        st.markdown("### Edit Data Transaksi")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Validasi dan konversi nominal
        edited_df["Nominal (Rp)"] = pd.to_numeric(edited_df["Nominal (Rp)"], errors="coerce").fillna(0)

        # Simpan hasil edit ke session state
        st.session_state.df_data_modal = edited_df

        # Tambahkan total di akhir
        total_row = {
            "Tanggal": "",
            "Nama Akun": "Total",
            "Nominal (Rp)": edited_df["Nominal (Rp)"].sum()
        }

        df_total = pd.concat([edited_df, pd.DataFrame([total_row])], ignore_index=True)

        st.markdown("### Data Transaksi (dengan Total)")
        st.dataframe(
            df_total.style.format({
                "Nominal (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

    # Halaman Neraca Saldo Periode Sebelumnya
elif selected == 'Neraca Saldo Periode Sebelumnya':
    st.subheader('Neraca Saldo Periode Sebelumnya')
    st.markdown('Periode 31 Maret 2025')

    with st.form("form_tambah_transaksi_neraca", clear_on_submit=True):
        nama_akun = st.selectbox("Nama Akun", ["Kas", "Persediaan", "Perlengkapan", "Aset Biologis", "Peralatan", "Modal"])
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
        tambah = col1.form_submit_button("Tambah Transaksi")
        reset = col2.form_submit_button("Reset Data")

        if tambah:
            if debit == 0 and kredit == 0:
                st.warning("Isi salah satu nilai Debit atau Kredit.")
            else:
                nomor = len(st.session_state.df_neraca_saldo) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit,
                    "Kredit (Rp)": kredit
                }
                st.session_state.df_neraca_saldo = pd.concat([
                    st.session_state.df_neraca_saldo, pd.DataFrame([row])
                ], ignore_index=True)
                update_buku_besar()
                st.success("Transaksi ditambahkan.")

        if reset:
            st.session_state.df_neraca_saldo = st.session_state.df_neraca_saldo.iloc[0:0]
            update_buku_besar()
            st.info("Data direset.")

    # Edit Data
    edited_df = st.data_editor(
        st.session_state.df_neraca_saldo,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

    st.session_state.df_neraca_saldo = edited_df
    update_buku_besar()


    # Halaman Jurnal Umum
elif selected == "Jurnal Umum":
    st.subheader("Jurnal Umum")
    st.markdown("Periode April 2025")

    with st.form("form_jurnal", clear_on_submit=True):
        tanggal = st.date_input("Tanggal")
        nama_akun = st.selectbox("Nama Akun", ["Persediaan", "Kas", "Penjualan", "Beban Listrik dan Air", "Beban Transportasi", "Beban Gaji"])
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
        tambah = col1.form_submit_button("Tambah Transaksi")
        reset = col2.form_submit_button("Reset Data")

        if tambah:
            if debit == 0 and kredit == 0:
                st.warning("Isi salah satu nilai Debit atau Kredit.")
            else:
                nomor = len(st.session_state.df_jurnal_umum) + 1
                row = {
                    "No": nomor,
                    "Tanggal": tanggal.strftime("%d/%m/%Y"),
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit,
                    "Kredit (Rp)": kredit
                }
                st.session_state.df_jurnal_umum = pd.concat([
                    st.session_state.df_jurnal_umum, pd.DataFrame([row])
                ], ignore_index=True)
                update_buku_besar()
                st.success("Transaksi ditambahkan.")

        if reset:
            st.session_state.df_jurnal_umum = st.session_state.df_jurnal_umum.iloc[0:0]
            update_buku_besar()
            st.info("Data direset.")

    # Edit Data
    edited_df = st.data_editor(
        st.session_state.df_jurnal_umum,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.df_jurnal_umum = edited_df
    update_buku_besar()


    # Halaman Buku Besar
elif selected == "Buku Besar":
    st.subheader("Buku Besar")
    st.markdown("Periode 31 Maret - 30 April 2025")

    if st.session_state.df_buku_besar.empty:
        st.info("Buku Besar masih kosong.")
    else:
        akun_unik = st.session_state.df_buku_besar["Nama Akun"].unique()
        for akun in akun_unik:
            st.markdown(f"### Akun: {akun}")
            df_akun = st.session_state.df_buku_besar[st.session_state.df_buku_besar["Nama Akun"] == akun]
            st.dataframe(
                df_akun.style.format({
                    "Debit (Rp)": "Rp {:,.0f}",
                    "Kredit (Rp)": "Rp {:,.0f}",
                    "Saldo (Rp)": "Rp {:,.0f}"
                }),
                use_container_width=True
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
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                nomor = len(st.session_state.df_neraca_saldo) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else None,
                    "Kredit (Rp)": kredit if kredit > 0 else None
                }
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
        df = st.session_state.df_neraca_saldo.copy()

        st.markdown("### Edit Data Neraca Saldo")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        edited_df["Debit (Rp)"] = pd.to_numeric(edited_df["Debit (Rp)"], errors="coerce").fillna(0)
        edited_df["Kredit (Rp)"] = pd.to_numeric(edited_df["Kredit (Rp)"], errors="coerce").fillna(0)

        st.session_state.df_neraca_saldo = edited_df

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

            # Halaman Laporan Laba Rugi
elif selected == 'Laporan Laba Rugi':
    st.subheader('Laporan Laba Rugi')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Memeriksa apakah DataFrame sudah ada dalam session_state
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

        # Logika untuk menambah transaksi
        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Menambah transaksi ke DataFrame
                nomor = len(st.session_state.df_laporan_laba_rugi) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0
                }
                st.session_state.df_laporan_laba_rugi = pd.concat(
                    [st.session_state.df_laporan_laba_rugi, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        # Reset Data
        if reset:
            st.session_state.df_laporan_laba_rugi = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Menampilkan tabel dan memungkinkan editing
    if st.session_state.df_laporan_laba_rugi.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        # Tampilkan dan edit tabel
        df_edit = st.data_editor(
            st.session_state.df_laporan_laba_rugi,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Memastikan kolom debit dan kredit diubah menjadi numerik dan diisi dengan 0 jika kosong
        df_edit["Debit (Rp)"] = pd.to_numeric(df_edit["Debit (Rp)"], errors="coerce").fillna(0)
        df_edit["Kredit (Rp)"] = pd.to_numeric(df_edit["Kredit (Rp)"], errors="coerce").fillna(0)

        # Update DataFrame di session_state
        st.session_state.df_laporan_laba_rugi = df_edit

        # Menampilkan tabel tanpa bagian total
        st.markdown("### Tabel Laporan Laba Rugi")
        st.dataframe(
            st.session_state.df_laporan_laba_rugi.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )


         # Halaman Laporan Perubahan Modal
elif selected == 'Laporan Perubahan Modal':
    st.subheader('Laporan Perubahan Modal')
    st.markdown('Periode 30 April 2025')
        
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Memeriksa apakah DataFrame sudah ada dalam session_state
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

        # Logika untuk menambah transaksi
        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Menambah transaksi ke DataFrame
                nomor = len(st.session_state.df_laporan_perubahan_modal) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0
                }
                st.session_state.df_laporan_perubahan_modal = pd.concat(
                    [st.session_state.df_laporan_perubahan_modal, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        # Reset Data
        if reset:
            st.session_state.df_laporan_perubahan_modal = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Menampilkan tabel dan memungkinkan editing
    if st.session_state.df_laporan_perubahan_modal.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        # Tampilkan dan edit tabel
        df_edit = st.data_editor(
            st.session_state.df_laporan_perubahan_modal,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Memastikan kolom debit dan kredit diubah menjadi numerik dan diisi dengan 0 jika kosong
        df_edit["Debit (Rp)"] = pd.to_numeric(df_edit["Debit (Rp)"], errors="coerce").fillna(0)
        df_edit["Kredit (Rp)"] = pd.to_numeric(df_edit["Kredit (Rp)"], errors="coerce").fillna(0)

        # Update DataFrame di session_state
        st.session_state.df_laporan_perubahan_modal = df_edit

        # Menampilkan tabel tanpa bagian total
        st.markdown("### Tabel Laporan Perubahan Modal")
        st.dataframe(
            st.session_state.df_laporan_perubahan_modal.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )


            # Halaman Laporan Posisi Keuangan
elif selected == 'Laporan Posisi Keuangan':
    st.subheader('Laporan Posisi Keuangan')
    st.markdown('Periode 30 April 2025')
    
    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Memeriksa apakah DataFrame sudah ada dalam session_state
    if "df_laporan_posisi_keuangan" not in st.session_state:
        st.session_state.df_laporan_posisi_keuangan = pd.DataFrame(columns=columns)

    # Formulir untuk menambah transaksi
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

        # Logika untuk menambah transaksi
        if tambah:
            # Validasi input
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                # Menambah transaksi ke DataFrame
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

        # Reset Data
        if reset:
            st.session_state.df_laporan_posisi_keuangan = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Menampilkan tabel dan memungkinkan editing
    if st.session_state.df_laporan_posisi_keuangan.empty:
        st.info("Tabel belum memiliki transaksi. Tambahkan transaksi di atas.")
    else:
        # Tampilkan dan edit tabel
        df_edit = st.data_editor(
            st.session_state.df_laporan_posisi_keuangan,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Memastikan kolom debit dan kredit diubah menjadi numerik dan diisi dengan 0 jika kosong
        df_edit["Debit (Rp)"] = pd.to_numeric(df_edit["Debit (Rp)"], errors="coerce").fillna(0)
        df_edit["Kredit (Rp)"] = pd.to_numeric(df_edit["Kredit (Rp)"], errors="coerce").fillna(0)

        # Update DataFrame di session_state
        st.session_state.df_laporan_posisi_keuangan = df_edit

        # Menampilkan tabel tanpa bagian total
        st.markdown("### Tabel Laporan Posisi Keuangan")
        st.dataframe(
            st.session_state.df_laporan_posisi_keuangan.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

            # Halaman Jurnal Penutup

elif selected == 'Jurnal Penutup':
    st.subheader('Jurnal Penutup')
    st.markdown('Periode 30 April 2025')  # Bisa pakai tanggal dinamis juga

    columns = ["No", "Nama Akun", "Debit (Rp)", "Kredit (Rp)"]

    # Inisialisasi session_state untuk jurnal penutup
    if "df_jurnal_penutup" not in st.session_state:
        st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)

    # Form tambah transaksi jurnal penutup
    with st.form("form_tambah_transaksi_jurnal_penutup", clear_on_submit=True):
        st.write("Tambah Transaksi Jurnal Penutup")
        nama_akun = st.text_input("Nama Akun")
        debit = st.number_input("Debit (Rp)", min_value=0, step=1000)
        kredit = st.number_input("Kredit (Rp)", min_value=0, step=1000)
        col1, col2 = st.columns(2)
        with col1:
            tambah = st.form_submit_button("Tambah Transaksi")
        with col2:
            reset = st.form_submit_button("Reset Data")

        # Tambah transaksi
        if tambah:
            if nama_akun.strip() == "" or (debit == 0 and kredit == 0):
                st.warning("Nama akun wajib diisi dan salah satu nilai (debit/kredit) tidak boleh nol.")
            else:
                nomor = len(st.session_state.df_jurnal_penutup) + 1
                row = {
                    "No": nomor,
                    "Nama Akun": nama_akun,
                    "Debit (Rp)": debit if debit > 0 else 0,
                    "Kredit (Rp)": kredit if kredit > 0 else 0
                }
                st.session_state.df_jurnal_penutup = pd.concat(
                    [st.session_state.df_jurnal_penutup, pd.DataFrame([row])],
                    ignore_index=True
                )
                st.success("Transaksi berhasil ditambahkan.")

        # Reset data
        if reset:
            st.session_state.df_jurnal_penutup = pd.DataFrame(columns=columns)
            st.info("Data berhasil direset.")

    # Tampilkan dan edit tabel
    if st.session_state.df_jurnal_penutup.empty:
        st.info("Belum ada transaksi jurnal penutup.")
    else:
        df_edit = st.data_editor(
            st.session_state.df_jurnal_penutup,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        # Konversi nilai debit dan kredit ke numerik (jika diedit user)
        df_edit["Debit (Rp)"] = pd.to_numeric(df_edit["Debit (Rp)"], errors="coerce").fillna(0)
        df_edit["Kredit (Rp)"] = pd.to_numeric(df_edit["Kredit (Rp)"], errors="coerce").fillna(0)

        # Update ulang nomor urut
        df_edit["No"] = range(1, len(df_edit) + 1)

        # Simpan kembali ke session_state
        st.session_state.df_jurnal_penutup = df_edit

        # Tampilkan tabel
        st.markdown("### Tabel Jurnal Penutup")
        st.dataframe(
            df_edit.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )

        # Total debit dan kredit
        total_debit = df_edit["Debit (Rp)"].sum()
        total_kredit = df_edit["Kredit (Rp)"].sum()

        st.markdown(f"**Total Debit: Rp {total_debit:,.0f}**")
        st.markdown(f"**Total Kredit: Rp {total_kredit:,.0f}**")


            # Halaman Neraca Saldo Setelah Penutup    
elif selected == 'Neraca Saldo Setelah Penutup':
    st.subheader('Neraca Saldo Setelah Penutup') 
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

        st.markdown("### Neraca Saldo (dengan Total)")
        st.dataframe(
            df_total.fillna(0).style.format({
                "Debit (Rp)": "Rp {:,.0f}",
                "Kredit (Rp)": "Rp {:,.0f}"
            }),
            use_container_width=True
        )