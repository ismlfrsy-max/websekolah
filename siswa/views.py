
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.utils.html import escape

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Mengubah satu hasil query menjadi dictionary."""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row is None:
        return None

    return dict(zip(columns, row))


def siswa_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM siswa_siswa
            ORDER BY id DESC
        """)
        data_siswa = dictfetchall(cursor)
    #pasing data dari view ke template
    search_text = "bandung"

    
    
    return render(request, 'list.html', {
        'keyword': 'Wonosobo',
        'data': data_siswa
    })





def siswa_detail(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM siswa_siswa
            WHERE id = %s
            """,
            [id]
        )
        siswa = dictfetchone(cursor)    

    return render(request, 'detail.html', {
        'siswa': siswa,
    })



def siswa_create(request):
    # cek request yg masuk kalo dia post (submit)
    if request.method == 'POST':
        # tarik data per name inputan
        nama = request.POST.get('nama', '').strip()
        # Ambil data, jika kosong (''), ubah jadi None agar dibaca NULL oleh database
        umur = request.POST.get('umur', '').strip()
        umur = int(umur) if umur else None

        tgl_lahir = request.POST.get('tgl_lahir', '').strip()
        tgl_lahir = tgl_lahir if tgl_lahir else None

        status_hadir_raw = request.POST.get('status_hadir', '').strip()
        # Jika teksnya 'Hadir' maka simpan True, jika 'Tidak Hadir' atau kosong simpan False
        status_hadir = True if status_hadir_raw == 'Hadir' else False

        nilai_akhir = request.POST.get('nilai_akhir', '').strip()
        nilai_akhir = float(nilai_akhir) if nilai_akhir else None

        # eksekusi perintah INSERT ke database        
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO siswa_siswa (nama, umur, tgl_lahir, status_hadir, nilai_akhir)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [nama, umur, tgl_lahir, status_hadir, nilai_akhir]
            )

        return redirect('siswa_list')
    
    
    return render(request, 'form.html')

def siswa_update(request, id):
    # 1. AMBIL DATA LAMA UNTUK DIISI KE FORM
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa_siswa WHERE id = %s", [id])
        siswa = dictfetchone(cursor)

    # Jika data tidak ketemu
    if not siswa:
        return HttpResponse("Data siswa tidak ditemukan")

    # 2. PROSES SIMPAN PERUBAHAN (KETIKA TOMBOL SIMPAN DIKLIK)
    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        
        umur = request.POST.get('umur', '').strip()
        umur = int(umur) if umur else None

        tgl_lahir = request.POST.get('tgl_lahir', '').strip()
        tgl_lahir = tgl_lahir if tgl_lahir else None

        # Sesuaikan dengan tipe Boolean database kamu
        status_hadir_raw = request.POST.get('status_hadir', '').strip()
        status_hadir = True if status_hadir_raw == 'Hadir' else False

        nilai_akhir = request.POST.get('nilai_akhir', '').strip()
        nilai_akhir = float(nilai_akhir) if nilai_akhir else None

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE siswa_siswa 
                SET nama=%s, umur=%s, tgl_lahir=%s, status_hadir=%s, nilai_akhir=%s
                WHERE id=%s
                """,
                [nama, umur, tgl_lahir, status_hadir, nilai_akhir, id]
            )
        
        return redirect('siswa_list')

    # 3. TAMPILKAN FORM DENGAN DATA SISWA
    # Karena tgl_lahir dari database mungkin berupa objek date, 
    # kita pastikan formatnya string YYYY-MM-DD agar bisa dibaca input type="date"
    # GANTI DENGAN KODE INI:
    if siswa['tgl_lahir']:
        # Jika tipe datanya string, kita ambil 10 karakter pertama saja (YYYY-MM-DD)
        if isinstance(siswa['tgl_lahir'], str):
            siswa['tgl_lahir'] = siswa['tgl_lahir'][:10]
        else:
            # Jaga-jaga kalau suatu saat tipenya berubah jadi objek date asli
            siswa['tgl_lahir'] = siswa['tgl_lahir'].strftime('%Y-%m-%d')

    return render(request, 'edit.html', {'siswa': siswa})


def siswa_delete(request, id):
    # 1. AMBIL DATA SISWA YANG AKAN DIHAPUS
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM siswa_siswa WHERE id = %s", [id])
        siswa = dictfetchone(cursor)

    # Jika data siswa tidak ditemukan
    if not siswa:
        return HttpResponse("Data siswa tidak ditemukan")

    # 2. PROSES JIKA TOMBOL "YA, HAPUS" DIKLIK (METHOD POST)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM siswa_siswa WHERE id = %s", [id])
        
        return redirect('siswa_list')

    # 3. TAMPILKAN HALAMAN KONFIRMASI (METHOD GET)
    return render(request, 'delete.html', {'siswa': siswa})
