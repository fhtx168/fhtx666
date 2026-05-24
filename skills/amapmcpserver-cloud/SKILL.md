---
name: 高德地图（导航/搜索/天气/路径规划）
description: 高德地图完整工具集，支持地理编码、路径规划（驾车/步行/骑行/公交）、周边搜索、关键词搜索、距离测量、天气查询、IP定位、行程规划地图、打车导航唤起。当用户需要"导航"、"路线规划"、"周边搜索"、"天气"、"地址转坐标"时，加载此 skill。
---

# 高德地图（导航/搜索/天气/路径规划）

高德地图完整工具集，共 **15 个工具**，覆盖导航、搜索、天气等全部地图服务。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有地图任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。读取该文件并**仅使用 `amapmcpserver-cloud` 对应的配置**。
- **列出工具**：`mcporter list amapmcpserver-cloud --schema`
- **调用工具**：`mcporter call amapmcpserver-cloud.<tool> key=value`

---

## 快速决策

**地址转坐标（地理编码）**
```
mcporter call amapmcpserver-cloud.maps_geo address="北京市朝阳区三里屯"
```

**坐标转地址（逆地理编码）**
```
mcporter call amapmcpserver-cloud.maps_regeocode location="116.481488,39.990464"
```

**查询天气**
```
mcporter call amapmcpserver-cloud.maps_weather city="北京"
```

**驾车路线规划**
```
mcporter call amapmcpserver-cloud.maps_direction_driving \
  origin="116.481488,39.990464" destination="116.434446,39.90816"
```

**步行路线规划**
```
mcporter call amapmcpserver-cloud.maps_direction_walking \
  origin="116.481488,39.990464" destination="116.434446,39.90816"
```

**公共交通路线规划（含跨城）**
```
mcporter call amapmcpserver-cloud.maps_direction_transit_integrated \
  origin="116.481488,39.990464" destination="121.473701,31.230416" \
  city="北京" cityd="上海"
```

**骑行路线规划**
```
mcporter call amapmcpserver-cloud.maps_direction_bicycling \
  origin="116.481488,39.990464" destination="116.434446,39.90816"
```

**周边搜索（餐厅/超市等）**
```
mcporter call amapmcpserver-cloud.maps_around_search \
  keywords="餐厅" location="116.481488,39.990464" radius="1000"
```

**关键词搜索POI**
```
mcporter call amapmcpserver-cloud.maps_text_search keywords="故宫" city="北京"
```

**IP定位**
```
mcporter call amapmcpserver-cloud.maps_ip_location ip="114.114.114.114"
```

**唤起高德地图导航**
```
mcporter call amapmcpserver-cloud.maps_schema_navi lon="116.434446" lat="39.90816"
```

**唤起打车**
```
mcporter call amapmcpserver-cloud.maps_schema_take_taxi \
  dlon="116.434446" dlat="39.90816" dname="天安门"
```

---

## 工具全览

| 工具名 | 功能 |
|--------|------|
| `maps_geo` | 地址转坐标（地理编码） |
| `maps_regeocode` | 坐标转地址（逆地理编码） |
| `maps_weather` | 天气查询 |
| `maps_direction_driving` | 驾车路线规划 |
| `maps_direction_walking` | 步行路线规划（≤100km） |
| `maps_direction_bicycling` | 骑行路线规划（≤500km） |
| `maps_direction_transit_integrated` | 公共交通路线规划 |
| `maps_distance` | 距离测量（驾车/步行/直线） |
| `maps_around_search` | 周边POI搜索 |
| `maps_text_search` | 关键词POI搜索 |
| `maps_search_detail` | POI详情查询 |
| `maps_ip_location` | IP定位 |
| `maps_schema_navi` | 唤起高德导航（返回URI链接） |
| `maps_schema_take_taxi` | 唤起打车（返回URI链接） |
| `maps_schema_personal_map` | 生成行程规划地图（返回URI链接） |

---

## 注意事项

- 坐标格式：**经度,纬度**（如 `116.481488,39.990464`）
- `maps_schema_navi`、`maps_schema_take_taxi`、`maps_schema_personal_map` 返回 URI 链接，**直接展示给用户，不需要总结**
- 调用前请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `amapmcpserver-cloud` 对应的配置
