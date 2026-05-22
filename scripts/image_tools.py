#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汽车行业图片识别与仿作工具
用于 xinmeiti Agent 的图片处理能力
支持OpenCV + PIL 图像处理
"""

import os
import io
import json
import base64
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

logger = logging.getLogger(__name__)

# ==================== 图片识别工具 ====================

class ImageRecognitionTools:
    """汽车行业图片识别工具"""

    # 常见汽车品牌色系
    BRAND_COLORS = {
        "传祺": [(0, 100, 200), (200, 50, 50), (255, 255, 255)],
        "奥迪": [(0, 0, 0), (255, 255, 255), (200, 200, 200)],
        "昊铂": [(0, 200, 255), (255, 255, 255), (0, 50, 100)],
        "埃安": [(0, 180, 100), (255, 255, 255), (0, 80, 50)],
    }

    @staticmethod
    def detect_brand_by_color(image_path: str) -> Dict[str, float]:
        """通过主色调识别品牌"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "无法读取图片"}

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixels = img_rgb.reshape(-1, 3)

        scores = {}
        for brand, colors in ImageRecognitionTools.BRAND_COLORS.items():
            score = 0
            for color in colors:
                distances = np.linalg.norm(pixels.astype(float) - np.array(color), axis=1)
                match_pct = np.sum(distances < 80) / len(pixels)
                score += match_pct
            scores[brand] = round(score / len(colors), 4)

        return scores

    @staticmethod
    def detect_car_features(image_path: str) -> Dict[str, Any]:
        """检测车辆特征"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "无法读取图片"}

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # 检测轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 分析轮廓特征
        large_contours = [c for c in contours if cv2.contourArea(c) > w * h * 0.01]

        # 判断是否有车辆特征轮廓
        has_vehicle_shape = len(large_contours) >= 3

        return {
            "image_size": f"{w}x{h}",
            "edge_density": round(np.sum(edges > 0) / (w * h), 4),
            "contour_count": len(contours),
            "large_contour_count": len(large_contours),
            "has_vehicle_shape": has_vehicle_shape
        }

    @staticmethod
    def analyze_image_composition(image_path: str) -> Dict[str, Any]:
        """分析图片构图"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "无法读取图片"}

        h, w = img.shape[:2]

        # 三分构图分析
        h_third = h // 3
        w_third = w // 3

        regions = {
            "top_left": img[0:h_third, 0:w_third],
            "top_center": img[0:h_third, w_third:2*w_third],
            "top_right": img[0:h_third, 2*w_third:w],
            "mid_left": img[h_third:2*h_third, 0:w_third],
            "center": img[h_third:2*h_third, w_third:2*w_third],
            "mid_right": img[h_third:2*h_third, 2*w_third:w],
            "bottom_left": img[2*h_third:h, 0:w_third],
            "bottom_center": img[2*h_third:h, w_third:2*w_third],
            "bottom_right": img[2*h_third:h, 2*w_third:w],
        }

        # 计算各区域复杂度（标准差作为复杂度指标）
        region_complexity = {}
        for name, region in regions.items():
            if region.size > 0:
                region_complexity[name] = round(float(np.std(region)), 2)

        # 找出焦点区域
        max_region = max(region_complexity, key=region_complexity.get)

        return {
            "composition": "三分构图",
            "focal_point": max_region,
            "region_complexity": region_complexity,
            "overall_balance": round(float(np.std(list(region_complexity.values()))), 2)
        }

    @staticmethod
    def detect_logo_and_text(image_path: str) -> Dict[str, Any]:
        """检测Logo和文字区域"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "无法读取图片"}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 文字区域检测（MSER）
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)

        # 分析文字区域分布
        text_regions = []
        for region in regions:
            x, y, w_box, h_box = cv2.boundingRect(region)
            aspect_ratio = w_box / max(h_box, 1)
            if 0.1 < aspect_ratio < 15 and w_box * h_box > 100:
                text_regions.append({
                    "x": int(x), "y": int(y),
                    "width": int(w_box), "height": int(h_box),
                    "area": int(w_box * h_box)
                })

        # 计算文字覆盖区域
        text_area_pct = sum(r["area"] for r in text_regions) / (img.shape[0] * img.shape[1])

        return {
            "text_region_count": len(text_regions),
            "text_coverage_pct": round(text_area_pct * 100, 2),
            "has_logo_likely": len(text_regions) > 3 and text_area_pct < 0.1
        }


# ==================== 图片仿作工具 ====================

class ImageImitationTools:
    """图片仿作工具"""

    @staticmethod
    def analyze_style(image_path: str) -> Dict[str, Any]:
        """分析参考图风格"""
        img = Image.open(image_path)

        # 色彩分析
        img_small = img.resize((100, 100))
        pixels = list(img_small.getdata())

        # 主色调
        from collections import Counter
        color_counts = Counter(pixels)
        dominant_colors = color_counts.most_common(5)

        # 亮度分析
        gray_img = img.convert("L")
        brightness = sum(list(gray_img.getdata())) / (gray_img.width * gray_img.height)

        # 对比度
        contrast = np.std(list(gray_img.getdata()))

        return {
            "dominant_colors": [
                {"rgb": c[0], "ratio": round(c[1] / len(pixels), 3)}
                for c in dominant_colors
            ],
            "brightness": round(brightness, 1),
            "contrast": round(float(contrast), 1),
            "color_temperature": "warm" if brightness > 150 else "cool",
            "style_type": "modern" if contrast > 60 else "classic"
        }

    @staticmethod
    def create_poster_imitation(
        reference_path: str,
        output_path: str,
        brand: str = "传祺",
        title: str = "",
        subtitle: str = ""
    ) -> str:
        """基于参考图创作海报仿作"""
        ref = Image.open(reference_path)
        ref_style = ImageImitationTools.analyze_style(reference_path)

        # 创建画布，与参考图同尺寸
        canvas = Image.new("RGB", ref.size, ref_style["dominant_colors"][0]["rgb"])

        draw = ImageDraw.Draw(canvas)

        # 品牌色系
        brand_palette = {
            "传祺": {"primary": (0, 100, 200), "accent": (200, 50, 50), "text": (255, 255, 255)},
            "奥迪": {"primary": (30, 30, 30), "accent": (200, 0, 0), "text": (255, 255, 255)},
            "昊铂": {"primary": (0, 150, 220), "accent": (0, 50, 100), "text": (255, 255, 255)},
            "埃安": {"primary": (0, 160, 80), "accent": (0, 80, 50), "text": (255, 255, 255)},
        }

        colors = brand_palette.get(brand, brand_palette["传祺"])

        # 绘制渐变背景
        w, h = canvas.size
        for y in range(h):
            ratio = y / h
            r = int(colors["primary"][0] * (1 - ratio) + colors["accent"][0] * ratio)
            g = int(colors["primary"][1] * (1 - ratio) + colors["accent"][1] * ratio)
            b = int(colors["primary"][2] * (1 - ratio) + colors["accent"][2] * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        # 添加装饰元素
        # 顶部品牌条
        draw.rectangle([0, 0, w, 60], fill=colors["accent"])

        # 底部CTA区域
        draw.rectangle([0, h-80, w, h], fill=(0, 0, 0, 180))

        # 添加文本（简化版）
        if title:
            try:
                font_large = ImageFont.truetype("simhei.ttf", 48)
            except Exception:
                font_large = ImageFont.load_default()

            # 标题居中
            bbox = draw.textbbox((0, 0), title, font=font_large)
            tw = bbox[2] - bbox[0]
            draw.text(((w - tw) // 2, h // 2 - 40), title, fill=colors["text"], font=font_large)

        if subtitle:
            try:
                font_small = ImageFont.truetype("simhei.ttf", 28)
            except Exception:
                font_small = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            sw = bbox[2] - bbox[0]
            draw.text(((w - sw) // 2, h // 2 + 20), subtitle, fill=(220, 220, 220), font=font_small)

        # 保存
        canvas.save(output_path, quality=95)
        return output_path

    @staticmethod
    def apply_style_transfer(
        content_path: str,
        style_reference_path: str,
        output_path: str,
        strength: float = 0.5
    ) -> str:
        """风格迁移（简化版 - 基于色彩映射）"""
        content = cv2.imread(content_path)
        style = cv2.imread(style_reference_path)

        if content is None or style is None:
            raise ValueError("无法读取图片")

        # 调整尺寸匹配
        content = cv2.resize(content, (style.shape[1], style.shape[0]))

        # LAB色彩空间转换
        content_lab = cv2.cvtColor(content, cv2.COLOR_BGR2LAB).astype(np.float32)
        style_lab = cv2.cvtColor(style, cv2.COLOR_BGR2LAB).astype(np.float32)

        # 色彩分布匹配
        for i in range(3):
            content_mean = np.mean(content_lab[:, :, i])
            content_std = np.std(content_lab[:, :, i])
            style_mean = np.mean(style_lab[:, :, i])
            style_std = np.std(style_lab[:, :, i])

            content_lab[:, :, i] = ((content_lab[:, :, i] - content_mean) *
                                     (style_std / max(content_std, 1e-5)) + style_mean) * strength + \
                                    content_lab[:, :, i] * (1 - strength)

        content_lab = np.clip(content_lab, 0, 255).astype(np.uint8)
        result = cv2.cvtColor(content_lab, cv2.COLOR_LAB2BGR)

        cv2.imwrite(output_path, result)
        return output_path

    @staticmethod
    def generate_branded_image(
        brand: str,
        template_type: str,
        output_path: str,
        custom_text: str = "",
        image_source: str = None
    ) -> str:
        """生成品牌化图片"""
        templates = {
            "poster": {"width": 1080, "height": 1920},
            "banner": {"width": 1920, "height": 600},
            "square": {"width": 1080, "height": 1080},
            "story": {"width": 1080, "height": 1920},
        }

        size = templates.get(template_type, templates["poster"])
        w, h = size["width"], size["height"]

        brand_palette = {
            "传祺": {"primary": (0, 100, 200), "accent": (200, 50, 50), "bg": (245, 245, 250)},
            "奥迪": {"primary": (20, 20, 20), "accent": (200, 0, 0), "bg": (240, 240, 240)},
            "昊铂": {"primary": (0, 160, 230), "accent": (0, 60, 120), "bg": (235, 245, 255)},
            "埃安": {"primary": (0, 170, 90), "accent": (0, 90, 60), "bg": (240, 255, 245)},
        }

        colors = brand_palette.get(brand, brand_palette["传祺"])

        canvas = Image.new("RGB", (w, h), colors["bg"])
        draw = ImageDraw.Draw(canvas)

        # 顶部装饰条
        draw.rectangle([0, 0, w, 80], fill=colors["primary"])

        # 底部装饰条
        draw.rectangle([0, h-100, w, h], fill=colors["accent"])

        # 中心装饰框
        margin = 60
        draw.rectangle(
            [margin, 120, w-margin, h-140],
            outline=colors["primary"],
            width=3
        )

        # 文字
        if custom_text:
            try:
                font = ImageFont.truetype("simhei.ttf", 42)
            except Exception:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), custom_text, font=font)
            tw = bbox[2] - bbox[0]
            draw.text(
                ((w - tw) // 2, h // 2 - 21),
                custom_text,
                fill=colors["primary"],
                font=font
            )

        canvas.save(output_path, quality=95)
        return output_path


# ==================== 批处理工具 ====================

class BatchImageProcessor:
    """批量图片处理器"""

    @staticmethod
    def batch_analyze(directory: str, file_pattern: str = "*.jpg") -> List[Dict[str, Any]]:
        """批量分析图片"""
        results = []
        path = Path(directory)

        for img_file in path.glob(file_pattern):
            try:
                style = ImageImitationTools.analyze_style(str(img_file))
                features = ImageRecognitionTools.detect_car_features(str(img_file))
                results.append({
                    "file": str(img_file),
                    "style": style,
                    "features": features
                })
            except Exception as e:
                results.append({
                    "file": str(img_file),
                    "error": str(e)
                })

        return results

    @staticmethod
    def batch_resize(directory: str, output_dir: str,
                     target_size: Tuple[int, int] = (1080, 1080),
                     file_pattern: str = "*.jpg"):
        """批量调整图片尺寸"""
        path = Path(directory)
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        results = []
        for img_file in path.glob(file_pattern):
            try:
                img = Image.open(img_file)
                img_resized = img.resize(target_size, Image.LANCZOS)
                output_file = out_path / img_file.name
                img_resized.save(str(output_file), quality=95)
                results.append({"file": str(output_file), "status": "success"})
            except Exception as e:
                results.append({"file": str(img_file), "status": "error", "error": str(e)})

        return results

    @staticmethod
    def batch_add_watermark(directory: str, output_dir: str,
                            watermark_text: str = "CONFIDENTIAL",
                            file_pattern: str = "*.jpg",
                            opacity: int = 40):
        """批量添加水印"""
        path = Path(directory)
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        results = []
        for img_file in path.glob(file_pattern):
            try:
                img = Image.open(img_file).convert("RGBA")
                w, h = img.size

                # 创建水印层
                watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark)

                try:
                    font = ImageFont.truetype("simhei.ttf", max(w, h) // 20)
                except Exception:
                    font = ImageFont.load_default()

                # 倾斜水印
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]

                for y in range(-h, h * 2, th * 3):
                    for x in range(-w, w * 2, tw * 3):
                        draw.text((x, y), watermark_text,
                                  fill=(255, 255, 255, opacity), font=font)

                watermark = watermark.rotate(30, expand=False)

                # 合成
                result = Image.alpha_composite(img, watermark.crop((0, 0, w, h)))
                result = result.convert("RGB")

                output_file = out_path / img_file.name
                result.save(str(output_file), quality=95)
                results.append({"file": str(output_file), "status": "success"})

            except Exception as e:
                results.append({"file": str(img_file), "status": "error", "error": str(e)})

        return results


if __name__ == "__main__":
    # 使用示例
    print("Image Tools for xinmeiti Agent")
    print("-" * 40)
    print("ImageRecognitionTools: 车辆识别、活动识别、设计识别")
    print("ImageImitationTools: 海报仿作、活动照片仿作、设计素材仿作")
    print("BatchImageProcessor: 批量分析、批量调整、批量水印")
