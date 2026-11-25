import streamlit as st
from datetime import datetime

# Pengaturan halaman web
st.set_page_config(page_title="PacilSpace", page_icon="🏫", layout="wide")

# Data sementara (nanti kita sambungkan ke CSV / Database)
if "ruang_kelas" not in st.session_state:
    st.session_state.ruang_kelas = {
        "Gedung A - 2301": {"status": "Kosong", "update": "Berdasarkan jadwal SIAK-NG"},
        "Gedung A - 2302": {"status": "Dipakai", "update": "Ada kelas DDP1 (10:00 - 12:00)"},
        "Gedung B - 2401": {"status": "Kosong", "update": "Berdasarkan jadwal SIAK-NG"},
        "Gedung B - 2402": {"status": "Dipakai", "update": "Dilaporkan dipakai rapat (5 menit lalu)"},
    }

if "area_umum" not in st.session_state:
    st.session_state.area_umum = {
        "Kantin Pacil": {"status": "Sedang", "meja": "Masih ada beberapa meja kosong", "update": "Baru saja"},
        "Student Lounge": {"status": "Penuh", "meja": "Hampir penuh", "update": "10 menit lalu"},
    }

# Header
st.title("🏫 PacilSpace")
st.caption("Pantau ketersediaan ruang kelas, Kantin Pacil, dan Student Lounge Fasilkom UI.")

# 3 Tab Utama
tab1, tab2, tab3 = st.tabs(["📚 Ruang Kelas", "🍜 Kantin & Lounge", "🎥 Simulasi AI CCTV"])

# --- TAB 1: RUANG KELAS ---
with tab1:
    st.subheader("Status Ruang Kelas")
    cols = st.columns(2)

    for idx, (nama_ruang, info) in enumerate(st.session_state.ruang_kelas.items()):
        with cols[idx % 2]:
            with st.container(border=True):
                ikon = "🟢" if info["status"] == "Kosong" else "🔴"
                st.markdown(f"### {ikon} {nama_ruang}")
                st.write(f"**Status:** {info['status']}")
                st.caption(f"Info: {info['update']}")

                tombol_label = "Lapor Dipakai" if info["status"] == "Kosong" else "Lapor Kosong"
                if st.button(tombol_label, key=f"btn_{nama_ruang}"):
                    status_baru = "Dipakai" if info["status"] == "Kosong" else "Kosong"
                    jam_sekarang = datetime.now().strftime("%H:%M")
                    st.session_state.ruang_kelas[nama_ruang] = {
                        "status": status_baru,
                        "update": f"Dilaporkan mahasiswa pukul {jam_sekarang}"
                    }
                    st.rerun()

# --- TAB 2: KANTIN & STUDENT LOUNGE ---
with tab2:
    st.subheader("Kondisi Kantin & Student Lounge")
    for tempat, info in st.session_state.area_umum.items():
        with st.container(border=True):
            warna = {"Sepi": "🟢", "Sedang": "🟡", "Penuh": "🔴"}[info["status"]]
            st.markdown(f"### {warna} {tempat} — {info['status']}")
            st.write(info["meja"])
            st.caption(f"Terakhir diupdate: {info['update']}")

            pilihan = st.radio(
                f"Update kondisi {tempat}:",
                ["Sepi", "Sedang", "Penuh"],
                horizontal=True,
                key=f"radio_{tempat}"
            )
            if st.button(f"Simpan Update {tempat}", key=f"save_{tempat}"):
                jam_sekarang = datetime.now().strftime("%H:%M")
                ket_meja = {
                    "Sepi": "Banyak meja kosong",
                    "Sedang": "Masih ada beberapa meja kosong",
                    "Penuh": "Hampir penuh / susah cari meja"
                }[pilihan]
                st.session_state.area_umum[tempat] = {
                    "status": pilihan,
                    "meja": ket_meja,
                    "update": f"Pukul {jam_sekarang} (Crowdsourcing)"
                }
                st.rerun()

# --- TAB 3: SIMULASI AI CCTV ---
with tab3:
    st.subheader("🎥 Prototype AI Deteksi Keramaian (YOLOv8 + OpenCV)")
    st.info("Fitur ini akan mendeteksi jumlah orang dari video/webcam untuk memperbarui status Kantin Pacil secara otomatis.")
    st.write("🚧 *Siap dipasang modul AI pada tahap berikutnya.*")