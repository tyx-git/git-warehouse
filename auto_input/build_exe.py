import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 图标路径
icon_path = os.path.join(current_dir, 'python.png')

# 打包参数
params = [
    'auto_input_tool.py',  # 主程序文件
    '--name=自动输入工具-V1.0',  # 生成的exe名称
    '--windowed',  # 使用GUI模式
    f'--icon={icon_path}',  # 图标
    '--noconfirm',  # 覆盖输出目录
    '--clean',  # 清理临时文件
    '--add-data=python.png;.',  # 添加图标文件
]

# 执行打包
PyInstaller.__main__.run(params) 