weblog-analyzer/
├── config/                          
│   ├── app_config.yaml             #主配置文件
│   ├── database/
│   │   └── mysql_config.yaml       #数据库配置文件
│   └── log_patterns/
│       ├── apache.yaml             #Apache日志格式配置文件
│       └── custom/
├── var/log                         #日志保存
├── scripts/                        #部署和维护脚本
│   ├── deploy.sh                   # 部署脚本
│   ├── db_migration/
│   │   └── migrate_v1.py           # 数据库迁移脚本
│   └── backup.sh                   # 备份脚本
├── src/
│   ├── config/
│   │   └── loader.py               # 配置加载器
│   ├── services/
│   │   ├── collector_service.py    # 日志采集服务
│   │   └── analysis_service.py     # 分析服务
│   ├── collector/                  # 日志采集模块
│   │   ├── sources/                # 数据源实现
│   │   │   └── file_source.py
│   │   ├── processors/             # 预处理
│   │   │   └── apache_processor.py # Apache专用处理器
│   │   └── storage/
│   │       └── buffer.py           # 临时存储
│   ├── parser/                     # 日志解析模块
│   │   └── engines/                # 解析引擎
│   │       └── apache_engine.py    # Apache解析引擎
│   ├── analyzer/                   # 统计分析模块
│   │   └── apache_analyzer.py      # Apache专用分析
│   ├── storage/                    # 数据存储模块(MySQL为主)
│   │   ├── connectors/             # 数据库连接器
│   │   │   └── mysql_conn.py       # MySQL连接器
│   │   └── models/                 # 数据模型
│   │       ├── apache_log.py       # Apache日志模型
│   │       └── analysis_result.py  # 分析结果模型
│   ├── ui/                         # 前端界面
│   │   └── main_window.py          # 主窗口
│   └── main.py                     # 主入口
├── requirements/                   # 依赖管理
│   ├── base.txt                    # 基础依赖
│   ├── dev.txt                     # 开发环境依赖
│   └── prod.txt                    # 生产环境依赖
└── README.md                       # 项目文档