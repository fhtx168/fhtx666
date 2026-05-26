# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 📈 投资数据源配置

### Tushare（备用数据源）

**API Token**: `<待填写，注册 https://tushare.pro 获取>`

**用途**: AKShare 故障时自动切换

**权限**: 基础权限（免费）— 行情/财务/估值/股东数据

### AKShare（首选数据源）

**状态**: ✅ 已配置，但连接不稳定

**用途**: A 股实时行情、财务指标、估值数据

### 数据源切换逻辑

```
优先级：AKShare → Tushare → 本地缓存
```

---

## 📍 投资持仓（6 只核心标的）

| 代码 | 名称 | 评级 | 仓位 |
|------|------|------|------|
| 688008 | 澜起科技 | S++ | 25% |
| 688037 | 芯源微 | S+ | 20% |
| 300620 | 光库科技 | S+ | 待建仓 |
| 002222 | 福晶科技 | S+ | 待建仓 |
| 300684 | 中石科技 | S+ | 暂缓 |
| 002335 | 科华数据 | S | 暂缓 |
