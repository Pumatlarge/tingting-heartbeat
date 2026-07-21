from __future__ import annotations

FOODS = [
    {"name": "蒜蓉空心菜", "category": "家常菜", "emoji": "🥬", "hunger": 20, "mood": 12, "energy": 8, "line": "空心菜脆脆的，蒜香也刚刚好！"},
    {"name": "白灼虾", "category": "海鲜", "emoji": "🦐", "hunger": 28, "mood": 18, "energy": 12, "line": "虾肉好鲜甜，谢谢你帮我剥壳～"},
    {"name": "香煎牛肉", "category": "肉类", "emoji": "🥩", "hunger": 35, "mood": 16, "energy": 22, "line": "牛肉火候正好，感觉充满力量了！"},
    {"name": "番茄炒蛋", "category": "家常菜", "emoji": "🍅", "hunger": 24, "mood": 10, "energy": 10, "line": "酸酸甜甜，是很安心的味道。"},
    {"name": "清蒸鲈鱼", "category": "海鲜", "emoji": "🐟", "hunger": 30, "mood": 13, "energy": 16, "line": "鱼肉很嫩，我会慢慢吃的。"},
    {"name": "牛肉面", "category": "主食", "emoji": "🍜", "hunger": 42, "mood": 14, "energy": 20, "line": "热乎乎的牛肉面，连汤都很香。"},
    {"name": "扬州炒饭", "category": "主食", "emoji": "🍚", "hunger": 38, "mood": 10, "energy": 18, "line": "每一口都有不同的配料呢。"},
    {"name": "小笼包", "category": "点心", "emoji": "🥟", "hunger": 26, "mood": 15, "energy": 10, "line": "小心汤汁……呼，差点烫到啦！"},
    {"name": "叉烧包", "category": "点心", "emoji": "🍞", "hunger": 25, "mood": 13, "energy": 11, "line": "软乎乎的，里面还有甜甜的叉烧。"},
    {"name": "寿司拼盘", "category": "海鲜", "emoji": "🍣", "hunger": 32, "mood": 17, "energy": 13, "line": "摆盘好漂亮，我都舍不得吃了。"},
    {"name": "菌菇火锅", "category": "主食", "emoji": "🍲", "hunger": 45, "mood": 18, "energy": 18, "line": "咕嘟咕嘟的火锅最有陪伴感。"},
    {"name": "烤红薯", "category": "小食", "emoji": "🍠", "hunger": 23, "mood": 12, "energy": 12, "line": "暖手又香甜，冬天吃最好了。"},
    {"name": "玉米杯", "category": "小食", "emoji": "🌽", "hunger": 18, "mood": 8, "energy": 9, "line": "一颗一颗吃，很快就见底啦。"},
    {"name": "草莓蛋糕", "category": "甜品", "emoji": "🍰", "hunger": 18, "mood": 24, "energy": 8, "line": "今天也值得一块草莓蛋糕！"},
    {"name": "芒果布丁", "category": "甜品", "emoji": "🍮", "hunger": 14, "mood": 20, "energy": 6, "line": "滑滑嫩嫩的，芒果味很浓。"},
    {"name": "西瓜", "category": "水果", "emoji": "🍉", "hunger": 13, "mood": 16, "energy": 5, "line": "清甜多汁，夏天一下子凉快了。"},
    {"name": "葡萄", "category": "水果", "emoji": "🍇", "hunger": 11, "mood": 12, "energy": 5, "line": "这串葡萄每一颗都甜甜的。"},
    {"name": "热牛奶", "category": "饮品", "emoji": "🥛", "hunger": 10, "mood": 12, "energy": 10, "line": "喝完暖暖的，晚上会睡得很好。"},
    {"name": "珍珠奶茶", "category": "饮品", "emoji": "🧋", "hunger": 16, "mood": 22, "energy": 9, "line": "偶尔喝一次，快乐加倍！"},
    {"name": "茉莉花茶", "category": "饮品", "emoji": "🍵", "hunger": 5, "mood": 14, "energy": 8, "line": "茶香很清雅，适合陪你安静工作。"},
]

FOOD_BY_NAME = {item["name"]: item for item in FOODS}

for _food, _price in zip(FOODS, [18, 36, 48, 22, 42, 45, 34, 28, 26, 46, 52, 20, 16, 32, 28, 18, 16, 20, 30, 14]):
    _food["price"] = _price


OUTFITS = [
    {"id": "burgundy", "name": "经典酒红长裙", "name_en": "Classic Burgundy Dress", "price": 0, "asset": "assets/spritesheet.webp", "pose_dir": "assets/outfits/burgundy-hd"},
    {"id": "blue_floral", "name": "浅蓝印花长裙", "name_en": "Pale Blue Floral Dress", "price": 800, "asset": "assets/outfits/blue-floral.webp", "pose_dir": "assets/outfits/blue-floral-hd"},
]

OUTFIT_BY_ID = {item["id"]: item for item in OUTFITS}

PART_REACTIONS = {
    "hair": {
        "label": "摸头发",
        "actions": ["pet", "shy", "peace", "sleepy"],
        "lines": ["轻一点呀，发型要被你揉乱啦。", "你是在帮我整理头发吗？谢谢～", "头顶被摸得暖暖的，有点想打瞌睡。", "今天的头发很顺吧？", "再摸一下也可以，不过只能一下哦。"],
    },
    "face": {
        "label": "碰脸",
        "actions": ["face_smile", "face_blush", "peace", "face_surprise"],
        "lines": ["脸颊不是按钮……但我收到你的问候啦。", "突然碰脸，我会害羞的。", "咦？被你戳到了！", "今天的笑容看起来怎么样？", "眼镜没有歪吧？帮我看看。"],
    },
    "chest": {
        "label": "碰胸部",
        "actions": ["guard", "shy", "angry"],
        "lines": ["这里不可以随便碰啦，请尊重一点。", "欸……这个位置会让我很不好意思。", "请把手放规矩一点哦。", "再这样我可要认真生气了。", "保持一点礼貌距离，我们还是好朋友。"],
    },
    "arms": {
        "label": "碰手臂",
        "actions": ["high_five", "hand_reach", "heart_hands", "clap", "stretch", "work"],
        "lines": ["要牵手还是击掌？", "手臂今天也很有力气。", "抓住我的手，一起加油吧。", "袖口……啊，我没有袖子呢。", "别担心，我会陪你把事情做完。"],
    },
    "skirt": {
        "label": "碰裙子",
        "actions": ["curtsey", "skirt_show", "shy", "dance"],
        "lines": ["这条酒红色长裙是我很喜欢的一件。", "裙摆转起来很好看吧？", "小心不要踩到裙角哦。", "金色腰链会轻轻响呢。", "想看我穿着这条裙子跳舞吗？"],
    },
}

LOGICAL_ACTIONS = {
    "idle": {"label": "安静陪伴", "row": "idle", "duration": 4.0},
    "wave": {"label": "挥手问候", "row": "waving", "pose": "wave", "duration": 2.4, "effect": "wave"},
    "jump": {"label": "开心跳跃", "row": "jumping", "duration": 2.2, "effect": "jump"},
    "work": {"label": "认真工作", "row": "running", "duration": 4.0, "effect": "work"},
    "review": {"label": "查看成果", "row": "review", "duration": 3.2, "effect": "review"},
    "wait": {"label": "等待回应", "row": "waiting", "duration": 3.2},
    "sad": {"label": "小小失落", "row": "failed", "duration": 3.0},
    "pet": {"label": "享受摸头", "row": "idle", "duration": 2.6, "effect": "squash"},
    "shy": {"label": "害羞", "row": "waving", "pose": "heart-hands", "duration": 2.8, "effect": "blush"},
    "surprised": {"label": "惊讶", "row": "jumping", "duration": 1.8, "effect": "pulse"},
    "tickle": {"label": "怕痒", "row": "jumping", "duration": 2.2, "effect": "shake"},
    "twirl": {"label": "展示裙摆", "row": "review", "pose": "skirt-show", "duration": 3.2},
    "eat": {"label": "享用美食", "row": "review", "duration": 3.0, "effect": "bob"},
    "think": {"label": "认真思考", "row": "waiting", "duration": 3.5, "effect": "think"},
    "celebrate": {"label": "庆祝", "row": "jumping", "duration": 3.0, "effect": "sparkle"},
    "dance": {"label": "跳舞", "row": "jumping", "pose": "skirt-show", "duration": 4.5, "effect": "dance"},
    "sleepy": {"label": "犯困", "row": "idle", "duration": 5.0, "effect": "sleepy"},
    "angry": {"label": "假装生气", "row": "failed", "duration": 2.8, "effect": "shake"},
    "walk": {"label": "桌面散步", "row": "running-right", "duration": 6.0, "effect": "walk"},
    "face_smile": {"label": "微笑", "row": "idle", "duration": 2.4, "effect": "smile"},
    "face_blush": {"label": "脸红", "row": "waving", "pose": "heart-hands", "duration": 2.6, "effect": "blush"},
    "face_surprise": {"label": "睁大眼睛", "row": "jumping", "duration": 1.8, "effect": "face_surprise"},
    "guard": {"label": "护住自己", "row": "failed", "duration": 2.4, "effect": "guard"},
    "arm_wave": {"label": "摆动手臂", "row": "waving", "pose": "wave", "duration": 2.6, "effect": "arm_wave"},
    "hand_reach": {"label": "伸出手掌", "row": "waving", "pose": "high-five", "duration": 2.8, "effect": "hand_reach"},
    "high_five": {"label": "和你击掌", "row": "waving", "pose": "high-five", "duration": 2.6, "effect": "hand_reach"},
    "heart_hands": {"label": "双手比心", "row": "waiting", "pose": "heart-hands", "duration": 3.0, "effect": "hearts"},
    "curtsey": {"label": "优雅屈膝礼", "row": "review", "pose": "curtsey", "duration": 3.0},
    "clap": {"label": "开心鼓掌", "row": "jumping", "pose": "clap", "duration": 2.8, "effect": "bob"},
    "peace": {"label": "剪刀手", "row": "waving", "pose": "peace", "duration": 2.8},
    "skirt_show": {"label": "展示裙摆", "row": "review", "pose": "skirt-show", "duration": 3.2},
    "stretch": {"label": "伸懒腰", "row": "idle", "pose": "stretch", "duration": 3.2, "effect": "bob"},
    "skirt_twirl": {"label": "展示裙摆", "row": "review", "pose": "skirt-show", "duration": 3.0},
    "skirt_spin": {"label": "优雅屈膝礼", "row": "review", "pose": "curtsey", "duration": 3.0},
    "gift_receive": {"label": "收下礼物", "row": "jumping", "duration": 3.2, "effect": "hearts"},
    "recover": {"label": "恢复元气", "row": "jumping", "duration": 2.8, "effect": "recover"},
    "hungry": {"label": "有点饿了", "row": "waiting", "duration": 4.2, "effect": "bob"},
    "starving": {"label": "饿得没力气", "row": "failed", "duration": 5.2, "effect": "shake"},
    "lonely": {"label": "心情低落", "row": "waiting", "duration": 4.2, "effect": "think"},
    "heartbroken": {"label": "非常难过", "row": "failed", "duration": 5.2, "effect": "tilt"},
    "tired": {"label": "有点困了", "row": "idle", "duration": 4.8, "effect": "sleepy"},
    "exhausted": {"label": "精疲力尽", "row": "failed", "duration": 5.5, "effect": "squash"},
    "desk_sleep": {"label": "电脑桌前睡觉", "row": "failed", "duration": 86400.0, "effect": "desk_sleep"},
}

GIFTS = [
    {"name": "向日葵花束", "emoji": "🌻", "price": 55, "mood": 24, "line": "像把一小片阳光送给了我，谢谢你。"},
    {"name": "红玫瑰", "emoji": "🌹", "price": 80, "mood": 32, "line": "这朵玫瑰和我的裙子很配呢。"},
    {"name": "蝴蝶发夹", "emoji": "🦋", "price": 95, "mood": 36, "line": "戴在头发上一定很好看！"},
    {"name": "毛绒小兔", "emoji": "🐰", "price": 120, "mood": 42, "line": "软乎乎的小兔，以后陪我们一起待在桌面上。"},
    {"name": "音乐盒", "emoji": "🎵", "price": 145, "mood": 48, "line": "旋律很温柔，我会好好收藏。"},
    {"name": "星星夜灯", "emoji": "⭐", "price": 135, "mood": 45, "line": "夜晚有这盏灯，就不会觉得孤单了。"},
    {"name": "精装小说", "emoji": "📕", "price": 75, "mood": 28, "line": "今晚可以安静地读一会儿书啦。"},
    {"name": "拍立得相册", "emoji": "📷", "price": 165, "mood": 52, "line": "以后把我们的回忆一页页放进去。"},
    {"name": "丝绸围巾", "emoji": "🧣", "price": 110, "mood": 39, "line": "颜色很雅致，你的眼光真好。"},
    {"name": "水晶摆件", "emoji": "💎", "price": 220, "mood": 60, "line": "亮晶晶的，像把一颗小星星捧在手心。"},
    {"name": "手写信", "emoji": "💌", "price": 45, "mood": 35, "line": "比起昂贵的礼物，我更喜欢你认真写下的话。"},
    {"name": "金色项链", "emoji": "📿", "price": 260, "mood": 65, "line": "我会在特别的日子戴上它。"},
]

RECOVERY_ITEMS = [
    {"name": "元气营养包", "emoji": "🧃", "price": 65, "hunger": 35, "energy": 45, "mood": 8, "line": "一下子补充了好多元气！"},
    {"name": "维生素饮料", "emoji": "🍊", "price": 45, "hunger": 10, "energy": 32, "mood": 6, "line": "酸甜的维生素饮料让我清醒多了。"},
    {"name": "暖心恢复汤", "emoji": "🥣", "price": 80, "hunger": 45, "energy": 38, "mood": 18, "line": "热汤喝下去，整个人都暖起来了。"},
    {"name": "急救恢复包", "emoji": "🩹", "price": 120, "hunger": 20, "energy": 70, "mood": 10, "line": "状态已经稳定下来，我会注意休息的。"},
]

GIFT_BY_NAME = {item["name"]: item for item in GIFTS}
RECOVERY_BY_NAME = {item["name"]: item for item in RECOVERY_ITEMS}

ACHIEVEMENTS = [
    ("first_meet", "初次见面", "第一次启动婷婷。", "launch_count", 1),
    ("companion_10m", "十分钟的陪伴", "累计陪伴 10 分钟。", "companion_seconds", 600),
    ("companion_1h", "一小时不孤单", "累计陪伴 1 小时。", "companion_seconds", 3600),
    ("companion_8h", "完整工作日", "累计陪伴 8 小时。", "companion_seconds", 28800),
    ("companion_24h", "朝夕相伴", "累计陪伴 24 小时。", "companion_seconds", 86400),
    ("companion_100h", "长久的朋友", "累计陪伴 100 小时。", "companion_seconds", 360000),
    ("click_10", "轻轻碰触", "累计点击 10 次。", "clicks", 10),
    ("click_100", "互动达人", "累计点击 100 次。", "clicks", 100),
    ("click_500", "默契养成", "累计点击 500 次。", "clicks", 500),
    ("click_1000", "千次回应", "累计点击 1000 次。", "clicks", 1000),
    ("head_50", "摸摸头发", "触摸头发 50 次。", "part:hair", 50),
    ("arms_30", "牵手邀请", "触摸手臂 30 次。", "part:arms", 30),
    ("all_parts", "哪里都认识", "触发全部身体部位反应。", "unique_parts", 5),
    ("feed_1", "第一顿饭", "第一次给婷婷喂食。", "feeds", 1),
    ("feed_10", "准时开饭", "累计喂食 10 次。", "feeds", 10),
    ("feed_50", "婷婷的私厨", "累计喂食 50 次。", "feeds", 50),
    ("feed_100", "百味宴", "累计喂食 100 次。", "feeds", 100),
    ("food_10", "美食探索家", "品尝 10 种不同菜品。", "unique_foods", 10),
    ("food_all", "菜单全收集", "品尝菜单中的全部菜品。", "unique_foods", len(FOODS)),
    ("morning_glory", "一抹青绿", "品尝蒜蓉空心菜。", "food:蒜蓉空心菜", 1),
    ("shrimp", "鲜甜一刻", "品尝白灼虾。", "food:白灼虾", 1),
    ("beef", "元气满满", "品尝香煎牛肉。", "food:香煎牛肉", 1),
    ("balanced_trio", "荤素海陆", "品尝空心菜、白灼虾和牛肉。", "special:trio", 1),
    ("chat_1", "说说话吧", "完成第一次 AI 对话。", "chats", 1),
    ("chat_20", "无话不谈", "完成 20 次 AI 对话。", "chats", 20),
    ("chat_100", "百句心声", "完成 100 次 AI 对话。", "chats", 100),
    ("streak_3", "三日相见", "累计启动 3 天。", "total_launch_days", 3),
    ("streak_7", "一周之约", "累计启动 7 天。", "total_launch_days", 7),
    ("streak_30", "月度陪伴", "累计启动 30 天。", "total_launch_days", 30),
    ("drag_10k", "桌面旅行家", "拖着婷婷移动累计 10000 像素。", "drag_distance", 10000),
    ("actions_10", "动作收藏家", "看过 10 种不同动作。", "unique_actions", 10),
    ("night_owl", "深夜守候", "凌晨 0—4 点与婷婷互动。", "flag:night_owl", 1),
    ("early_bird", "早安婷婷", "早上 5—8 点与婷婷互动。", "flag:early_bird", 1),
    ("gift_1", "第一份心意", "第一次送给婷婷礼物。", "gifts_given", 1),
    ("gift_20", "礼物收藏家", "累计送出 20 份礼物。", "gifts_given", 20),
    ("coins_1000", "勤劳的小金库", "累计获得 1000 金币。", "coins_earned", 1000),
    ("drops_10", "幸运派送", "领取 10 次系统随机派发。", "system_drops", 10),
    ("companion_500h", "岁月相知", "累计陪伴 500 小时。", "companion_seconds", 1800000),
    ("companion_1000h", "千时相守", "累计陪伴 1000 小时。", "companion_seconds", 3600000),
    ("click_5000", "心有灵犀", "累计点击 5000 次。", "clicks", 5000),
    ("click_10000", "万次心动", "累计点击 10000 次。", "clicks", 10000),
    ("feed_500", "五星主厨", "累计喂食 500 次。", "feeds", 500),
    ("gift_100", "百份珍藏", "累计送出 100 份礼物。", "gifts_given", 100),
    ("chat_500", "知心密友", "完成 500 次 AI 对话。", "chats", 500),
    ("streak_100", "百日之约", "累计启动 100 天。", "total_launch_days", 100),
    ("streak_365", "四季相伴", "累计启动 365 天。", "total_launch_days", 365),
    ("drag_100k", "桌面环游记", "拖着婷婷移动累计 100000 像素。", "drag_distance", 100000),
    ("coins_10000", "富足小金库", "累计获得 10000 金币。", "coins_earned", 10000),
    ("coins_100000", "心动宝库", "累计获得 100000 金币。", "coins_earned", 100000),
    ("drops_100", "天选幸运星", "领取 100 次系统随机派发。", "system_drops", 100),
]

ROW_INDEX = {
    "idle": (0, 6),
    "running-right": (1, 8),
    "running-left": (2, 8),
    "waving": (3, 4),
    "jumping": (4, 5),
    "failed": (5, 8),
    "waiting": (6, 6),
    "running": (7, 6),
    "review": (8, 6),
}
