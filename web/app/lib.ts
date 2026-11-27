// Hàm và hằng dùng chung giữa trang chat và trang danh sách quán.

export const vnd = (n?: number | null) => (n == null ? "" : `${Math.round(n).toLocaleString("vi-VN")}đ`);

export const READ: Record<string, string> = {
  hai_san: "hải sản", dau_phong: "đậu phộng", sua: "sữa", trung: "trứng", gluten: "gluten", dau_nanh: "đậu nành",
};
