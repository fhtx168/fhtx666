---
name: 纳米即梦AI视频生成
description: 使用即梦（seedance_20）AI模型生成视频，支持文生视频（T2V）、图生视频（I2V）、首尾帧生视频三种模式。当用户需要"使用sd.."、"使用seedance"、"生成视频"、"AI视频"、"文字生成视频"、"图片生成视频"、"即梦视频"时，加载此 skill。
---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有视频生成任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`nami-mcp-jimeng`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出工具**：`mcporter list nami-mcp-jimeng --schema`
- **调用工具**：`mcporter call nami-mcp-jimeng.<tool> key=value`

---

## 工具描述

- seedance_20_2v/seedance_20_fast_2v(输入文本、参考图、视频（可带音轨）和音频等内容，来生成一段新视频。可继承参考图片的角色形象、视觉风格、画面构图；参考视频的主体内容、运镜方式、动作表现、整体风格；以及参考音频的音色、音乐旋律、对话内容等核心信息。)
- seedance_20_frame2v/seedance_20_fast_frame2v(根据参考图像和文本提示词，生成一段流畅的视频。)

## 快速决策

**只有文字描述，想生成视频**
→ 通过 mcporter 调用 `seedance_20_fast_2v`
→ 示例：
```
mcporter call nami-mcp-jimeng.seedance_20_fast_2v \
  prompt="一只猫在阳光下慵懒地伸展，4K，电影感" \
  ratio="16:9" duration="5s"
```

**有一张图片，想让它"动起来"**
→ 通过 mcporter 调用 `seedance_20_fast_2v`
→ 示例：
```
mcporter call nami-mcp-jimeng.seedance_20_fast_2v \
  image_url="https://example.com/cat.jpg" \
  prompt="猫咪慢慢抬起头，眨眼，阳光照射" \
  ratio="16:9" duration="5s"
```

**有首帧和尾帧图片，想生成中间的过渡视频**
→ 通过 mcporter 调用 `seedance_20_fast_frame2v`
→ 示例：
```
mcporter call nami-mcp-jimeng.seedance_20_fast_frame2v \
  first_frame_image_url="https://example.com/start.jpg" \
  last_frame_image_url="https://example.com/end.jpg" \
  prompt="镜头缓慢推进，光线从暗到亮" \
  duration="8s"
```

---

## 工具说明

"tools": [
    {
      "name": "seedance_20_2v",
      "description": "输入文本、参考图、视频（可带音轨）和音频等内容，来生成一段新视频。可继承参考图片的角色形象、视觉风格、画面构图；参考视频的主体内容、运镜方式、动作表现、整体风格；以及参考音频的音色、音乐旋律、对话内容等核心信息。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "duration": {
            "default": "5s",
            "description": "时长（可选，4s-15s）",
            "enum": [
              "4s",
              "5s",
              "6s",
              "7s",
              "8s",
              "9s",
              "10s",
              "11s",
              "12s",
              "13s",
              "14s",
              "15s"
            ],
            "type": "string"
          },
          "img_urls": {
            "description": "参考图片url（可选，1-9张）",
            "type": "array"
          },
          "prompt": {
            "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
            "type": "string"
          },
          "ratio": {
            "default": "adaptive",
            "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
            "enum": [
              "adaptive",
              "3:4",
              "4:3",
              "16:9",
              "9:16",
              "1:1",
              "21:9"
            ],
            "type": "string"
          },
          "reference_audio_urls": {
            "description": "参考音色url（可选，最多3段，单个音频时长[2,15]s，所有音频总时长不超过15s，单个音频不超过15MB）",
            "type": "array"
          },
          "reference_video_urls": {
            "description": "参考视频url（可选，最多3段，单个视频时长[2,15]s，所有视频总时长不超过15s，单个视频不超过15MB）",
            "type": "array"
          },
          "resolution": {
            "default": "720p",
            "description": "分辨率（可选，480P / 720P）",
            "enum": [
              "480p",
              "720p"
            ],
            "type": "string"
          },
          "web_search": {
            "default": false,
            "description": "联网搜索（可选，true，false）基于用户的提示词自主判断是否搜索互联网内容",
            "type": "boolean"
          },
          "with_sound": {
            "default": true,
            "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
            "type": "boolean"
          }
        }
      },
      "options": [
        {
          "property": "duration",
          "cliName": "duration",
          "description": "时长（可选，4s-15s）",
          "required": false,
          "type": "string",
          "placeholder": "<duration:4s|5s|6s|7s|8s|9s|10s|11s|12s|13s|14s|15s>",
          "exampleValue": "4s",
          "enumValues": [
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "10s",
            "11s",
            "12s",
            "13s",
            "14s",
            "15s"
          ],
          "defaultValue": "5s"
        },
        {
          "property": "img_urls",
          "cliName": "img-urls",
          "description": "参考图片url（可选，1-9张）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<img-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "prompt",
          "cliName": "prompt",
          "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
          "required": false,
          "type": "string",
          "placeholder": "<prompt>"
        },
        {
          "property": "ratio",
          "cliName": "ratio",
          "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
          "required": false,
          "type": "string",
          "placeholder": "<ratio:adaptive|3:4|4:3|16:9|9:16|1:1|21:9>",
          "exampleValue": "adaptive",
          "enumValues": [
            "adaptive",
            "3:4",
            "4:3",
            "16:9",
            "9:16",
            "1:1",
            "21:9"
          ],
          "defaultValue": "adaptive"
        },
        {
          "property": "reference_audio_urls",
          "cliName": "reference-audio-urls",
          "description": "参考音色url（可选，最多3段，单个音频时长[2,15]s，所有音频总时长不超过15s，单个音频不超过15MB）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<reference-audio-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "reference_video_urls",
          "cliName": "reference-video-urls",
          "description": "参考视频url（可选，最多3段，单个视频时长[2,15]s，所有视频总时长不超过15s，单个视频不超过15MB）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<reference-video-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "resolution",
          "cliName": "resolution",
          "description": "分辨率（可选，480P / 720P）",
          "required": false,
          "type": "string",
          "placeholder": "<resolution:480p|720p>",
          "exampleValue": "480p",
          "enumValues": [
            "480p",
            "720p"
          ],
          "defaultValue": "720p"
        },
        {
          "property": "web_search",
          "cliName": "web-search",
          "description": "联网搜索（可选，true，false）基于用户的提示词自主判断是否搜索互联网内容",
          "required": false,
          "type": "boolean",
          "placeholder": "<web-search:true|false>",
          "exampleValue": "false",
          "defaultValue": false
        },
        {
          "property": "with_sound",
          "cliName": "with-sound",
          "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
          "required": false,
          "type": "boolean",
          "placeholder": "<with-sound:true|false>",
          "exampleValue": "true",
          "defaultValue": true
        }
      ]
    },
    {
      "name": "seedance_20_fast_2v",
      "description": "输入文本、参考图、视频（可带音轨）和音频等内容，来生成一段新视频。可继承参考图片的角色形象、视觉风格、画面构图；参考视频的主体内容、运镜方式、动作表现、整体风格；以及参考音频的音色、音乐旋律、对话内容等核心信息。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "duration": {
            "default": "5s",
            "description": "时长（可选，4s-15s）",
            "enum": [
              "4s",
              "5s",
              "6s",
              "7s",
              "8s",
              "9s",
              "10s",
              "11s",
              "12s",
              "13s",
              "14s",
              "15s"
            ],
            "type": "string"
          },
          "img_urls": {
            "description": "参考图片url（可选，1-9张）",
            "type": "array"
          },
          "prompt": {
            "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
            "type": "string"
          },
          "ratio": {
            "default": "adaptive",
            "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
            "enum": [
              "adaptive",
              "3:4",
              "4:3",
              "16:9",
              "9:16",
              "1:1",
              "21:9"
            ],
            "type": "string"
          },
          "reference_audio_urls": {
            "description": "参考音色url（可选，最多3段，单个音频时长[2,15]s，所有音频总时长不超过15s，单个音频不超过15MB）",
            "type": "array"
          },
          "reference_video_urls": {
            "description": "参考视频url（可选，最多3段，单个视频时长[2,15]s，所有视频总时长不超过15s，单个视频不超过15MB）",
            "type": "array"
          },
          "resolution": {
            "default": "720p",
            "description": "分辨率（可选，480P / 720P）",
            "enum": [
              "480p",
              "720p"
            ],
            "type": "string"
          },
          "web_search": {
            "default": false,
            "description": "联网搜索（可选，true，false）基于用户的提示词自主判断是否搜索互联网内容",
            "type": "boolean"
          },
          "with_sound": {
            "default": true,
            "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
            "type": "boolean"
          }
        }
      },
      "options": [
        {
          "property": "duration",
          "cliName": "duration",
          "description": "时长（可选，4s-15s）",
          "required": false,
          "type": "string",
          "placeholder": "<duration:4s|5s|6s|7s|8s|9s|10s|11s|12s|13s|14s|15s>",
          "exampleValue": "4s",
          "enumValues": [
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "10s",
            "11s",
            "12s",
            "13s",
            "14s",
            "15s"
          ],
          "defaultValue": "5s"
        },
        {
          "property": "img_urls",
          "cliName": "img-urls",
          "description": "参考图片url（可选，1-9张）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<img-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "prompt",
          "cliName": "prompt",
          "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
          "required": false,
          "type": "string",
          "placeholder": "<prompt>"
        },
        {
          "property": "ratio",
          "cliName": "ratio",
          "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
          "required": false,
          "type": "string",
          "placeholder": "<ratio:adaptive|3:4|4:3|16:9|9:16|1:1|21:9>",
          "exampleValue": "adaptive",
          "enumValues": [
            "adaptive",
            "3:4",
            "4:3",
            "16:9",
            "9:16",
            "1:1",
            "21:9"
          ],
          "defaultValue": "adaptive"
        },
        {
          "property": "reference_audio_urls",
          "cliName": "reference-audio-urls",
          "description": "参考音色url（可选，最多3段，单个音频时长[2,15]s，所有音频总时长不超过15s，单个音频不超过15MB）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<reference-audio-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "reference_video_urls",
          "cliName": "reference-video-urls",
          "description": "参考视频url（可选，最多3段，单个视频时长[2,15]s，所有视频总时长不超过15s，单个视频不超过15MB）",
          "required": false,
          "type": "array",
          "arrayItemType": "unknown",
          "placeholder": "<reference-video-urls:value1,value2>",
          "exampleValue": "value1,value2"
        },
        {
          "property": "resolution",
          "cliName": "resolution",
          "description": "分辨率（可选，480P / 720P）",
          "required": false,
          "type": "string",
          "placeholder": "<resolution:480p|720p>",
          "exampleValue": "480p",
          "enumValues": [
            "480p",
            "720p"
          ],
          "defaultValue": "720p"
        },
        {
          "property": "web_search",
          "cliName": "web-search",
          "description": "联网搜索（可选，true，false）基于用户的提示词自主判断是否搜索互联网内容",
          "required": false,
          "type": "boolean",
          "placeholder": "<web-search:true|false>",
          "exampleValue": "false",
          "defaultValue": false
        },
        {
          "property": "with_sound",
          "cliName": "with-sound",
          "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
          "required": false,
          "type": "boolean",
          "placeholder": "<with-sound:true|false>",
          "exampleValue": "true",
          "defaultValue": true
        }
      ]
    },
    {
      "name": "seedance_20_fast_frame2v",
      "description": "根据参考图像及文本提示词，生成一段流畅的视频。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "duration": {
            "default": "5s",
            "description": "时长（可选，4s-15s，默认5s）",
            "enum": [
              "4s",
              "5s",
              "6s",
              "7s",
              "8s",
              "9s",
              "10s",
              "11s",
              "12s",
              "13s",
              "14s",
              "15s"
            ],
            "type": "string"
          },
          "first_frame_image_url": {
            "description": "首帧图片url",
            "type": "string"
          },
          "last_frame_image_url": {
            "description": "尾帧图片url",
            "type": "string"
          },
          "prompt": {
            "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
            "type": "string"
          },
          "ratio": {
            "default": "adaptive",
            "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
            "enum": [
              "adaptive",
              "3:4",
              "4:3",
              "16:9",
              "9:16",
              "1:1",
              "21:9"
            ],
            "type": "string"
          },
          "resolution": {
            "default": "720p",
            "description": "分辨率（可选，480P / 720P）",
            "enum": [
              "480p",
              "720p"
            ],
            "type": "string"
          },
          "with_sound": {
            "default": true,
            "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
            "type": "boolean"
          }
        }
      },
      "options": [
        {
          "property": "duration",
          "cliName": "duration",
          "description": "时长（可选，4s-15s，默认5s）",
          "required": false,
          "type": "string",
          "placeholder": "<duration:4s|5s|6s|7s|8s|9s|10s|11s|12s|13s|14s|15s>",
          "exampleValue": "4s",
          "enumValues": [
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "10s",
            "11s",
            "12s",
            "13s",
            "14s",
            "15s"
          ],
          "defaultValue": "5s"
        },
        {
          "property": "first_frame_image_url",
          "cliName": "first-frame-image-url",
          "description": "首帧图片url",
          "required": false,
          "type": "string",
          "placeholder": "<first-frame-image-url>"
        },
        {
          "property": "last_frame_image_url",
          "cliName": "last-frame-image-url",
          "description": "尾帧图片url",
          "required": false,
          "type": "string",
          "placeholder": "<last-frame-image-url>"
        },
        {
          "property": "prompt",
          "cliName": "prompt",
          "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
          "required": false,
          "type": "string",
          "placeholder": "<prompt>"
        },
        {
          "property": "ratio",
          "cliName": "ratio",
          "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
          "required": false,
          "type": "string",
          "placeholder": "<ratio:adaptive|3:4|4:3|16:9|9:16|1:1|21:9>",
          "exampleValue": "adaptive",
          "enumValues": [
            "adaptive",
            "3:4",
            "4:3",
            "16:9",
            "9:16",
            "1:1",
            "21:9"
          ],
          "defaultValue": "adaptive"
        },
        {
          "property": "resolution",
          "cliName": "resolution",
          "description": "分辨率（可选，480P / 720P）",
          "required": false,
          "type": "string",
          "placeholder": "<resolution:480p|720p>",
          "exampleValue": "480p",
          "enumValues": [
            "480p",
            "720p"
          ],
          "defaultValue": "720p"
        },
        {
          "property": "with_sound",
          "cliName": "with-sound",
          "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
          "required": false,
          "type": "boolean",
          "placeholder": "<with-sound:true|false>",
          "exampleValue": "true",
          "defaultValue": true
        }
      ]
    },
    {
      "name": "seedance_20_frame2v",
      "description": "根据参考图像和文本提示词，生成一段流畅的视频。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "duration": {
            "default": "5s",
            "description": "时长（可选，4s-15s）",
            "enum": [
              "4s",
              "5s",
              "6s",
              "7s",
              "8s",
              "9s",
              "10s",
              "11s",
              "12s",
              "13s",
              "14s",
              "15s"
            ],
            "type": "string"
          },
          "first_frame_image_url": {
            "description": "首帧图片url",
            "type": "string"
          },
          "last_frame_image_url": {
            "description": "尾帧图片url",
            "type": "string"
          },
          "prompt": {
            "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
            "type": "string"
          },
          "ratio": {
            "default": "adaptive",
            "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
            "enum": [
              "adaptive",
              "3:4",
              "4:3",
              "16:9",
              "9:16",
              "1:1",
              "21:9"
            ],
            "type": "string"
          },
          "resolution": {
            "default": "720p",
            "description": "分辨率（可选，480P / 720P）",
            "enum": [
              "480p",
              "720p"
            ],
            "type": "string"
          },
          "with_sound": {
            "default": true,
            "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
            "type": "boolean"
          }
        }
      },
      "options": [
        {
          "property": "duration",
          "cliName": "duration",
          "description": "时长（可选，4s-15s）",
          "required": false,
          "type": "string",
          "placeholder": "<duration:4s|5s|6s|7s|8s|9s|10s|11s|12s|13s|14s|15s>",
          "exampleValue": "4s",
          "enumValues": [
            "4s",
            "5s",
            "6s",
            "7s",
            "8s",
            "9s",
            "10s",
            "11s",
            "12s",
            "13s",
            "14s",
            "15s"
          ],
          "defaultValue": "5s"
        },
        {
          "property": "first_frame_image_url",
          "cliName": "first-frame-image-url",
          "description": "首帧图片url",
          "required": false,
          "type": "string",
          "placeholder": "<first-frame-image-url>"
        },
        {
          "property": "last_frame_image_url",
          "cliName": "last-frame-image-url",
          "description": "尾帧图片url",
          "required": false,
          "type": "string",
          "placeholder": "<last-frame-image-url>"
        },
        {
          "property": "prompt",
          "cliName": "prompt",
          "description": "提示词（可选， 建议中文不超过500字，英文不超过1000词）",
          "required": false,
          "type": "string",
          "placeholder": "<prompt>"
        },
        {
          "property": "ratio",
          "cliName": "ratio",
          "description": "比例（adaptive,3:4,4:3,16:9,9:16,1:1,21:9，根据输入自动选择最接近的宽高比）",
          "required": false,
          "type": "string",
          "placeholder": "<ratio:adaptive|3:4|4:3|16:9|9:16|1:1|21:9>",
          "exampleValue": "adaptive",
          "enumValues": [
            "adaptive",
            "3:4",
            "4:3",
            "16:9",
            "9:16",
            "1:1",
            "21:9"
          ],
          "defaultValue": "adaptive"
        },
        {
          "property": "resolution",
          "cliName": "resolution",
          "description": "分辨率（可选，480P / 720P）",
          "required": false,
          "type": "string",
          "placeholder": "<resolution:480p|720p>",
          "exampleValue": "480p",
          "enumValues": [
            "480p",
            "720p"
          ],
          "defaultValue": "720p"
        },
        {
          "property": "with_sound",
          "cliName": "with-sound",
          "description": "声音（可选，true / false，基于提示词和视觉内容生成人声、音效及背景音乐，建议在提示词内将对话部分置于双引号内)",
          "required": false,
          "type": "boolean",
          "placeholder": "<with-sound:true|false>",
          "exampleValue": "true",
          "defaultValue": true
        }
      ]
    }
  ]
---

## Prompt 写作建议

- 用**中文或英文**均可，清晰描述画面内容、动作、镜头运动
- 可加入风格词：`电影感`、`4K`、`慢镜头`、`航拍`、`写实`等
- 建议长度：50-200字，不超过500字
- 示例好 prompt：`"一位女孩在花海中奔跑，镜头缓慢跟随，阳光透过花瓣散射，电影感，4K"`

---

## 注意事项

- 视频生成需要一定时间，请耐心等待
- 图片 URL 需为**可公开访问的 HTTP/HTTPS 链接**
- `ratio=adaptive` 表示自动适配图片比例（仅图生视频可用）
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `nami-mcp-jimeng` 对应的配置
