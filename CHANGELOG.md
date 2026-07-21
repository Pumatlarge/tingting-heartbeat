# 心动婷婷更新记录 / Tingting Heartbeat Changelog

## 待发布 / Unreleased

## v1.6.4

- 使用 GPT Image 重新绘制浅蓝印花长裙的待机、左右奔跑、跳跃、失败、等待、工作、查看等完整高清动画及 8 个高清互动姿势，单帧由 192×208 提升至 384×416。
- 服装购买和换装从设置页迁移至商店的独立“服装”分页，并增加皮肤预览。
- 修复浅蓝皮肤待机帧中心偏移造成的人物左右晃动，待机播放速度调整得更自然。
- 修复脸红装饰过大且位置错误的问题，改为只显示在左右脸颊的柔和红晕。
- 移除人物水平翻转的转圈效果，新增击掌、比心、屈膝礼、鼓掌、剪刀手、展示裙摆和伸懒腰等真实绘制动作。
- 重新绘制“认真思考”和“查看成果”高清动画，修复浅蓝皮肤脸部及裙面出现黑色斑块的问题。
- 浅蓝印花裙使用与当前服装匹配的互动台词和 AI 角色描述，不再提到酒红长裙或金色腰链。
- 移除胸部防护动作中遮挡人物的六边形盾牌轮廓。
- 重新对齐浅蓝皮肤的奔跑、挥手、工作和失败等动画帧，修复拖拽及动作播放时的人物上下跳动，并移除所有程序化旋转。
- 商店的食物、礼物和恢复品新增单品历史购买数量记录；恢复品不足一页时固定从顶部排列并隐藏无效滚动条。
- 为经典酒红长裙补齐挥手、击掌、比心、屈膝礼、鼓掌、剪刀手、展示裙摆和伸懒腰八个高清专属姿势。
- 提升服装皮肤的线稿、五官与花纹清晰度，并在高 DPI 放大显示时进行自适应锐化，同时保持原有透明轮廓和动作碰撞区域不变。

## v1.6.3

- 右键功能中心新增一键免打扰，暂停主动气泡、低状态提醒和随机动作。
- 五分钟闲置后的桌前睡眠形象由 88% 缩小为 72%。
- 手臂和裙子点击新增“伸出手掌”和“转圈圈”动作，各部位动作改为按次序轮换。
- 设置页新增付费衣橱：可用 800 金币购买浅蓝印花长裙，并在两套服装间永久切换。

## v1.6.2

- 确认并完善“千时相守”成就，累计陪伴 1000 小时后自动解锁。
- 饱腹、心情、元气低于 50% 和 10% 时分级提醒，新增饥饿、虚弱、低落、难过、困倦和精疲力尽动作。
- 状态提醒只在跨过阈值时触发，恢复后再次降低才会重新提醒，避免反复打扰。
- 右键功能中心打开的聊天、商店、成就、设置等窗口不再强制置顶，切换到其他窗口时可正常退到后台。

- 成就页新增当前值、目标值、完成百分比与可视化进度条。
- 所有启动天数成就由“连续启动”改为“累计启动”，并兼容迁移旧存档进度。
- 修复人物拖到负坐标屏幕边缘时突然跳到另一侧的问题；现在最多可将一半人物藏进当前显示器边缘。
- 设置页新增 40%—100% 人物透明度滑动条，支持即时预览并保存。

## v1.6.1

- 修复拖动人物时不再播放左右奔跑动画的问题，并支持拖动中实时改变朝向。
- 新增 GitHub Releases 自动更新：启动时可自动检查新版，发现新版后显示更新说明并下载安装包。
- 设置页面新增自动检查更新开关和“检查更新”按钮。
- 更新包下载限定为 GitHub HTTPS 地址，并在 Release 提供 SHA-256 摘要时自动校验完整性。

## v1.5.1

- 设置页面现在会显示当前程序版本号，方便确认已安装版本。

### English

- The Settings page now shows the current app version for quick installed-version checks.

## v1.5.0

- AI 对话会自动保存在本机，关闭聊天窗口后不再丢失。
- 新增多会话管理，可在聊天窗口右上角新建对话或通过历史菜单切换记录。
- 聊天文字支持选择、`Ctrl+C`、`Ctrl+A` 和右键复制；联网回答中的来源链接可直接点击。
- 发送期间显示“让我想一想 · N 秒”和旋转等待图标，并锁定输入、新建和历史切换，确保一次只处理一条消息。
- 人物头顶只显示 AI 回答的简短摘要，过长内容自动以 `...` 省略，完整回答仍保留在聊天窗口。
- 设置中新增可选 Responses API 联网搜索；模型及接口需要支持 `web_search` 工具。
- 五分钟闲置后的桌前睡眠人物缩小至常规尺寸的 88%，使人物、桌子和电脑比例更协调。
- 心情改为持续衰减，并在 6 小时、24 小时未送礼后分级加速；离线期间同样计算。
- 成就由 37 项扩展至 50 项，新增千小时陪伴、万次互动、百日/周年连续陪伴、十万金币等高难度目标，并提高高级奖励上限。
- 聊天窗口移除左侧历史面板，改为完整宽度的单栏布局。

### English

- AI conversations are now saved locally and remain available after closing the chat window.
- Added multi-conversation management with New Chat and History controls in the top-right corner.
- Chat text is selectable and supports Ctrl+C, Ctrl+A, and context-menu copying; cited web sources are clickable.
- While a reply is running, the UI shows an elapsed “Let me think” status and animated wait button, locking the composer and conversation controls to enforce one request at a time.
- Long AI replies are shortened with `...` above the character while the complete answer remains in the chat window.
- Added optional Responses API web search when supported by the configured model and endpoint.
- Reduced the five-minute idle desk-sleep character to 88% of the regular sprite scale.
- Mood now decays continuously, accelerates after 6 and 24 hours without a gift, and also updates while offline.
- Expanded achievements from 37 to 50 with advanced long-term goals and higher reward ceilings.
- Removed the left conversation sidebar in favor of a full-width, single-column chat layout.

## v1.4.2

- 修复双屏或多屏环境下右键功能中心超出当前显示器、底部按钮显示不全的问题。
- 功能中心会根据当前显示器工作区和实际控件高度自适应，并优先保留顶部状态及底部“暂时隐藏/退出程序”按钮。
- 修复高 DPI 或 Windows 显示缩放环境下功能中心标题、状态栏和按钮被固定尺寸裁切的问题。
- 人物拖动到不同 DPI 的显示器并松开后，会按显示器缩放比例自动调整大小，同时保留设置中的用户大小比例。
- 支持位于主屏幕左侧或上方的负坐标显示器，启动动画、人物、气泡、行走和功能中心均可正确定位。
- 缩小对话气泡字体并限制最大字号，改善较小人物尺寸及多行台词的可读性。

### English

- Fixed the quick panel extending beyond the active monitor or clipping its footer in multi-monitor setups.
- The quick panel now adapts to the monitor work area and actual widget size while keeping its status header and Hide/Quit controls visible.
- Fixed fixed-size clipping of quick-panel titles, status values, and buttons under high-DPI Windows display scaling.
- The character now rescales proportionally after being dropped on a monitor with a different DPI while preserving the user-selected size setting.
- Added correct negative-coordinate support for monitors positioned left of or above the primary display.
- Reduced and capped speech-bubble font sizes for clearer multiline dialogue at smaller character sizes.

## v1.4.1

- 桌面人物窗口不再显示在 Windows 任务栏，可通过系统托盘或右键功能中心退出程序。
- 移除会导致鼠标靠近人物时漂移或卡在边缘的自定义指针，恢复稳定的系统鼠标行为。
- 新增粉金爱心轮廓、菱形闪光与放射线点击光效；光效独立以 30 FPS 刷新，并严格限制在人物可见区域内。
- 启动动画会根据当前显示器和 DPI 居中，不再偏离屏幕中央。
- 修复功能中心顶部状态及底部按钮被裁切的问题；顶部仅显示饱腹、心情和元气。
- 功能中心新增明确的“退出程序”按钮。
- 修复商店与背包右侧空白过多的问题，商品卡片会随窗口宽度自动填满。
- 修复多行对话气泡文字贴近或越过顶部边框的问题。
- 更新中英文 README、授权说明和发布文档，并加入真实程序截图与动作 GIF 演示。

## v1.4.0

- 修复触摸脸部时，微笑效果在脸部中央绘制多余线条的问题；保留自然原始嘴型和脸颊表情。
- 新增约 2.25 秒的品牌启动动画：头像淡入、心形脉动、加载指示后再显示婷婷。
- 新增 Inno Setup 安装版，使用固定 AppId 和安装路径，可直接覆盖安装后续更新。
- 安装、覆盖升级和卸载均不会删除 `%APPDATA%\TingtingDesktopPet`，金币、背包、成就、语言和 API 设置会保留。
- 安装包支持开始菜单快捷方式、可选桌面快捷方式、运行中程序检测和标准卸载。

## v1.3.1

- 将人物鼠标爱心改为更宽、更短的方正比例，移除容易拉长视觉的星光装饰。
- 爱心鼠标现在只在人物实际可见像素上显示，移到透明区域会立即恢复普通指针。
- 新增 80 毫秒边界检测，即使窗口没有正确触发离开事件，也会自动清除残留爱心，避免卡在人物边缘。

## v1.3.0 — 心动婷婷 / Tingting Heartbeat

- 软件正式命名为“心动婷婷 / Tingting Heartbeat”。
- 新增简体中文与英文界面，可在设置中切换，默认使用简体中文并记住选择。
- 英文化覆盖功能中心、商店、动作、聊天、设置、统计、成就、说明、托盘菜单、物品名称及 AI 回复语言。
- 桌前睡觉动画降速至约 1.65 秒一帧，使低头与呼吸变化更自然。
- 将不明确的灰色方块重画为带屏幕、边框、铰链和键盘底座的打开式笔记本电脑。
- 使用图像生成制作全新的婷婷头部特写可爱风程序图标，并生成 Windows 多尺寸 ICO。

## v1.2.3

- 修复部分 Windows 环境下右键功能中心“动作”按钮图标缺失的问题。
- “动作”入口改为使用随程序打包的本地音乐动作图标，不再依赖系统 Emoji 字体。

## v1.2.2

- 修复触摸人物时，自定义爱心鼠标在部分 Windows/Tk 环境中显示为白色方块的问题。
- 爱心鼠标改为程序内绘制的粉色图层，不再依赖可能被单色解析的 CUR 显示方式。
- 胸部触摸的防护效果改为不透明轮廓，避免透明色键产生异常色块。

## v1.2.1

- 已达成成就现在会显示金币奖励，可单独领取，也可一键领取全部未领取奖励。
- 成就奖励具有领取记录，同一奖励无法重复领取。
- 商店、成就和使用说明等带滚动区域的功能页支持直接使用鼠标滚轮，不必拖动右侧滚动条。

## v1.2.0

- 动作面板新增十枚独立绘制的动作图标。
- 超过 5 分钟没有触摸后，婷婷会在电脑桌前进入睡眠；点击即可唤醒。
- 修复聊天窗口输入区域被内容挤出窗口的问题。
- 修复成就列表只占左侧、右侧大面积空白的问题，并统一为现代卡片风格。
- 使用与设置页一致的视觉风格重做使用说明窗口。
- 新增爱心与星光造型的专属人物鼠标指针。
- 对话气泡会按实际字宽自动换行并增高，避免文字越过边框。

## v1.1.1

- 修复“害羞”表情显示为两个悬浮白点的问题。
- 表情系统现在通过肤色连通区域自动识别每一帧的脸部位置。
- 腮红改为绘制在真实脸颊上的不透明玫红短线，不再使用会被 Windows 色键错误渲染的半透明椭圆。
- 新增脸部表情位置回归测试，确保表情像素不会出现在脸部范围之外。

## v1.1.0

- 修复透明色键与半透明像素混合导致的动态黑色/锯齿外圈。
- 身体点击改为基于每帧可见 Alpha 区域定位，划分为头发、脸、胸部、手臂和裙子。
- 每个身体部位增加多组不连续重复的台词；脸部增加微笑、脸红和惊讶效果。
- 使用现代功能中心替换传统右键菜单，重新设计聊天窗口。
- 动作面板中的十项动作改为十种独立效果，并完成动作映射自检。
- 新增金币、挂机收益、离线收益、商店、背包和购买机制。
- 新增 12 种礼物、4 种恢复品以及系统随机派送。
- 长期不进食会降低状态，长期没有收到礼物会影响心情。
- 新增总陪伴、挂机、触摸、聊天、金币、喂食、送礼、偏好和互动分布统计。
- 人物大小滑块改为实时预览。
- 设置中新增清除 API Key 和重置全部参数。
- 构建流程增加密钥特征和 `state.json` 扫描，发布包不会携带本机 API Key 或存档。
