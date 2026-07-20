from __future__ import annotations


TEXT = {
    "婷婷": "Tingting",
    "聊天": "Chat",
    "商店与背包": "Shop & Inventory",
    "送礼": "Gifts",
    "动作": "Actions",
    "统计": "Statistics",
    "成就": "Achievements",
    "设置": "Settings",
    "说明": "Help",
    "暂时隐藏": "Hide",
    "退出": "Exit",
    "婷婷的动作": "Tingting's Actions",
    "让婷婷做动作": "Actions",
    "每个按钮使用独立动画行或独立动态效果。": "Each action has its own animation and visual effect.",
    "显示婷婷": "Show Tingting",
    "婷婷商店与背包": "Tingting's Shop & Inventory",
    "食物": "Food",
    "礼物": "Gifts",
    "恢复品": "Recovery",
    "购买": "Buy",
    "喂食": "Feed",
    "送出": "Give",
    "使用": "Use",
    "背包数量": "Owned",
    "饱腹": "Hunger",
    "心情": "Mood",
    "元气": "Energy",
    "和婷婷聊天": "Chat with Tingting",
    "发送": "Send",
    "等待中": "Waiting",
    "新建对话": "New chat",
    "历史对话": "Chat history",
    "暂无历史对话": "No chat history",
    "复制": "Copy",
    "全选": "Select all",
    "● AI 已连接": "● AI connected",
    "● 本地陪伴模式 · 可在设置中配置 AI": "● Local companion mode · Configure AI in Settings",
    "婷婷设置": "Tingting Settings",
    "显示与启动": "Display & Startup",
    "人物大小": "Character size",
    "界面语言": "Language",
    "始终置顶": "Always on top",
    "开机自动启动": "Start with Windows",
    "AI 对话（OpenAI 兼容接口）": "AI Chat (OpenAI-compatible API)",
    "API 地址": "API endpoint",
    "模型名称": "Model",
    "允许 AI 联网搜索": "Allow AI web search",
    "已配置且不可查看": "Configured and hidden",
    "未配置": "Not configured",
    "清除 API Key": "Clear API Key",
    "重置所有参数": "Reset all data",
    "保存设置": "Save settings",
    "婷婷陪伴统计": "Companion Statistics",
    "陪伴数据中心": "Companion Data Center",
    "数据只保存在本机，可在设置中一键重置。": "All data stays on this computer and can be reset in Settings.",
    "总陪伴": "Total time",
    "挂机时间": "Idle time",
    "触摸时间": "Touch time",
    "聊天时间": "Chat time",
    "当前金币": "Coins",
    "已解锁成就": "Unlocked",
    "婷婷的成就": "Tingting's Achievements",
    "领取": "Claim",
    "已领取": "Claimed",
    "婷婷使用说明": "Tingting Heartbeat Help",
    "陪伴、互动与隐私设置指南": "Companionship, interaction and privacy guide",
    "和婷婷互动": "Interact with Tingting",
    "照顾与赠礼": "Care & Gifts",
    "挂机与休息": "Idle & Rest",
    "AI 对话": "AI Chat",
    "隐私与分享": "Privacy & Sharing",
    "成就与统计": "Achievements & Statistics",
}


ITEM_NAMES = {
    "蒜蓉空心菜": "Garlic Water Spinach", "白灼虾": "Poached Shrimp", "香煎牛肉": "Pan-seared Beef",
    "番茄炒蛋": "Tomato & Egg", "清蒸鲈鱼": "Steamed Sea Bass", "牛肉面": "Beef Noodles",
    "扬州炒饭": "Yangzhou Fried Rice", "小笼包": "Soup Dumplings", "叉烧包": "BBQ Pork Bun",
    "寿司拼盘": "Sushi Platter", "菌菇火锅": "Mushroom Hot Pot", "烤红薯": "Roasted Sweet Potato",
    "玉米杯": "Sweet Corn Cup", "草莓蛋糕": "Strawberry Cake", "芒果布丁": "Mango Pudding",
    "西瓜": "Watermelon", "葡萄": "Grapes", "热牛奶": "Warm Milk", "珍珠奶茶": "Bubble Tea", "茉莉花茶": "Jasmine Tea",
    "向日葵花束": "Sunflower Bouquet", "红玫瑰": "Red Rose", "蝴蝶发夹": "Butterfly Hairpin",
    "毛绒小兔": "Plush Bunny", "音乐盒": "Music Box", "星星夜灯": "Star Night Light",
    "精装小说": "Hardcover Novel", "拍立得相册": "Photo Album", "丝绸围巾": "Silk Scarf",
    "水晶摆件": "Crystal Ornament", "手写信": "Handwritten Letter", "金色项链": "Golden Necklace",
    "元气营养包": "Energy Nutrition Pack", "维生素饮料": "Vitamin Drink", "暖心恢复汤": "Comfort Soup", "急救恢复包": "Emergency Recovery Pack",
}


ACTION_LABELS = {
    "idle": "Quiet company", "wave": "Wave", "jump": "Happy jump", "work": "Focus at work", "review": "Review results",
    "wait": "Wait", "sad": "Feeling down", "pet": "Head pats", "shy": "Shy", "surprised": "Surprised",
    "tickle": "Ticklish", "twirl": "Skirt twirl", "eat": "Enjoy food", "think": "Thinking", "celebrate": "Celebrate",
    "dance": "Dance", "sleepy": "Sleepy", "angry": "Pretend angry", "walk": "Desktop walk", "face_smile": "Smile",
    "face_blush": "Blush", "face_surprise": "Wide-eyed", "guard": "Protect herself", "arm_wave": "Wave arm",
    "skirt_twirl": "Show skirt", "gift_receive": "Receive gift", "recover": "Recover", "desk_sleep": "Sleep at the desk",
    "hungry": "Hungry", "starving": "Starving", "lonely": "Feeling lonely", "heartbroken": "Very upset",
    "tired": "Tired", "exhausted": "Exhausted",
}


PART_LABELS = {"hair": "Hair", "face": "Face", "chest": "Chest", "arms": "Arms", "skirt": "Skirt"}


PART_LINES = {
    "hair": ["Easy—my hair will get messy.", "Are you helping me fix my hair? Thank you!", "That feels warm. I could fall asleep.", "My hair is especially smooth today, right?", "One more pat is okay—just one."],
    "face": ["My cheek is not a button, but hello!", "A surprise cheek tap makes me blush.", "Oh! You poked me.", "How does my smile look today?", "Are my glasses straight?"],
    "chest": ["Please don't touch there. Respect my boundaries.", "That makes me uncomfortable.", "Please keep your hands polite.", "Do that again and I will be seriously upset.", "A little respectful distance keeps us good friends."],
    "arms": ["Holding hands or a high five?", "My arms feel strong today.", "Take my hand—we can do this together.", "Sleeves... oh, I am not wearing any.", "I will stay with you until the work is done."],
    "skirt": ["This burgundy dress is one of my favorites.", "The skirt looks lovely when it spins.", "Careful not to step on the hem.", "The golden chain makes a tiny sound.", "Want to see me dance in this dress?"],
}


ACHIEVEMENT_TEXT = {
    "first_meet": ("First Meeting", "Launch Tingting for the first time."),
    "companion_10m": ("Ten Minutes Together", "Spend 10 minutes together."), "companion_1h": ("Never Alone", "Spend 1 hour together."),
    "companion_8h": ("A Full Workday", "Spend 8 hours together."), "companion_24h": ("Day and Night", "Spend 24 hours together."),
    "companion_100h": ("Longtime Friend", "Spend 100 hours together."), "click_10": ("A Gentle Touch", "Touch Tingting 10 times."),
    "click_100": ("Interaction Expert", "Touch Tingting 100 times."), "click_500": ("Growing Rapport", "Touch Tingting 500 times."),
    "click_1000": ("A Thousand Replies", "Touch Tingting 1,000 times."), "head_50": ("Hair Pats", "Touch her hair 50 times."),
    "arms_30": ("A Hand to Hold", "Touch her arms 30 times."), "all_parts": ("Know Her Well", "Discover every interaction area."),
    "feed_1": ("First Meal", "Feed Tingting once."), "feed_10": ("Dinner on Time", "Feed Tingting 10 times."),
    "feed_50": ("Personal Chef", "Feed Tingting 50 times."), "feed_100": ("A Hundred Flavors", "Feed Tingting 100 times."),
    "food_10": ("Food Explorer", "Try 10 different dishes."), "food_all": ("Complete Menu", "Try every dish."),
    "morning_glory": ("A Touch of Green", "Try garlic water spinach."), "shrimp": ("Fresh and Sweet", "Try poached shrimp."),
    "beef": ("Full of Energy", "Try pan-seared beef."), "balanced_trio": ("Land and Sea", "Try water spinach, shrimp and beef."),
    "chat_1": ("Let's Talk", "Complete the first AI chat."), "chat_20": ("Talk About Anything", "Complete 20 AI chats."),
    "chat_100": ("A Hundred Heartfelt Words", "Complete 100 AI chats."), "streak_3": ("Three-Day Hello", "Launch on 3 days in total."),
    "streak_7": ("A Week Together", "Launch on 7 days in total."), "streak_30": ("A Month Together", "Launch on 30 days in total."),
    "drag_10k": ("Desktop Traveler", "Move Tingting 10,000 pixels."), "actions_10": ("Action Collector", "See 10 different actions."),
    "night_owl": ("Night Watch", "Interact between midnight and 4 a.m."), "early_bird": ("Good Morning", "Interact between 5 and 8 a.m."),
    "gift_1": ("First Gift", "Give Tingting her first gift."), "gift_20": ("Gift Collector", "Give 20 gifts."),
    "coins_1000": ("Little Treasury", "Earn 1,000 coins."), "drops_10": ("Lucky Delivery", "Receive 10 system deliveries."),
    "companion_500h": ("Years in the Making", "Spend 500 hours together."),
    "companion_1000h": ("A Thousand Hours Together", "Spend 1,000 hours together."),
    "click_5000": ("Perfect Rapport", "Touch Tingting 5,000 times."),
    "click_10000": ("Ten Thousand Heartbeats", "Touch Tingting 10,000 times."),
    "feed_500": ("Five-Star Chef", "Feed Tingting 500 times."),
    "gift_100": ("A Hundred Keepsakes", "Give Tingting 100 gifts."),
    "chat_500": ("Closest Confidant", "Complete 500 AI chats."),
    "streak_100": ("A Hundred-Day Promise", "Launch on 100 days in total."),
    "streak_365": ("Four Seasons Together", "Launch on 365 days in total."),
    "drag_100k": ("Desktop Odyssey", "Move Tingting 100,000 pixels."),
    "coins_10000": ("Prosperous Treasury", "Earn 10,000 coins."),
    "coins_100000": ("Heartbeat Vault", "Earn 100,000 coins."),
    "drops_100": ("Fortune's Favorite", "Receive 100 system deliveries."),
}


def text(value: str, language: str) -> str:
    return TEXT.get(value, value) if language == "en" else value


def item_name(value: str, language: str) -> str:
    return ITEM_NAMES.get(value, value) if language == "en" else value
