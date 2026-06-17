import streamlit as st

# 1. Cấu hình giao diện ứng dụng
st.set_page_config(page_title="App Tính Thu Nhập Cá Nhân", page_icon="💰", layout="centered")
st.title("💰 Ứng Dụng Tính Thuế TNCN & Lương Thực Nhận")
st.write("Nhập thông tin thu nhập Gross của bạn để tự động tính toán.")

# 2. Tạo các ô nhập liệu ở thanh bên (Sidebar) hoặc màn hình chính
st.header("📌 Nhập thông tin thu nhập")
thu_nhap_gross = st.number_input("Tổng thu nhập tháng (Gross) - VNĐ:", min_value=0, value=20000000, step=500000)
so_nguoi_phu_thuoc = st.number_input("Số người phụ thuộc:", min_value=0, value=0, step=1)

# Thêm tùy chọn các khoản phụ cấp không tính thuế (nếu có)
phu_cap_mien_thue = st.number_input("Khoản phụ cấp được miễn thuế (Ăn trưa, điện thoại...) - VNĐ:", min_value=0, value=0, step=100000)

# 3. Logic xử lý tính toán dựa trên Luật Thuế TNCN
GIAM_TRU_BAN_THAN = 11000000
GIAM_TRU_PHU_THUOC = 4400000
MUC_TRAN_BH = 46800000  # Mức trần đóng BHXH/BHYT áp dụng từ 01/07/2024 (23.4 triệu x 20)

# Tính bảo hiểm bắt buộc (8% BHXH, 1.5% BHYT, 1% BHTN trên lương gross)
# Lưu ý: BHXH và BHYT bị giới hạn bởi mức trần lương cơ sở
luong_tinh_bh = min(thu_nhap_gross, MUC_TRAN_BH)
tien_bhxh = luong_tinh_bh * 0.08
tien_bhyt = luong_tinh_bh * 0.015
# BHTN tính trên mức trần tối đa của lương tối thiểu vùng (ở đây đơn giản hóa theo lương gross)
tien_bhtn = thu_nhap_gross * 0.01 if thu_nhap_gross < 93600000 else 936000
tong_bao_hiem = tien_bhxh + tien_bhyt + tien_bhtn

# Tính toán các khoản giảm trừ gia cảnh
tong_giam_tru = GIAM_TRU_BAN_THAN + (so_nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC)

# Thu nhập tính thuế (TNTT)
thu_nhap_tinh_thue = thu_nhap_gross - tong_bao_hiem - phu_cap_mien_thue - tong_giam_tru
thu_nhap_tinh_thue = max(0, thu_nhap_tinh_thue) # Nếu âm thì bằng 0

# Hàm tính thuế lũy tiến từng phần theo Biểu thuế lũy tiến Việt Nam
def tinh_thue_tncn(tntt):
    if tntt <= 5000000:
        return tntt * 0.05
    elif tntt <= 10000000:
        return tntt * 0.1 - 250000
    elif tntt <= 18000000:
        return tntt * 0.15 - 750000
    elif tntt <= 32000000:
        return tntt * 0.2 - 1650000
    elif tntt <= 52000000:
        return tntt * 0.25 - 3250000
    elif tntt <= 80000000:
        return tntt * 0.3 - 5850000
    else:
        return tntt * 0.35 - 9850000

thue_phai_nop = tinh_thue_tncn(thu_nhap_tinh_thue)
luong_net = thu_nhap_gross - tong_bao_hiem - thue_phai_nop

# 4. Hiển thị kết quả ra màn hình bằng Streamlit giao diện đẹp
st.markdown("---")
st.header("📊 Kết Quả Phân Tích Thu Nhập")

# Hiển thị số tiền Lương Thực Nhận (Net) nổi bật
st.metric(label="💰 LƯƠNG THỰC NHẬN (NET)", value=f"{luong_net:,.0f} VNĐ")
# Hiển thị bảng chi tiết các khoản khấu trừ dưới dạng cấu trúc cột
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Các khoản giảm trừ")
    st.write(f"- **Bảo hiểm bắt buộc (10.5%):** {tong_bao_hiem:,.0f} VNĐ")
    st.write(f"- **Giảm trừ gia cảnh bản thân:** {GIAM_TRU_BAN_THAN:,.0f} VNĐ")
    st.write(f"- **Giảm trừ người phụ thuộc:** {so_nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC:,.0f} VNĐ")
    if phu_cap_mien_thue > 0:
        st.write(f"- **Phụ cấp miễn thuế:** {phu_cap_mien_thue:,.0f} VNĐ")

with col2:
    st.subheader("💸 Nghĩa vụ Thuế")
    st.write(f"- **Thu nhập chịu thuế:** {max(0, thu_nhap_gross - phu_cap_mien_thue):,.0f} VNĐ")
    st.write(f"- **Thu nhập tính thuế:** {thu_nhap_tinh_thue:,.0f} VNĐ")
    st.error(f"- **Thuế TNCN phải nộp:** {thue_phai_nop:,.0f} VNĐ")

# Thêm biểu đồ hình tròn trực quan hóa phân bổ thu nhập (tùy chọn)
st.subheader("🍕 Phân bổ thu nhập Gross của bạn")
bieu_do_data = {
    "Lương thực nhận (Net)": luong_net,
    "Bảo hiểm bắt buộc": tong_bao_hiem,
    "Thuế TNCN": thue_phai_nop
}
st.bar_chart(bieu_do_data)
