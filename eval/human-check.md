# Phiếu chấm độc lập — người thứ hai

> Người chấm **không phải người viết spec** (đề xuất: Thu). Chấm 5 output dưới đây của `run-4@20261128-040930` theo `eval/metric_spec.yaml`,
> **không xem cột `pass` của code trước khi chấm**. Mỗi ô ghi 1 (đạt) / 0 (không). Xong thì ghi "khớp x/5" vào `eval/README.md` (cần ≥ 4/5) và mục `khop_so_thich`.
> Một câu "khớp" khi kết luận đạt / không đạt của người chấm trùng với cột `pass` của code (và, với `khop_so_thich`, trùng đề xuất LLM).

Người chấm: Claude Code đối chiếu từng quán / món / giá / km với `data/restaurants.json`, Thu (không viết spec) rà lại và xác nhận · Thời điểm: 28/11/2026

| Câu | khong_bia_so_lieu | dung_rang_buoc_cung | xu_ly_dung_tinh_huong | khop_so_thich | Đạt cả câu? | Ghi chú |
|---|---|---|---|---|---|---|
| B01 | 1 | 1 | 1 | 1 | 1 | Cả 2 quán, 8 món khớp data. Tổng 250k ≤ 280k. Cơm cá kho (com), bún chay nấm (chay=true), há cảo hấp không chiên. Quán ≤ 1km. |
| B09 | 1 | 1 | 1 | 1 | 1 | Món, giá khớp data. Tổng 131k ≤ 180k. Cháo nấm chay cho người tránh cay. Lý do nêu cả 3 sở thích. Lưu ý nhỏ: "ăn no" được đáp bằng cháo gà xé, quán 2 có cơm no hơn. |
| B16 | 1 | 1 | 1 | 1 | 1 | Anh Tuấn hạng 1, 0,5 km. Bún 60k, phở chay (pho) 70k, cơm chay thập cẩm (com, chay=true) 70k. Tổng đúng 200k. Nhãn "Cơm chay (chay; muốn cơm)" đặt hơi lạ nhưng không sai. |
| B24 | 1 | 1 | 1 | 1 | 1 | Bánh bao kim sa 30k (an_vat), khoai tây chiên 28k khớp data. Tổng 90k ≤ 90k, không lẩu. Lưu ý: hạng 1 cách 4,1 km, đề bài không giới hạn km; cả 3 người cùng một món. |
| B28 | 1 | 1 | 1 | — | 1 | Không có quán nào ≤ 1km có cả bún chả lẫn phở (đã quét data). Bot nói "chưa có" và hỏi nới. 0,3 km = Mẹ Mít (bún chả), 0,5 km = Anh Tuấn (phở chay), khớp data. `khop_so_thich` không áp dụng vì không gợi ý quán. |

Sau khi chấm: code chấm 5/5 đạt; LLM đề xuất `khop_so_thich` đạt cả 5. **Khớp: 5/5** (kết luận đạt / không đạt trùng cột `pass` của code, và `khop_so_thich` trùng đề xuất LLM với 4 câu có gợi ý quán; B28 không áp dụng)

---

## B01 · thuong

**Input:** Nhóm 4 người: Lan muốn ăn gì có nước, Hùng thèm cơm, Mai không ăn đồ chiên, Nam ăn chay. Mỗi người tầm 70k, dưới 1km

**pass_criterion:** Quán có trong data và khoang_cach_km ≤ 1; món của Hùng có loai=com; món của Nam có chay=true; tổng tiền món ≤ 280.000đ

**Output của bot:**

```
Mình nghiêng về Ông Ngoại: đủ món cho cả nhóm, có món hấp cho Mai và các lựa chọn chay, cơm, món nước; quán cách 0,4 km.

1. Ông Ngoại - Cơm Văn Phòng & Cơm — cách 0.4 km · ★ 4.5 · mở 06:00-14:00 17:00-21:30
- Lan (tối đa 70.000đ): Bún chay nấm đặc biệt — 60.000đ
- Hùng (muốn cơm; tối đa 70.000đ): Cơm cá kho (lớn) — 70.000đ
- Mai (tối đa 70.000đ): Há cảo hấp (lớn) — 60.000đ
- Nam (chay; tối đa 70.000đ): Bún chay nấm đặc biệt — 60.000đ
Tổng tiền món 250.000đ (chưa gồm phí ship) / ngân sách 280.000đ
Lý do: Ông Ngoại có bún chay nấm cho Lan và Nam, cơm cá kho cho Hùng, há cảo hấp cho Mai; phù hợp ngân sách và cách dưới 1 km.

2. Hai Lúa - Cơm Văn Phòng - Cơm Rang - S1.09 — cách 1.0 km · ★ 4.6 · mở 09:00-22:00
- Lan (tối đa 70.000đ): Cháo sườn (nhỏ) — 55.000đ
- Hùng (muốn cơm; tối đa 70.000đ): Cơm sườn nướng — 65.000đ
- Mai (tối đa 70.000đ): Cơm chay thập cẩm (nhỏ) — 65.000đ
- Nam (chay; tối đa 70.000đ): Cơm chay thập cẩm (nhỏ) — 65.000đ
Tổng tiền món 250.000đ (chưa gồm phí ship) / ngân sách 280.000đ
Lý do: Hai Lúa có cháo sườn cho Lan, cơm sườn nướng cho Hùng và cơm chay cho Nam; Mai có thể chọn cơm chay để tránh món chiên.
So với lựa chọn 1: Mai dùng món chay thay vì món mặn; quán cách đúng 1 km.
```

## B09 · kho

**Input:** 3 đứa: 1 đứa muốn ăn gì nhẹ nhẹ, 1 đứa đói muốn ăn no, 1 đứa không ăn cay. Mỗi người 60k

**pass_criterion:** Quán và cả 3 món có trong data; tổng ≤ 180.000đ; phần lý do nhắc tới ít nhất 2 trong 3 sở thích

**Output của bot:**

```
Mình nghiêng về O Hạnh vì có cả món nhẹ lẫn cháo gà xé, hợp gom một đơn cho cả nhóm; Hai Lúa là lựa chọn nếu người đói muốn ăn cơm no hơn.

1. O Hạnh - Cháo gà xé - Cháo trai - Tòa R1.03 — cách 0.9 km · ★ 4.6 · mở 07:00-21:00
- Người 1 (tối đa 60.000đ): Súp cua — 39.000đ
- Người 2 (tối đa 60.000đ): Cháo gà xé — 50.000đ
- Người 3 (tối đa 60.000đ): Cháo nấm chay — 42.000đ
Tổng tiền món 131.000đ (chưa gồm phí ship) / ngân sách 180.000đ
Lý do: O Hạnh có món nhẹ như súp cua, cháo gà xé cho người muốn ăn no và cháo nấm chay; lựa chọn cháo nấm phù hợp hơn với người tránh cay.

2. Hai Lúa - Cơm Văn Phòng - Cơm Rang - S1.09 — cách 1.0 km · ★ 4.6 · mở 09:00-22:00
- Người 1 (tối đa 60.000đ): Cháo sườn (nhỏ) — 55.000đ
- Người 2 (tối đa 60.000đ): Cơm gà xối mỡ — 55.000đ
- Người 3 (tối đa 60.000đ): Cơm gà xối mỡ (nhỏ) — 55.000đ
Tổng tiền món 165.000đ (chưa gồm phí ship) / ngân sách 180.000đ
Lý do: Hai Lúa có cháo sườn nhỏ cho người muốn ăn nhẹ và cơm gà cho hai người còn lại; người không ăn cay có thể chọn cơm gà.
So với lựa chọn 1: Nhiều lựa chọn cơm no, nhưng món nhẹ chủ yếu là cháo.
```

## B16 · thuong

**Input:** Mình đặt về văn phòng: 1 bún, 1 phở, 1 cơm chay, tổng 200k, dưới 1km

**pass_criterion:** Mọi quán gợi ý ≤ 1km và tổng ≤ 200.000đ; mỗi quán có 1 suất loai=bun, 1 suất loai=pho, 1 suất loai=com có chay=true; quán xếp hạng 1 = Anh Tuấn - Bún Chay - Cơm Chay - Tòa R1.03

**Output của bot:**

```
Anh Tuấn là lựa chọn phù hợp nhất: có đủ cả ba suất và gần văn phòng. Lưu ý quán mở từ 17:00 đến 22:30.

❓ Bạn định đặt lúc nào? Mình có thể kiểm tra quán có mở đúng giờ không.

1. Anh Tuấn - Bún Chay - Cơm Chay - Tòa R1.03 — cách 0.5 km · ★ 4.2 · mở 17:00-22:30
- Người 1 (muốn bún): Bún chay nấm (lớn) — 60.000đ
- Người 2 (muốn phở): Phở chay đặc biệt — 70.000đ
- Cơm chay (chay; muốn cơm): Cơm chay thập cẩm (nhỏ) — 70.000đ
Tổng tiền món 200.000đ (chưa gồm phí ship) / ngân sách 200.000đ
Lý do: Anh Tuấn có đủ bún, phở và cơm chay cho cả đơn, đồng thời nằm trong khoảng cách bạn muốn.
```

## B24 · kho

**Input:** chiều đói bụng, 3 đứa muốn ăn vặt gì đó, mỗi đứa 30k

**pass_criterion:** Quán và món có trong data; tổng ≤ 90.000đ; không gợi ý lẩu hay món phần lớn; nếu không có thì có câu "không có quán nào"

**Output của bot:**

```
Mình nghiêng về Món hoa P3 - OCP2: có bánh bao kim sa vừa mức 30k mỗi bạn. Nếu muốn món khoai chiên thì Út Hoa gần nhất; còn Combo gà rán + khoai burger góc phố trâu quỳ cũng có khoai chiên.

❓ Chiều bạn định ăn khoảng mấy giờ? Hai quán khoai chiên chỉ mở từ 17:00 nha.

1. Món hoa P3 - OCP2 — cách 4.1 km · ★ 4.6 · mở 06:00-14:00 17:00-21:30
- Người 1 (muốn ăn vặt): Bánh bao kim sa — 30.000đ
- Người 2 (muốn ăn vặt): Bánh bao kim sa — 30.000đ
- Người 3 (muốn ăn vặt): Bánh bao kim sa — 30.000đ
Tổng tiền món 90.000đ (chưa gồm phí ship) / ngân sách 90.000đ
Lý do: Món hoa P3 - OCP2 có bánh bao kim sa vừa ngân sách mỗi bạn, hợp ăn vặt nhẹ.

2. combo gà rán + khoai burger góc phố trâu quỳ — cách 2.4 km · ★ 4.4 · mở 17:00-22:30
- Người 1 (muốn ăn vặt): Khoai tây chiên — 28.000đ
- Người 2 (muốn ăn vặt): Khoai tây chiên — 28.000đ
- Người 3 (muốn ăn vặt): Khoai tây chiên — 28.000đ
Tổng tiền món 84.000đ (chưa gồm phí ship) / ngân sách 90.000đ
Lý do: Combo gà rán + khoai burger góc phố trâu quỳ có khoai tây chiên, gần hơn lựa chọn đầu.
So với lựa chọn 1: Tổng thấp hơn nhưng quán chỉ mở từ 17:00.

3. Út Hoa - Gà rán 2 miếng & Gà rán — cách 1.7 km · ★ 4.3 · mở 17:00-22:30
- Người 1 (muốn ăn vặt): Khoai tây chiên — 28.000đ
- Người 2 (muốn ăn vặt): Khoai tây chiên — 28.000đ
- Người 3 (muốn ăn vặt): Khoai tây chiên — 28.000đ
Tổng tiền món 84.000đ (chưa gồm phí ship) / ngân sách 90.000đ
Lý do: Út Hoa - Gà rán 2 miếng & Gà rán gần nhất trong các lựa chọn, có khoai tây chiên.
So với lựa chọn 1: Tổng thấp hơn nhưng quán chỉ mở từ 17:00.
```

## B28 · kho

**Input:** 2 người, 1 đứa ăn bún chả 1 đứa ăn phở, tổng 120k, dưới 1km

**pass_criterion:** Không gợi ý quán như một phương án; có câu "không có quán" / "chưa có quán" hoặc hỏi lại đặt nhiều quán / nới yêu cầu

**Output của bot:**

```
Trong phạm vi 1 km và tổng 120k chưa có một quán đáp ứng cả bún chả lẫn phở. Có thể gọi mỗi món ở một quán riêng (cách nhau 0,3 km và 0,5 km), hay bạn muốn nới ngân sách để tìm một quán cho cả hai?
```
