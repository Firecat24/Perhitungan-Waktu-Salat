from flask import Flask, render_template, request, redirect
from calendar import monthrange
from datetime import datetime
import math

app=Flask(__name__)

@app.route("/", methods=["GET"])
def salat():
    if request.method == "GET":
        return render_template('salat.html')
        
@app.route("/result", methods=["GET","POST"])
def result():
    if request.method == "GET":
        return redirect("/", code=405)
    elif request.method == "POST":
        results = []
        Hari, Bulan, Tahun = request_form("khd", "kbbm", "ktj")
        month = Bulan
        year = Tahun
        Hari = 1
        datenow = datetime(Tahun, Bulan, Hari)
        max_day = monthrange(datenow.year, datenow.month)[1]
        for day in range(1, max_day+1):
            result = []
            lintang_jam, lintang_menit, lintang_detik = request_form("klj", "klm", "kld")
            lintang = math.radians((lintang_jam) + (lintang_menit/60) + (lintang_detik/3600))

            bujur_jam, bujur_menit, bujur_detik = request_form("kbj", "kbm", "kbd")
            bujur = (bujur_jam) + (bujur_menit/60) + (bujur_detik/3600)

            zona_waktu = int(request.form["kzw"])
            KWD = ((zona_waktu - bujur)/15) 
            date = datetime(year, month, day)
            tanggal = convert_date(date)


            if Bulan <=2 :
                Bulan = Bulan + 12
                Tahun = Tahun - 1
                A = math.floor (Tahun/100)
            else :
                A = math.floor (Tahun/100)
            if Tahun <=1582:
                B = 0
            elif Tahun >1582:
                B = 2 + math.floor (A/4) - A
            Dsubuh = (day-1) + (((21 * 3600)+(0 * 60)+ 0)/86400)
            Dzuhur = day + (((5 * 3600)+(0 * 60)+ 0)/86400)
            Dasar = day + (((8 * 3600)+(0 * 60)+ 0)/86400)
            Dmagrib = day + (((11 * 3600)+(0 * 60)+ 0)/86400)
            Disya = day + (((12 * 3600)+(0 * 60)+ 0)/86400)

            deklinasi_zuhur, eot = perhitungan_equation(Tahun, Bulan, B, Dzuhur)
            EoT_zuhur = eot
            rdeklinasi_zuhur = math.radians(deklinasi_zuhur)
            deklinasi_subuh, eot = perhitungan_equation(Tahun, Bulan, B, Dsubuh)
            EoT_subuh = eot
            rdeklinasi_subuh = math.radians(deklinasi_subuh)
            deklinasi_asar, eot = perhitungan_equation(Tahun, Bulan, B, Dasar)
            EoT_asar = eot
            rdeklinasi_asar = math.radians(deklinasi_asar)
            deklinasi_magrib, eot = perhitungan_equation(Tahun, Bulan, B, Dmagrib)
            EoT_magrib = eot
            rdeklinasi_magrib = math.radians(deklinasi_magrib)
            deklinasi_isya, eot = perhitungan_equation(Tahun, Bulan, B, Disya)
            EoT_isya = eot
            rdeklinasi_isya = math.radians(deklinasi_isya)

            i = 2/60

            # subuh
            tinggi_subuh= -20
            rtinggi_subuh= math.radians(tinggi_subuh)

            # asar
            
            lintang1 = lintang_jam + (lintang_menit/60) + (lintang_detik/3600)
            deklinasi_2 = deklinasi_asar
            tinggi_asar0= math.radians(abs(lintang1 - deklinasi_2))
            tinggi_asar= math.degrees(math.atan(1/((math.tan(tinggi_asar0))+1)))
            rtinggi_asar= math.radians(tinggi_asar)

            # magrib
            rtinggi_magrib= math.radians(-1)
            
            # isya
            rtinggi_isya= math.radians(-18)

            # perhitungan
            # perhitungan waktu subuh
            t_subuh = perhitungan_degree(lintang, rdeklinasi_subuh, rtinggi_subuh)
            t_selesai_subuh = (t_subuh)/15
            pk = 12-(EoT_subuh)-(t_selesai_subuh)+(KWD)+(i)
            # perhitungan waktu zuhur
            pk1 = 12-(EoT_zuhur)+(KWD)+(i)
            # perhitungan waktu asar
            t_asar = perhitungan_degree(lintang, rdeklinasi_asar, rtinggi_asar)
            t_selesai_asar = (t_asar)/15
            pk2 = 12-(EoT_asar)+(t_selesai_asar)+(KWD)+(i)
            # perhitungan waktu magrib
            t_magrib = perhitungan_degree(lintang, rdeklinasi_magrib, rtinggi_magrib)
            t_selesai_magrib = (t_magrib)/15
            pk3 = 12-(EoT_magrib)+(t_selesai_magrib)+(KWD)+(i)
            # perhitungan waktu isya
            t_isya=  perhitungan_degree(lintang, rdeklinasi_isya, rtinggi_isya)
            t_selesai_isya = (t_isya)/15
            pk4 = 12-(EoT_isya)+(t_selesai_isya)+(KWD)+(i)
            
            jams, menits = hasil (pk)
            Subuh = "{jam}:{menit}".format(jam=jams, menit=str(menits).zfill(2))
            jams, menits = hasil (pk1)
            Zuhur = "{jam}:{menit}".format(jam=jams, menit=str(menits).zfill(2))
            jams, menits = hasil (pk2)
            Asar = "{jam}:{menit}".format(jam=jams, menit=str(menits).zfill(2))
            jams, menits = hasil (pk3)
            Magrib = "{jam}:{menit}".format(jam=jams, menit=str(menits).zfill(2))
            jams, menits = hasil (pk4)
            Isya = "{jam}:{menit}".format(jam=jams, menit=str(menits).zfill(2))
            result.append(tanggal)
            result.append(Subuh)
            result.append(Zuhur)
            result.append(Asar)
            result.append(Magrib)
            result.append(Isya)
            results.append(result)
            tupled = tuple(results)
       
        return render_template("result.html", result = tupled, len = len(tupled))

def hasil(Pk):
    jams = math.floor(Pk)
    menit0 = (Pk) - math.floor(Pk)
    menits = round((menit0)*60)
    return jams, menits

def perhitungan_equation (Tahun, Bulan, B, Dzuhur):
    JD = 1720994.5 + math.floor(365.25*Tahun)+ math.floor(30.6001*(Bulan+1))+ (B) + (Dzuhur)
    T = (JD - 2451545)/36525
    L00 = 280.46607 + (36000.7698*T)
    L01 = math.floor((280.46607 + (36000.7698*T))/360)
    L02 = L01 * 360
    L0 =  L00 - L02
    L0R = math.radians (L0)
    EoT = (-(1789 + 237 * T)* math.sin (L0R) - (7146 - 62*T)* math.cos (L0R) + (9934 - 14*T)* math.sin(2*L0R)- (29 + 5*T)* math.cos(2*L0R) + (74 + 10*T)* math.sin(3*L0R) + (320 - 4*T)* math.cos(3*L0R) - 212* math.sin(4*L0R))/1000
    Jam = 0
    Menit = math.floor(EoT)
    detik0 = EoT - math.floor(EoT)
    detik = math.floor((detik0)*60)
    eot = Jam + (Menit/60) + (detik/3600)
    U = T/100
    L0 = 280.46646 + (36000.76983*T)+ (0.0003032*(T**2))
    while L0 < 0:
        L0 += 360
    while L0 > 360:
        L0 -= 360
    M = 357.52911 + (35999.05029*T)+ (0.0001537*(T**2))
    while M < 0:
        M += 360
    while M > 360:
        M -= 360
    Mrad = math.radians(M)
    eksentrisitas = 0.016708634 - (0.000042037*T) - (0.0000001267*(T**2))
    C = (1.914602-(0.004817*T)- 0.000014*(T**2))* math.sin(Mrad) + (0.019993-(0.000101*T))* math.sin(2*Mrad) + 0.000289 * math.sin(3*Mrad)
    longitude = L0 + C
    longituderad = math.radians(longitude)
    v = M + C
    vrad = math.radians(v)
    R = 1.000001018*(1-(eksentrisitas**2)) / (1 + eksentrisitas *math.cos(vrad))
    omega = 125.04452 - 1934.136261*T + 0.0020708*(T**2) + ((T**3)/450000)
    omegarad = math.radians(omega)
    lamda = longitude - 0.00569 - 0.00478 * math.sin(omegarad)
    L = 280.4665 + 36000.7698*T
    Lrad = math.radians(L)
    L1 = 218.3165 + 481267.8813*T
    L1rad = math.radians(L1)
    #sampek sini delta_obliquity memakai rumus low accuracy 
    delta_obliquity1 = ((9.20/3600) * math.cos(omegarad)) + (0.57/3600)* math.cos(2*Lrad) + (0.10/3600)*math.cos(2*L1rad) - (0.09/3600)*math.cos(2*omegarad)
    epsilon0 = (23*3600) + (26*60) + 21.448 - 4680.93*U - 1.55*(U**2) + 1999.25*(U**3) - 51.38*(U**4) - 249.67*(U**5) - 39.05*(U**6) + 7.12*(U**7) + 27.87*(U**8) + 5.79*(U**9) + 2.45*(U**10)
    obliquity = epsilon0/3600
    obliquity_benar = obliquity + delta_obliquity1
    obliquity_benarrad = math.radians(obliquity_benar)
    alpha = math.degrees(math.atan2((math.cos(obliquity_benarrad)* math.sin(longituderad)), math.cos(longituderad)))
    while alpha < 0:
        alpha += 360
    while alpha > 360:
        alpha -= 360
    deklinasi = math.degrees(math.asin(math.sin(obliquity_benarrad)* math.sin(longituderad)))
    return deklinasi, eot
    

def perhitungan_degree(rlintang, rdeklinasi, rtinggi):
    t = math.degrees(math.acos(-math.tan(rlintang)* math.tan(rdeklinasi)+ 1/math.cos(rlintang)* 1/math.cos(rdeklinasi)* math.sin (rtinggi)))
    return t

def request_form(name1, name2, name3):
    x = int(request.form[name1])
    y = int(request.form[name2])
    z = int(request.form[name3])
    return x,y,z

def convert_date(date_conversion):
    if isinstance(date_conversion, datetime):
        date_converted = f"{date_conversion:%A, %d %B %Y}"
        if 'Monday' in date_converted:
            date_converted = date_converted.replace("Monday","Senin")
        elif 'Tuesday' in date_converted:
            date_converted = date_converted.replace("Tuesday","Selasa")
        elif 'Wednesday' in date_converted:
            date_converted = date_converted.replace("Wednesday","Rabu")
        elif 'Thursday' in date_converted:
            date_converted = date_converted.replace("Thursday","Kamis")
        elif 'Friday' in date_converted:
            date_converted = date_converted.replace("Friday","Jum\'at")
        elif 'Saturday' in date_converted:
            date_converted = date_converted.replace("Saturday","Sabtu")
        elif 'Sunday' in date_converted:
            date_converted = date_converted.replace("Sunday","Minggu")

        if 'January' in date_converted:
            date_converted = date_converted.replace("January", "Januari")
        elif 'February' in date_converted:
            date_converted = date_converted.replace("February", "Februari")
        elif 'March' in date_converted:
            date_converted = date_converted.replace("March", "Maret")
        elif 'April' in date_converted:
            date_converted = date_converted.replace("April", "April")
        elif 'May' in date_converted:
            date_converted = date_converted.replace("May", "Mei")
        elif 'June' in date_converted:
            date_converted = date_converted.replace("Juni", "Juni")
        elif 'July' in date_converted:
            date_converted = date_converted.replace("July", "Juli")
        elif 'August' in date_converted:
            date_converted = date_converted.replace("August", "Agustus")
        elif 'September' in date_converted:
            date_converted = date_converted.replace("September", "September")
        elif 'October' in date_converted:
            date_converted = date_converted.replace("October", "Oktober")
        elif 'November' in date_converted:
            date_converted = date_converted.replace("November", "November")
        elif 'December' in date_converted:
            date_converted = date_converted.replace("December", "Desember")
        return date_converted

if __name__ == '__main__':
    app.run(debug=True)
