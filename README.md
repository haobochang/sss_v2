# 量化投资组合管理系统

基于统一投资组合节点树的量化投资管理系统，支持多层次策略配置、持仓跟踪和交易管理。

## 技术栈

### 后端
- Python 3.12
- FastAPI
- MongoDB
- Pydantic
- Uvicorn

### 前端
- React 18
- TypeScript
- Ant Design
- ECharts
- React Router

## 项目结构

```
sss_v2/
├── src/                    # 后端源码
│   ├── api/               # FastAPI应用
│   │   ├── main.py        # 主应用
│   │   └── routers/       # 路由模块
│   ├── core/              # 核心模块
│   │   ├── models.py      # 基础模型
│   │   └── quantitative_models.py  # 量化模型
│   ├── config/            # 配置模块
│   └── utils/             # 工具模块
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── services/      # API服务
│   │   └── types/         # TypeScript类型
│   └── package.json
├── docs/                  # 文档和图表
├── start_backend.py       # 后端启动脚本
└── pyproject.toml         # Python依赖配置
```

## 核心功能

### 1. 统一投资组合节点树
- **产品层**: 管理整体投资组合
- **投资策略层**: 中性策略、择时策略等
- **策略组合层**: 策略池管理
- **基准策略层**: 具体的Alpha模型

### 2. 持仓跟踪
- 支持目标持仓和实际持仓对比
- 多层次持仓聚合和分发
- 实时市值和盈亏计算

### 3. 交易管理
- 从底层策略向上聚合交易指令
- 交易执行结果向下分发
- 完整的交易链路追踪

### 4. 可视化界面
- 产品列表页面：统计图表和产品概览
- 产品详情页面：树形结构展示和节点详情
- 中性策略敞口分析
- 持仓分布图表

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.12
- Node.js 18+
- MongoDB (本地运行)

### 2. 安装依赖

```bash
# 安装Python依赖
uv install

# 安装前端依赖
cd frontend
npm install
```

### 3. 启动MongoDB

```bash
# 启动本地MongoDB服务
mongod --dbpath /path/to/data/db
```

### 4. 初始化数据

```bash
# 初始化测试数据
uv run python src/init_data.py
```

### 5. 启动服务

```bash
# 启动后端服务 (端口8000)
uv run python start_backend.py

# 启动前端服务 (端口3000)
cd frontend
npm start
```

### 6. 访问应用

- 前端界面: http://localhost:3000
- API文档: http://localhost:8000/docs
- API健康检查: http://localhost:8000/health

## API接口

### 产品管理
- `GET /api/products` - 获取产品列表
- `GET /api/products/{id}` - 获取产品详情
- `GET /api/products/{id}/tree` - 获取产品树结构

### 持仓管理
- `GET /api/positions` - 获取持仓列表
- `GET /api/positions/node/{id}` - 获取节点持仓

### 交易管理
- `GET /api/trades` - 获取交易列表
- `GET /api/trades/{id}` - 获取交易详情

## 数据模型

### PortfolioNode (投资组合节点)
- 统一的节点模型，支持所有层级
- 节点类型：PRODUCT, INVESTMENT_STRATEGY, STRATEGY_POOL, BASE_STRATEGY
- 配置详情以JSON格式存储

### PortfolioHierarchy (层级关系)
- 定义节点间的父子关系和权重
- 支持时间版本管理

### NodePosition (节点持仓)
- 统一的持仓模型
- 支持TARGET和ACTUAL两种持仓类型
- 包含市值、成本价、权重等信息

### TradeOrder & TradeAllocation (交易管理)
- 产品级交易指令
- 底层策略贡献分配

## 开发指南

### 后端开发
```bash
# 运行测试
uv run python -m pytest

# 代码格式化
uv run ruff format src/
```

### 前端开发
```bash
cd frontend

# 开发模式
npm start

# 构建生产版本
npm run build

# 运行测试
npm test
```

## 部署

### 生产环境部署
1. 构建前端
```bash
cd frontend
npm run build
```

2. 配置生产环境变量
3. 使用生产级WSGI服务器部署FastAPI
4. 配置Nginx反向代理

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
