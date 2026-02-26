# Investment Analysis Framework
# Tham khảo: Corporate Finance (FTU/UEH), Investment Banking, VC Analysis

## Mô tả
Framework phân tích đầu tư chuyên sâu để xác định một dự án/startup có ĐÁNG ĐẦU TƯ hay không.
Kết hợp các chỉ số tài chính chuẩn MBA + VC/PE metrics.

## I. Financial Viability Metrics

### 1. Net Present Value (NPV)
- NPV = Σ [CFt / (1+r)^t] - Initial Investment
- NPV > 0 → Đáng đầu tư
- Discount rate: WACC hoặc required rate of return (thường 15-25% cho startup)
- Horizon: 3-5 năm

### 2. Internal Rate of Return (IRR)
- Rate tại đó NPV = 0
- IRR > WACC (hoặc hurdle rate) → Đáng đầu tư
- Startup target: IRR > 25-30%
- SME target: IRR > 15-20%

### 3. Return on Investment (ROI)
- ROI = (Net Profit / Total Investment) x 100%
- Timeline: Annual ROI
- Tech startup: Target >20%/năm sau Year 2
- Traditional: Target >15%/năm

### 4. Payback Period
- Thời gian thu hồi vốn đầu tư
- Startup: < 2-3 năm
- Traditional business: < 3-5 năm
- Discounted Payback Period (chính xác hơn)

### 5. Profitability Index (PI)
- PI = PV of Future Cash Flows / Initial Investment
- PI > 1 → Đáng đầu tư
- PI càng cao càng hiệu quả vốn

## II. Startup-Specific Metrics

### 6. Unit Economics
- **CAC** (Customer Acquisition Cost): Chi phí để có 1 khách hàng
- **LTV** (Lifetime Value): Giá trị trọn đời 1 khách hàng
- **LTV/CAC Ratio**: Target > 3:1
- **Payback on CAC**: < 12 tháng

### 7. Burn Rate & Runway
- Monthly Burn Rate = Monthly Expenses - Monthly Revenue
- Runway = Cash Balance / Monthly Burn Rate
- Target Runway: > 18 tháng trước next funding

### 8. MRR/ARR Growth
- MRR (Monthly Recurring Revenue)
- ARR = MRR x 12
- Growth Rate target: >15-20% MoM (early stage), >100% YoY

### 9. Gross Margin
- Gross Margin = (Revenue - COGS) / Revenue
- SaaS target: > 70-80%
- Marketplace: > 50-60%
- E-commerce: > 30-40%

## III. Risk Assessment

### 10. Sensitivity Analysis
- Best case / Base case / Worst case scenarios
- Key variables: Revenue growth, churn rate, pricing, CAC
- Monte Carlo simulation nếu cần

### 11. Break-Even Analysis
- Break-Even Point (units) = Fixed Costs / (Price - Variable Cost per unit)
- Break-Even Point (revenue) = Fixed Costs / Contribution Margin Ratio
- Thời gian đạt break-even

### 12. Risk-Adjusted Return
- Expected Value = Σ (Probability x Outcome)
- Sharpe Ratio concept: (Return - Risk-free rate) / Std Dev
- Scenario weighting: Optimistic 25%, Base 50%, Pessimistic 25%

## IV. Market Opportunity Scoring

### 13. TAM/SAM/SOM Validation
- TAM (Total Addressable Market): Toàn bộ thị trường
- SAM (Serviceable Available Market): Phần thị trường có thể phục vụ
- SOM (Serviceable Obtainable Market): Phần thực tế chiếm được
- SOM target: 1-5% of SAM trong 3 năm đầu

### 14. Market Growth Rate
- CAGR của ngành
- Growing market (>10% CAGR) preferred
- Decline market (<0%) = red flag

## V. Investment Decision Matrix

| Criteria | Weight | Score (1-10) | Weighted |
|---|---|---|---|
| NPV Positive | 15% | | |
| IRR > Hurdle Rate | 15% | | |
| Payback < Target | 10% | | |
| LTV/CAC > 3:1 | 10% | | |
| Gross Margin > Industry | 10% | | |
| Market Size (TAM) | 10% | | |
| Market Growth (CAGR) | 10% | | |
| Competitive Moat | 10% | | |
| Team/Execution Risk | 5% | | |
| Regulatory Risk | 5% | | |
| **Total** | **100%** | | |

**Decision Rules:**
- Score > 7.0 → **INVEST** (Strong opportunity)
- Score 5.0-7.0 → **CONDITIONAL** (Needs improvement in weak areas)
- Score < 5.0 → **PASS** (Too risky or unattractive)

## VI. Go/No-Go Checklist
- [ ] NPV > 0 với discount rate hợp lý?
- [ ] IRR > hurdle rate (15-25%)?
- [ ] Payback period chấp nhận được?
- [ ] Unit economics khả thi (LTV > 3x CAC)?
- [ ] Gross margin > industry benchmark?
- [ ] Market size đủ lớn (TAM > $100M)?
- [ ] Clear competitive advantage?
- [ ] Founder-market fit?
- [ ] Runway đủ (>18 tháng)?
- [ ] Exit strategy rõ ràng?
