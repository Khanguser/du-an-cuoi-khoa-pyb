from guizero import *
def luu_vao_file(ten_mon, dia_chi, sdt):
    ten_file = "lich_su.txt"
    du_lieu_moi = []
    mon_da_co = False

    # Đọc và kiểm tra file cũ để tìm xem món ăn đó đã chọn lần nào chưa
    try:
        with open(ten_file, "r", encoding="utf-8") as f:
            for dong in f:
                cot = dong.strip().split(" | ")
                if cot[0] == ten_mon:
                    # Trường hợp thấy tên món đã chọn thì tăng số lần chọn lên 1
                    lan_moi = int(cot[3]) + 1
                    du_lieu_moi.append(f"{ten_mon} | {dia_chi} | {sdt} | {lan_moi}\n")
                    mon_da_co = True
                else:
                    du_lieu_moi.append(dong)
    except:
        pass # Nếu chưa có file thì bỏ qua

    # Nếu đây là lần đầu chọn món này
    if not mon_da_co:
        du_lieu_moi.append(f"{ten_mon} | {dia_chi} | {sdt} | 1\n")

    # Ghi đè lại toàn bộ file với con số mới
    with open(ten_file, "w", encoding="utf-8") as f:
        f.writelines(du_lieu_moi)

def chon_mon_an():
    window_1 = Window(app, title="Danh sách món ăn", width=1000, height=600)
    Text(window_1, "Danh sách các món ăn đề xuất", size=12, bold=True)
    Box_1 = Box(window_1, layout="grid")
    
    #  Hàm ghi vào file lịch sử + thông báo và đóng cửa sổ
    btn_pho = PushButton(Box_1, image="pho_bo.png", width=300, height=250, text="Phở Bò", grid=[0, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Phở Bò"), luu_vao_file("Phở Bò", "123 Lý Tự Trọng", "090123"), window_1.destroy()])
    btn_banhmi = PushButton(Box_1, image="banh_mi.png", width=300, height=250, text="Bánh Mì", grid=[1, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Bánh Mì"), luu_vao_file("Bánh Mì", "45 Lê Lợi", "090777"), window_1.destroy()])
    btn_comtam = PushButton(Box_1, image="com_tam.png", width=300, height=250, text="Cơm Tấm", grid=[2, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Cơm Tấm"), luu_vao_file("Cơm Tấm", "89 Nguyễn Huệ", "098812"), window_1.destroy()])
    btn_bunbo = PushButton(Box_1, image="bun_bo.png", width=300, height=250, text="Bún Bò", grid=[0, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Bún Bò"), luu_vao_file("Bún Bò", "12 Võ Văn Tần", "091234"), window_1.destroy()])
    btn_xoi = PushButton(Box_1, image="xoi.png", width=300, height=250, text="Xôi Gà", grid=[1, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Xôi Gà"), luu_vao_file("Xôi Gà", "202 CMT8", "093344"), window_1.destroy()])
    btn_miquang = PushButton(Box_1, image="mi_quang.png", width=300, height=250, text="Mì Quảng", grid=[2, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Mì Quảng"), luu_vao_file("Mì Quảng", "55 Phan Chu Trinh", "094455"), window_1.destroy()])

def mo_lich_su():
    win_ls = Window(app, title="Lịch sử chọn món ăn", width=500, height=400)
    Text(win_ls, "THÔNG TIN ĐÃ LƯU", size=12, bold=True)
    
    ds_hien_thi = ListBox(win_ls, width="fill", height="fill")
    
    try:
        with open("lich_su.txt", "r", encoding="utf-8") as f:
            for dong in f:
                ds_hien_thi.append(dong.strip())
    except:
        ds_hien_thi.append("Chưa có dữ liệu.")

    PushButton(win_ls, text="Đóng", command=win_ls.destroy)
app = App(title="Ứng dụng đề xuất đồ ăn", width=400, height=300)
Text(app, "CHỌN MÓN ĂN", size=18, bold=True)
Box(app, height=20)
PushButton(app, text="Chọn món ăn", width=20, command=chon_mon_an)
PushButton(app, text="Lịch sử chọn", width=20, command=mo_lich_su)
PushButton(app, text="Thoát", width=20, command=app.destroy)

app.display()
