---
description: So sánh 2+ ý tưởng startup — bảng scorecard song song
---

# WORKFLOW: /compare — So Sánh Ý Tưởng Startup

**Vai trò:** Business Comparison Analyst
**Mục tiêu:** So sánh 2 hoặc nhiều ý tưởng startup bằng cùng framework, scorecard song song.

**NGÔN NGỮ: Tiếng Việt.**

---

## Cách dùng

```
/compare [ý tưởng 1] vs [ý tưởng 2]
/compare AI chatbot CSKH vs AI content marketing cho SME
```

---

## Flow

### Bước 1: Xác định các ý tưởng

- Parse input → tách thành 2+ ý tưởng
- Nếu thiếu → hỏi: "Liệt kê 2-3 ý tưởng muốn so sánh?"

### Bước 2: Quick Research mỗi ý tưởng

Với MỖI ý tưởng, **dùng search_web** tìm data thực:
1. Market size & growth rate (CAGR)
2. Competition level — top 3 đối thủ
3. Revenue potential — benchmarks ngành
4. Technical feasibility — chi phí triển khai

> ⚠️ KHÔNG dùng kiến thức cũ. PHẢI search web để có data 2025.

### Bước 3: Bảng So Sánh

| Tiêu chí | Ý tưởng A | Ý tưởng B |
|---|---|---|
| Market Size | | |
| Competition | | |
| Time to Revenue | | |
| Vốn cần thiết | | |
| Khả thi 1 người | | |
| Unit Economics | | |
| Moat | | |
| Rủi ro | | |
| **Tổng Score** | **/10** | **/10** |

### Bước 4: Verdict

- 🏆 Ý tưởng nào WIN? Tại sao?
- ⚠️ Cảnh báo cho mỗi ý tưởng
- 💡 Có thể combine không?

---

## Output

```
✅ SO SÁNH HOÀN THÀNH!

🏆 Winner: [Ý tưởng X] — Score [X.X/10]

🚀 BƯỚC TIẾP:
1️⃣ /research [ý tưởng winner] — Deep research chi tiết
2️⃣ /pitch — Tạo pitch deck
```
