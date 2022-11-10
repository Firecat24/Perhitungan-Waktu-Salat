from flask import Flask, render_template, request
import math

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def salat():
    if request.method == "GET":
        return render_template('salat.html')
    elif request.method == "POST":
        deklinasi_jam_1, deklinasi_menit_1, deklinasi_detik_1 = request_form("kds", "kdsm", "kdsd")
        rdeklinasi_subuh = math.radians((deklinasi_jam_1) + (deklinasi_menit_1/60) + (deklinasi_detik_1/3600))

        deklinasi_jam_2, deklinasi_menit_2, deklinasi_detik_2 = request_form("kda", "kdam", "kdad")
        rdeklinasi_asar = math.radians((deklinasi_jam_2) + (deklinasi_menit_2/60) + (deklinasi_detik_2/3600))

        deklinasi_jam_3, deklinasi_menit_3, deklinasi_detik_3 = request_form("kdm", "kdmm", "kdmd")
        rdeklinasi_magrib = math.radians((deklinasi_jam_3) + (deklinasi_menit_3/60) + (deklinasi_detik_3/3600))

        deklinasi_jam_4, deklinasi_menit_4, deklinasi_detik_4 = request_form("kdm", "kdmm", "kdmd")
        rdeklinasi_isya = math.radians((deklinasi_jam_4) + (deklinasi_menit_4/60) + (deklinasi_detik_4/3600))

        lintang_jam, lintang_menit, lintang_detik = request_form("klj", "klm", "kld")
        lintang = math.radians((lintang_jam) + (lintang_menit/60) + (lintang_detik/3600))

        bujur_jam, bujur_menit, bujur_detik = request_form("kbj", "kbm", "kbd")
        bujur = (bujur_jam) + (bujur_menit/60) + (bujur_detik/3600)

        zona_waktu = int(request.form["kzw"])
        KWD = ((zona_waktu - bujur)/15)

        Hari, Bulan, Tahun = request_form("kbj", "kbbm", "ktj")

        if Bulan == 1:
            Tahun = Tahun - 1
            Bulan = 1 + 12
        if Bulan == 2:
            Tahun = Tahun - 1
            Bulan = 2 + 12
        A = math.floor (Tahun/100)
        B = 2 + math.floor (A/4) - A

        Dsubuh = (Hari-1) + (((21 * 3600)+(0 * 60)+ 0)/86400)
        Dzuhur = Hari + (((5 * 3600)+(0 * 60)+ 0)/86400)
        Dasar = Hari + (((8 * 3600)+(0 * 60)+ 0)/86400)
        Dmagrib = Hari + (((11 * 3600)+(0 * 60)+ 0)/86400)
        Disya = Hari + (((12 * 3600)+(0 * 60)+ 0)/86400)

        eot = perhitungan_equation(Tahun, Bulan, B, Dzuhur)
        EoT_zuhur = eot
        eot = perhitungan_equation(Tahun, Bulan, B, Dsubuh)
        EoT_subuh = eot
        eot = perhitungan_equation(Tahun, Bulan, B, Dasar)
        EoT_asar = eot
        eot = perhitungan_equation(Tahun, Bulan, B, Dmagrib)
        EoT_magrib = eot
        eot = perhitungan_equation(Tahun, Bulan, B, Disya)
        EoT_isya = eot

        # tinggi_tempat_jam = int(request.form["kt"])
        i = 2/60

        # subuh
        tinggi_subuh= -20
        rtinggi_subuh= math.radians(tinggi_subuh)

        # asar
        
        lintang1 = lintang_jam + (lintang_menit/60) + (lintang_detik/3600)
        deklinasi_2 = deklinasi_jam_2 + (deklinasi_menit_2/60) + (deklinasi_detik_2/3600)
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
        
        jams, menits, detiks = hasil (pk)
        Subuh = "Subuh = {jam}:{menit}:{detik}".format(jam=jams, menit=menits, detik=detiks)
        jams, menits, detiks = hasil (pk1)
        Zuhur = "Zuhur = {jam}:{menit}:{detik}".format(jam=jams, menit=menits, detik=detiks)
        jams, menits, detiks = hasil (pk2)
        Asar = "Asar = {jam}:{menit}:{detik}".format(jam=jams, menit=menits, detik=detiks)
        jams, menits, detiks = hasil (pk3)
        Magrib = "Magrib = {jam}:{menit}:{detik}".format(jam=jams, menit=menits, detik=detiks)
        jams, menits, detiks = hasil (pk4)
        Isya = "Isya = {jam}:{menit}:{detik}".format(jam=jams, menit=menits, detik=detiks)

        return render_template("salat.html", Subuh=Subuh, Zuhur=Zuhur, Asar=Asar, Magrib=Magrib, Isya=Isya)

def hasil(Pk):
    jams = math.floor(Pk)
    menit0 = (Pk) - math.floor(Pk)
    menits = math.floor((menit0)*60)
    detik0 = (Pk) - math.floor(Pk)
    detik1 = (detik0) - (math.floor(detik0)*60)
    detiks = math.floor((detik1)*60)
    return jams, menits, detiks

def perhitungan_equation (Tahun, Bulan, B, Dzuhur):
    JD = 1720994.5 + math.floor(365.25*Tahun)+ math.floor(30.6001*(Bulan+1))+ (B) + (Dzuhur)
    U = (JD - 2451545)/36525
    L00 = 280.46607 + (36000.7698*U)
    L01 = math.floor((280.46607 + (36000.7698*U))/360)
    L02 = L01 * 360
    L0 =  L00 - L02
    L0R = math.radians (L0)
    EoT = (-(1789 + 237 * U)* math.sin (L0R) - (7146 - 62*U)* math.cos (L0R) + (9934 - 14*U)* math.sin(2*L0R)- (29 + 5*U)* math.cos(2*L0R) + (74 + 10*U)* math.sin(3*L0R) + (320 - 4*U)* math.cos(3*L0R) - 212* math.sin(4*L0R))/1000
    Jam = 0
    Menit = math.floor(EoT)
    detik0 = EoT - math.floor(EoT)
    detik = math.floor((detik0)*60)
    eot = Jam + (Menit/60) + (detik/3600)
    return eot

def perhitungan_degree(rlintang, rdeklinasi, rtinggi):
    t = math.degrees(math.acos(-math.tan(rlintang)* math.tan(rdeklinasi)+ 1/math.cos(rlintang)* 1/math.cos(rdeklinasi)* math.sin (rtinggi)))
    return t

def request_form(name1, name2, name3):
    x = int(request.form[name1])
    y = int(request.form[name2])
    z = int(request.form[name3])
    return x,y,z

if __name__ == '__main__':
    app.run()
