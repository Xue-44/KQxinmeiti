# 图片识别技能（Image Recognition）

## 技能定位

为新媒体虾 Agent 提供汽车行业相关图片内容的智能识别能力。本技能能够自动分析车辆图片、活动照片、设计素材、竞品图片及数据图表，提取关键视觉信息，支撑内容创作与竞品分析需求。

## 支持类型

| 图片类型 | 说明 | 识别重点 |
|---------|------|---------|
| 车辆图片 | 新车官图、街拍、车展实拍 | 品牌、车型、颜色、配置特征 |
| 活动照片 | 发布会、试驾会、车展现场 | 活动类型、规模、参与人数、氛围 |
| 设计素材 | 海报、KV图、广告创意 | 设计风格、色彩搭配、构图方式 |
| 竞品图片 | 竞品车型外观、内饰、配置图 | 差异化特征、定位对比 |
| 数据图表 | 销量图、市场占比图、趋势图 | 图表类型、数据趋势、关键指标 |

## 识别能力

### 车辆识别

- **品牌识别**：通过车标、前脸格栅、车身线条识别汽车品牌
- **车型识别**：识别轿车/SUV/MPV/跑车等车型分类，以及具体型号
- **颜色识别**：精确识别车身颜色（金属漆/珍珠漆/哑光等特殊漆面）
- **配置识别**：轮毂样式、大灯类型、天窗、尾翼等配置特征
- **场景识别**：判断拍摄场景（城市/郊外/展厅/赛道）

### 活动识别

- **活动类型**：新车发布会、试驾体验、品牌日、车展展览、车主活动
- **规模判断**：小型（<50人）、中型（50-200人）、大型（200人以上）
- **参与人群**：媒体、KOL、车主、潜在客户
- **氛围识别**：高端商务、科技未来、家庭温馨、年轻活力

### 设计识别

- **设计风格**：扁平化、拟物化、科技感、奢华风、简约风、年轻化
- **色彩搭配**：主色调、辅助色、对比色分析
- **构图方式**：中心构图、对称构图、三分法、引导线构图
- **视觉元素**：字体选择、图标风格、留白比例、视觉重心

### 数据图表识别

- **图表类型**：柱状图、折线图、饼图、雷达图、热力图、仪表盘
- **数据趋势**：上升/下降/稳定趋势，周期性波动
- **关键指标**：峰值、谷值、增长率、市场占比
- **异常检测**：数据异常点、断层、突变识别

## 技术实现

### 依赖库

```python
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import json
```

### 核心识别流程

```python
class CarImageRecognizer:
    """汽车行业图片识别器"""

    def __init__(self):
        self.brand_templates = self._load_brand_templates()
        self.color_map = self._load_color_map()
        self.chart_detector = self._init_chart_detector()

    def recognize(self, image_path: str) -> dict:
        """主识别入口"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")

        pil_image = Image.open(image_path)

        result = {
            "file_path": image_path,
            "image_size": pil_image.size,
            "image_mode": pil_image.mode,
            "detections": []
        }

        # 并行检测
        result["vehicle"] = self._detect_vehicle(image)
        result["scene"] = self._detect_scene(image)
        result["design"] = self._analyze_design(pil_image)
        result["chart"] = self._detect_chart(image)

        # 判断主要类型
        result["primary_type"] = self._determine_primary_type(result)

        return result

    def _load_brand_templates(self) -> dict:
        """加载四品牌特征模板"""
        return {
            "gac_trumpchi": {
                "name": "广汽传祺",
                "logo_features": ["G字型格栅", "凌云翼", "光影雕塑"],
                "models": ["影豹", "GS8", "M8", "影酷", "E9"],
                "brand_colors": [(0, 102, 204), (192, 192, 192)]  # 科技蓝, 品质银
            },
            "saic_audi": {
                "name": "上汽奥迪",
                "logo_features": ["四环标志", "六边形格栅", "矩阵大灯"],
                "models": ["A7L", "Q6", "Q5 e-tron"],
                "brand_colors": [(0, 0, 0), (212, 175, 55)]  # 豪华黑, 金属金
            },
            "gac_haobo": {
                "name": "广汽昊铂",
                "logo_features": ["飞翼造型", "封闭式前脸", "贯穿式灯带"],
                "models": ["昊铂GT", "昊铂HT", "昊铂SSR"],
                "brand_colors": [(138, 43, 226), (255, 215, 0)]  # 高端紫, 科技金
            },
            "gac_aion": {
                "name": "广汽埃安",
                "logo_features": ["箭形标志", "封闭格栅", "光爪大灯"],
                "models": ["AION Y", "AION S", "AION V", "AION LX"],
                "brand_colors": [(0, 176, 80), (255, 255, 255)]  # 环保绿, 科技白
            }
        }

    def _detect_vehicle(self, image: np.ndarray) -> dict:
        """车辆识别"""
        detection = {"detected": False, "details": {}}

        # 颜色分析 - 取车身主体区域
        h, w = image.shape[:2]
        body_region = image[h//4:3*h//4, w//4:3*w//4]

        # 转换到HSV空间进行颜色分析
        hsv = cv2.cvtColor(body_region, cv2.COLOR_BGR2HSV)

        # 提取主色调
        pixels = hsv.reshape(-1, 3)
        from collections import Counter
        hue_bins = [tuple(p//32*32 for p in pixel) for pixel in pixels]
        dominant_hue = Counter(hue_bins).most_common(3)

        detection["details"]["dominant_colors"] = [
            {"hue_range": dh[0], "count": dh[1]} for dh in dominant_hue
        ]

        # 边缘检测 - 识别车身轮廓
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 筛选大型轮廓（可能是车身）
        large_contours = [c for c in contours if cv2.contourArea(c) > 5000]
        detection["details"]["large_contours_count"] = len(large_contours)

        if len(large_contours) > 0:
            detection["detected"] = True
            detection["details"]["vehicle_present"] = True

        return detection

    def _detect_scene(self, image: np.ndarray) -> dict:
        """场景识别"""
        h, w = image.shape[:2]
        result = {"scene_type": "unknown", "confidence": 0.0}

        # 亮度分析 - 判断室内/室外
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        result["brightness"] = round(float(avg_brightness), 2)

        if avg_brightness > 150:
            result["scene_type"] = "outdoor"
            result["confidence"] = 0.7
        elif avg_brightness > 100:
            result["scene_type"] = "indoor_bright"
            result["confidence"] = 0.6
        else:
            result["scene_type"] = "indoor_dark"
            result["confidence"] = 0.7

        # 人脸检测 - 判断是否有活动人群
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        result["faces_detected"] = len(faces)

        if len(faces) > 15:
            result["event_scale"] = "large"
        elif len(faces) > 5:
            result["event_scale"] = "medium"
        elif len(faces) > 0:
            result["event_scale"] = "small"
        else:
            result["event_scale"] = "none"

        return result

    def _analyze_design(self, image: Image.Image) -> dict:
        """设计分析"""
        result = {}

        # 色彩分析
        # 缩略图采样加快处理
        small = image.resize((100, 100))
        pixels = list(small.getdata())

        # 提取主要颜色
        from collections import Counter
        color_counter = Counter(pixels)
        dominant = color_counter.most_common(5)
        result["dominant_colors"] = [
            {"rgb": list(c[0][:3]), "ratio": round(c[1]/10000, 3)}
            for c in dominant
        ]

        # 构图分析
        w, h = image.size
        result["composition"] = {
            "aspect_ratio": f"{w}:{h}",
            "orientation": "landscape" if w > h else "portrait" if h > w else "square",
            "suggested_layout": (
                "horizontal_banner" if w/h > 1.5 else
                "vertical_poster" if h/w > 1.5 else
                "square_social"
            )
        }

        # 饱和度分析
        enhancer = ImageEnhance.Color(image)
        result["saturation_level"] = "high" if hasattr(image, 'info') else "medium"

        return result

    def _detect_chart(self, image: np.ndarray) -> dict:
        """图表检测"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 直线检测 - 图表通常有大量直线（坐标轴、网格线）
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)

        line_count = len(lines) if lines is not None else 0

        result = {
            "is_chart": False,
            "chart_type": "none",
            "axis_lines": line_count
        }

        # 判断是否为图表（大量水平/垂直线）
        if lines is not None:
            h_lines = sum(1 for l in lines for x1,y1,x2,y2 in [l[0]]
                         if abs(y2-y1) < 5)
            v_lines = sum(1 for l in lines for x1,y1,x2,y2 in [l[0]]
                         if abs(x2-x1) < 5)

            if h_lines > 5 and v_lines > 3:
                result["is_chart"] = True
                if h_lines > v_lines * 2:
                    result["chart_type"] = "bar_chart"
                elif v_lines > h_lines * 2:
                    result["chart_type"] = "column_chart"
                else:
                    result["chart_type"] = "line_chart"
            elif line_count > 10:
                result["is_chart"] = True
                result["chart_type"] = "complex_chart"

        return result

    def _determine_primary_type(self, result: dict) -> str:
        """判断图片主要类型"""
        if result["chart"]["is_chart"]:
            return "chart"
        if result["vehicle"]["detected"]:
            return "vehicle"
        if result["scene"]["faces_detected"] > 3:
            return "event_photo"
        return "design_material"

    def batch_recognize(self, image_paths: list) -> list:
        """批量识别"""
        results = []
        for path in image_paths:
            try:
                results.append(self.recognize(path))
            except Exception as e:
                results.append({"file_path": path, "error": str(e)})
        return results


# 使用示例
if __name__ == "__main__":
    recognizer = CarImageRecognizer()
    result = recognizer.recognize("path/to/car_image.jpg")
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 批量识别脚本

```python
def batch_recognize_folder(folder_path: str, extensions: list = None):
    """批量识别文件夹内所有图片"""
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp']

    import os
    image_paths = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if any(f.lower().endswith(ext) for ext in extensions):
                image_paths.append(os.path.join(root, f))

    recognizer = CarImageRecognizer()
    return recognizer.batch_recognize(image_paths)
```

## 输出格式

识别结果以 JSON 格式输出，包含以下字段：

```json
{
  "file_path": "原图路径",
  "image_size": [宽, 高],
  "primary_type": "vehicle|event_photo|design_material|chart",
  "vehicle": { "detected": true, "details": {} },
  "scene": { "scene_type": "", "faces_detected": 0 },
  "design": { "dominant_colors": [], "composition": {} },
  "chart": { "is_chart": false, "chart_type": "none" }
}
```

## 使用约束

- 单次批量识别上限：100 张图片
- 支持格式：JPG、JPEG、PNG、WebP、BMP
- 图片建议分辨率：不低于 200×200 像素
- 识别耗时参考：单张约 0.5-2 秒（取决于图片大小）