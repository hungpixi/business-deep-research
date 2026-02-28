---
name: bdr-research-engine
description: Hướng dẫn AI cách chạy Business Deep Research pipeline — search, analyze, cross-validate
---

# BDR Research Engine Skill

## Khi nào skill này được kích hoạt?

Khi user dùng `/research`, `/pitch`, `/compare`, hoặc bất kỳ lệnh nào liên quan đến phân tích kinh doanh.

## Nguyên tắc Research

### 1. LUÔN Search Web — Không Hallucinate

- Mỗi claim PHẢI có data từ web search thực
- Số liệu phải CỤ THỂ: %, VND, USD, market size, growth rate
- Ghi rõ "Ước tính" nếu data không chính xác 100%
- LUÔN giữ citations [Source](URL)

### 2. Batch Search Strategy

Thay vì search 1 query → batch 3-4 queries liên quan:

**Ví dụ cho market research:**
```
Batch 1 (Thị trường):
1. "Quy mô thị trường [ngành] tại [thị trường] 2024-2026 CAGR"
2. "Nhu cầu [target] tại [thị trường] 2025"
3. "Xu hướng AI [ngành] [thị trường] 2025"
4. "Chính sách hỗ trợ startup [thị trường] 2025"

Batch 2 (Đối thủ):
1. "Top đối thủ [ngành] [thị trường] 2025 pricing features"
2. "Đối thủ quốc tế [ngành] so sánh giá"
3. "Chi tiêu [target] willingness to pay"
4. "Chi phí cloud API hosting startup 2025"
```

### 3. Framework-Driven Analysis

Không trả lời chung chung. Áp MBA frameworks cụ thể:

| Framework | Khi nào dùng |
|---|---|
| Lean Canvas | Mọi startup |
| SWOT + TOWS | Mọi startup |
| Porter's Five Forces | Ngành có nhiều đối thủ |
| PESTEL | Ngành bị ảnh hưởng chính sách |
| Blue Ocean ERRC | Tìm thị trường ngách |
| TAM/SAM/SOM | Ước tính market size |
| BCG Matrix | Có nhiều sản phẩm |
| Ansoff Matrix | Chiến lược mở rộng |
| Value Chain | Chuỗi cung ứng phức tạp |

### 4. Financial Cross-Validation

- Revenue 3 scenarios BẮT BUỘC: Pessimistic / Base / Optimistic
- Nếu CAC = 0 → ghi rõ "sweat equity, opportunity cost ~X triệu/tháng"
- Unit Economics: LTV/CAC > 3 mới healthy
- Break-even: tháng CỤ THỂ, số customers CỤ THỂ
- Sensitivity analysis: ±20%

### 5. Devil's Advocate Protocol

Khi chạy phản biện:
- CHUYỂN vai hoàn toàn — chỉ phê bình, KHÔNG khen
- Mỗi phê bình có DATA hoặc LOGIC cụ thể
- 6 phần bắt buộc: Assumptions, Cross-check, Đối thủ attack, Worst case, Blind spots, Stress test
- KHÔNG làm nhẹ phản biện trong bản tổng hợp cuối

### 6. Context Consistency

- Pricing phải NHẤT QUÁN across tất cả sections
- Nếu user cho pricing → dùng CHÍNH XÁC giá đó
- Nếu bootstrap (vốn < 100tr) → KHÔNG đề cập gọi vốn, VC, nhà đầu tư
- Tên dự án → dùng đúng tên user đã cho

### 7. Output Quality

- Tối thiểu 5000 words cho full business plan
- Tất cả analysis sections phải có TABLES markdown
- Sources section liệt kê TẤT CẢ URLs
- Viết tiếng Việt, thuật ngữ chuyên môn giữ tiếng Anh

## Supported Industries

```
tech_startup      → Startup Công Nghệ
trading_finance   → Trading & Tài Chính
fnb               → F&B (Nhà Hàng / Quán Cà Phê)
education         → Giáo Dục (Mầm Non)
tourism           → Du Lịch & Lữ Hành
ecommerce         → Thương Mại Điện Tử
export_import     → Xuất Nhập Khẩu
```

## Supported Markets

```
vietnam           → Thị Trường Việt Nam
international     → Thị Trường Quốc Tế
sea               → Đông Nam Á
```
