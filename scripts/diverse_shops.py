"""18 kiểu quán thêm vào data giả cho ĐA DẠNG như data GrabFood thật (Nhật, Hàn, Hoa, Thái, gà rán, pizza…).

Dùng bởi scripts/gen_synthetic.py. Tên quán là TÊN DỰNG, không phải thương hiệu thật.
Mỗi món: (tên, mô tả, loại món, (giá thấp, giá thường, giá cao)) — khoảng giá theo mặt bằng menu trên GrabFood
quanh Vinhomes Ocean Park (bản crawl của nhóm), làm tròn *(tự ước tính theo data crawl)*.
"""

# Loại món mới (thêm vào bun / pho / com / mi / banh_mi / lau / khac)
LOAI_MOI = ["chao", "xoi", "sushi", "ga_ran", "pizza", "nuong", "an_vat"]

K = 1000
SHOPS = {
    "nhat": ("Món Nhật, Sushi", ["Sakura Bento", "Sushi Hoa Anh Đào", "Nhà Bếp Tokyo Nhỏ"], [
        ("Sushi cá hồi (8 miếng)", "cá hồi, cơm giấm", "sushi", (89, 129, 189)), ("Sashimi tổng hợp", "cá hồi, cá ngừ, bạch tuộc", "sushi", (159, 219, 299)),
        ("Cơm bento gà teriyaki", "gà sốt teriyaki, cơm, rau", "com", (69, 89, 119)), ("Ramen tonkotsu", "nước hầm xương heo, thịt xá xíu, trứng", "mi", (89, 115, 149)),
        ("Udon bò", "mì udon, thịt bò", "mi", (79, 99, 129)), ("Cơm cà ri Nhật", "cà ri, thịt heo chiên xù", "com", (75, 95, 120)),
        ("Sushi cuộn chay", "dưa leo, bơ, cà rốt", "sushi", (55, 69, 89)), ("Gà karaage", "gà chiên kiểu Nhật", "ga_ran", (65, 79, 99))]),
    "han": ("Món Hàn", ["Seoul Corner", "Kimbap Nhà Min"], [
        ("Tokbokki phô mai", "bánh gạo, chả cá, phô mai", "an_vat", (55, 69, 89)), ("Kimbap truyền thống", "cơm cuộn rong biển, trứng, xúc xích", "an_vat", (39, 49, 65)),
        ("Mì cay hải sản cấp 2", "mì, tôm, mực", "mi", (59, 75, 99)), ("Cơm trộn bibimbap", "cơm, rau, trứng, thịt bò", "com", (69, 85, 109)),
        ("Gà sốt cay Hàn Quốc", "gà rán, sốt cay ngọt", "ga_ran", (79, 99, 139)), ("Canh kimchi đậu phụ", "kimchi, đậu phụ, thịt heo", "khac", (65, 79, 99)),
        ("Cơm trộn chay", "rau củ, nấm, đậu phụ", "com", (59, 69, 85))]),
    "hoa": ("Món Hoa, Dimsum", ["Dimsum Phố Hoa", "Quảng Đông Quán"], [
        ("Há cảo tôm (4 viên)", "tôm, bột năng", "khac", (45, 55, 69)), ("Xíu mại hấp", "thịt heo, tôm", "khac", (39, 49, 59)),
        ("Cơm chiên Dương Châu", "trứng, lạp xưởng, tôm", "com", (55, 69, 85)), ("Mì vằn thắn", "vằn thắn tôm thịt, nước dùng", "mi", (49, 59, 75)),
        ("Vịt quay (phần)", "vịt quay da giòn", "khac", (89, 119, 159)), ("Bánh bao kim sa", "nhân trứng muối sữa", "an_vat", (35, 45, 55)),
        ("Cháo cá", "cá lóc, gừng", "chao", (45, 55, 65))]),
    "thai": ("Món Thái", ["Bếp Thái Xanh"], [
        ("Pad Thái tôm", "bánh phở xào, tôm, lạc rang", "mi", (65, 79, 99)), ("Lẩu Tom Yum (suất 1 người)", "tôm, nấm, sả, lá chanh", "lau", (99, 129, 159)),
        ("Cơm chiên dứa", "dứa, tôm, hạt điều", "com", (65, 79, 95)), ("Gỏi đu đủ Thái", "đu đủ, tôm khô, lạc", "khac", (45, 55, 69)),
        ("Cà ri xanh gà", "gà, nước cốt dừa, cà tím", "com", (75, 89, 109)), ("Pad Thái chay", "bánh phở, đậu phụ, giá", "mi", (55, 65, 79))]),
    "dailoan": ("Món Đài Loan", ["Đài Bắc Nhỏ"], [
        ("Cơm thịt kho Đài Loan", "thịt heo băm kho, trứng", "com", (49, 59, 75)), ("Gà rán Đài Loan", "gà tẩm bột chiên, bột ớt", "ga_ran", (49, 65, 79)),
        ("Mì bò Đài Loan", "bò hầm, mì sợi to", "mi", (69, 85, 109)), ("Bánh bao chiên", "nhân thịt heo", "an_vat", (35, 45, 55))]),
    "an": ("Món Ấn Độ", ["Gia Vị Ấn"], [
        ("Cà ri gà bơ", "gà, sốt cà chua bơ", "com", (89, 109, 139)), ("Cơm Biryani gà", "cơm gia vị, gà", "com", (89, 109, 129)),
        ("Bánh naan bơ tỏi", "bột mì, bơ, tỏi", "an_vat", (35, 45, 55)), ("Cà ri rau củ chay", "đậu gà, rau củ", "com", (69, 85, 99))]),
    "garan": ("Gà rán, Burger", ["Gà Giòn Phố", "Burger Góc Phố"], [
        ("Gà rán 2 miếng", "gà tẩm bột chiên giòn", "ga_ran", (59, 69, 85)), ("Combo gà rán + khoai", "gà rán, khoai tây chiên", "ga_ran", (79, 95, 119)),
        ("Burger bò phô mai", "bò, phô mai, rau", "banh_mi", (55, 69, 89)), ("Burger gà giòn", "gà chiên, sốt mayo", "banh_mi", (49, 59, 75)),
        ("Cơm gà sốt cay", "gà rán, cơm", "com", (55, 65, 79)), ("Khoai tây chiên", "khoai tây", "an_vat", (25, 35, 45))]),
    "pizza": ("Pizza, Pasta", ["Pizza Lò Củi Nhỏ", "Bếp Ý Phố"], [
        ("Pizza hải sản (size M)", "tôm, mực, phô mai", "pizza", (129, 169, 219)), ("Pizza phô mai (size M)", "phô mai mozzarella", "pizza", (109, 139, 179)),
        ("Pizza rau củ chay (size M)", "nấm, ớt chuông, ô liu", "pizza", (99, 129, 159)), ("Mỳ Ý bò bằm", "spaghetti, bò bằm, sốt cà chua", "mi", (69, 89, 115)),
        ("Mỳ Ý kem nấm", "spaghetti, kem, nấm", "mi", (69, 85, 109)), ("Salad Caesar", "xà lách, gà, phô mai", "khac", (59, 75, 95))]),
    "haisan": ("Món Hải Sản", ["Hải Sản Biển Đêm"], [
        ("Ốc hương xào bơ tỏi", "ốc hương, bơ, tỏi", "khac", (89, 119, 159)), ("Tôm nướng muối ớt", "tôm sú", "nuong", (129, 169, 219)),
        ("Mực hấp gừng", "mực ống, gừng", "khac", (109, 139, 179)), ("Cháo hải sản", "tôm, mực, nghêu", "chao", (59, 75, 95)),
        ("Cơm chiên hải sản", "tôm, mực, trứng", "com", (65, 79, 99))]),
    "nuong": ("Lẩu & Nướng", ["Nướng Ngói Sân Thượng", "Lẩu Nướng Bếp Than"], [
        ("Ba chỉ bò Mỹ nướng (suất)", "ba chỉ bò, nấm", "nuong", (119, 149, 189)), ("Sườn heo nướng mật ong (suất)", "sườn heo", "nuong", (99, 129, 159)),
        ("Lẩu thái chua cay (suất 1 người)", "hải sản, nấm", "lau", (119, 149, 189)), ("Lẩu nấm chay (suất 1 người)", "nấm các loại, đậu phụ", "lau", (99, 119, 149)),
        ("Rau củ nướng", "ngô, cà tím, đậu bắp", "nuong", (45, 55, 69))]),
    "chao": ("Cháo, Súp", ["Cháo Dinh Dưỡng Mẹ Nấu", "Súp Cua Góc Chợ"], [
        ("Cháo sườn sụn", "sườn heo, quẩy", "chao", (35, 45, 55)), ("Cháo gà xé", "gà ta, hành phi", "chao", (39, 49, 59)),
        ("Cháo trai", "trai, rau răm", "chao", (35, 45, 55)), ("Súp cua", "cua, trứng, nấm", "chao", (30, 39, 49)),
        ("Cháo nấm chay", "nấm, rau củ", "chao", (35, 42, 49))]),
    "xoi": ("Xôi, Bánh Mì", ["Xôi Sáng Phố Cổ", "Bánh Mì Lò Than"], [
        ("Xôi xéo", "đỗ xanh, hành phi", "xoi", (25, 30, 39)), ("Xôi gà", "gà xé, nấm hương", "xoi", (35, 45, 55)),
        ("Xôi pate chả", "pate, chả lụa, ruốc", "xoi", (30, 39, 49)), ("Bánh mì thịt nướng", "thịt heo nướng, dưa góp", "banh_mi", (25, 30, 39)),
        ("Bánh mì trứng pate", "trứng ốp, pate", "banh_mi", (20, 25, 30)), ("Xôi chay đậu xanh", "đỗ xanh, lạc", "xoi", (25, 30, 35))]),
    "banhcuon": ("Bánh Cuốn, Món Hà Nội", ["Bánh Cuốn Bà Hoành Nhỏ", "Bún Chả Phố Hàng"], [
        ("Bánh cuốn nhân thịt", "thịt heo, mộc nhĩ, chả", "khac", (35, 45, 55)), ("Bánh cuốn trứng", "trứng gà, hành phi", "khac", (39, 49, 59)),
        ("Bún chả Hà Nội", "chả nướng, thịt ba chỉ", "bun", (45, 55, 69)), ("Nem rán (5 cái)", "thịt heo, miến", "an_vat", (35, 45, 55)),
        ("Bánh cuốn chay", "nấm, mộc nhĩ", "khac", (30, 39, 45))]),
    "healthy": ("Healthy, Salad", ["Green Bowl Ocean", "Bếp Lành"], [
        ("Salad ức gà sốt mè", "ức gà, rau xanh, mè rang", "khac", (59, 75, 95)), ("Bowl cá hồi áp chảo", "cá hồi, gạo lứt, bơ", "com", (99, 129, 159)),
        ("Cơm gạo lứt ức gà", "gạo lứt, ức gà, rau luộc", "com", (59, 69, 85)), ("Salad rau củ chay", "rau củ, hạt, sốt chanh", "khac", (49, 59, 75)),
        ("Wrap gà nướng", "bánh tortilla, gà, rau", "banh_mi", (55, 65, 79))]),
    "anvat": ("Ăn Vặt", ["Ăn Vặt Cô Ba Ngõ Chợ", "Quán Xiên Que Tuổi Thơ"], [
        ("Nem chua rán", "nem chua, bột chiên", "an_vat", (35, 45, 55)), ("Bánh tráng trộn", "bánh tráng, trứng cút, khô bò", "an_vat", (25, 30, 39)),
        ("Khoai lang lắc phô mai", "khoai lang, bột phô mai", "an_vat", (25, 35, 45)), ("Xiên que thập cẩm", "xúc xích, cá viên, đậu phụ", "an_vat", (30, 39, 49)),
        ("Cá viên chiên", "cá viên, tương ớt", "an_vat", (25, 30, 39))]),
    "vanphong": ("Cơm Văn Phòng", ["Cơm Văn Phòng Tòa S2", "Cơm Nhà Làm Ocean"], [
        ("Cơm sườn xào chua ngọt", "sườn heo, cơm, canh", "com", (40, 45, 55)), ("Cơm cá kho tộ", "cá kho, rau luộc", "com", (40, 45, 55)),
        ("Cơm thịt rang cháy", "thịt ba chỉ, cơm", "com", (40, 45, 50)), ("Cơm đậu phụ sốt cà chay", "đậu phụ, cà chua", "com", (35, 40, 45)),
        ("Cơm gà luộc", "gà ta, nước mắm gừng", "com", (45, 50, 60))]),
    "mientrung": ("Món Miền Trung", ["Mì Quảng Hội An Nhỏ"], [
        ("Mì Quảng gà", "gà, trứng cút, bánh đa", "mi", (45, 55, 69)), ("Bún bò Huế", "bò, giò heo, chả cua", "bun", (49, 59, 75)),
        ("Cao lầu", "thịt xá xíu, rau sống", "mi", (49, 59, 69)), ("Bánh bèo (đĩa)", "tôm chấy, mỡ hành", "an_vat", (35, 45, 55)),
        ("Mì Quảng chay", "đậu phụ, nấm", "mi", (40, 49, 59))]),
    "miennam": ("Món Miền Nam", ["Cơm Tấm Sài Gòn Phố", "Hủ Tiếu Nam Bộ"], [
        ("Cơm tấm sườn bì chả", "sườn nướng, bì, chả trứng", "com", (49, 59, 75)), ("Hủ tiếu Nam Vang", "tôm, thịt, gan", "mi", (49, 59, 69)),
        ("Bánh xèo", "tôm, thịt, giá", "an_vat", (45, 55, 69)), ("Cơm tấm chay", "sườn chay, đậu hũ", "com", (39, 49, 59))]),
}
# 30 quán: mỗi kiểu ≥ 1 quán, phần còn lại chia theo tần suất kiểu quán trên GrabFood (cơm, phở/bún, Nhật, gà rán… phổ biến hơn)
EXTRA_WEIGHTS = {"nhat": 3, "han": 2, "hoa": 2, "garan": 3, "pizza": 2, "chao": 2, "xoi": 2, "vanphong": 3, "anvat": 2,
                 "healthy": 2, "nuong": 2, "banhcuon": 2, "miennam": 2, "haisan": 1, "thai": 1, "dailoan": 1, "an": 1, "mientrung": 1}


# ---------- Tên quán theo KIỂU ĐẶT TÊN thật trên GrabFood (tên dựng, ghép ngẫu nhiên) ----------
# Mẫu thật hay gặp: "<Tên chủ / thương hiệu> - <món chính> - <món phụ> - <toà / khu>", viết hoa thường lộn xộn,
# có mã toà (S2.05, R1), viết tắt OCP1, đôi khi chữ thường toàn bộ. Tên chủ dưới đây là TÊN DỰNG.
OWNERS = ["Mẹ Mít", "Chị Ngân", "Anh Tuấn", "Cô Ba", "Bà Tư", "Dì Năm", "O Hạnh", "Chú Hải", "Nhà Nấm", "Bếp Nhà Bông",
          "Bếp Cô Thu", "Nhà Mây", "Bé Na", "Ông Ngoại", "Hai Lúa", "Bếp Mẹ Gạo", "Út Hoa", "Anh Béo", "Chị Lan", "Nhà Sóc"]
PLACES = ["Vinhomes Ocean Park", "Ocean Park", "OCP1", "OCP2", "Tòa S2.05", "Tòa R1.03", "S1.09", "Tòa P3", "Đa Tốn",
          "Trâu Quỳ", "Gia Lâm", "Ngõ 12 Đa Tốn", "Chung Cư Ecopark", "Tòa Sapphire 2"]
DISH_WORDS = {
    "Cơm": ["Cơm Văn Phòng", "Cơm Rang", "Cơm Gà", "Cơm Niêu"], "Bún": ["Bún Chả", "Bún Cá", "Bún Riêu", "Bún Bò"],
    "Phở": ["Phở Bò", "Phở Gà", "Phở Cuốn"], "Mì Miến": ["Mì Xào", "Miến Lươn", "Mỳ Vằn Thắn", "Miến Trộn"],
    "Bánh Mì": ["Bánh Mì", "Bánh Mì Chảo", "Xôi"], "Lẩu": ["Lẩu", "Lẩu Thái", "Lẩu Riêu Cua"],
    "Món chay": ["Cơm Chay", "Bún Chay", "Đồ Chay"], "Cơm, Bún, Món Việt": ["Cơm", "Bún", "Món Nhà Làm", "Cơm Văn Phòng"],
}


def grab_name(rng, kind_words, base=None):
    """Ghép tên quán theo vài kiểu đặt tên phổ biến trên GrabFood."""
    owner = base or rng.choice(OWNERS)
    w = list(dict.fromkeys(kind_words))
    rng.shuffle(w)
    a, b = w[0], (w[1] if len(w) > 1 else w[0])
    place = rng.choice(PLACES)
    style = rng.randrange(6)
    if style == 0:
        return "%s %s - %s - %s" % (a, owner, b, place)
    if style == 1:
        return "%s - %s & %s" % (owner, a, b)
    if style == 2:  # kiểu "Phở gà VM17 - OCP1"
        code = rng.choice(["VM17", "S2.05", "R1", "P3", "S1.09", "R2.11", "Z38"])
        name = a[0] + a[1:].lower() if rng.random() < 0.5 else a
        return "%s %s - OCP%d" % (name, code, rng.randint(1, 2))
    if style == 3:
        return "%s - %s - %s - %s" % (owner, a, b, place)
    if style == 4:
        return ("%s %s %s" % (a, owner, place)).lower()
    return "%s %s" % (a, owner)
