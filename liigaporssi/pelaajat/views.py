import sqlite3
from django.shortcuts import render
from django.conf import settings

def satunnaiset_pelaajat(request):
    DB_PATH = settings.DATABASES['default']['NAME']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT nimi FROM HIFK_pelaajat ORDER BY RANDOM() LIMIT 6")
    pelaajat = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render(request, 'pelaajat/satunnaiset.html', {'pelaajat': pelaajat})

# Create your views here.
