---
name: variflight-cloud
description: 航班信息查询工具，支持航班实时状态、航班搜索、中转信息、机场天气、机票价格查询等。当用户需要查询航班、飞机动态、机票、航班号、起降时间、中转路线、机场天气时使用此 skill。触发关键词：航班查询、飞机票、机票、航班号、起飞时间、降落时间、航班动态、中转航班、机场天气、飞行信息、实时航班。
compatibility:
  - server: variflight-cloud
    tools:
      - VariFlightAviation__flightHappinessIndex
      - VariFlightAviation__getFlightTransferInfo
      - VariFlightAviation__getFutureWeatherByAirport
      - VariFlightAviation__getRealtimeLocationByAnum
      - VariFlightAviation__getTodayDate
      - VariFlightAviation__searchFlightItineraries
      - VariFlightAviation__searchFlightsByDepArr
      - VariFlightAviation__searchFlightsByNumber
---

# variflight-cloud — 航班信息查询

VariFlight 航班大数据平台，提供航班搜索、实时动态、中转路线、机场天气、机票价格等全面的航空出行信息。

---

## MCP Access: Use mcporter

**你必须通过 mcporter skill 来操作 MCP，完成本 skill 的所有航班查询任务。** 不得直接调用 MCP 工具；所有 MCP 操作都必须经由 mcporter 路由。

- **配置**：全局 MCP 配置文件位于 `~/.openclaw/workspace/config/mcporter.json`。在使用 mcporter 之前，你必须读取该文件，并**仅使用本 skill 声明的 MCP 服务器/工具对应的配置**（服务器名：`variflight-cloud`）。不得使用配置文件中其他 MCP；只能使用本 skill 明确声明的那些。
- **列出服务器/工具**：`mcporter list variflight-cloud --schema` 查看工具详情。
- **调用工具**：`mcporter call variflight-cloud.<tool> key=value`
- 本 skill 的工具列表定义了可用的 MCP 服务器/工具；请仅通过 mcporter 调用它们，并使用全局配置文件中对应的配置项。

---

## 快速决策

| 需求 | 工具 | 示例 |
|------|------|------|
| 按航班号查询航班 | `VariFlightAviation__searchFlightsByNumber` | `mcporter call variflight-cloud.VariFlightAviation__searchFlightsByNumber fnum="CA1234" date="2024-01-15"` |
| 按出发/到达地查询 | `VariFlightAviation__searchFlightsByDepArr` | `mcporter call variflight-cloud.VariFlightAviation__searchFlightsByDepArr dep="PEK" arr="SHA" date="2024-01-15"` |
| 查询机票价格/可购买航班 | `VariFlightAviation__searchFlightItineraries` | `mcporter call variflight-cloud.VariFlightAviation__searchFlightItineraries dep="PEK" arr="SHA" date="2024-01-15"` |
| 查询中转路线 | `VariFlightAviation__getFlightTransferInfo` | `mcporter call variflight-cloud.VariFlightAviation__getFlightTransferInfo dep="PEK" arr="LAX" date="2024-01-15"` |
| 查询机场天气 | `VariFlightAviation__getFutureWeatherByAirport` | `mcporter call variflight-cloud.VariFlightAviation__getFutureWeatherByAirport airport="PEK"` |
| 查询飞机实时位置 | `VariFlightAviation__getRealtimeLocationByAnum` | `mcporter call variflight-cloud.VariFlightAviation__getRealtimeLocationByAnum anum="B-1234"` |
| 查询航班服务评价 | `VariFlightAviation__flightHappinessIndex` | `mcporter call variflight-cloud.VariFlightAviation__flightHappinessIndex fnum="CA1234" date="2024-01-15"` |
| 获取今日日期 | `VariFlightAviation__getTodayDate` | `mcporter call variflight-cloud.VariFlightAviation__getTodayDate` |

---

## 工具详情

### searchFlightsByNumber — 按航班号查询
```bash
mcporter call variflight-cloud.VariFlightAviation__searchFlightsByNumber fnum="MU2157" date="2024-01-15"
```

### searchFlightsByDepArr — 按出发/到达地查询
机场代码使用 IATA 三字码（如 PEK=北京首都、SHA=上海虹桥、CAN=广州）
```bash
mcporter call variflight-cloud.VariFlightAviation__searchFlightsByDepArr dep="PEK" arr="CAN" date="2024-01-15"
```

### searchFlightItineraries — 查询可购买机票
```bash
mcporter call variflight-cloud.VariFlightAviation__searchFlightItineraries dep="PEK" arr="SHA" date="2024-01-15"
```

### getFutureWeatherByAirport — 机场天气预报（未来3天）
```bash
mcporter call variflight-cloud.VariFlightAviation__getFutureWeatherByAirport airport="PEK"
```

---

## 注意事项

- 调用工具前，请先读取 `~/.openclaw/workspace/config/mcporter.json`，仅使用 `variflight-cloud` 的配置
- 日期格式为 `YYYY-MM-DD`，若用户只提供月日，需先调用 `getTodayDate` 获取年份
- 机场代码使用 IATA 三字码
- 航班号需包含航司代码（如 CA1234、MU2157）
