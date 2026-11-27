// Kiểu dữ liệu khớp với codebase/web.py và ket_qua trong codebase/agent.py.

export type Loai = "goi_y" | "hoi_lai" | "khong_co" | "tu_choi";

export type LuaChon = {
  quan: { id: string; ten: string; khoang_cach_km: number; danh_gia: number | null; so_danh_gia?: number; muc_gia?: string; gio_mo: string | null };
  mon: { nguoi: string; mon_id: string; mon: string; gia: number; loai: string }[];
  tong_tien: number;
  ly_do: string;
  danh_doi: string;
};

export type KetQua = {
  lua_chon?: LuaChon[];
  loai: Loai;
  che_do_gia?: boolean;
  quan?: { id: string; ten: string; khoang_cach_km: number; danh_gia: number | null; so_danh_gia?: number; muc_gia?: string; gio_mo: string | null };
  mon?: { nguoi: string; mon_id: string; mon: string; gia: number; loai: string }[];
  tong_tien?: number;
  ngan_sach?: number | null;
  ly_do?: string;
  canh_bao?: string[];
  loi_nhan?: string;
  cau_hoi?: string[] | null;
  hoi_them?: string | null;
  ai_bi_thay?: boolean;
  goi_y_noi?: string[];
};

export type Buoc = { loai: "model" | "tool" | "note"; ten: string; chi_tiet?: string; loi?: string; t?: number };

export type ThongKe = { model_calls: number; tool_calls: number; tokens_in: number; tokens_out: number; models: string[] };

export type AnswerResponse = {
  output: string;
  ket_qua: KetQua | null;
  thong_ke: ThongKe;
  cac_buoc: Buoc[];
};

export type Mon = {
  id: string;
  ten: string;
  gia: number;
  loai: string;
  nhom: string;
  mo_ta: string;
  chay: boolean | null;
  co_nhac: string[];
  thit: string[];
  ghi_thanh_phan: boolean;
};

export type Quan = {
  id: string;
  ten: string;
  am_thuc: string;
  khoang_cach_km: number;
  danh_gia: number | null;
  so_danh_gia?: number;
  muc_gia?: string;
  gio_mo: string | null;
  freeship: boolean;
  khuyen_mai: string | null;
  mon: Mon[];
};

export type DuLieu = { _ghi_chu: string; quan: Quan[] };
