# 📹 视频转录增强配置

**版本**: 1.0  
**创建时间**: 2026-05-24  
**状态**: ✅ 已具备基础能力，待优化

---

## 📌 当前能力

### 已有技能
- ✅ [audio_to_text](file://c:\Users\Admin\opcclawai\project\skills\audio_to_text) - 音频转文字
- ✅ [video-subtitle](file://c:\Users\Admin\opcclawai\project\skills\video-subtitle) - 视频字幕提取
- ✅ [video-frames](file://c:\Users\Admin\opcclawai\project\skills\video-frames) - 视频帧提取
- ✅ [content-rewriter](file://c:\Users\Admin\opcclawai\project\skills\content-rewriter) - 内容改写（口播稿生成）

### 支持场景
- ✅ 本地音频文件转文字
- ✅ 本地视频文件提取字幕
- ✅ 视频关键帧截图
- ✅ 转录内容改写润色

---

## ⚠️ 能力缺口

### ❌ 视频自动下载
- 无法自动下载微博视频
- 无法自动下载 B 站视频
- 无法自动下载抖音/视频号

### ❌ 直播监控
- 无法自动监控直播开始
- 无法自动录制直播内容

### ❌ 批量处理
- 无法批量转录多个视频
- 无法自动合并分段转录

---

## 🎯 优化方案

### 方案 A: 手动下载 + 自动转录（立即可用）

**流程**:
1. 用户手动下载视频（浏览器/第三方工具）
2. 保存到 `videos/` 目录
3. 调用 `audio_to_text` 技能转录
4. 调用 `content-rewriter` 提炼观点

**优点**: 无需额外配置，立即可用  
**缺点**: 需要手动下载

### 方案 B: 集成下载工具（1-2 周）

**工具选型**:
- 微博视频：`you-get` / `lux`
- B 站视频：`you-get` / `BBDown`
- 抖音视频：`tiktok-download`
- 通用：`yt-dlp`

**流程**:
1. 配置视频下载脚本
2. 自动下载指定 URL 视频
3. 自动转录 + 提炼观点
4. 归档到 `memory/` 目录

**优点**: 全自动化  
**缺点**: 需要安装额外工具，可能失效

### 方案 C: 云端 API（长期方案）

**服务选型**:
- 阿里云：语音识别 + 视频理解
- 腾讯云：语音识别 + 视频内容分析
- 百度智能云：语音识别 + 视频内容审核

**优点**: 稳定可靠，支持直播  
**缺点**: 需要付费，配置复杂

---

## ⚙️ 方案 A 实施指南（立即执行）

### 1. 创建视频目录

```powershell
# 创建视频存储目录
New-Item -ItemType Directory -Path "C:\Users\Admin\opcclawai\project\videos" -Force
```

### 2. 视频命名规范

```
videos/
├── yrt_20260521_112.mp4          # 叶荣添《预见》第 112 集
├── yrt_20260517_seminar.mp4      # 叶荣添 5-17 内部视频会
├── livestream_20260513.mp4       # 5-13 半年度战略直播
└── ...
```

### 3. 转录流程

```powershell
# 调用 audio_to_text 技能
# 输入：视频文件路径
# 输出：文字稿

# 示例（伪代码）
audio_to_text --input videos/yrt_20260521_112.mp4 --output memory/transcript_20260521.md
```

### 4. 观点提炼

```
# 转录完成后，调用 content-rewriter 提炼核心观点
# Prompt 示例：

请提炼以下视频转录稿的核心观点：
1. 投资主线（3-5 条）
2. 重点推荐方向
3. 风险提示
4. 时间节点判断

输出格式：
## 核心观点
- 观点 1
- 观点 2

## 推荐方向
- 方向 1：逻辑 + 标的
- 方向 2：逻辑 + 标的

## 风险提示
- 风险 1
- 风险 2

## 时间节点
- 时间 1：事件
- 时间 2：事件
```

---

## 📋 视频转录检查清单

### 叶荣添系列
- [ ] 《预见》第 112 集（5-21）：长鑫科技 IPO 红利
- [ ] 《预见》第 111 集（5-15）：牛市持续时间
- [ ] 5-17 内部视频会：长鑫 IPO+ 光互联
- [ ] 5-13 半年度战略直播（63.1 万观看）

### 其他财经大佬
- [ ] 徐小明直播回放
- [ ] 冯矿伟直播回放
- [ ] 券商策略会视频

---

## 🔧 方案 B 工具安装（可选）

### 安装 you-get

```powershell
# 安装 you-get（支持微博/B 站/抖音等）
pip install you-get -U

# 测试
you-get --version
```

### 使用示例

```powershell
# 下载微博视频
you-get https://weibo.com/tv/show/xxx

# 下载 B 站视频
you-get https://www.bilibili.com/video/BVxxx

# 指定输出目录
you-get -o videos/ https://weibo.com/xxx
```

### 注意事项
- 微博视频可能需要登录 cookie
- B 站高清视频需要大会员 cookie
- 工具可能随时失效，需维护更新

---

## 📊 转录质量优化

### 提升准确率
1. **预处理**: 降噪、音量标准化
2. **分段**: 长视频按 10 分钟分段转录
3. **后处理**: 合并分段、校对关键术语

### 专业术语库
创建投资术语词典，提升转录准确性：
```
光模块 → 光模块 (正确)
CPO → CPO (正确)
HBM → HBM (正确)
PCB → PCB (正确)
```

---

## 🔄 与现有流程集成

### 每日巡检增强
当前每日巡检包含"抖音视频监控"，可增加：
1. 发现新视频 → 记录 URL
2. 手动/自动下载
3. 转录 + 提炼观点
4. 归档到 `memory/YYYY-MM-DD.md`

### 周报生成增强
周报生成时可引用：
- 本周视频转录稿
- 核心观点摘要
- 与上周观点对比

---

**文件位置**: `config/video_transcription.md`  
**优先级**: P1 级 - 本周内完成方案 A 部署
