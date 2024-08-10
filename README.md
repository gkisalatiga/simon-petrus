# simon-petrus
Manajemen konten digital terintegrasi dan panel kendali administrator GKI Salatiga

Tidak ada kompilasi biner dari program ini, karena hasil uji coba awal menunjukkan bahwa ukuran kode biner mencapai 1 GB.
Program hanya dapat dijalankan menggunakan Python.

## Cara Instal

1. Klon repositori ini

```
git clone https://github.com/gkisalatiga/simon-petrus
cd simon-petrus
```

2. Instal dependensi Python

```
python -m pip install -r requirements.txt
```

3. Jalankan modul utama aplikasi

```
python src/simon_petrus/main.py
```

## Dependencies

- [**GhostScript**](http://www.a-pdf.com/convert-to-pdf/gs.exe) for generating PDF preview thumbnails.
- [**Poppler**](https://github.com/oschwartz10612/poppler-windows/releases/) for converting PDF to image using [`pdf2image`](https://pypi.org/project/pdf2image/).

## Attribution

- [ThreadWithResult](https://github.com/shailshouryya/save-thread-result) by Shail Shouryya (MIT-Licensed)
