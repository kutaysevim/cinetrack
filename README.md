# 🎬 CineTrack - Film & Dizi Öneri Platformu

CineTrack, kullanıcıların film ve dizileri keşfedebileceği, puanlayabileceği,
yorum yapabileceği ve izleme listesi oluşturabileceği bir web uygulamasıdır.

## 🚀 Özellikler

- 🎥 Film ve dizi listeleme, detay görüntüleme
- ➕ Film/dizi ekleme, düzenleme, silme (CRUD)
- ⭐ Puanlama ve yorum sistemi
- 🔖 Kişisel izleme listesi
- 🔍 Arama ve tür/kategori filtreleme
- 📄 Sayfalama (Pagination)
- 👤 Kullanıcı kayıt/giriş/çıkış sistemi
- 🔒 Yetkilendirme (sadece kendi filminizi düzenleyebilirsiniz)
- 🌐 REST API (Django REST Framework)
- 📱 Responsive tasarım (Bootstrap 5)

## 🛠️ Kurulum

### Gereksinimler
- Python 3.10+
- pip

### Adımlar

1. Repoyu klonlayın:
```bash
git clone https://github.com/kullaniciadi/cinetrack.git
cd cinetrack
```

2. Virtual environment oluşturun:
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Mac/Linux
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:
```bash
python manage.py migrate
```

5. Admin kullanıcısı oluşturun:
```bash
python manage.py createsuperuser
```

6. Sunucuyu başlatın:
```bash
python manage.py runserver
```

7. Tarayıcıda açın: `http://127.0.0.1:8000`

## 📁 Proje Yapısı