#!/usr/bin/env node

/**
 * 视频字幕提取脚本
 * 使用阿里云 Qwen-VL 模型识别视频关键帧中的文字
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const https = require('https');

// 配置
const API_KEY = process.env.DASHSCOPE_API_KEY || 'sk-f8abd7b7af1c484e9b93758b5c594fea';
const API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
const MODEL = 'qwen-vl-max-latest';
const TEMP_DIR = path.join(require('os').tmpdir(), 'video-frames');

/**
 * 使用 ffmpeg 提取视频关键帧
 */
function extractFrames(videoPath, outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 每秒提取一帧
  const framePattern = path.join(outputDir, 'frame_%04d.jpg');
  const cmd = `ffmpeg -i "${videoPath}" -vf "fps=1" "${framePattern}" -loglevel quiet`;
  
  try {
    execSync(cmd, { stdio: 'pipe' });
    const frames = fs.readdirSync(outputDir).filter(f => f.endsWith('.jpg'));
    return frames.map(f => path.join(outputDir, f));
  } catch (error) {
    console.error('FFmpeg 提取失败:', error.message);
    console.error('请确保已安装 ffmpeg: https://ffmpeg.org/download.html');
    process.exit(1);
  }
}

/**
 * 图片转 base64
 */
function imageToBase64(imagePath) {
  const data = fs.readFileSync(imagePath);
  return data.toString('base64');
}

/**
 * 识别单帧文字
 */
async function recognizeFrame(imagePath) {
  const base64Image = imageToBase64(imagePath);
  const imageExt = path.extname(imagePath).slice(1);
  const mimeType = `image/${imageExt === 'jpg' ? 'jpeg' : imageExt}`;

  const requestBody = {
    model: MODEL,
    messages: [{
      role: 'user',
      content: [
        {
          type: 'image_url',
          image_url: { url: `data:${mimeType};base64,${base64Image}` }
        },
        {
          type: 'text',
          text: '请识别这张图片中的所有文字内容，保持原有格式。如果是视频截图，请提取字幕、标题、关键信息。用中文回复。'
        }
      ]
    }],
    max_tokens: 2048
  };

  return new Promise((resolve, reject) => {
    const req = https.request(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          resolve(response.choices?.[0]?.message?.content || '');
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(requestBody));
    req.end();
  });
}

/**
 * 主函数
 */
async function processVideo(videoPath, outputFormat = 'text') {
  console.log(`开始处理视频：${videoPath}`);
  
  // 提取关键帧
  const frameDir = path.join(TEMP_DIR, `frames_${Date.now()}`);
  const frames = extractFrames(videoPath, frameDir);
  console.log(`提取了 ${frames.length} 帧`);

  // 逐帧识别
  const results = [];
  for (let i = 0; i < frames.length; i++) {
    const timestamp = new Date(i * 1000).toISOString().substr(14, 8);
    console.log(`处理第 ${i + 1}/${frames.length} 帧...`);
    
    try {
      const text = await recognizeFrame(frames[i]);
      if (text.trim()) {
        results.push({ timestamp, frame: i, text });
      }
    } catch (error) {
      console.error(`第 ${i + 1} 帧识别失败:`, error.message);
    }
  }

  // 输出结果
  if (outputFormat === 'json') {
    console.log(JSON.stringify(results, null, 2));
  } else if (outputFormat === 'srt') {
    // SRT 字幕格式
    results.forEach((r, i) => {
      const nextTime = new Date((i + 1) * 1000).toISOString().substr(14, 8);
      console.log(`${i + 1}`);
      console.log(`${r.timestamp},000 --> ${nextTime},000`);
      console.log(r.text);
      console.log('');
    });
  } else {
    // 纯文本
    results.forEach(r => {
      console.log(`[${r.timestamp}] ${r.text}`);
      console.log('---');
    });
  }

  // 清理临时文件
  try {
    fs.rmSync(frameDir, { recursive: true, force: true });
  } catch (e) {
    // 忽略清理错误
  }
}

// 命令行参数
const videoPath = process.argv[2];
const outputFormat = process.argv[3] || 'text';

if (!videoPath) {
  console.log('用法：video-subtitle.js <video_path> [output_format]');
  console.log('  video_path: 视频文件路径 (mp4, mov, avi, webm)');
  console.log('  output_format: 输出格式 (text|srt|json)，默认为 text');
  process.exit(1);
}

if (!fs.existsSync(videoPath)) {
  console.error(`错误：文件不存在 - ${videoPath}`);
  process.exit(1);
}

processVideo(videoPath, outputFormat).catch(error => {
  console.error('处理失败:', error.message);
  process.exit(1);
});
