from guizero import *
import random
app = App(title="Ứng dụng đề xuất đồ ăn", width=400, height=350)

def chon_mon_an():
    window_1 = Window(app, title="Danh sách món ăn", width=450, height=400)
    text = Text(window_1, "Danh sách các món ăn đề xuất", size=12)
    Box_1 = Box(window_1, layout="grid")
    btn_pho = PushButton(Box_1, image="pho_bo.png", width=300, height=250, text="Phở Bò", grid=[0, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Phở Bò"), window_1, window_1.destroy()])
    btn_banhmi = PushButton(Box_1, image="banh_mi.png", width=300, height=250, text="Bánh Mì", grid=[1, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Bánh Mì"), window_1, window_1.destroy()])
    btn_comtam = PushButton(Box_1, image="com_tam.png", width=300, height=250, text="Cơm Tấm", grid=[2, 1], command=lambda: [info("Thông báo", "Bạn đã chọn Cơm Tấm"), window_1, window_1.destroy()])
    btn_bunbo = PushButton(Box_1, image="bun_bo.png", width=300, height=250, text="Bún Bò", grid=[0, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Bún Bò"), window_1, window_1.destroy()])
    btn_xoi = PushButton(Box_1, image="xoi.png", width=300, height=250, text="Xôi Gà", grid=[1, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Xôi Gà"), window_1, window_1.destroy()])
    btn_miquang = PushButton(Box_1, image="mi_quang.png", width=300, height=250, text="Mì Quảng", grid=[2, 2], command=lambda: [info("Thông báo", "Bạn đã chọn Mì Quảng"), window_1, window_1.destroy()])

def lich_su():
    window_2 = Window(app)
    text = Text(window_2, "Danh sách lịch sử đã lựa chọn món ăn")
    

Text(app, text="MENU LỰA CHỌN ĐỒ ĂN", size=20, font="Arial", bold=True)
Box(app, height=20, width="fill")

button_chon = PushButton(app, text="Chọn món ăn", width=20, command=chon_mon_an)
button_lich_su = PushButton(app, text="Lịch sử chọn", width=20, command=lich_su)
button_thoat = PushButton(app, text="Thoát", width=20)

app.display()