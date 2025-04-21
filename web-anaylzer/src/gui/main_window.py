import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QFileDialog, QMessageBox,
                           QTextEdit, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from src.analyzer.log_analyzer import LogAnalyzer
from src.analyzer.report_generator import ReportGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analyzer = None
        self.setup_ui()
        self.setup_menu()
        
    def setup_ui(self):
        """设置主窗口UI"""
        self.setWindowTitle('Web日志分析系统')
        self.setMinimumSize(1000, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)
        
        self.open_button = QPushButton('打开日志文件')
        self.open_button.setIcon(QIcon.fromTheme('document-open'))
        self.open_button.clicked.connect(self.open_log_file)
        
        self.export_button = QPushButton('导出报告')
        self.export_button.setIcon(QIcon.fromTheme('document-save'))
        self.export_button.clicked.connect(self.export_report)
        self.export_button.setEnabled(False)
        
        toolbar_layout.addWidget(self.open_button)
        toolbar_layout.addWidget(self.export_button)
        toolbar_layout.addStretch()
        
        # 创建日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont('Consolas', 10))
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 添加组件到主布局
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.log_display)
        
    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        open_action = file_menu.addAction('打开日志文件')
        open_action.triggered.connect(self.open_log_file)
        
        export_action = file_menu.addAction('导出报告')
        export_action.triggered.connect(self.export_report)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        about_action = help_menu.addAction('关于')
        about_action.triggered.connect(self.show_about)
        
    def open_log_file(self):
        """打开日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择日志文件',
            '',
            '日志文件 (*.log);;所有文件 (*.*)'
        )
        
        if file_path:
            try:
                # 创建分析器
                self.analyzer = LogAnalyzer()
                
                # 读取并处理日志文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        self.analyzer.process_log(line.strip())
                
                # 更新UI
                self.log_display.setText(f'已加载日志文件：{file_path}\n')
                self.log_display.append(f'总请求数：{self.analyzer.total_requests}')
                self.log_display.append(f'独立IP数：{len(self.analyzer.unique_hosts)}')
                
                # 启用导出按钮
                self.export_button.setEnabled(True)
                
                # 更新状态栏
                self.statusBar.showMessage(f'已加载日志文件：{file_path}')
                
            except Exception as e:
                QMessageBox.critical(self, '错误', f'加载日志文件失败：{str(e)}')
                
    def export_report(self):
        """导出分析报告"""
        if not self.analyzer:
            QMessageBox.warning(self, '警告', '请先加载日志文件')
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '导出报告',
            '',
            'HTML文件 (*.html)'
        )
        
        if file_path:
            try:
                # 创建报告生成器
                report_generator = ReportGenerator(self.analyzer)
                
                # 生成报告
                report_generator.generate_report(
                    output_path=file_path,
                    time_range='全部时间'
                )
                
                QMessageBox.information(self, '成功', '报告已成功导出')
                self.statusBar.showMessage(f'报告已导出：{file_path}')
                
            except Exception as e:
                QMessageBox.critical(self, '错误', f'导出报告失败：{str(e)}')
                
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            '关于',
            'Web日志分析系统 v1.0\n\n'
            '一个用于分析Web服务器日志的工具。'
        ) 