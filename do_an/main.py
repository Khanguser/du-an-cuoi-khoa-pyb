from guizero import *

# --- Hàm 1: Xử lí dữ liệu lưu vào file lichsu.txt ---
def luu_vao_file(ten_mon, dia_chi, sdt):
    ten_file, du_lieu_moi, mon_da_co = "lich_su.txt", [], False
    
    # Đọc file để kiểm tra món ăn đã tồn tại hay chưa
    try:
        with open(ten_file, "r", encoding="utf-8") as f:
            for dong in f:
                cot = dong.strip().split(" | ")
                if cot[0] == ten_mon:
                    # Nếu thấy món cũ, tăng số lần chọn lên 1 (cột index 3)
                    du_lieu_moi.append(f"{ten_mon} | {dia_chi} | {sdt} | {int(cot[3]) + 1}\n")
                    mon_da_co = True
                else:
                    du_lieu_moi.append(dong)
    except:
        pass # Bỏ qua nếu chưa có file

    # Nếu là món mới, thêm dòng mới với số lần khởi tạo là 1
    if not mon_da_co:
        du_lieu_moi.append(f"{ten_mon} | {dia_chi} | {sdt} | 1\n")
    
    # Ghi đè lại toàn bộ danh sách đã cập nhật vào file
    with open(ten_file, "w", encoding="utf-8") as f:
        f.writelines(du_lieu_moi)

# --- Hàm 2: Giao diện lựa chọn món ăn ---
def chon_mon_an():
    window_1 = Window(app, title="Danh sách món ăn", width=1000, height=600)
    Text(window_1, "Danh sách các món ăn đề xuất", size=12, bold=True)
    
    # Dữ liệu hiển thị chi tiết
    ds_chi_tiet = [
        "Phở Bò | 45.000đ | 123 Lý Tự Trọng | 090123",
        "Bánh Mì | 20.000đ | 45 Lê Lợi | 090777",
        "Cơm Tấm | 40.000đ | 89 Nguyễn Huệ | 098812",
        "Bún Bò | 45.000đ | 12 Võ Văn Tần | 091234",
        "Xôi Gà | 25.000đ | 202 CMT8 | 093344",
        "Mì Quảng | 35.000đ | 55 Phan Chu Trinh | 094455"
    ]

    container = Box(window_1, width="fill")
    
    # Khu vực chứa các nút bấm (Layout Grid)
    Box_1 = Box(container, layout="grid", align="left", border=3)
    
    btn_pho = PushButton(Box_1, image="pho_bo.png", width=220, height=180, text="Phở Bò", grid=[0, 1], command=lambda: chon_mon_tu_anh("Phở Bò"))
    btn_banhmi = PushButton(Box_1, image="banh_mi.png", width=220, height=180, text="Bánh Mì", grid=[1, 1], command=lambda: chon_mon_tu_anh("Bánh Mì"))
    btn_comtam = PushButton(Box_1, image="com_tam.png", width=220, height=180, text="Cơm Tấm", grid=[2, 1], command=lambda: chon_mon_tu_anh("Cơm Tấm"))
    btn_bunbo = PushButton(Box_1, image="bun_bo.png", width=220, height=180, text="Bún Bò", grid=[0, 2], command=lambda: chon_mon_tu_anh("Bún Bò"))
    btn_xoi = PushButton(Box_1, image="xoi.png", width=220, height=180, text="Xôi Gà", grid=[1, 2], command=lambda: chon_mon_tu_anh("Xôi Gà"))
    btn_miquang = PushButton(Box_1, image="mi_quang.png", width=220, height=180, text="Mì Quảng", grid=[2, 2], command=lambda: chon_mon_tu_anh("Mì Quảng"))
    
    # Danh sách các nút để phục vụ việc ẩn/hiện nhanh
    cac_nut = [btn_pho, btn_banhmi, btn_comtam, btn_bunbo, btn_xoi, btn_miquang]
    ten_cac_nut = ["Phở Bò", "Bánh Mì", "Cơm Tấm", "Bún Bò", "Xôi Gà", "Mì Quảng"]

    # Khu vực bộ lọc (Đã sửa lỗi bg)
    Box_2 = Box(container, align="left")
    Box_2.bg = "lightblue" 
    
    Text(Box_2, "Lọc theo:", size=15)
    choice = ButtonGroup(Box_2, options=["Tất cả", "Rẻ nhất", "Gần nhất", "Hay ăn nhất"], selected="Tất cả")
    choice.text_size = 15
    
    # Hàm xử lý logic ẩn hiện khi nhấn nút Lọc
    def xu_ly_loc():
        for b in cac_nut: b.hide() # Ẩn hết đi trước khi lọc
        tieu_chi = choice.value
        
        if tieu_chi == "Tất cả":
            for b in cac_nut: b.show()
        elif tieu_chi == "Rẻ nhất":
            btn_banhmi.show(); btn_xoi.show()
        elif tieu_chi == "Gần nhất":
            btn_pho.show(); btn_comtam.show()
        elif tieu_chi == "Hay ăn nhất":
            mon_hot, max_lan = "", 0
            try:
                with open("lich_su.txt", "r", encoding="utf-8") as f:
                    for dong in f:
                        cot = dong.strip().split(" | ")
                        if len(cot) >= 4 and int(cot[3]) > max_lan:
                            max_lan, mon_hot = int(cot[3]), cot[0]
                if mon_hot in ten_cac_nut:
                    cac_nut[ten_cac_nut.index(mon_hot)].show()
            except: pass

    PushButton(Box_2, text="THAY ĐỔI", command=xu_ly_loc)
    
    # Danh sách hiển thị thông tin chi tiết
    Text(window_1, "Chi tiết thực đơn:", size=11, bold=True)
    lb_chi_tiet = ListBox(window_1, width="fill", height=150, scrollbar=True)
    
    # Hàm khi bấm vào hình ảnh: Đồng bộ dữ liệu lên ListBox
    def chon_mon_tu_anh(ten_mon):
        lb_chi_tiet.clear()
        for dong in ds_chi_tiet:
            if dong.startswith(ten_mon):
                lb_chi_tiet.append(dong)
                lb_chi_tiet.value = dong
                break

    # Hàm xác nhận: Lưu thông tin cuối cùng vào file và đóng tab
    def xac_nhan_va_luu():
        if not lb_chi_tiet.value:
            warn("Thông báo", "Vui lòng chọn món trước!")
            return
        # Tách chuỗi để lấy đúng: Tên | Địa chỉ | SĐT
        thong_tin = lb_chi_tiet.value.split(" | ")
        luu_vao_file(thong_tin[0], thong_tin[2], thong_tin[3])
        window_1.destroy()

    PushButton(window_1, text="Xác nhận và lưu", command=xac_nhan_va_luu, width=20)

# --- Hàm 3: Cửa sổ xem lịch sử ---
def mo_lich_su():
    win_ls = Window(app, title="Lịch sử chọn", width=500, height=400)
    Text(win_ls, "THÔNG TIN ĐÃ LƯU", size=12, bold=True)
    
    ds_hien_thi = ListBox(win_ls, width="fill", height="fill")
    
    try:
        with open("lich_su.txt", "r", encoding="utf-8") as f:
            for dong in f:
                ds_hien_thi.append(dong.strip())
    except:
        ds_hien_thi.append("Chưa có dữ liệu.")

    PushButton(win_ls, text="Đóng", command=win_ls.destroy)

# --- Menu lựa chọn ---
app = App(title="Ứng dụng đề xuất đồ ăn", width=400, height=350)

Text(app, "CHỌN MÓN ĂN", size=18, bold=True)
Box(app, height=20, width="fill") # Tạo khoảng trống
PushButton(app, text="Chọn món ăn", width=20, command=chon_mon_an)
PushButton(app, text="Lịch sử chọn", width=20, command=mo_lich_su)
PushButton(app, text="Thoát", width=20, command=app.destroy)

app.display()
