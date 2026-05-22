# 图片仿作技能 (Image Imitation)

## 定位

基于参考图片，提取其风格特征（配色、构图、字体、元素），生成同风格但内容不同的新图片。支持海报仿作、活动照片仿作、设计素材仿作，并适配四品牌差异化风格。

---

## 1. 仿作类型

### 1.1 海报仿作

**输入**：参考海报图片 + 新文案内容 + 目标品牌

**仿作要素**：
| 要素 | 提取方式 | 应用方式 |
|------|---------|---------|
| 配色方案 | K-Means提取主色调和配色比例 | 替换为品牌色系，保持色调关系 |
| 构图结构 | 检测文字/图片区域分割 | 保持版式，替换内容 |
| 字体风格 | 识别粗/细/衬线/无衬线 | 替换为品牌字体 |
| 视觉元素 | 提取装饰图形位置 | 替换为品牌元素 |
| 文字层级 | 识别标题/副标题/正文大小 | 保持层级，替换文案 |

### 1.2 活动照片仿作

**输入**：活动照片 + 目标车型 + 目标品牌

**仿作要素**：
- 场景氛围（灯光色调、场地风格）
- 拍摄角度（前45度、正侧、内饰特写）
- 构图方式（三分法、对称、引导线）
- 后期风格（冷暖调、对比度、饱和度）
- 人物姿态（站姿、手势、互动方式）

### 1.3 设计素材仿作

**输入**：参考设计素材 + 用途描述

**仿作要素**：
- 图形风格（扁平/渐变/3D/手绘/线框）
- 纹理质感（磨砂/金属/玻璃/纸质）
- 图标体系（线性/面性/双色/多彩）
- 装饰元素（光效、粒子、波纹、网格）

---

## 2. 四品牌风格适配

### 2.1 广汽传祺 — 科技+品质

```python
TRUMPCHI_STYLE = {
    "primary_color": "#0066CC",      # 科技蓝
    "secondary_color": "#C0C0C0",    # 品质银
    "accent_color": "#FF6600",       # 活力橙
    "bg_gradient": ["#0066CC", "#003366"],  # 蓝色渐变
    "font_family": "思源黑体, Microsoft YaHei",
    "decorative_elements": ["钻石切割纹", "几何线条", "光晕"],
    "tone": "稳重中带科技感",
    "keywords": ["品质", "科技", "可靠", "家用"],
}
```

### 2.2 上汽奥迪 — 豪华+质感

```python
AUDI_STYLE = {
    "primary_color": "#000000",      # 豪华黑
    "secondary_color": "#D4AF37",    # 金属金
    "accent_color": "#CC0000",       # 运动红
    "bg_gradient": ["#1A1A1A", "#000000"],  # 暗黑渐变
    "font_family": "Arial, 思源黑体",
    "decorative_elements": ["四环纹样", "菱形格", "金属拉丝"],
    "tone": "低调奢华",
    "keywords": ["豪华", "性能", "尊贵", "品质"],
}
```

### 2.3 广汽昊铂 — 高端+科技

```python
HYPER_STYLE = {
    "primary_color": "#8A2BE2",      # 高端紫
    "secondary_color": "#FFD700",    # 科技金
    "accent_color": "#00FFFF",       # 电光青
    "bg_gradient": ["#1A0033", "#0D0020", "#2A004D"],
    "font_family": "Futura, 思源黑体",
    "decorative_elements": ["极光光效", "粒子流", "赛博网格"],
    "tone": "未来科技感",
    "keywords": ["智能", "极致", "未来", "先锋"],
}
```

### 2.4 广汽埃安 — 环保+年轻

```python
AION_STYLE = {
    "primary_color": "#00B050",      # 环保绿
    "secondary_color": "#FFFFFF",    # 科技白
    "accent_color": "#00D4FF",       # 天空蓝
    "bg_gradient": ["#00B050", "#006633"],  # 绿色渐变
    "font_family": "PingFang SC, 思源黑体",
    "decorative_elements": ["叶片纹样", "充电波", "圆润几何"],
    "tone": "清新活力",
    "keywords": ["环保", "智能", "年轻", "出行"],
}
```

---

## 3. 仿作流程

```
参考图片 → 风格提取 → 品牌映射 → 元素替换 → 合成输出
   │            │           │           │           │
   │        配色分析    品牌VI映射   文案替换     质量检查
   │        构图分析    字体映射     元素替换     尺寸规范
   │        元素识别    装饰映射     Logo嵌入     色彩检查
```

---

## 4. 代码示例

### 4.1 风格提取器

```python
from PIL import Image, ImageStat, ImageFilter
import numpy as np
import cv2
from collections import Counter


def extract_style_from_reference(image_path: str) -> dict:
    """
    从参考图片中提取风格特征
    返回配色、构图、亮度等信息
    """
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.open(image_path)
    height, width = img_rgb.shape[:2]

    style = {
        "image_size": f"{width}x{height}",
        "aspect_ratio": round(width / height, 2),
    }

    # --- 配色提取 ---
    pixels = img_rgb.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, 6, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    centers = centers.astype(np.uint8)
    unique, counts = np.unique(labels, return_counts=True)
    sorted_idx = np.argsort(counts)[::-1]

    palette = []
    for idx in sorted_idx[:5]:
        color = tuple(centers[idx].tolist())
        hex_color = "#{:02X}{:02X}{:02X}".format(*color)
        ratio = round(counts[idx] / len(labels), 3)
        palette.append({"hex": hex_color, "rgb": color, "ratio": ratio})

    style["color_palette"] = palette
    style["dominant_color"] = palette[0]["hex"]

    # --- 亮度与对比度 ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    style["mean_brightness"] = round(np.mean(gray), 1)
    style["contrast"] = round(np.std(gray), 1)

    # --- 饱和度和色调 ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    style["mean_saturation"] = round(np.mean(hsv[:, :, 1]), 1)
    hue_mean = np.mean(hsv[:, :, 0])
    if hue_mean < 30 or hue_mean > 150:
        style["color_temperature"] = "暖色调"
    elif 80 < hue_mean < 130:
        style["color_temperature"] = "冷色调"
    else:
        style["color_temperature"] = "中性调"

    # --- 构图检测 ---
    # 检测三分线位置
    style["composition"] = detect_composition(img_rgb)

    # --- 文字区域检测 ---
    mser = cv2.MSER_create()
    text_regions, _ = mser.detectRegions(gray)
    text_areas = []
    for region in text_regions:
        x, y, w, h = cv2.boundingRect(region)
        if w > 30 and h > 15:
            zone = "top" if y < height / 3 else ("center" if y < 2 * height / 3 else "bottom")
            text_areas.append({
                "position": f"({x}, {y})", "size": f"{w}x{h}",
                "zone": zone, "area": w * h
            })
    text_areas.sort(key=lambda t: t["area"], reverse=True)
    style["text_regions"] = text_areas[:5]

    # --- 边缘复杂度 ---
    edges = cv2.Canny(gray, 50, 150)
    style["edge_density"] = round(np.sum(edges > 0) / (height * width), 4)

    return style


def detect_composition(img_rgb: np.ndarray) -> str:
    """检测图片构图方式"""
    h, w = img_rgb.shape[:2]
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    # 简化版：基于边缘分布判断
    edges = cv2.Canny(gray, 50, 150)

    left_third = np.sum(edges[:, :w//3] > 0)
    center_third = np.sum(edges[:, w//3:2*w//3] > 0)
    right_third = np.sum(edges[:, 2*w//3:] > 0)

    total = left_third + center_third + right_third
    if total == 0:
        return "均匀分布"

    left_ratio = left_third / total
    center_ratio = center_third / total

    if center_ratio > 0.5:
        return "中心构图"
    elif abs(left_ratio - (1 - left_ratio)) < 0.15:
        return "对称构图"
    elif left_ratio < 0.35:
        return "右重构图（三分法）"
    else:
        return "左重构图（三分法）"
```

### 4.2 品牌风格应用器

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


def apply_brand_style(
    base_image_path: str,
    brand: str,
    output_path: str = None,
    overlay_text: str = None,
    text_position: str = "bottom",
) -> str:
    """
    将参考图片的风格映射为指定品牌风格

    参数:
        base_image_path: 参考图路径
        brand: 目标品牌 (trumpchi / audi / hyper / aion)
        output_path: 输出路径
        overlay_text: 叠加的文案
        text_position: 文案位置 (top / center / bottom)
    """
    brand_styles = {
        "trumpchi": {
            "primary": "#0066CC", "secondary": "#C0C0C0",
            "gradient_start": (0, 102, 204), "gradient_end": (0, 51, 102),
            "name": "广汽传祺",
        },
        "audi": {
            "primary": "#000000", "secondary": "#D4AF37",
            "gradient_start": (26, 26, 26), "gradient_end": (0, 0, 0),
            "name": "上汽奥迪",
        },
        "hyper": {
            "primary": "#8A2BE2", "secondary": "#FFD700",
            "gradient_start": (26, 0, 51), "gradient_end": (42, 0, 77),
            "name": "广汽昊铂",
        },
        "aion": {
            "primary": "#00B050", "secondary": "#FFFFFF",
            "gradient_start": (0, 176, 80), "gradient_end": (0, 102, 51),
            "name": "广汽埃安",
        },
    }

    brand = brand.lower()
    if brand not in brand_styles:
        raise ValueError(f"不支持的品牌: {brand}。可选: {list(brand_styles.keys())}")

    style = brand_styles[brand]
    img = Image.open(base_image_path).convert("RGBA")
    w, h = img.size

    # 1. 创建品牌色渐变叠加层
    gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        ratio = y / h
        r = int(style["gradient_start"][0] * (1 - ratio) + style["gradient_end"][0] * ratio)
        g = int(style["gradient_start"][1] * (1 - ratio) + style["gradient_end"][1] * ratio)
        b = int(style["gradient_start"][2] * (1 - ratio) + style["gradient_end"][2] * ratio)
        for x in range(w):
            gradient.putpixel((x, y), (r, g, b, 40))  # 40为透明度

    # 2. 合成渐变色
    img = Image.alpha_composite(img, gradient)

    # 3. 添加品牌色边框
    draw = ImageDraw.Draw(img)
    border_width = 4
    border_color = style["primary"]
    draw.rectangle([0, 0, w - 1, h - 1], outline=border_color, width=border_width)

    # 4. 叠加文案（如果提供）
    if overlay_text:
        try:
            font_size = min(w // 15, 80)
            font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", font_size)
        except OSError:
            font = ImageFont.load_default()

        # 文字阴影
        shadow_draw = ImageDraw.Draw(img)
        text_bbox = draw.textbbox((0, 0), overlay_text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

        if text_position == "bottom":
            text_y = h - text_h - 60
        elif text_position == "top":
            text_y = 40
        else:
            text_y = (h - text_h) // 2
        text_x = (w - text_w) // 2

        # 文字底色条
        bar_padding = 20
        draw.rectangle(
            [text_x - bar_padding, text_y - bar_padding // 2,
             text_x + text_w + bar_padding, text_y + text_h + bar_padding // 2],
            fill=(0, 0, 0, 160)
        )
        # 品牌色底线
        draw.line(
            [text_x - bar_padding, text_y + text_h + bar_padding // 2,
             text_x + text_w + bar_padding, text_y + text_h + bar_padding // 2],
            fill=style["primary"], width=3
        )
        # 绘制文字
        draw.text((text_x, text_y), overlay_text, fill=style["secondary"], font=font)

    # 5. 保存
    output = output_path or base_image_path.replace(".", f"_{brand}.")
    img = img.convert("RGB")
    img.save(output, quality=95)
    return output


def create_branded_thumbnail(
    image_path: str, brand: str, title: str, output_path: str
) -> str:
    """
    为图片创建带品牌标识的缩略图/封面
    适用于社交媒体封面、视频封面等
    """
    style_configs = {
        "trumpchi": {"primary": "#0066CC", "accent": "#FF6600", "logo_text": "GAC"},
        "audi": {"primary": "#D4AF37", "accent": "#CC0000", "logo_text": "OOOO"},
        "hyper": {"primary": "#8A2BE2", "accent": "#FFD700", "logo_text": "HYPER"},
        "aion": {"primary": "#00B050", "accent": "#FFFFFF", "logo_text": "AION"},
    }

    brand = brand.lower()
    config = style_configs[brand]

    img = Image.open(image_path).convert("RGBA")
    target_w, target_h = 1080, 1920  # 竖版封面

    # 裁剪填充
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if img_ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)

    # 底部渐变遮罩
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    for y in range(target_h // 2, target_h):
        alpha = int(200 * (y - target_h // 2) / (target_h // 2))
        draw_overlay.rectangle([0, y, target_w, y + 1], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, overlay)

    # 标题文字
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
        font_brand = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 36)
    except OSError:
        font_title = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # 标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((target_w - title_w) // 2, target_h - 300), title,
              fill=config["accent"], font=font_title)

    # 品牌标识
    brand_bbox = draw.textbbox((0, 0), config["logo_text"], font=font_brand)
    brand_w = brand_bbox[2] - brand_bbox[0]
    draw.text(((target_w - brand_w) // 2, target_h - 200), config["logo_text"],
              fill=config["primary"], font=font_brand)

    img = img.convert("RGB")
    img.save(output_path, quality=95)
    return output_path
```

### 4.3 批量仿作流水线

```python
def batch_imitation(
    reference_paths: list,
    brand: str,
    output_dir: str,
    texts: list = None,
) -> list:
    """
    批量仿作：输入多张参考图，统一应用品牌风格

    参数:
        reference_paths: 参考图片路径列表
        brand: 目标品牌
        output_dir: 输出目录
        texts: 对应每张图的文案（可选）
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i, ref_path in enumerate(reference_paths):
        # 提取参考风格
        ref_style = extract_style_from_reference(ref_path)

        # 应用品牌风格
        text = texts[i] if texts and i < len(texts) else None
        output_name = f"imitation_{brand}_{i+1:03d}.jpg"
        output_path = os.path.join(output_dir, output_name)

        output = apply_brand_style(ref_path, brand, output_path, text)

        results.append({
            "reference": ref_path,
            "reference_style": ref_style,
            "output": output,
            "brand": brand,
        })

    return results
```

---

## 5. 使用说明

1. **单图仿作**：`apply_brand_style("参考图.jpg", "trumpchi", "输出.jpg", "春季促销")`
2. **封面生成**：`create_branded_thumbnail("车图.jpg", "audi", "全新A7L上市", "封面.jpg")`
3. **批量仿作**：`batch_imitation(["ref1.jpg", "ref2.jpg"], "aion", "./output/", ["文案1", "文案2"])`