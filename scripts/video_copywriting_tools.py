#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汽车行业爆款短视频文案创作工具
用于 xinmeiti Agent 的视频文案生成能力
支持四品牌差异化文案风格
"""

import os, json, random, logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class VideoScript:
    title: str
    hook: str
    content: List[str]
    call_to_action: str
    hashtags: List[str]
    brand: str
    style: str
    duration_estimate: int

    def to_dict(self):
        return {
            "title": self.title,
            "hook": self.hook,
            "content": self.content,
            "call_to_action": self.call_to_action,
            "hashtags": self.hashtags,
            "brand": self.brand,
            "style": self.style,
            "duration_estimate": self.duration_estimate,
            "total_sentences": len(self.content)
        }

    def format_for_platform(self, platform="douyin"):
        if platform == "douyin": return self._fmt_dy()
        elif platform == "kuaishou": return self._fmt_ks()
        else: return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def _fmt_dy(self):
        parts = [f"🎬 {self.title}", "", f"🔥 {self.hook}", ""]
        parts.extend(self.content)
        parts.extend(["", f"👉 {self.call_to_action}", "", " ".join(f"#{t}" for t in self.hashtags[:5])])
        return chr(10).join(parts)

    def _fmt_ks(self):
        parts = [f"【{self.title}】", "", f"💥 {self.hook}", ""]
        parts.extend(self.content)
        parts.extend(["", f"💡 {self.call_to_action}", "", " ".join(f"#{t}" for t in self.hashtags[:8])])
        return chr(10).join(parts)

class CopywritingDatabase:
    """文案素材数据库"""

    HOT_TOPICS = [
        "新能源汽车","智能驾驶","续航焦虑","充电桩","电池安全",
        "自动驾驶","车联网","OTA升级","智能座舱","激光雷达",
        "零百加速","麋鹿测试","碰撞测试","保值率","用车成本",
        "国产崛起","合资对比","豪华平替","家庭用车","商务接待"
    ]

    BRAND_STYLES = {
        "传祺": ["科技感","家庭","实用","性价比","国民车"],
        "奥迪": ["豪华","运动","商务","经典","德系品质"],
        "昊铂": ["年轻","潮流","智能","电动","未来感"],
        "埃安": ["家用","舒适","安全","经济","新能源"]
    }

    HOOKS = {
        "传祺": [
            "传祺这波操作，让BBA都慌了！",
            "10万预算，传祺给你B级车的享受！",
            "传祺车主才知道的5个隐藏功能！",
            "传祺这款车，月销3万台的秘密！",
            "传祺智能座舱，比手机还好用？"
        ],
        "奥迪": [
            "奥迪的灯，为什么这么贵？",
            "开奥迪的人，到底在开什么？",
            "奥迪的quattro，到底有多强？",
            "百年奥迪，如何保持年轻？",
            "奥迪车主不会告诉你的秘密！"
        ],
        "昊铂": [
            "昊铂这设计，未来感拉满！",
            "年轻人的第一台电动车，为什么选昊铂？",
            "昊铂的智能驾驶，比特斯拉还强？",
            "昊铂车主：开了就回不去了！",
            "昊铂的800V快充，到底有多快？"
        ],
        "埃安": [
            "埃安车主：一年省下2万油费！",
            "家庭第一台车，为什么选埃安？",
            "埃安的弹匣电池，到底有多安全？",
            "埃安车主真实续航，打几折？",
            "埃安这款车，为什么能月销5万？"
        ]
    }

    CONTENT_TEMPLATES = [
        "你知道吗？{brand}的{feature}采用了{tech}技术，比传统方案提升{percent}%！",
        "很多车主不知道，{brand}的{model}其实隐藏了{feature}功能，打开后体验完全不同！",
        "对比{competitor}，{brand}的{advantage}优势明显，特别是{detail}方面！",
        "实测数据来了！{brand}的{model}在{situation}场景下，表现超出预期！",
        "车主反馈：{brand}的{feature}最让人满意，尤其是{detail}这一点！",
        "行业专家分析：{brand}的{strategy}正在改变{industry}格局！",
        "技术解析：{brand}的{tech}如何实现{benefit}效果？",
        "购车建议：如果你需要{need}，那么{brand}的{model}是最好选择！",
        "使用技巧：{brand}的{feature}这样用，效率提升一倍！",
        "未来展望：{brand}的{plan}将带来哪些革命性变化？"
    ]

    CTA_TEMPLATES = [
        "关注我，了解更多{brand}最新资讯！",
        "评论区告诉我，你对{brand}的{model}有什么看法？",
        "点赞收藏，下次选车不迷茫！",
        "转发给需要的朋友，一起讨论{brand}！",
        "点击主页，查看{brand}全系车型解析！"
    ]

    HASHTAGS = {
        "传祺": ["传祺","广汽传祺","国产车","性价比","家庭用车","SUV","MPV","智能汽车"],
        "奥迪": ["奥迪","Audi","豪华车","德系车","quattro","灯厂","性能车","商务车"],
        "昊铂": ["昊铂","Hyper","电动车","智能驾驶","未来出行","年轻座驾","科技感","800V"],
        "埃安": ["埃安","AION","新能源","家用车","续航","充电","经济实用","安全出行"]
    }

    @classmethod
    def get_random_hook(cls, brand):
        hooks = cls.HOOKS.get(brand, cls.HOOKS["传祺"])
        return random.choice(hooks)

    @classmethod
    def get_content_template(cls, brand, topic=None):
        template = random.choice(cls.CONTENT_TEMPLATES)
        bf = {
            "传祺": {"feature":"智能座舱","tech":"ADiGO 4.0","model":"影豹","advantage":"性价比"},
            "奥迪": {"feature":"矩阵大灯","tech":"quattro","model":"A6L","advantage":"操控性"},
            "昊铂": {"feature":"NDA智能驾驶","tech":"800V高压平台","model":"昊铂GT","advantage":"智能化"},
            "埃安": {"feature":"弹匣电池","tech":"GEP2.0平台","model":"AION Y","advantage":"安全性"}
        }
        features = bf.get(brand, bf["传祺"])
        return template.format(brand=brand, **features,
            percent=random.randint(20,80),
            competitor=random.choice(["特斯拉","比亚迪","宝马","奔驰"]),
            situation=random.choice(["城市拥堵","高速巡航","山路驾驶","冬季低温"]),
            industry="汽车",
            need=random.choice(["家用代步","商务接待","性能驾驶","长途旅行"]),
            benefit=random.choice(["节能","安全","舒适","智能"]),
            plan=random.choice(["电动化转型","智能化升级","全球化布局","生态建设"]),
            detail=random.choice(["响应速度","使用体验","成本控制","可靠性"]))

    @classmethod
    def get_cta(cls, brand, model=None):
        template = random.choice(cls.CTA_TEMPLATES)
        return template.format(brand=brand, model=model or random.choice(["全系车型","最新车型","热门车型"]))

    @classmethod
    def get_hashtags(cls, brand, count=8):
        base_tags = cls.HASHTAGS.get(brand, cls.HASHTAGS["传祺"])
        hot_topics = random.sample(cls.HOT_TOPICS, min(3, len(cls.HOT_TOPICS)))
        all_tags = base_tags + hot_topics
        return random.sample(all_tags, min(count, len(all_tags)))

class VideoCopywritingGenerator:
    def __init__(self):
        self.db = CopywritingDatabase()

    def generate_script(self, brand, style=None, topic=None, target_duration=60):
        if style is None:
            style = random.choice(CopywritingDatabase.BRAND_STYLES.get(brand, ["科技感"]))
        title = self._gen_title(brand, style, topic)
        hook = self.db.get_random_hook(brand)
        sc = max(3, target_duration // 15)
        content = [self.db.get_content_template(brand, topic) for _ in range(sc)]
        cta = self.db.get_cta(brand)
        hashtags = self.db.get_hashtags(brand)
        return VideoScript(title=title, hook=hook, content=content,
            call_to_action=cta, hashtags=hashtags, brand=brand, style=style,
            duration_estimate=len(hook)//3 + sum(len(c)//5 for c in content) + 5)

    def _gen_title(self, brand, style, topic=None):
        templates = [
            f"{brand}{style}解析：{topic or chr(39)你不知道的秘密chr(39)}",
            f"{brand}车主必看：{random.choice([chr(39)使用技巧chr(39),chr(39)隐藏功能chr(39),chr(39)保养攻略chr(39)])}",
            f"{brand} vs {random.choice([chr(39)特斯拉chr(39),chr(39)比亚迪chr(39),chr(39)宝马chr(39),chr(39)奔驰chr(39)])}：谁更值得买？",
            f"{brand}{random.choice([chr(39)最新chr(39),chr(39)热门chr(39),chr(39)经典chr(39)])}车型深度评测",
            f"{style}之选：为什么{random.choice([chr(39)年轻人chr(39),chr(39)家庭用户chr(39),chr(39)商务人士chr(39)])}都选{brand}？"
        ]
        return random.choice(templates)

    def generate_batch_scripts(self, brand, count=5, styles=None):
        if styles is None:
            styles = CopywritingDatabase.BRAND_STYLES.get(brand, ["科技感"])
        return [self.generate_script(brand, random.choice(styles)) for _ in range(count)]

    def generate_comparison_script(self, brand_a, brand_b, comparison_point="性价比"):
        title = f"{brand_a} vs {brand_b}：谁才是{comparison_point}之王？"
        hook = f"花{random.randint(10,50)}万买车，{brand_a}和{brand_b}到底怎么选？"
        content = [
            f"首先看{brand_a}，在{comparison_point}方面，它的优势是{random.choice(['技术成熟','配置丰富','品牌认可','售后服务'])}",
            f"而{brand_b}的强项在于{random.choice(['智能化','设计感','性能表现','能耗控制'])}",
            f"实测：{brand_a}的{random.choice(['加速','刹车','续航','空间'])}比{brand_b}高出{random.randint(5,20)}%",
            f"但{brand_b}在{random.choice(['舒适性','科技配置','驾驶乐趣','使用成本'])}方面更胜一筹",
            f"结论：{random.choice(['家庭用户选','年轻人选','商务人士选'])}{random.choice([brand_a,brand_b])}"
        ]
        cta = f"关注我，下期对比{brand_a}和{brand_b}的{random.choice(['智能驾驶','内饰','保值率','用车成本'])}！"
        ht = CopywritingDatabase.HASHTAGS.get(brand_a,[]) + CopywritingDatabase.HASHTAGS.get(brand_b,[])
        ht += [f"#{comparison_point}对比","#选车指南"]
        return VideoScript(title=title, hook=hook, content=content, call_to_action=cta,
            hashtags=list(set(ht))[:10], brand=f"{brand_a}vs{brand_b}", style="对比评测", duration_estimate=70)

class HitScriptAnalyzer:
    """爆款文案分析器"""
    @staticmethod
    def analyze(script):
        score, factors = 0, []
        hl = len(script.hook)
        if 10 <= hl <= 30: score += 20; factors.append("钩子长度合适")
        elif hl < 10: score += 5; factors.append("钩子过短")
        else: score += 10; factors.append("钩子偏长")
        cl = sum(len(c) for c in script.content)
        if cl > 200: score += 20; factors.append("内容丰富")
        elif cl > 100: score += 15; factors.append("内容适中")
        else: score += 5; factors.append("内容偏短")
        if len(script.hashtags) >= 5: score += 10; factors.append("标签充足")
        ctas = ["关注","评论","点赞","转发","主页"]
        if any(w in script.call_to_action for w in ctas): score += 10; factors.append("CTA有效")
        trend_words = ["AI","智能","新能源","自动驾驶","OTA"]
        if any(w in script.hook + str(script.content) for w in trend_words):
            score += 15; factors.append("包含趋势关键词")
        level = "S" if score >= 70 else ("A" if score >= 50 else ("B" if score >= 30 else "C"))
        return {"score": score, "level": level, "factors": factors}

class ScriptExporter:
    """脚本导出器"""
    @staticmethod
    def export_markdown(scripts, output_path):
        md_lines = ["# 视频脚本合集", "", f"生成时间: {datetime.now().isoformat()}", "", "---", ""]
        for i, s in enumerate(scripts, 1):
            md_lines.extend([f"## {i}. {s.title}", "", f"**钩子**: {s.hook}", "", "**内容主体**:"])
            for j, line in enumerate(s.content, 1):
            md_lines.append(f"{j}. {line}")
            md_lines.extend(["", f"**行动号召**: {s.call_to_action}", "", f"**标签**: {', '.join(s.hashtags)}", "", "---", ""])
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text("\n".join(md_lines), encoding="utf-8")
        return output_path

    @staticmethod
    def export_json(scripts, output_path):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(json.dumps([s.to_dict() for s in scripts], indent=2, ensure_ascii=False), encoding="utf-8")
        return output_path

if __name__ == "__main__":
    gen = VideoCopywritingGenerator()
    print("=== 视频文案生成示例 ===")
    s = gen.generate_script("传祺", "科技感")
    print(s.format_for_platform("douyin"))
