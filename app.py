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
