# Web Analyzer

一个基于Python的Web数据分析工具，提供数据采集、分析和可视化功能。

## 项目概述

Web Analyzer是一个功能强大的Web数据分析工具，它能够：
- 采集网页数据
- 分析数据特征
- 生成可视化报告
- 提供友好的图形用户界面

## 技术栈

- Python 3.x
- PyQt5 (GUI框架)
- MySQL (数据存储)
- Pandas (数据处理)
- Matplotlib (数据可视化)
- PyQtGraph (实时图表)
- 其他依赖详见requirements/base.txt

## 项目结构

```
web-anaylzer/
├── src/                    # 源代码目录
│   ├── main.py            # 程序入口
│   ├── gui/               # 图形界面相关代码
│   ├── analyzer/          # 数据分析模块
│   ├── collector/         # 数据采集模块
│   ├── parser/            # 数据解析模块
│   ├── storage/           # 数据存储模块
│   ├── services/          # 服务层
│   └── config/            # 配置管理
├── requirements/          # 依赖管理
│   └── base.txt          # 基础依赖
├── config/               # 配置文件
├── scripts/              # 脚本文件
├── var/                  # 运行时数据
└── .venv/                # Python虚拟环境
```

## 主要功能

1. **数据采集**
   - 支持多种数据源
   - 可配置的采集策略
   - 自动数据更新

2. **数据分析**
   - 数据清洗和预处理
   - 统计分析
   - 趋势分析
   - 异常检测

3. **数据可视化**
   - 实时图表
   - 交互式仪表盘
   - 自定义报告生成

4. **用户界面**
   - 直观的操作界面
   - 实时数据展示
   - 配置管理

## 安装说明

2. 创建并激活虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements/base.txt
```

## 使用说明

1. 启动程序
```bash
python src/main.py
```

2. 配置数据源
   - 在config目录下配置数据源信息
   - 设置采集参数

3. 开始分析
   - 选择数据源
   - 设置分析参数
   - 查看分析结果

## 开发说明

- 遵循PEP 8编码规范
- 使用Git进行版本控制
- 提交代码前进行测试

## 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request
