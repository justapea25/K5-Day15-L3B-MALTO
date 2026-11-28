import QuanList from "./quan-list";

export const metadata = { title: "Danh sách quán · MALTO" };

export default function Page() {
  return (
    <section className=" border-2 border-ink bg-panel p-5 shadow-[6px_6px_0_#242434]">
      <div className="mb-1 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-lg font-semibold">Các quán trong dữ liệu</h2>
        <p className="text-xs text-muted">Bấm vào quán để xem menu</p>
      </div>
      <p className="mb-4 text-xs text-muted">
        Quán dựng giả (tên dựng), sinh theo số liệu menu thật trên GrabFood · ảnh quán là ảnh minh hoạ do AI tạo (gpt-image-2) · nhãn chay / thành phần gắn theo tên và mô tả món, có thể thiếu.
      </p>
      <QuanList />
    </section>
  );
}
