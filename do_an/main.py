from guizero import *
import random
import os
import shutil
ds_chi_tiet = []
def doc_du_lieu_tu_file():
    global ds_chi_tiet
    ds_chi_tiet = []  # Làm sạch danh sách trước khi nạp mới
    try:
        with open("mon_an.txt", "r", encoding="utf-8") as f:
            for dong in f:
                if dong.strip():
                    ds_chi_tiet.append(dong.strip())
    except FileNotFoundError:
        pass # Nếu chưa có file thì danh sách để trống

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

def them_mon_an(callback_cap_nhat=None):
    window_2 = Window(app, title="Thêm món ăn", width=650, height=580, bg="#FFF5EE")
    window_2.tk.attributes("-topmost", True)
    
    Text(window_2, "NHẬP THÔNG TIN MÓN ĂN MỚI", size=20, bold=True, color="#D2691E")
    Box(window_2, height=10, width="fill")
    
    form = Box(window_2, layout="grid", width="fill", height=320)
    labels = ["Tên món ăn:", "Giá tiền:", "Địa chỉ:", "Số điện thoại:", "Hình ảnh:"]
    inputs = []
    
    for i, lb_text in enumerate(labels):
        Text(form, text=lb_text, grid=[0, i], align="left", size=14)
        if i < 4:
            inputs.append(TextBox(form, grid=[1, i], width=45))
        else:
            box_anh = Box(form, grid=[1, i], align="left", layout="grid")
            txt_anh = TextBox(box_anh, grid=[0,0], width=30, enabled=False)
            txt_anh.bg = "white"
            inputs.append(txt_anh)
            
            def mo_hop_chon_file():
                from tkinter import filedialog
                # Sử dụng filedialog của tkinter với tham số parent để cửa sổ chọn file nổi lên trên window_2
                duong_dan = filedialog.askopenfilename(parent=window_2.tk, title="Chọn ảnh", filetypes=[("Image", "*.png *.jpg")])
                
                if duong_dan:
                    ten_file = os.path.basename(duong_dan)
                    # COPY file ảnh từ nguồn vào thư mục hiện tại của dự án
                    try:
                        shutil.copy(duong_dan, ten_file)
                    except shutil.SameFileError:
                        pass # Nếu chọn ảnh đã có sẵn trong thư mục thì bỏ qua
                    txt_anh.enabled = True
                    txt_anh.value = ten_file
                    txt_anh.enabled = False
                window_2.focus()

            PushButton(box_anh, text="📁 Chọn file", grid=[1,0], command=mo_hop_chon_file).text_size = 11

    def thuc_hien_ghi_file():
        vals = [inp.value.strip() for inp in inputs]
        if vals[1].isdigit(): # Định dạng giá tiền
            vals[1] = "{:,}".format(int(vals[1])).replace(",", ".") + "đ"
        
        if all([vals[0], vals[1], vals[4]]):
            with open("mon_an.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{' | '.join(vals)}") # Ghi đủ 5 cột
            doc_du_lieu_tu_file()
            window_2.destroy()
            if callback_cap_nhat:
                callback_cap_nhat() # Gọi hàm cập nhật giao diện danh sách
        else:
            warn("Lỗi", "Vui lòng nhập đủ thông tin và CHỌN ẢNH!")

    Box(window_2, height=20, width="fill") 
    btn_save = PushButton(window_2, text="LƯU VÀO HỆ THỐNG", command=thuc_hien_ghi_file, width=25)
    btn_save.bg = "#98FB98"
    btn_save.text_size = 16
# --- Hàm 2: Giao diện lựa chọn món ăn (Phiên bản Fix ô hiển thị ngang) ---
# --- Hàm 2: Giao diện lựa chọn món ăn (Bản Fix Lọc Dữ Liệu Thật) ---
def chon_mon_an():
    doc_du_lieu_tu_file()
    window_1 = Window(app, title="Danh sách món ăn", width=1250, height=880, bg="#FFF5EE")
    window_1.tk.attributes("-topmost", True)
    
    Text(window_1, "Danh sách các món ăn đề xuất", size=28, bold=True, color="#D2691E")
    container = Box(window_1, width="fill", height=460)
    
    # Khu vực lưới ảnh: Cố định 6 vị trí
    Box_1 = Box(container, layout="grid", align="left", border=3, width=820, height=450)
    
    anh_mac_dinh = ["pho_bo.png", "banh_mi.png", "com_tam.png", "bun_bo.png", "xoi.png", "mi_quang.png"]
    ten_mac_dinh = ["Phở bò", "Bánh mì", "Cơm tấm", "Bún bò", "Xôi gà", "Mì quảng"]
    
    def chon_mon_tu_anh(ten_mon):
        txt_chi_tiet.enabled = True
        txt_chi_tiet.value = "" 
        for dong in ds_chi_tiet:
            # So khớp chính xác tên món ở cột đầu tiên
            # Cập nhật logic tách chuỗi để đồng bộ với dữ liệu mới (xử lý cả "|")
            parts = [s.strip() for s in dong.split("|")]
            if parts and ten_mon.lower() == parts[0].lower():
                txt_chi_tiet.value = dong 
                break
        txt_chi_tiet.enabled = False

    # --- CƠ CHẾ LỌC DỮ LIỆU THỰC TẾ ---
    def cap_nhat_giao_dien():
        txt_chi_tiet.value = "" # Xóa thông tin chi tiết cũ để người dùng biết giao diện đã làm mới
        # Xóa các nút cũ để vẽ lại theo bộ lọc mới
        for widget in list(Box_1.children):
            widget.destroy()
        
        doc_du_lieu_tu_file()
        ds_hien_thi = ds_chi_tiet.copy()
        tieu_chi = choice.value

        # Hàm hỗ trợ lấy giá tiền từ chuỗi
        def lay_gia(s):
            try:
                return int(s.split("|")[1].replace(".", "").replace("đ", "").strip())
            except: return 999999999

        if tieu_chi == "Rẻ nhất":
            # Tìm mức giá thấp nhất trong danh sách hiện có
            tat_ca_gia = [lay_gia(s) for s in ds_hien_thi]
            if tat_ca_gia:
                min_gia = min(tat_ca_gia)
                # Lọc: Chỉ giữ lại các món có giá bằng giá thấp nhất
                ds_hien_thi = [s for s in ds_hien_thi if lay_gia(s) == min_gia]

        elif tieu_chi == "Gần nhất":
            # Mô phỏng tìm quán gần nhất từ dữ liệu thực tế trong file
            # Chọn ngẫu nhiên 2 món từ danh sách hiện có để hiển thị
            if len(ds_hien_thi) > 0:
                k = min(len(ds_hien_thi), 2)
                ds_hien_thi = random.sample(ds_hien_thi, k)

        elif tieu_chi == "Hay ăn nhất":
            # Tìm món có số lần ăn nhiều nhất (Logic giống snippet)
            tan_suat = {}
            max_lan = 0
            try:
                with open("lich_su.txt", "r", encoding="utf-8") as f:
                    for dong in f:
                        cot = dong.strip().split(" | ")
                        if len(cot) >= 4:
                            ten = cot[0].lower()
                            sl = int(cot[3])
                            tan_suat[ten] = sl
                            if sl > max_lan:
                                max_lan = sl
            except: pass
            
            # Chỉ hiển thị món có số lần ăn cao nhất (Filter)
            if max_lan > 0:
                ds_hien_thi = [s for s in ds_hien_thi if tan_suat.get(s.split(" | ")[0].lower(), 0) == max_lan]
            else:
                random.shuffle(ds_hien_thi)
        else:
            # Nếu chọn "Tất cả", trộn ngẫu nhiên danh sách để thay đổi vị trí hiển thị
            random.shuffle(ds_hien_thi)

        # Vẽ lưới 6 ô dựa trên danh sách đã lọc
        img_w, img_h = 270, 215
        
        # Tạo từ điển ánh xạ tên món -> ảnh để đảm bảo lấy đúng ảnh khi danh sách bị trộn
        dict_anh_mac_dinh = {t.lower(): a for t, a in zip(ten_mac_dinh, anh_mac_dinh)}

        for i in range(6):
            col, row = i % 3, (i // 3) + 1
            ten, anh = "", ""
            
            if i < len(ds_hien_thi):
                # Tách chuỗi an toàn (xử lý cả trường hợp dính chữ như "Tên|Giá")
                thong_tin = [s.strip() for s in ds_hien_thi[i].split("|")]
                ten = thong_tin[0]
                
                # Logic: Nếu file có ảnh thì dùng, nếu không thì tra cứu theo tên trong danh sách mặc định
                anh = thong_tin[4] if len(thong_tin) > 4 and thong_tin[4] else dict_anh_mac_dinh.get(ten.lower(), anh_mac_dinh[i % 6])
                
                # KIỂM TRA AN TOÀN: Nếu file ảnh không tồn tại thực tế, dùng ảnh mặc định để tránh crash
                if not os.path.exists(anh):
                    anh = anh_mac_dinh[i % 6]
            elif tieu_chi == "Tất cả": # Chỉ hiện dữ liệu mặc định khi chọn Tất cả
                ten, anh = ten_mac_dinh[i], anh_mac_dinh[i]
                
            if ten: # Chỉ tạo nút nếu có dữ liệu
                PushButton(Box_1, image=anh, width=img_w, height=img_h, grid=[col, row], 
                            command=lambda t=ten: chon_mon_tu_anh(t))

    # Sidebar điều khiển lọc
    Box_2 = Box(container, align="left", width=340, height=450)
    Box_2.bg = "#FFCC66" 
    Text(Box_2, "Lọc theo:", size=20, bold=True)
    choice = ButtonGroup(Box_2, options=["Tất cả", "Rẻ nhất", "Gần nhất", "Hay ăn nhất"], selected="Tất cả")
    choice.text_size = 18

    # --- KHU VỰC Ô TRỐNG HIỂN THỊ CHI TIẾT ---
    Box(window_1, height=30, width="fill") 
    row_info = Box(window_1, width="fill", layout="grid")
    Text(row_info, "Chi tiết thực đơn: ", size=24, bold=True, grid=[0,0], align="left")
    txt_chi_tiet = TextBox(row_info, grid=[1,0], width=70, align="left", enabled=False)
    txt_chi_tiet.text_size = 22
    txt_chi_tiet.bg = "white"

    # --- HÀM XÁC NHẬN VÀ LƯU (Sửa lỗi nhảy dòng) ---
    def xac_nhan_va_luu():
        du_lieu = txt_chi_tiet.value
        if "|" in du_lieu:
            thong_tin = [s.strip() for s in du_lieu.split("|")]
            if len(thong_tin) >= 4:
                # thong_tin[0]: tên, [2]: địa chỉ, [3]: sđt
                luu_vao_file(thong_tin[0], thong_tin[2], thong_tin[3])
                window_1.destroy()

    # Nút xác nhận đẩy lên cao
    Box(window_1, height=40, width="fill") 
    btn_confirm = PushButton(window_1, text="✔️ Xác nhận và lưu", command=xac_nhan_va_luu, width=30)
    btn_confirm.text_size = 24
    btn_confirm.bg = "#98FB98"
    Box(window_1, height=80, width="fill") 

    # Các nút bấm bên Sidebar
    Box(Box_2, height=10, width="fill")
    PushButton(Box_2, text="🔄 THAY ĐỔI", command=cap_nhat_giao_dien, width=15).text_size = 16
    Box(Box_2, height=10, width="fill")
    PushButton(Box_2, text="➕ THÊM MÓN ĂN", command=lambda: them_mon_an(cap_nhat_giao_dien), width=15).text_size = 16

    cap_nhat_giao_dien() # Gọi lần đầu để hiển thị ngay khi mở
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
app = App(title="Ứng dụng đề xuất đồ ăn", width=500, height=550, bg="#FFF5EE")

Box(app, height=20, width="fill") 
# Tiêu đề cực lớn (Size 30)
Text(app, "🍟 CHỌN MÓN ĂN 🍱", size=30, bold=True, color="#D2691E")
Box(app, height=40, width="fill") 

# Các nút Menu chính (Size 18)
btn_1 = PushButton(app, text="✨ Chọn món ăn", width=25, command=chon_mon_an)
btn_1.bg = "#FFD700"
btn_1.text_size = 18

Box(app, height=20, width="fill")

btn_2 = PushButton(app, text="📜 Lịch sử chọn", width=25, command=mo_lich_su)
btn_2.bg = "#98FB98"
btn_2.text_size = 18

Box(app, height=20, width="fill")

btn_3 = PushButton(app, text="❌ Thoát", width=25, command=app.destroy)
btn_3.bg = "#FF7F50"
btn_3.text_color = "white"
btn_3.text_size = 18

app.display()
