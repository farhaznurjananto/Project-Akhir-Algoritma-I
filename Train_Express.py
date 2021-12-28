import os
import csv
import json
import datetime
import hashlib

db_account = "db_account.json"
db_train = "db_train.csv"
db_ticket = "db_ticket.csv"
db_basket = "db_basket.csv"
db_reporting = "db_reporting.csv"
db_reporting2 = "db_reporting2.csv"
day = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

# MENU FUNCTION
def strat_menu():
    try:
        open_file_db_account = open(db_account)
        open_file_db_train = open(db_train)
        open_file_db_ticket = open(db_ticket)
        open_file_db_basket = open(db_basket)
        open_file_db_reporting1 = open(db_reporting)
        open_file_db_reporting2 = open(db_reporting2)
        open_file_db_train.close()
        open_file_db_ticket.close()
        open_file_db_basket.close()
        open_file_db_reporting1.close()
        open_file_db_reporting2.close()
        open_file_db_account.close()
    except FileNotFoundError:
        with open(db_account, "w") as new_file:
            new_file.write(json.dumps([{"username": "admin", "password":"21232f297a57a5a743894a0e4a801fc3", "level":"ADMIN"}], indent=2))
        with open(db_train, "w", newline='') as database:
            writer = csv.DictWriter(database, fieldnames=["kereta","hari","asal","tujuan","harga","berangkat","tiba","tiket"])
            writer.writeheader()
        with open(db_ticket, "w", newline='') as database:
            writer = csv.DictWriter(database, fieldnames=["pemesan","penumpang","kereta","asal","tujuan","berangkat","tiba","harga","tanggal_berangkat","hari"])
            writer.writeheader()
        with open(db_basket, "w", newline='') as database:
            writer = csv.DictWriter(database, fieldnames=["pemesan","penumpang","kereta","asal","tujuan","berangkat","tiba","harga","tanggal_berangkat","hari"])
            writer.writeheader()
        with open(db_reporting, "w", newline='') as database:
            writer = csv.DictWriter(database, fieldnames=["total_user","total_pendapatan","total_tiket_terjual"])
            writer.writeheader()
            writer.writerows([{"total_user": 0, "total_pendapatan": 0, "total_tiket_terjual":0}])
        with open(db_reporting2, "w", newline='') as database:
            writer = csv.DictWriter(database, fieldnames=["asal","tujuan","pembeli","pendapatan"])
            writer.writeheader()
    while True:
        clear()
        header("SELAMAT DATANG DI TRAIN EXPRESS")

        menu = ["1 | MASUK", "2 | DAFTAR AKUN", "0 | KELUAR"]

        for i in menu:
            print("|{:<138}|".format(i))
        print("="*140)

        choice = input("MENU: ")
        if choice.isnumeric():
            choice = int(choice)
            if choice == 1:
                masuk()
            elif choice == 2:
                daftar()
            elif choice == 0:
                input("\nTERIMA KASIH")
                clear()
                exit()
            else:
                input(f"\nMENU {choice} TIDAK ADA")
        else:
            input(f"\nMENU {choice} TIDAK ADA")

def main_menu():
    while True:
        clear()
        if level == 'USER':
            header("SELAMAT DATANG DI TRAIN EXPRESS")

            menu = [
                    "1 | CARI TIKET KERETA", 
                    "2 | TIKET KERETA ANDA",  
                    "3 | PEMBATALAN TIKET", 
                    "4 | KERANJANG & BAYAR", 
                    "5 | GANTI PASSWORD", 
                    "0 | KELUAR"
                    ]

            for i in menu:
                print("|{:<138}|".format(i))
            print("="*140)

            choice = input("Menu: ")

            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    search()
                elif choice == 2:
                    show_ticket()
                    input("ENTER UNTUK KEMBALI KE MENU UTAMA.... ")
                elif choice == 3:
                    delete()
                elif choice == 4:
                    basket()
                elif choice == 5:
                    change_pw()
                elif choice == 0:
                    input("\nTERIMA KASIH")
                    strat_menu()
                else:
                    input("\nMENU TIDAK ADA")
            else:
                input("\nMENU TIDAK ADA")
        elif level == "ADMIN":
            header("MENU ADMIN TRAIN EXPRESS")
            
            trains = load_csv(db_train)

            menu = [
                    "1 | TAMPILKAN JADWAL KERETA API", 
                    "2 | TAMBAH JADWAL KERETA API",  
                    "3 | UPDATE JADWAL KERETA API", 
                    "4 | HAPUS JADWAL KERETA API", 
                    "5 | GANTI PASSWORD", 
                    "6 | REPORTING",
                    "0 | KELUAR"
                    ]

            for i in menu:
                print("|{:<138}|".format(i))
            print("="*140)

            choice = input("Menu: ")

            if choice.isnumeric():
                choice = int(choice)
                if choice == 1:
                    show_train(trains)
                    input("ENTER UNTUK KEMBALI KE MENU UTAMA.... ")
                elif choice == 2:
                    add_data()
                elif choice == 3:
                    update()
                elif choice == 4:
                    delete()
                elif choice == 5:
                    change_pw()
                elif choice == 6:
                    reporting()
                elif choice == 0:
                    input("\nTERIMA KASIH")
                    strat_menu()
                else:
                    input("\nMENU TIDAK ADA")
            else:
                input("\nMENU TIDAK ADA")

# GENERAL FUNCTION
def clear():
    os.system("cls")

def header(arg1):
    print("="*140)
    print("|{:^138}|".format(arg1))
    print("="*140)

def load_json():
    with open(db_account, "r") as dt_account:
        account = json.load(dt_account)
    return account

def load_csv(arg1):
    lst = []
    with open(arg1, "r") as database:
        reader = csv.DictReader(database)
        for rows in reader:
            lst.append(rows)
    return lst

def write_csv_ticket(arg1, arg2):
    with open(arg1, "w", newline='') as database:
        writer = csv.DictWriter(database, fieldnames=["pemesan","penumpang","kereta","asal","tujuan","berangkat","tiba","harga","tanggal_berangkat","hari"])
        writer.writeheader()
        writer.writerows(arg2)

def write_csv_train(arg1, arg2):
    with open(arg1, "w", newline='') as database:
        writer = csv.DictWriter(database, fieldnames=["kereta","hari","asal","tujuan","harga","berangkat","tiba","tiket"])
        writer.writeheader()
        writer.writerows(arg2)
    
def write_csv_reporting(arg1):
    with open(db_reporting, "w", newline='') as database:
        writer = csv.DictWriter(database, fieldnames=["total_user","total_pendapatan","total_tiket_terjual"])
        writer.writeheader()
        writer.writerows(arg1)

def write_csv_reporting2(arg1):
    with open(db_reporting2, "w", newline='') as database:
        writer = csv.DictWriter(database, fieldnames=["asal","tujuan","pembeli","pendapatan"])
        writer.writeheader()
        writer.writerows(arg1)

def show_train(arg1):
    clear()
    if isinstance(arg1, list):
        header("TIKET KERETA API")
        print("|{:^3}|{:<20}|{:^20}|{:^20}|{:^15}|{:^15}|{:^11}|{:^11}|{:^15}|".format("NO", "KERETA", "HARI", "ASAL", "TUJUAN", "HARGA", "BERANGKAT", "TIBA", "TIKET"))
        print("="*140)
        for idx, item in enumerate(arg1):
            print("|{:^3}|{:<20}|{:^20}|{:^20}|{:^15}|{:^15}|{:^11}|{:^11}|{:^15}|".format((idx+1), item["kereta"], item["hari"], item["asal"], item["tujuan"], item["harga"], item["berangkat"], item["tiba"], item["tiket"]))
        print("="*140)
    else:
        print('TIPE DATA TIDAK SESUAI')

def change_pw():
    while True:
        clear()
        header("GANTI PASSWORD")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

        accounts = load_json()

        old_pw = input("{:<30}: ".format("MASUKKAN PASSWORD LAMA"))
        hashed_password = hashlib.md5(old_pw.encode('utf-8')).hexdigest()
        if hashed_password == pw:
            new_pw1 = input("{:<30}: ".format("MASUKKAN PASSWORD BARU"))
            if new_pw1.upper() == "B":
                main_menu()
            else:
                new_pw2 = input("{:30}: ".format("MASUKKAN KEMBALI PASSWORD BARU"))
                if new_pw2.upper() == "B":
                    main_menu()
                elif new_pw2 == new_pw1:
                    for i in range(len(accounts)):
                        if accounts[i]['username'] == who:
                            accounts[i]['password'] = hashlib.md5(new_pw2.encode('utf-8')).hexdigest()

                    with open(db_account, "w") as output:
                        output.write(json.dumps(accounts, indent=2))
                    
                    input("\nPASSWORD BERHASIL DIRUBAH")
                    main_menu()
        elif old_pw.upper() == "B":
            main_menu()
        else:
            input("\nPASSWORD LAMA SALAH")

def delete():
    while True:
        if level == "USER":
            clear()
            load_file = []

            baskets = load_csv(db_basket)
            trains = load_csv(db_train)

            for i in range(len(baskets)):
                if baskets[i]["pemesan"] == who:
                    load_file.append(baskets[i])

            header("PEMBATALAN TIKET KERETA API")
            print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format("NO", "KERETA", "PENUMPANG", "TANGGAL BERANGKAT", "ASAL", "TUJUAN", "BERANGKAT", "TIBA"))
            print("="*140)
            for idx, item in enumerate(load_file):
                print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format((idx+1), item["kereta"], item["penumpang"], item["tanggal_berangkat"], item["asal"], item["tujuan"], item["berangkat"], item["tiba"]))
            print("="*140)
            
            print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
            print("="*140)
            idx = (input('TIKET YANG AKAN DIBATALKAN [NO/B]: '))
        elif level == "ADMIN":
            load_file = load_csv(db_train)
            show_train(load_file)
            header("DELETE JADWAL")
            print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
            print("="*140)
            idx = (input('JADWAL YANG AKAN DIHAPUS [NO/B]: '))

        if idx.isnumeric():
            idx = int(idx)
            if (idx - 1) in range(len(load_file)):
                choice = input("APAKAH ANDA YAKIN? [Y/N/B]: ")
                if choice.upper() == "Y":
                    if level == "USER":
                        baskets.remove(load_file[idx-1])

                        for i in range(len(trains)):
                            if trains[i]["kereta"] == load_file[idx-1]["kereta"] and trains[i]["asal"] == load_file[idx-1]["asal"] and trains[i]["tujuan"] == load_file[idx-1]["tujuan"] and trains[i]["harga"] == load_file[idx-1]["harga"] and trains[i]["berangkat"] == load_file[idx-1]["berangkat"] and trains[i]["tiba"] == load_file[idx-1]["tiba"] and trains[i]["hari"] == load_file[idx-1]["hari"]:
                                sisa_tiket = int(trains[i]["tiket"]) + 1
                                trains[i]["tiket"] = sisa_tiket

                        load_file.pop(idx - 1)
                            
                        write_csv_train(db_train, trains)
                        write_csv_ticket(db_basket, load_file)
                    elif level == "ADMIN":
                        load_file.pop(idx - 1)
                        write_csv_train(db_train, load_file)
                        
                    input("\nTELAH DIHAPUS")
                elif choice.upper() == "N":
                    input("\nKONFIRMASI DITERIMA")
                elif choice.upper() == "B":
                    main_menu()
                else:
                    input("\nMENU TIDAK ADA")
            else:
                input("\nPILIHAN TIDAK ADA")
        elif idx.upper() == "B":
            main_menu()
        else:
            input("\nANDA MEMASUKKAN SELAIN ANGKA")

# FUNCTION MENU AWAL
def masuk():
    while True:
        clear()
        header("MENU MASUK")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

        global level
        global who
        global pw

        accounts = load_json()
        username = input("Username: ")
        if username.upper() == "B":
            strat_menu()
        else:
            password = input("Password: ")
            if password.upper() == "B":
                strat_menu()
            else:
                hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
                for akun in accounts:
                    if username == akun['username'] and hashed_password == akun['password']:
                        level = akun["level"]
                        who = akun["username"]
                        pw = akun["password"]
                        main_menu()
                else:
                    input("\nUSERNAME ATAU PASSWORD SALAH")

def daftar():
    while True:
        clear()
        header("MENU DAFTAR AKUN")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

        new = {}

        accounts = load_json()
        reporting_data = load_csv(db_reporting)
        new['username'] = input("USERNAME: ")
        for account in accounts:
            if new["username"] in account["username"]:
                input("\nUSERNAME TELAH DIGUNAKAN")
                daftar()
        if new['username'].upper() == "B":
            strat_menu()
        else:
            new['password'] = input("PASSWORD: ")
            if new['password'].upper() == "B":
                strat_menu()
            else:
                pasword_confirm = input("RE-PASSWORD: ")
                if pasword_confirm == new["password"]:
                    new['password'] = hashlib.md5(new['password'].encode('utf-8')).hexdigest()
                    new['level'] = 'USER'
                    accounts.append(new)
                    with open(db_account,'w') as output:
                        output.write(json.dumps(accounts, indent=2))
                    
                    total_user = int(reporting_data[0]["total_user"]) + 1
                    reporting_data[0]["total_user"] = total_user

                    write_csv_reporting(reporting_data)
                    input("\nDAFTAR BERHASIL")
                    strat_menu()
                else:
                    input("\nPASSWORD TIDAK SAMA")
                
# FUNCTION MENU UTAMA USER
def search():
    while True:
        clear()
        header("CARI TIKET KERETA")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

        trains = load_csv(db_train)
        basket = load_csv(db_basket)

        asal    = input("{:<25}: ".format("Asal"))
        if asal.upper() == "B":
            main_menu()
        else: 
            tujuan  = input("{:<25}: ".format("Tujuan"))
            if tujuan.upper() == "B":
                main_menu()
            else:            
                tanggal = input("{:<25}: ".format("Tangal Berangkat [1-31]"))
                if tanggal.upper() == "B":
                    main_menu()
                else:
                    bulan   = input("{:<25}: ".format("Bulan Berangkat [1-12]"))
                    if bulan.upper() == "B":
                        main_menu()
                    else:
                        tahun   = input("{:<25}: ".format("Tahun Berangkat"))
                        if tahun.upper() == "B":
                            main_menu()
                        else:
                            tanggal_berangkat = f"{tanggal} {bulan} {tahun}"

                            try:
                                now = datetime.datetime.now()
                                kalender = datetime.datetime(int(tahun), int(bulan), int(tanggal))
                                if kalender < now:
                                    input("\nTANGGAL/BULAN/TAHUN ANDA SALAH")
                                    search()
                            except:
                                input("\nTANGGAL/BULAN/TAHUN ANDA SALAH")
                                search()

                            hari     = kalender.strftime("%A").upper()

                            konfirmasi = input("APA DATA SUDAH BENAR? [Y/N/B]: ")

                            if konfirmasi.upper() == "Y":
                                rekomendasi_kereta = []
                                not_rekomendasi_kereta = []
                                for i in trains:
                                    if asal.upper() == i["asal"] and tujuan.upper() == i["tujuan"] and hari == i["hari"]:
                                        rekomendasi_kereta.append(i)
                                    else:
                                        not_rekomendasi_kereta.append(i)
                                if rekomendasi_kereta != []:
                                    while True:
                                        show_train(rekomendasi_kereta)
                                        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
                                        print("="*140)
                                        choice = input("{:<25}: ".format("Pilih Kereta Api [No]"))
                                        
                                        if choice.isnumeric():

                                            tmp_tiket = []
                                            choice = int(choice)

                                            if (choice-1) in range(len(rekomendasi_kereta)):
                                                jumlah = input("{:<25}: ".format("Jumlah Penumpang"))
                                                if jumlah.isnumeric():
                                                    jumlah = int(jumlah)
                                                    if 0 < jumlah <= int(rekomendasi_kereta[choice-1]["tiket"]):
                                                        for i in range(jumlah):
                                                            nama = input("{:<25}: ".format("Nama Penumpang"))
                                                            tmp = { "pemesan": who,
                                                                    "penumpang": nama, 
                                                                    "kereta": rekomendasi_kereta[choice-1]["kereta"], 
                                                                    "asal": rekomendasi_kereta[choice-1]["asal"], 
                                                                    "tujuan": rekomendasi_kereta[choice-1]["tujuan"], 
                                                                    "berangkat": rekomendasi_kereta[choice-1]["berangkat"], 
                                                                    "tiba": rekomendasi_kereta[choice-1]["tiba"], 
                                                                    "harga": rekomendasi_kereta[choice-1]["harga"], 
                                                                    "tanggal_berangkat": tanggal_berangkat,
                                                                    "hari": rekomendasi_kereta[choice-1]["hari"]
                                                                    }
                                                            tmp_tiket.append(tmp)

                                                        konfirmasi = input("APA DATA SUDAH BENAR? [Y/N/B]: ")

                                                        if konfirmasi.upper() == "Y":
                                                            sisa_tiket = int(rekomendasi_kereta[choice-1]["tiket"]) - jumlah
                                                            rekomendasi_kereta[choice-1]["tiket"] = sisa_tiket
                                                            update_db_train = rekomendasi_kereta + not_rekomendasi_kereta

                                                            for i in tmp_tiket:
                                                                basket.append(i)

                                                            write_csv_train(db_train, update_db_train)
                                                            write_csv_ticket(db_basket, basket)
                                                            input("\nTERIMAKASIH TELAH MEMESAN, LIHAT PEMBAYARAN ANDA PADA MENU KERANJANG & BAYAR")
                                                            main_menu()
                                                        elif konfirmasi.upper() == "N":
                                                            input("\nKONFIRMASI DITERIMA")
                                                        elif konfirmasi.upper() == "B":
                                                            search()
                                                        else:
                                                            input("\nOPSI TIDAK ADA")
                                                    else:
                                                        input("\nTIKET TIDAK MENCUKUPI")
                                                elif jumlah.upper() == "B":
                                                    search()
                                                else:
                                                    input("\nANDA MEMASUKKAN SELAIN ANGKA")       
                                            else:
                                                input("\nKERETA API TIDAK ADA")
                                        elif choice.upper() == "B":
                                            search()
                                        else:
                                            input("\nANDA MEMASUKKAN SELAIN ANGKA")
                                else:
                                    input("\nTIDAK ADA JADWAL")
                            elif konfirmasi.upper() == "N":
                                input("\nKONFIRMASI DITERIMA")
                            elif konfirmasi.upper() == "B":
                                main_menu()
                            else:
                                input("\nMENU TIDAK ADA")

def show_ticket():
    clear()
    user_ticket = []
    tickets = load_csv(db_ticket)
    for i in range(len(tickets)):
        if tickets[i]["pemesan"] == who:
            user_ticket.append(tickets[i])
            
    if isinstance(user_ticket, list):
        print("="*140)
        print("|{:^138}|".format("TIKET KERETA API ANDA"))
        print("="*140)
        print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format("NO", "KERETA", "PENUMPANG", "TANGGAL BERANGKAT", "ASAL", "TUJUAN", "BERANGKAT", "TIBA"))
        print("="*140)
        for idx, item in enumerate(user_ticket):
            print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format((idx+1), item["kereta"], item["penumpang"], item["tanggal_berangkat"], item["asal"], item["tujuan"], item["berangkat"], item["tiba"]))
        print("="*140)
    else:
        print('TIPE DATA TIDAK SESUAI')

def basket():
    while True:
        clear()
        header("KERANJANG & BAYAR")

        user_basket = []
        total_harga = 0
        baskets = load_csv(db_basket)
        tickets = load_csv(db_ticket)
        reporting_data = load_csv(db_reporting)
        reporting_data2 = load_csv(db_reporting2)

        for i in range(len(baskets)):
            if baskets[i]["pemesan"] == who:
                user_basket.append(baskets[i])
                total_harga += int(baskets[i]['harga'])

        print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format("NO", "KERETA", "PENUMPANG", "TANGGAL BERANGKAT", "ASAL", "TUJUAN", "BERANGKAT", "TIBA"))
        print("="*140)
        for idx, item in enumerate(user_basket):
            print("|{:^3}|{:<25}|{:^30}|{:^20}|{:^15}|{:^15}|{:^12}|{:^11}|".format((idx+1), item["kereta"], item["penumpang"], item["tanggal_berangkat"], item["asal"], item["tujuan"], item["berangkat"], item["tiba"]))
        print("="*140)
        
        if total_harga != 0:
            print("{:<15}: {}".format("TOTAL HARGA", total_harga))
            bayar = input("{:<15}: ".format("UANG ANDA"))
            if bayar.isnumeric():
                bayar = int(bayar)
                if bayar >= total_harga:
                    for i in user_basket:
                        tickets.append(i)
                        total_tiket_terjual = int(reporting_data[0]["total_tiket_terjual"]) + 1
                        reporting_data[0]["total_tiket_terjual"] = total_tiket_terjual

                    total_pendapatan = int(reporting_data[0]["total_pendapatan"]) + total_harga
                    reporting_data[0]["total_pendapatan"] = total_pendapatan

                    for i in range(len(reporting_data2)):
                        for idx in range(len(user_basket)):
                            if reporting_data2[i]["asal"] == user_basket[idx]["asal"] and reporting_data2[i]["tujuan"] == user_basket[idx]["tujuan"]:
                                pembeli = int(reporting_data2[i]["pembeli"]) + 1
                                pendapatan = int(reporting_data2[i]["pendapatan"]) + int(user_basket[idx]["harga"])
                                reporting_data2[i]["pembeli"] = pembeli
                                reporting_data2[i]["pendapatan"] = pendapatan
                    user_basket.clear()

                    write_csv_reporting2(reporting_data2)
                    write_csv_reporting(reporting_data)
                    write_csv_ticket(db_ticket, tickets)
                    write_csv_ticket(db_basket, user_basket)
                    kembalian = bayar - total_harga
                    print("{:<15}: {}".format("KEMBALI", kembalian))
                    input("\nTERIMA KASIH")
                    main_menu()
                else:
                    input("\nUANG ANDA TIDAK CUKUP")
            elif bayar.upper() == "B":
                main_menu()
            else:
                input("\nANDA MEMASUKKAN SELAIN ANGKA")
        else:
            input("\nKERANJANG MASIH KOSONG")
            main_menu()

# FUNCTION UNTUK ADMIN
def add_data():
    while True:
        clear()
        header("TAMBAH JADWAL KERETA API")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

        trains = load_csv(db_train)
        data_reporting2 = load_csv(db_reporting2)
        tmp = {}
        rpt = {}
        
        tmp["kereta"] = input("{:<25}: ".format("NAMA KERETA")).upper()
        if tmp["kereta"].upper() == "B":
            main_menu()
        else:
            tmp["hari"] = input("{:<25}: ".format("HARI PEROPRASI [ENGLISH]")).upper()
            if tmp["hari"].upper() == "B":
                main_menu()
            elif tmp["hari"].upper() not in day:
                input("\nMASUKKAN HARI DENGAN BENAR")
            else:   
                tmp["asal"] = input("{:<25}: ".format("ASAL")).upper()
                if tmp["asal"].upper() == "B":
                    main_menu()
                else:
                    tmp["tujuan"] = input("{:<25}: ".format("TUJUAN")).upper()
                    if tmp["tujuan"].upper() == "B":
                        main_menu()
                    else:
                        tmp["harga"] = input("{:<25}: ".format("HARGA"))
                        if tmp["harga"].isnumeric():
                            tmp["berangkat"] = input("{:<25}: ".format("BERANGKAT PUKUL [00:00]")).upper()
                            if tmp["berangkat"].upper() == "B":
                                main_menu()
                            else:
                                tmp["tiba"] = input("{:<25}: ".format("TIBA PUKUL [00:00]")).upper()
                                if tmp["tiba"].upper() == "B":
                                    main_menu()
                                else:
                                    tmp["tiket"] = input("{:<25}: ".format("JUMLAH TIKET")).upper()
                                    if tmp["tiket"].isnumeric():
                                        konfirmasi = input("APAKAH DATA SUDAH BENAR? [Y/N/B]: ")
                                        if konfirmasi.upper() == "Y":
                                            trains.append(tmp)

                                            rpt["asal"] = tmp["asal"]
                                            rpt["tujuan"] = tmp["tujuan"]
                                            rpt["pembeli"] = 0
                                            rpt["pendapatan"] = 0
                                            
                                            data_exist = []
                                            for i in range(len(data_reporting2)):
                                                if data_reporting2[i]["asal"] == rpt["asal"] and data_reporting2[i]["tujuan"] == rpt["tujuan"]:
                                                    data_exist.append(data_reporting2[i])

                                            if data_exist == []:
                                                data_reporting2.append(rpt)
                                                write_csv_reporting2(data_reporting2)

                                            write_csv_train(db_train, trains)
                                            
                                            input("\nDATA BERHASIL DITAMBAHKAN")
                                            main_menu()
                                        elif konfirmasi.upper() == "N":
                                            input("\nKONFIRMASI DITERIMA")
                                        elif konfirmasi.upper() == "B":
                                            main_menu()
                                        else:
                                            input("\nOPSI TIDAK ADA")
                                    elif tmp["tiket"].upper() == "B":
                                        main_menu()
                                    else:
                                        input("\nMASUKKAN JUMLAH TIKET DENGAN BENAR")
                        elif tmp["harga"].upper() == "B":
                            main_menu()
                        else:
                            input("\nANDA MEMASUKKAN SELAIN ANGKA")

def update():
    while True:
        trains = load_csv(db_train)

        show_train(trains)
        header("UPDATE DATA KERETA")
        print("|{:^138}|".format("B: BACK, UNTUK KEMBALI"))
        print("="*140)

 
        idx = input('{:<20}: '.format("NOMOR KERETA"))
        if idx.isnumeric():
            idx = int(idx)
            if (idx-1) in range(len(trains)):
                kategori = input('{:<20}: '.format("KATEGORI YANG AKAN DI GANTI")).lower()
                if kategori in trains[idx-1].keys():
                    if kategori == "harga":
                        data_baru = input("{:<20}: ".format(f"{kategori.upper()} BARU")).upper()
                        if data_baru.isnumeric():
                            trains[idx-1][kategori] = data_baru

                            write_csv_train(db_train, trains)

                            input("\nDATA BERHASIL DI UPDATE")
                        else:
                            input("\nANDA MEMASUKKAN SELAIN ANGKA")
                    elif kategori == "tiket":
                        data_baru = input("{:<30}: ".format(f"JUMLAH {kategori.upper()} YANG AKAN DITAMBAHKAN")).upper()
                        if data_baru.isnumeric():
                            trains[idx-1][kategori] = int(trains[idx-1][kategori]) + int(data_baru)

                            write_csv_train(db_train, trains)

                            input("\nDATA BERHASIL DI UPDATE")
                        else:
                            input("\nANDA MEMASUKKAN SELAIN ANGKA")
                    elif kategori == 'hari':
                        hari_baru = input("{:<20}: ".format(f"{kategori.upper()} BARU")).upper()
                        if hari_baru in day:
                            trains[idx-1][kategori] = hari_baru

                            write_csv_train(db_train, trains)

                            input("\nDATA BERHASIL DI UPDATE")
                        else:
                            input("\nMASUKKAN HARI DENGAN BENAR")
                    elif kategori == 'berangkat' or kategori == 'tiba':
                        berangkat_baru = input("{:<20}: ".format("BERANGKAT BARU")).upper()
                        tiba_baru = input("{:<20}: ".format("TIBA BARU")).upper()
                        trains[idx-1]["berangkat"] = berangkat_baru
                        trains[idx-1]["tiba"] = tiba_baru

                        write_csv_train(db_train, trains)

                        input("\nDATA BERHASIL DI UPDATE")
                    else:
                        trains[idx-1][kategori] = input("{:<20}: ".format(f"{kategori.upper()} BARU")).upper()

                        write_csv_train(db_train, trains)

                        input("\nDATA BERHASIL DI UPDATE")
                elif kategori == "b":
                    main_menu()
                else:
                    input("\nKATEGORI TIDAK ADA")
            else:
                input("\nNOMOR KERETA API TIDAK ADA")
        elif idx.upper() == "B":
            main_menu()
        else:
            input("\nANDA MEMASUKKAN SELAIN ANGKA")

def reporting():
    clear()
    data_reporting = load_csv(db_reporting)
    data_reporting2 = load_csv(db_reporting2)
    if isinstance(data_reporting, list):
        print("="*83)
        print("|{:^81}|".format("REPORTING DATA"))
        print("="*83)
        print("|{:^3}|{:<22}|{:^22}|{:^15}|{:^15}|".format("NO", "ASAL", "TUJUAN", "PEMBELI", "PENDAPATAN"))
        print("="*83)
        for idx, item in enumerate(data_reporting2):
            print("|{:^3}|{:<22}|{:^22}|{:^15}|{:^15}|".format((idx+1), item["asal"], item["tujuan"], item["pembeli"], item["pendapatan"]))
        print("="*83)
        print("| {:<40} | {:^36} |".format("TOTAL PENGGUNA",data_reporting[0]["total_user"]))
        print("| {:<40} | {:^36} |".format("TOTAL PENDAPATAN",data_reporting[0]["total_pendapatan"]))
        print("| {:<40} | {:^36} |".format("TOTAL TIKET TERJUAL",data_reporting[0]["total_tiket_terjual"]))
        print("="*83)
        input("\nENTER UNTUK KEMBALI....")
        main_menu()
    else:
        print('TIPE DATA TIDAK SESUAI')

# MAIN PROGRAM
strat_menu()