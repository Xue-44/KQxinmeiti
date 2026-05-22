# 新媒体表格制作技能

## 技能定位
本技能用于生成新媒体运营相关的数据表格，支持平台数据汇总、内容排期、KPI追踪、竞品对比、月度运营数据表等多种场景。

## 支持场景
| 场景 | 说明 | 使用频率 |
|------|------|---------|
| 各平台数据汇总表 | 汇总抖音/小红书/视频号等各平台运营数据 | 每周 |
| 内容发布排期表 | 规划月度内容排期与状态追踪 | 每月 |
| KPI追踪表 | 追踪核心指标完成进度 | 持续 |
| 竞品数据对比表 | 多品牌新媒体表现横向对比 | 每月 |
| 月度运营数据表 | 月度完整运营数据汇总分析 | 每月 |

## 表格规范

### 表头样式
- 背景色: 品牌主色，白色加粗文字
- 行高: 不低于 25pt
- 对齐: 水平居中，垂直居中
- 字体: 微软雅黑 Bold，11pt

### 数据格式
- 数值: 千分位分隔，右对齐
- 百分比: 保留1位小数，如 "12.5%"
- 日期: YYYY-MM-DD 格式
- 文本: 左对齐，避免过长换行

### 条件格式
- 环比增长 > 10%: 绿色背景
- 环比下降 > 10%: 红色背景
- KPI完成率 > 100%: 绿色字体加粗
- KPI完成率 < 60%: 红色字体加粗

### 冻结窗格
- 首行（表头行）始终冻结
- 首列（指标名称）在数据较多时冻结

## 四品牌专用模板

### 1. 周报数据表结构
| 列: 平台 | 粉丝数 | 本周新增 | 发布量 | 曝光量 | 互动量 | 互动率 | 转化数 | 转化率 | 环比趋势 |

### 2. 月度汇总表结构
| 列: 平台 | 月初粉丝 | 月末粉丝 | 净增 | 总发布量 | 总曝光 | 总互动 | 平均互动率 | 总线索 | 线索成本 | KPI达成率 |

### 3. 活动效果评估表结构
| 列: 活动名称 | 活动时间 | 预算 | 实际花费 | 曝光量 | 互动量 | 线索数 | CPL | ROI | 目标达成率 |

## Python 代码模板 (openpyxl)

### 四品牌配色

```python
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side,
    numbers
)
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from datetime import datetime

BRAND_STYLES = {
    "trumpchi": {
        "header_fill": PatternFill(start_color="0052CC", end_color="0052CC", fill_type="solid"),
        "header_font": Font(name="微软雅黑", bold=True, color="FFFFFF", size=11),
        "alt_fill": PatternFill(start_color="E6F2FF", end_color="E6F2FF", fill_type="solid"),
        "name": "广汽传祺",
    },
    "audi": {
        "header_fill": PatternFill(start_color="000000", end_color="000000", fill_type="solid"),
        "header_font": Font(name="Arial", bold=True, color="FFFFFF", size=11),
        "alt_fill": PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid"),
        "name": "上汽奥迪",
    },
    "hyper": {
        "header_fill": PatternFill(start_color="6A0DAD", end_color="6A0DAD", fill_type="solid"),
        "header_font": Font(name="阿里巴巴普惠体", bold=True, color="FFFFFF", size=11),
        "alt_fill": PatternFill(start_color="F0E6FF", end_color="F0E6FF", fill_type="solid"),
        "name": "广汽昊铂",
    },
    "aion": {
        "header_fill": PatternFill(start_color="00A86B", end_color="00A86B", fill_type="solid"),
        "header_font": Font(name="微软雅黑", bold=True, color="FFFFFF", size=11),
        "alt_fill": PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid"),
        "name": "广汽埃安",
    },
}

# 通用边框
thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)
```

### 基础表格创建函数

```python
def create_styled_workbook(brand, sheet_name="数据表"):
    """创建带品牌样式的Workbook"""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    return wb, ws


def write_header(ws, brand, headers, row=1):
    """写入表头并应用品牌样式"""
    styles = BRAND_STYLES.get(brand, BRAND_STYLES["trumpchi"])
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col_idx, value=header)
        cell.fill = styles["header_fill"]
        cell.font = styles["header_font"]
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    ws.row_dimensions[row].height = 28


def write_data_rows(ws, brand, row_data_list, start_row=2):
    """写入数据行并应用交替背景色"""
    styles = BRAND_STYLES.get(brand, BRAND_STYLES["trumpchi"])
    for row_idx, row_data in enumerate(row_data_list):
        current_row = start_row + row_idx
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=current_row, column=col_idx, value=value)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if (row_idx + 1) % 2 == 1:
                cell.fill = styles["alt_fill"]


def apply_conditional_formatting(ws, brand, col_letter, start_row, end_row):
    """为百分比/环比列应用条件格式"""
    range_str = f"{col_letter}{start_row}:{col_letter}{end_row}"

    # 正值绿色
    ws.conditional_formatting.add(
        range_str,
        CellIsRule(operator="greaterThan", formula=["0"],
                  fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
                  font=Font(color="006100"))
    )
    # 负值红色
    ws.conditional_formatting.add(
        range_str,
        CellIsRule(operator="lessThan", formula=["0"],
                  fill=PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
                  font=Font(color="9C0006"))
    )


def freeze_panes(ws, cell="A2"):
    """冻结首行"""
    ws.freeze_panes = cell


def auto_width(ws, min_width=10, max_width=40):
    """自适应列宽"""
    for col in ws.columns:
        column = col[0].column_letter
        max_length = 0
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        adjusted = max(min(max_length + 4, max_width), min_width)
        ws.column_dimensions[column].width = adjusted
```

### 周报数据表完整示例

```python
def generate_weekly_data_table(brand, data, output_path):
    """生成新媒体周报数据表"""
    wb, ws = create_styled_workbook(brand, "周报数据")

    headers = [
        "平台", "粉丝数", "本周新增", "发布量",
        "曝光量", "互动量", "互动率", "转化数", "转化率", "环比趋势"
    ]
    write_header(ws, brand, headers)

    write_data_rows(ws, brand, data["platforms"])

    # 条件格式：环比趋势列 (第10列)
    last_row = len(data["platforms"]) + 1
    apply_conditional_formatting(ws, brand, "J", 2, last_row)

    freeze_panes(ws)
    auto_width(ws)

    wb.save(output_path)
    return output_path
```

### 内容排期表

```python
def generate_content_calendar(brand, schedule_data, output_path):
    """生成内容发布排期表"""
    wb, ws = create_styled_workbook(brand, "内容排期")

    headers = [
        "日期", "平台", "内容标题", "内容类型",
        "目标人群", "发布时间", "状态", "负责人", "备注"
    ]
    write_header(ws, brand, headers)

    write_data_rows(ws, brand, schedule_data["schedule"])

    # 状态列数据验证
    dv = DataValidation(type="list", formula1='"待发布,已发布,制作中,审核中"', allow_blank=True)
    status_col = get_column_letter(7)  # 状态列
    dv.add(f"{status_col}2:{status_col}{len(schedule_data['schedule']) + 1}")
    ws.add_data_validation(dv)

    freeze_panes(ws)
    auto_width(ws)

    wb.save(output_path)
    return output_path
```

### KPI追踪表

```python
def generate_kpi_tracker(brand, kpi_data, output_path):
    """生成KPI追踪表"""
    wb, ws = create_styled_workbook(brand, "KPI追踪")

    headers = [
        "指标", "年度目标", "本月目标", "当前完成",
        "完成率", "剩余", "日均需完成", "趋势", "状态"
    ]
    write_header(ws, brand, headers)

    write_data_rows(ws, brand, kpi_data["metrics"])

    last_row = len(kpi_data["metrics"]) + 1

    # 完成率列条件格式
    completion_col = get_column_letter(5)
    ws.conditional_formatting.add(
        f"{completion_col}2:{completion_col}{last_row}",
        CellIsRule(operator="greaterThan", formula=["1"],
                  fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
                  font=Font(bold=True, color="006100"))
    )
    ws.conditional_formatting.add(
        f"{completion_col}2:{completion_col}{last_row}",
        CellIsRule(operator="lessThan", formula=["0.6"],
                  fill=PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
                  font=Font(bold=True, color="9C0006"))
    )

    freeze_panes(ws)
    auto_width(ws)

    wb.save(output_path)
    return output_path
```

### 竞品数据对比表

```python
def generate_competitor_comparison(brand, comp_data, output_path):
    """生成竞品数据对比表"""
    wb, ws = create_styled_workbook(brand, "竞品对比")

    headers = [
        "品牌", "平台", "粉丝数", "月发布量",
        "月曝光量", "月互动量", "互动率", "月线索数",
        "预估投放费用", "综合评分"
    ]
    write_header(ws, brand, headers)

    write_data_rows(ws, brand, comp_data["competitors"])

    # 综合评分列 (第10列) 条件格式
    last_row = len(comp_data["competitors"]) + 1
    score_col = get_column_letter(10)
    ws.conditional_formatting.add(
        f"{score_col}2:{score_col}{last_row}",
        CellIsRule(operator="greaterThan", formula=["80"],
                  fill=PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"))
    )

    freeze_panes(ws)
    auto_width(ws)

    wb.save(output_path)
    return output_path
```

## 表格质量标准检查清单

### 数据准确性
- [ ] 所有数据可追溯到原始来源
- [ ] 公式计算无误，无循环引用
- [ ] 数据格式统一（日期/数字/百分比）

### 可读性
- [ ] 表头清晰，冻结窗格
- [ ] 列宽自适应，无截断内容
- [ ] 条件格式正确标识异常值

### 专业性
- [ ] 品牌配色一致
- [ ] 字体统一，层级分明
- [ ] 打印设置合理（页边距/页眉页脚）

## 使用方式

在 Agent 指令中调用：

```
使用 spreadsheet-generation 技能为 [品牌] 生成 [类型] 表格:
- 品牌: trumpchi / audi / hyper / aion
- 类型: weekly / monthly / calendar / kpi / competitor
- 数据: [提供具体数据]

生成脚本参考 scripts/make_excel.py
```
