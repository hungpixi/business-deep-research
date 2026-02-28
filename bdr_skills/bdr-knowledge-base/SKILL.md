---
name: bdr-knowledge-base
description: Hướng dẫn AI cách sử dụng 12+ MBA framework files trong knowledge base
---

# BDR Knowledge Base Skill

## Khi nào skill này được kích hoạt?

Khi AI cần áp dụng MBA frameworks trong phân tích kinh doanh.

## Knowledge Base Location

Sau khi cài BDR Kit, knowledge base nằm ở:
- Global: `~/.bdr/knowledge/`
- Workspace: `./knowledge/`

## Cấu trúc

```
knowledge/
├── frameworks/          # 14 MBA framework templates
│   ├── lean_canvas.md
│   ├── business_model_canvas.md
│   ├── tam_sam_som.md
│   ├── swot_tows.md
│   ├── competitive_analysis.md
│   ├── porters_five_forces.md
│   ├── blue_ocean.md
│   ├── financial_projections.md
│   ├── investment_analysis.md
│   ├── ansoff_matrix.md
│   ├── bcg_matrix.md
│   ├── value_chain.md
│   ├── pestel.md
│   └── moat_strategy.md
├── industries/          # Industry-specific knowledge
│   └── [industry].md
└── markets/             # Market-specific knowledge
    ├── vietnam.md
    ├── sea.md
    └── international.md
```

## Cách sử dụng Frameworks

### Nguyên tắc

1. **Đọc framework file TRƯỚC khi phân tích** — mỗi file có template chuẩn
2. **Chọn frameworks phù hợp với ngành** (xem bảng mapping bên dưới)
3. **Điền ĐÚNG format** theo template trong file
4. **KHÔNG bỏ trống** bất kỳ section nào trong template

### Industry → Frameworks Mapping

| Ngành | Frameworks áp dụng |
|---|---|
| tech_startup | lean_canvas, business_model_canvas, tam_sam_som, swot_tows, competitive_analysis, porters_five_forces, blue_ocean, financial_projections, investment_analysis |
| trading_finance | swot_tows, porters_five_forces, financial_projections, investment_analysis, pestel, competitive_analysis |
| fnb | business_model_canvas, swot_tows, porters_five_forces, pestel, value_chain, financial_projections, investment_analysis |
| education | business_model_canvas, swot_tows, pestel, tam_sam_som, financial_projections, investment_analysis |
| tourism | business_model_canvas, swot_tows, pestel, porters_five_forces, value_chain, ansoff_matrix, financial_projections, investment_analysis |
| ecommerce | lean_canvas, business_model_canvas, tam_sam_som, swot_tows, competitive_analysis, financial_projections, investment_analysis |
| export_import | business_model_canvas, swot_tows, pestel, porters_five_forces, value_chain, financial_projections, investment_analysis |

### Editable Knowledge

User có thể **chỉnh sửa trực tiếp** các framework .md files:
- Thay đổi template → thay đổi cách AI phân tích
- Thêm industry/market files → mở rộng kiến thức
- Web UI có tab Knowledge Base để edit real-time

## Market Knowledge

### vietnam.md
- Thông tin thị trường Việt Nam cập nhật
- Chính sách, quy định pháp lý
- Đặc thù tiêu dùng

### sea.md
- Thông tin Đông Nam Á
- So sánh cross-market

### international.md
- Benchmark quốc tế
- Best practices global
