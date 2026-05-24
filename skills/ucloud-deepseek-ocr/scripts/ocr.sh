#!/usr/bin/env node

/**
 * DeepSeek OCR - 图片文字识别脚本
 * 使用 DeepSeek-OCR 模型识别图片中的文字
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 配置
const API_KEY = process.env.DEEPSEEK_API_KEY || 'sk-106f9d3972484484ac520c2b28ac48ca';
const API_URL = process.env.DEEPSEEK_OCR_API_URL || 'https://api.modelverse.cn/v1/chat/completions';
const MODEL = 'deepseek-ocr-v1';

async function imageToBase64(imagePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(imagePath, (err, data) => {
      if (err) reject(err);
      else resolve(data.toString('base64'));
    });
  });
}

async function ocr(imagePath, outputFormat = 'markdown') {
  try {
    // 检查文件是否存在
    if (!fs.existsSync(imagePath)) {
      console.error(`错误：文件不存在 - ${imagePath}`);
      process.exit(1);
    }

    // 转换为 base64
    const base64Image = await imageToBase64(imagePath);
    const imageExt = path.extname(imagePath).toLowerCase().slice(1);
    const mimeType = `image/${imageExt === 'jpg' ? 'jpeg' : imageExt}`;
    
    // 构建请求
    const requestBody = {
      model: MODEL,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'image_url',
              image_url: {
                url: `data:${mimeType};base64,${base64Image}`
              }
            },
            {
              type: 'text',
              text: outputFormat === 'json' 
                ? '请提取图片中的所有内容，并以 JSON 格式返回，包括文字、表格等结构化信息。'
                : '请准确识别并提取这张图片中的所有文字内容，保持原有的格式和结构。如果是中文图片，请用中文回复。'
            }
          ]
        }
      ],
      max_tokens: 4096
    };

    // 发送请求
    const response = await new Promise((resolve, reject) => {
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
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`解析响应失败：${e.message}`));
          }
        });
      });

      req.on('error', reject);
      req.write(JSON.stringify(requestBody));
      req.end();
    });

    // 处理响应
    if (response.error) {
      console.error('API 错误:', response.error.message || response.error);
      process.exit(1);
    }

    const result = response.choices?.[0]?.message?.content;
    
    if (!result) {
      console.error('未识别到任何内容');
      process.exit(1);
    }

    // 输出结果
    if (outputFormat === 'text') {
      // 纯文本输出，去除 markdown 格式
      console.log(result.replace(/[#*_~`]/g, '').trim());
    } else {
      // 默认 markdown 格式
      console.log(result);
    }

  } catch (error) {
    console.error('OCR 识别失败:', error.message);
    process.exit(1);
  }
}

// 主函数
const imagePath = process.argv[2];
const outputFormat = process.argv[3] || 'markdown';

if (!imagePath) {
  console.log('用法：ocr.sh <image_path> [output_format]');
  console.log('  image_path: 图片文件路径 (jpg, png, webp, gif, bmp)');
  console.log('  output_format: 输出格式 (markdown|text|json)，默认为 markdown');
  process.exit(1);
}

ocr(imagePath, outputFormat);
