import QuanList from "./quan-list";

export const metadata = { title: "Danh sách quán · MALTO" };

export default function Page() {
  return (
    <section className="rounded-2xl border border-line bg-panel p-5">
      <div className="mb-1 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-lg font-semibold">Các quán trong dữ liệu</h2>
        <p className="text-xs text-muted">Bấm vào quán để xem menu</p>
      </div>
      <p className="mb-4 text-xs text-muted">
        Quán dựng giả (tên dựng), sinh theo số liệu menu thật trên GrabFood · nhãn chay / thành phần gắn theo tên và mô tả món, có thể thiếu.
      </p>
      <QuanList />
    </section>
  );
}
