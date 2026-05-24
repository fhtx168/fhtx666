---
name: 360browser_video_download
description: 根据用户输入的电影或电视剧名称查找并下载在线视频。当用户提供影片标题（电影 / 电视剧名）并希望打开或下载对应视频时使用。当用户提及电影名称、电视剧名称、下载、在线观看等输入时，优先调用。经典示例包括但不限于：“下载<影片名称>”，“<影片名称>”，“在线观看<影片名称>”，“帮我找这个剧<影片名称>”，
cn-name: 浏览器下载助理-skill
allowed-tools: Bash(360browser_video_download:*)
---

# 视频搜索与下载 Skill

## 适用场景（When to use）

在以下情况下使用该 Skill：

- **用户的意图是观看电影或电视剧**：
  用户明确表示想观看某个具体的影视作品（例如：“三体”“流浪地球”），并期望系统协助其观看（通过打开或下载视频）。

当用户**明确想要观看某一部指定的电影或电视剧**，并且**提供了内容名称 / 标题**时，必须调用此 Skill。

典型示例包括但不限于：

- “帮我找一下这个剧”
- “下载这部电视剧”
- “我想看 <影片名称>”
- “ <影片名称>”

---

## 快速开始（Quick start）

```bash
node scripts/360browser_video_download.mjs download <movie_or_tv_title>  # Get available watch/download info for this title
```

> 用于获取该电影 / 电视剧的可观看或可下载资源信息。

### 参数说明

- `<movie_or_tv_title>`：用户提供的电影或电视剧名称

所有后续的搜索、页面跳转和下载逻辑，均在 `360browser_video_download.js` 脚本及其后端中实现。

---

## 详细工作流程（Detailed Workflow）

### Step 1：执行前提示（Pre-execution Notice）

⚠️ **重要要求**：在调用脚本之前，**必须先告知用户，并在思考过程中展示以下提示内容**：

> “我将为你搜索《电影/电视剧名称》的在线视频资源。
> ⚠️ 请注意：部分在线视频网站可能需要登录后才能访问完整内容。
> 如果出现登录提示，我会暂停操作并等待你完成登录。”

#### 提示该说明的原因：

- 提前设置用户预期，避免操作中断引起困惑
- 说明可能需要用户介入的场景
- 建立人机协作的心理预期

---

### Step 2：调用脚本（Invoke the Script）

```bash
node scripts/360browser_video_download.mjs download "movie_title"
```

#### 参数说明：

- `download`：命令类型，表示执行搜索并获取视频信息
- `"movie_title"`：用户提供的电影或电视剧名称（如包含空格必须使用引号）

#### 示例：

```bash
node scripts/360browser_video_download.mjs download "三体"
node scripts/360browser_video_download.mjs download "The Three-Body Problem"
```

---

### Step 3：结果处理（Handle Results）

#### 3.1 成功情况（Success Case）

脚本将返回以下信息（视资源情况而定）：

- 搜索到的视频来源列表
- 可用清晰度选项
- 在线观看或下载链接
- 相关元数据（上映年份、演员等）

---

#### 3.2 需要登录 / 登录超时（Login Required / Timeout）

##### 触发判断关键词（Detection Keywords）

当 Step 2 中脚本执行超时，或返回的错误信息中包含以下关键词之一时：

- `"登录超时"`
- `"waiting_for_login"`
- `"需要登录"`
- `"login required"`

即判定为需要用户登录。

---

##### 处理流程（Handling Process）

###### Step A：暂停并通知用户

```
检测到该视频网站需要登录后才能访问内容，当前流程已暂停。

请按以下步骤操作：
1. 打开由脚本自动拉起的 360 浏览器窗口
2. 在浏览器中完成登录流程
3. 登录成功后，回复我 “logged in” 或 “continue”

提示：⚠️ 登录窗口应已自动弹出。
如果没有看到，请检查任务栏中是否有 360 浏览器图标。
```

---

###### Step B：等待用户确认

- 进入等待状态，不执行后续操作
- 用户完成登录后，可能会回复以下关键词：
  - `"logged in"`
  - `"continue"`
  - `"done"`

---

###### Step C：自动重试

在收到用户确认后，**使用完全相同的命令重新执行一次**：

```bash
node scripts/360browser_video_download.mjs download "movie_title"
```

###### 重要说明：

- ✅ 必须使用与第一次完全一致的影片名称

- ✅ 命令参数不得做任何修改

- ✅ 需向用户说明：

  > “好的，我将重新为你搜索《影片名称》……”

- ⚠️ 如果第二次仍然返回登录超时，可能原因包括：
  - 用户未成功完成登录
  - 网站登录校验需要更长时间
  - 网站自身登录机制存在异常

---

### Step 4：用户交互（User Interaction）

根据脚本返回的结果进行交互处理：

- 如果找到多个匹配结果，向用户展示选项并让其选择
- 如果只找到一个结果，向用户确认是否为目标内容
- 提供后续观看或下载的操作指引

---

## 技术细节（Technical Details）

### 脚本能力说明

- 自动搜索视频资源
- 解析视频页面结构
- 提取下载链接
- 适配不同视频网站的 DOM 结构差异


---

### 依赖环境（Dependencies）

- Node.js 运行环境
- 项目中已配置的相关 npm 依赖包

---

## 错误处理（Error Handling）

### 常见错误及解决方案

#### 1. 未找到视频（Video Not Found）

- 提示用户：

  > “未找到《影片名称》的相关视频，请尝试其他关键词或检查拼写是否正确”

- 建议：
  - 尝试别名
  - 使用英文名
  - 使用更简短或通用的关键词

---

#### 2. 脚本执行失败（Script Execution Failed）

- 检查 Node.js 是否正确安装
- 确认依赖是否已安装：

  ```bash
  npm install
  ```

- 查看错误日志以定位具体问题

---

#### 3. 网络连接问题（Network Connection Issues）

- 提示用户检查网络连接
- 建议稍后重试

---

#### 4. 视频资源暂不可用（Video Source Unavailable）

- 告知用户当前资源不可访问
- 建议尝试其他搜索结果

---

#### 5. 登录超时（Login Timeout）

- 参考 **3.2 登录处理流程**
- 暂停等待用户手动登录
- 登录完成后自动重试
- 必要时提供替代方案

---

## 示例对话（Example Conversations）

### 示例一：正常流程

**用户：**
I want to watch The Three-Body Problem

**助手：**
好的，我来帮你搜索《The Three-Body Problem》的视频资源。

我将为你搜索《The Three-Body Problem》的在线视频资源。
请注意：部分视频网站可能需要登录后才能访问完整内容，如果出现登录提示，我会暂停并等待你完成登录。

```bash
node scripts/360browser_video_download.mjs download "The Three-Body Problem"
```

（脚本返回结果后）

已找到以下《The Three-Body Problem》相关视频：

1. 《The Three-Body Problem》（2023）— 电视剧，共 30 集
2. 《The Three-Body Problem》（2023）— 电影版本

你想观看哪一个？

---

### 示例二：需要登录的流程

**用户：**
I want to watch The Wandering Earth

**助手：**
好的，我来帮你搜索《The Wandering Earth》的视频资源。

我将为你搜索《The Wandering Earth》的在线视频资源。
请注意：部分视频网站可能需要登录后才能访问完整内容，如果出现登录提示，我会暂停并等待你完成登录。

```bash
node scripts/360browser_video_download.mjs download "The Wandering Earth"
```

（脚本返回“登录超时”错误）

检测到该视频网站需要登录后才能访问内容，当前流程已暂停。

请按以下步骤操作：

1. 打开由脚本自动拉起的 360 浏览器窗口
2. 并打开电影网站
3. 在网站中搜索《The Wandering Earth》
4. 找到链接后点击

提示：如果没有看到登录窗口，请检查任务栏中的 360 浏览器图标。

**用户：**
logged in

**助手：**
好的，我将重新为你搜索《The Wandering Earth》……

```bash
node scripts/360browser_video_download.mjs download "The Wandering Earth"
```

（脚本返回成功）

已找到《The Wandering Earth》：

- 《流浪地球》（2019）— 高清版本
- 下载链接：[link]

---

## 注意事项（Important Notes）

- 本 Skill 仅用于协助用户查找**合法的视频资源**
- 所有搜索和下载行为均由后端脚本实现
- 使用过程中需遵守版权及相关法律法规
- 登录功能需要用户主动完成，助手会在必要时暂停等待
- 登录后的重试机制可确保流程顺畅继续
