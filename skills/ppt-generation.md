# 新媒体PPT制作技能

## 技能定位
本技能用于生成新媒体运营相关的演示文稿，支持周报/月报、数据复盘、内容策略、竞品分析、活动方案等多种场景。

## 支持场景
| 场景 | 典型内容 | 使用频率 |
|------|---------|---------|
| 周报/月报PPT | 新媒体运营数据汇报 | 每周/月 |
| 数据复盘PPT | 活动效果、内容表现复盘 | 活动结束后 |
| 内容策略PPT | 月度/季度内容规划 | 每月/季度 |
| 竞品分析PPT | 竞品新媒体表现分析 | 每月 |
| 活动方案PPT | 线上/线下活动策划方案 | 按需 |

## 四品牌PPT模板规范

### 1. 广汽传祺 (Trumpchi)
- **主色调**: #0052CC (科技蓝) + #FFFFFF (白)
- **辅助色**: #E6F2FF (浅蓝) + #003D99 (深蓝)
- **字体**: 思源黑体 CN Medium (标题), 思源黑体 CN Regular (正文)
- **视觉风格**: 科技感、品质感、现代简约
- **适用场景**: 技术发布会、产品介绍、品牌升级

### 2. 上汽奥迪 (Audi)
- **主色调**: #000000 (纯黑) + #C0C0C0 (银灰)
- **辅助色**: #FFD700 (金色点缀) + #333333 (深灰)
- **字体**: Arial Black (标题), Arial (正文)
- **视觉风格**: 高端豪华、商务精英、简约大气
- **适用场景**: 高端车型发布、品牌形象展示、商务汇报

### 3. 广汽昊铂 (Hyper)
- **主色调**: #6A0DAD (深紫) + #FFD700 (金色)
- **辅助色**: #F0E6FF (浅紫) + #B38BFF (中紫)
- **字体**: 阿里巴巴普惠体 Bold (标题), Regular (正文)
- **视觉风格**: 新能源科技、未来感、年轻活力
- **适用场景**: 新能源技术发布、年轻化营销、创新活动

### 4. 广汽埃安 (Aion)
- **主色调**: #00A86B (环保绿) + #FFFFFF (白)
- **辅助色**: #E8F5E9 (浅绿) + #007A5E (深绿)
- **字体**: 微软雅黑 Bold (标题), Regular (正文)
- **视觉风格**: 科技环保、智能出行、清新自然
- **适用场景**: 环保理念宣传、智能科技展示、用户活动

## 标准幻灯片结构模板

### 1. 封面页
- 品牌Logo + 主标题 + 副标题
- 报告日期 + 汇报人 / 部门
- 品牌专属背景设计

### 2. 目录页
- 报告结构概览 (3-5 个主要部分)
- 页码标注
- 品牌色系装饰元素

### 3. 核心数据页
- 关键指标展示 (表格 / 图表)
- 数据趋势分析
- 核心结论提炼

### 4. 分析页
- SWOT 分析 / 竞品对比
- 问题诊断 / 机会识别
- 数据支撑的深度分析

### 5. 策略页
- 行动方案 / 实施路径
- 时间节点 / 责任分工
- 预期效果 / 风险控制

### 6. 总结页
- 核心观点重申
- 下一步行动计划
- Q&A / 联系方式

## PPT 质量标准检查清单

### 内容质量
- [ ] 标题清晰，能准确概括页面内容
- [ ] 数据准确，来源可靠
- [ ] 逻辑连贯，前后呼应
- [ ] 结论明确，建议可行

### 视觉设计
- [ ] 品牌配色一致，不超过 3 种主色
- [ ] 字体统一，标题正文区分明显
- [ ] 图文比例协调，避免文字过密
- [ ] 图表清晰，数据可视化效果好

### 技术规范
- [ ] 文件大小控制在 50MB 以内
- [ ] 兼容 Office 2016 及以上版本
- [ ] 所有图片已压缩优化
- [ ] 超链接、动画效果正常

## Python 代码模板 (python-pptx)

### 品牌配色方案定义

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime

# 四品牌主色调
BRAND_COLORS = {
    "trumpchi": {
        "primary": RGBColor(0, 82, 204),
        "secondary": RGBColor(230, 242, 255),
        "accent": RGBColor(0, 61, 153),
        "name": "广汽传祺",
    },
    "audi": {
        "primary": RGBColor(0, 0, 0),
        "secondary": RGBColor(192, 192, 192),
        "accent": RGBColor(255, 215, 0),
        "name": "上汽奥迪",
    },
    "hyper": {
        "primary": RGBColor(106, 13, 173),
        "secondary": RGBColor(240, 230, 255),
        "accent": RGBColor(255, 215, 0),
        "name": "广汽昊铂",
    },
    "aion": {
        "primary": RGBColor(0, 168, 107),
        "secondary": RGBColor(232, 245, 233),
        "accent": RGBColor(0, 122, 94),
        "name": "广汽埃安",
    },
}
```

### 封面页生成

```python
def create_cover_page(prs, brand, title, subtitle, date=None, presenter=None):
    """创建封面页"""
    colors = BRAND_COLORS.get(brand, BRAND_COLORS["trumpchi"])
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白版式

    # 品牌色顶部装饰条
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(10), Inches(0.15)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = colors["primary"]
    shape.line.fill.background()

    # 主标题
    title_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(2.0), Inches(8.4), Inches(1.2)
    )
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = colors["primary"]
    p.alignment = PP_ALIGN.LEFT

    # 副标题
    sub_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(3.3), Inches(8.4), Inches(0.8)
    )
    tf = sub_box.text_frame
    p = tf.add_paragraph()
    p.text = subtitle
    p.font.size = Pt(24)
    p.font.color.rgb = colors["accent"]
    p.alignment = PP_ALIGN.LEFT

    # 日期和汇报人
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    footer_text = f"报告日期: {date}"
    if presenter:
        footer_text += f"  |  汇报人: {presenter}"

    footer_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(5.8), Inches(8.4), Inches(0.4)
    )
    tf = footer_box.text_frame
    p = tf.add_paragraph()
    p.text = footer_text
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(128, 128, 128)
    p.alignment = PP_ALIGN.LEFT
```

### 数据表格页生成

```python
def create_table_slide(prs, brand, title, headers, rows_data):
    """创建数据表格页"""
    colors = BRAND_COLORS.get(brand, BRAND_COLORS["trumpchi"])
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 标题
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(9), Inches(0.6)
    )
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = colors["primary"]

    # 表格
    num_rows = len(rows_data) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(0.5), Inches(1.2),
        Inches(9), Inches(0.45) * num_rows
    )
    table = table_shape.table

    # 表头
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = colors["primary"]
        for p in cell.text_frame.paragraphs:
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.bold = True
            p.font.size = Pt(11)
            p.alignment = PP_ALIGN.CENTER

    # 数据行
    for row_idx, row_data in enumerate(rows_data, 1):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(cell_text)
            if row_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = colors["secondary"]
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.alignment = PP_ALIGN.CENTER
```

### 策略页生成

```python
def create_strategy_slide(prs, brand, title, strategies):
    """创建策略行动页
    strategies: [{"action": "行动", "owner": "负责人", "timeline": "时间", "kpi": "指标"}, ...]
    """
    headers = ["行动方案", "负责人", "时间节点", "KPI 指标"]
    rows_data = [
        [s.get("action", ""), s.get("owner", ""),
         s.get("timeline", ""), s.get("kpi", "")]
        for s in strategies
    ]
    create_table_slide(prs, brand, title, headers, rows_data)
```

### 总结页生成

```python
def create_summary_slide(prs, brand, title, key_points, next_steps):
    """创建总结页"""
    colors = BRAND_COLORS.get(brand, BRAND_COLORS["trumpchi"])
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 标题
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(9), Inches(0.6)
    )
    tf = title_box.text_frame
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = colors["primary"]

    # 核心观点
    content_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.2), Inches(4.2), Inches(4.5)
    )
    tf = content_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = "核心观点"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = colors["primary"]

    for point in key_points:
        p = tf.add_paragraph()
        p.text = f"  {chr(9679)} {point}"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(8)

    # 下一步行动
    action_box = slide.shapes.add_textbox(
        Inches(5.2), Inches(1.2), Inches(4.3), Inches(4.5)
    )
    tf = action_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = "下一步行动"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = colors["primary"]

    for idx, step in enumerate(next_steps, 1):
        p = tf.add_paragraph()
        p.text = f"  {idx}. {step}"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(8)
```

### 完整示例：生成周报PPT

```python
def generate_weekly_report(brand, data, output_path):
    """生成完整的新媒体周报PPT"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    colors = BRAND_COLORS.get(brand, BRAND_COLORS["trumpchi"])
    brand_name = colors["name"]

    # 1. 封面
    create_cover_page(
        prs, brand,
        title=f"{brand_name}新媒体运营周报",
        subtitle=data.get("subtitle", "每周数据复盘与策略优化"),
        date=data.get("date"),
        presenter=data.get("presenter"),
    )

    # 2. 核心数据
    create_table_slide(
        prs, brand,
        "本周核心数据概览",
        ["指标", "本周", "上周", "环比"],
        data.get("metrics", [])
    )

    # 3. 平台分析
    create_table_slide(
        prs, brand,
        "各平台运营数据",
        ["平台", "粉丝数", "发布量", "互动量", "转化数"],
        data.get("platform_data", [])
    )

    # 4. 内容分析
    create_table_slide(
        prs, brand,
        "热门内容 TOP5",
        ["排名", "标题", "阅读量", "互动率", "类型"],
        data.get("top_content", [])
    )

    # 5. 策略行动
    create_strategy_slide(
        prs, brand,
        "下周运营策略与行动计划",
        data.get("strategies", [])
    )

    # 6. 总结
    create_summary_slide(
        prs, brand,
        "总结与展望",
        data.get("key_points", []),
        data.get("next_steps", []),
    )

    prs.save(output_path)
    return output_path
```

## 使用方式

在 Agent 指令中调用：

```
使用 ppt-generation 技能为 [品牌] 生成一份 [类型] PPT:
- 品牌: trumpchi / audi / hyper / aion
- 类型: weekly / monthly / analysis / strategy / activity
- 数据: [提供具体数据]

生成脚本参考 scripts/make_ppt.py
```
