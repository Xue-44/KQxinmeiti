# 图片识别技能 (Image Recognition)

## 定位

汽车行业图片智能识别与分析，支持车辆、活动、设计、数据图表四大类图片的自动化识别与信息提取。

---

## 1. 车辆识别

### 1.1 识别维度

| 维度 | 识别内容 | 输出格式 |
|------|---------|---------|
| 品牌 | 广汽传祺 / 上汽奥迪 / 广汽昊铂 / 广汽埃安 | 品牌名 |
| 车型 | 具体车型名称（如传祺GS8、奥迪A7L、昊铂GT、埃安Y Plus） | 车型名 |
| 颜色 | 车身主色调 + 配色方案 | 颜色描述 |
| 角度 | 前45°/正前/正侧/后45°/正后/内饰 | 拍摄角度 |
| 场景 | 城市/自然/展厅/赛道/夜间 | 场景分类 |

### 1.2 四品牌车型特征库

#### 广汽传祺
- **家族特征**：凌云翼前脸、贯穿式尾灯、悬浮式车顶
- **代表车型**：GS8（大型SUV）、M8（MPV）、影豹（轿车）、GS4（紧凑SUV）
- **辨识要点**：大面积镀铬中网、"G"字形日行灯

#### 上汽奥迪
- **家族特征**：六边形大嘴格栅、矩阵式LED大灯、无框车门（部分车型）
- **代表车型**：A7L（轿跑）、Q5 e-tron（电动SUV）、Q6（大型SUV）
- **辨识要点**：四环logo位置、贯穿式OLED尾灯

#### 广汽昊铂
- **家族特征**：封闭式前脸、剪刀门/鸥翼门（GT）、流线型车身
- **代表车型**：昊铂GT、昊铂SSR、昊铂HT
- **辨识要点**：低趴姿态、前后灯组设计语言

#### 广汽埃安
- **家族特征**："人机共生美学"设计、贯穿式日行灯、隐藏式门把手
- **代表车型**：AION Y Plus、AION S、AION V、AION LX
- **辨识要点**："7"字形大灯、车身颜色双拼方案

---

## 2. 活动识别

### 2.1 活动类型分类

| 活动类型 | 视觉特征 | 典型场景 |
|---------|---------|---------|
| 新车发布会 | 舞台、灯光、幕布、展车 | 大型场馆、户外发布会 |
| 试驾活动 | 车队、路线标识、体验区 | 赛道、公路、越野场地 |
| 车展 | 展台、人群、宣传物料 | 国际车展、地方车展 |
| 品牌体验日 | 互动装置、科技展示、茶歇区 | 展厅、体验中心 |
| 促销活动 | 价格牌、礼品堆、红地毯 | 4S店、商场中庭 |
| 车主活动 | 车队巡游、聚餐、合影 | 户外、餐厅 |

### 2.2 活动关键信息提取

从活动图片中提取以下信息：
- 活动名称 / 主题
- 活动时间（从物料日期推断）
- 参与品牌及车型
- 活动规模预估（根据场地和人数）
- 物料质量评估

---

## 3. 设计识别

### 3.1 设计类型识别

| 设计类型 | 尺寸特征 | 用途 |
|---------|---------|------|
| 海报 | 1080×1920 或 A3/A4 比例 | 线上传播、店内展示 |
| Banner | 超宽比例 (1920×600 等) | 网页、小程序 |
| 信息流广告 | 多种尺寸 | 抖音、朋友圈、头条 |
| 长图 | 超高比例 | 微信公众号 |
| 宣传册 | 多页PDF | 线下发放 |
| 展架/易拉宝 | 80×200cm 等比例 | 活动现场 |

### 3.2 设计风格识别

- **科技感**：蓝色调、渐变光影、网格线、芯片纹样
- **豪华感**：黑金配色、大理石纹理、极简留白
- **年轻感**：高饱和度、撞色设计、动感线条
- **环保感**：绿色系、自然元素、叶片纹样

### 3.3 品牌设计元素检测

识别图片中是否包含以下品牌元素：
- **传祺**：科技蓝色块、"GAC"标识、钻石切割纹
- **奥迪**：四环logo、金属质感、菱形格纹、红色S-line标识
- **昊铂**：Hyper标识、紫色渐变、极光色块
- **埃安**：AION字标、绿色科技元素、未来感线条

---

## 4. 数据图表识别

### 4.1 图表类型

- 销量趋势图（折线图）
- 市场份额饼图
- 车型对比柱状图
- 用户画像雷达图
- 竞品分析矩阵图
- 满意度热力图

### 4.2 数据提取要点

- 图表标题
- 坐标轴标签
- 数据系列名称
- 关键数据点数值
- 数据时间范围
- 数据来源标注

---

## 5. 代码示例

### 5.1 OpenCV 车辆检测示例

```python
import cv2
import numpy as np
from PIL import Image

def detect_vehicle_brand(image_path: str) -> dict:
    """
    识别汽车图片中的品牌信息
    返回：品牌、颜色、场景等分析结果
    """
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "无法读取图片"}

    # 转换为RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width = img_rgb.shape[:2]

    result = {
        "image_size": f"{width}x{height}",
        "aspect_ratio": round(width / height, 2),
    }

    # 1. 主色调提取（K-Means聚类）
    pixels = img_rgb.reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    centers = centers.astype(np.uint8)

    # 按占比排序
    unique, counts = np.unique(labels, return_counts=True)
    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = []
    color_names = {
        (0, 0, 0): "黑色", (255, 255, 255): "白色",
        (255, 0, 0): "红色", (0, 0, 255): "蓝色",
        (0, 255, 0): "绿色", (128, 128, 128): "灰色",
        (192, 192, 192): "银色", (255, 215, 0): "金色",
    }
    for idx in sorted_indices[:3]:
        color = tuple(centers[idx].tolist())
        ratio = counts[idx] / len(labels)
        name = color_names.get(color, f"RGB{color}")
        dominant_colors.append({"color": f"RGB{color}", "name": name, "ratio": round(ratio, 2)})

    result["dominant_colors"] = dominant_colors

    # 2. 场景判断（基于色彩分布）
    mean_brightness = np.mean(img_rgb)
    color_std = np.std(pixels, axis=0)
    if mean_brightness < 80:
        result["scene"] = "夜间/暗光场景"
    elif np.mean(color_std) < 30:
        result["scene"] = "展厅/室内场景"
    elif mean_brightness > 180:
        result["scene"] = "户外明亮场景"
    else:
        result["scene"] = "日常户外场景"

    # 3. 图像复杂度评估
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.sum(edges > 0) / (height * width)
    if edge_ratio > 0.15:
        result["complexity"] = "复杂（多元素）"
    elif edge_ratio > 0.05:
        result["complexity"] = "中等"
    else:
        result["complexity"] = "简洁（主体突出）"

    return result


def detect_activity_type(image_path: str) -> dict:
    """
    识别活动图片类型
    """
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width = img_rgb.shape[:2]

    result = {
        "image_size": f"{width}x{height}",
        "possible_types": [],
    }

    # 基于宽高比判断
    ratio = width / height
    if ratio > 2.5:
        result["possible_types"].append("Banner广告")
    elif ratio > 1.5:
        result["possible_types"].append("横版海报")
    elif ratio < 0.6:
        result["possible_types"].append("竖版海报/长图")
    elif 0.7 < ratio < 1.5:
        result["possible_types"].append("方形设计/社交媒体")

    # 色彩饱和度分析
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat_mean = np.mean(hsv[:, :, 1])
    if sat_mean > 150:
        result["color_style"] = "高饱和度（年轻活力风格）"
    elif sat_mean > 80:
        result["color_style"] = "中等饱和度"
    else:
        result["color_style"] = "低饱和度（沉稳高端风格）"

    return result


def extract_text_regions(image_path: str) -> list:
    """
    检测图片中的文字区域
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # MSER文字区域检测
    mser = cv2.MSER_create()
    regions, _ = mser.detectRegions(gray)

    text_boxes = []
    for region in regions:
        x, y, w, h = cv2.boundingRect(region)
        if w > 20 and h > 10 and w * h > 500:
            text_boxes.append({
                "position": f"({x}, {y})",
                "size": f"{w}x{h}",
                "area": w * h
            })

    # 按面积排序，取前10个
    text_boxes.sort(key=lambda b: b["area"], reverse=True)
    return text_boxes[:10]
```

### 5.2 PIL 图片预处理

```python
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_for_recognition(image_path: str, output_path: str = None) -> str:
    """
    图片预处理：增强对比度、锐化、调整大小
    提高后续识别准确率
    """
    img = Image.open(image_path)

    # 1. 自动增强对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)

    # 2. 锐化
    img = img.filter(ImageFilter.SHARPEN)

    # 3. 限制最大尺寸
    max_size = 2048
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)

    # 4. 保存
    output = output_path or image_path.replace(".", "_processed.")
    img.save(output, quality=95)
    return output


def batch_analyze_images(image_paths: list) -> list:
    """
    批量分析多张图片
    """
    results = []
    for path in image_paths:
        try:
            vehicle_info = detect_vehicle_brand(path)
            activity_info = detect_activity_type(path)
            results.append({
                "file": path,
                "vehicle": vehicle_info,
                "activity": activity_info,
            })
        except Exception as e:
            results.append({"file": path, "error": str(e)})
    return results
```

---

## 6. 使用说明

1. **车辆识别**：传入汽车图片路径，自动分析品牌特征、颜色、场景
2. **活动识别**：传入活动现场图片，判断活动类型和规模
3. **设计识别**：传入设计稿图片，识别设计类型、风格、品牌元素
4. **批量处理**：支持批量分析，输出结构化JSON结果