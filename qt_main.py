import sys
import os
import yaml
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QTextEdit, QFileDialog, QMessageBox,
    QStatusBar, QMenuBar, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from core import WatermarkCore
import locale

class WatermarkGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = self.get_system_language()
        self.load_config()
        self.init_ui()

    def get_system_language(self):
        try:
            system_lang = locale.getlocale()[0]
            if not system_lang:
                system_lang = locale.getdefaultlocale()[0]
        except:
            system_lang = locale.getdefaultlocale()[0]
        if system_lang and system_lang.startswith('zh'):
            if 'TW' in system_lang or 'HK' in system_lang:
                return 'zh_tw'
            return 'zh_cn'
        return 'en'

    def load_config(self):
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def get_text(self, key_path):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            value = value[key]
        if isinstance(value, dict) and self.current_language in value:
            return value[self.current_language]
        return value

    def init_ui(self):
        self.setWindowTitle(self.get_text('ui.window.title'))
        self.setGeometry(100, 100, self.config['ui']['window']['width'], self.config['ui']['window']['height'])
        self.setWindowIcon(QIcon('logo.ico'))
        self.create_menu_bar()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(self.get_text('ui.status.ready'))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 檔案選擇區
        file_layout = QVBoxLayout()
        # TXT
        txt_layout = QHBoxLayout()
        self.txt_label = QLabel(self.get_text('ui.layout.watermark_content.label'))
        self.txt_path = QLineEdit()
        self.txt_path.setReadOnly(True)
        self.txt_path.setPlaceholderText(self.get_text('ui.layout.watermark_content.placeholder'))
        self.txt_btn = QPushButton(self.get_text('ui.layout.watermark_content.button'))
        self.txt_btn.setStyleSheet(self.config['ui']['style']['button']['normal'])
        self.txt_btn.clicked.connect(self.select_txt)
        txt_layout.addWidget(self.txt_label)
        txt_layout.addWidget(self.txt_path)
        txt_layout.addWidget(self.txt_btn)
        file_layout.addLayout(txt_layout)
        # PDF
        pdf_layout = QHBoxLayout()
        self.pdf_label = QLabel("PDF:")
        self.pdf_path = QLineEdit()
        self.pdf_path.setReadOnly(True)
        self.pdf_path.setPlaceholderText(self.get_text('ui.layout.target_pdf.placeholder'))
        self.pdf_btn = QPushButton(self.get_text('ui.layout.target_pdf.button'))
        self.pdf_btn.setStyleSheet(self.config['ui']['style']['button']['normal'])
        self.pdf_btn.clicked.connect(self.select_pdf)
        pdf_layout.addWidget(self.pdf_label)
        pdf_layout.addWidget(self.pdf_path)
        pdf_layout.addWidget(self.pdf_btn)
        file_layout.addLayout(pdf_layout)
        layout.addLayout(file_layout)

        # 新增目的地資料夾欄位
        self.output_dir_label = QLabel(self.get_text('ui.layout.output_dir.label'))
        self.output_dir_edit = QLineEdit(self)
        self.output_dir_edit.setPlaceholderText(self.get_text('ui.layout.output_dir.placeholder'))
        self.output_dir_btn = QPushButton(self.get_text('ui.layout.output_dir.button'), self)
        self.output_dir_btn.setStyleSheet(self.config['ui']['style']['button']['normal'])
        self.output_dir_btn.clicked.connect(self.choose_output_dir)
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.output_dir_edit)
        output_dir_layout.addWidget(self.output_dir_btn)
        layout.addLayout(output_dir_layout)

        # 浮水印參數
        param_layout = QHBoxLayout()
        self.x_label = QLabel("X：")
        self.x_spin = QSpinBox()
        self.x_spin.setMaximum(40)
        self.x_spin.setValue(5)
        self.y_label = QLabel("Y：")
        self.y_spin = QSpinBox()
        self.y_spin.setMaximum(50)
        self.y_spin.setValue(5)
        self.r_label = QLabel("角度：")
        self.r_spin = QSpinBox()
        self.r_spin.setMaximum(180)
        self.r_spin.setValue(30)
        self.fontsize_label = QLabel("字體大小：")
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setMaximum(500)
        self.fontsize_spin.setSingleStep(5)
        self.fontsize_spin.setValue(90)
        self.trans_label = QLabel("透明度：")
        self.trans_spin = QSpinBox()
        self.trans_spin.setMaximum(100)
        self.trans_spin.setSingleStep(10)
        self.trans_spin.setValue(40)
        param_layout.addWidget(self.x_label)
        param_layout.addWidget(self.x_spin)
        param_layout.addWidget(self.y_label)
        param_layout.addWidget(self.y_spin)
        param_layout.addWidget(self.r_label)
        param_layout.addWidget(self.r_spin)
        param_layout.addWidget(self.fontsize_label)
        param_layout.addWidget(self.fontsize_spin)
        param_layout.addWidget(self.trans_label)
        param_layout.addWidget(self.trans_spin)
        layout.addLayout(param_layout)

        # 控制按鈕
        btn_layout = QVBoxLayout()
        self.start_btn = QPushButton(self.get_text('ui.buttons.start_copy'))
        self.start_btn.setStyleSheet(self.config['ui']['style']['button']['primary'])
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.start_watermark)
        
        clear_btn_layout = QHBoxLayout()
        clear_btn_layout.addStretch()  # 在按钮前添加弹性空间，使按钮靠右
        self.clear_btn = QPushButton(self.get_text('ui.buttons.clear_log'))
        self.clear_btn.setStyleSheet(self.config['ui']['style']['button']['normal'])
        self.clear_btn.clicked.connect(self.clear_log)
        self.clear_btn.setFixedWidth(100)  # 设置固定宽度
        clear_btn_layout.addWidget(self.clear_btn)
        clear_btn_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addLayout(clear_btn_layout)
        layout.addLayout(btn_layout)

        # 日誌區
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # 版權與版本
        bottom_layout = QHBoxLayout()
        self.copyright_label = QLabel(self.get_text('app.copyright'))
        self.copyright_label.setAlignment(Qt.AlignLeft)
        bottom_layout.addWidget(self.copyright_label)
        version_label = QLabel(f"v{self.config['app']['version']}")
        version_label.setStyleSheet("color: gray;")
        version_label.setAlignment(Qt.AlignRight)
        bottom_layout.addWidget(version_label)
        layout.addLayout(bottom_layout)

    def create_menu_bar(self):
        menubar = self.menuBar()
        # 檔案
        file_menu = menubar.addMenu(self.get_text('ui.menu.file'))
        exit_action = QAction(self.get_text('ui.menu.exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        # 說明
        help_menu = menubar.addMenu(self.get_text('ui.menu.help'))
        usage_action = QAction(self.get_text('ui.menu.usage'), self)
        usage_action.triggered.connect(self.show_usage)
        help_menu.addAction(usage_action)
        about_action = QAction(self.get_text('ui.menu.about'), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        # 語言
        language_menu = menubar.addMenu(self.get_text('ui.menu.language'))
        zh_cn_action = QAction("简体中文", self)
        zh_cn_action.triggered.connect(lambda: self.change_language('zh_cn'))
        language_menu.addAction(zh_cn_action)
        zh_tw_action = QAction("繁體中文", self)
        zh_tw_action.triggered.connect(lambda: self.change_language('zh_tw'))
        language_menu.addAction(zh_tw_action)
        en_action = QAction("English", self)
        en_action.triggered.connect(lambda: self.change_language('en'))
        language_menu.addAction(en_action)

    def change_language(self, lang_code):
        self.current_language = lang_code
        self.update_ui_text()

    def update_ui_text(self):
        self.setWindowTitle(self.get_text('ui.window.title'))
        self.statusBar.showMessage(self.get_text('ui.status.ready'))
        
        # 更新菜单栏文本
        menubar = self.menuBar()
        file_menu = menubar.actions()[0]
        file_menu.setText(self.get_text('ui.menu.file'))
        file_menu.menu().actions()[0].setText(self.get_text('ui.menu.exit'))
        
        help_menu = menubar.actions()[1]
        help_menu.setText(self.get_text('ui.menu.help'))
        help_actions = help_menu.menu().actions()
        help_actions[0].setText(self.get_text('ui.menu.usage'))
        help_actions[1].setText(self.get_text('ui.menu.about'))
        
        language_menu = menubar.actions()[2]
        language_menu.setText(self.get_text('ui.menu.language'))
        
        # 更新按钮文本 - 修正键名
        self.txt_btn.setText(self.get_text('ui.layout.watermark_content.button'))
        self.pdf_btn.setText(self.get_text('ui.layout.target_pdf.button'))
        self.start_btn.setText(self.get_text('ui.buttons.start_copy'))
        self.clear_btn.setText(self.get_text('ui.buttons.clear_log'))
        
        # 更新标签文本
        self.txt_label.setText(self.get_text('ui.layout.watermark_content.label'))
        self.pdf_label.setText(self.get_text('ui.layout.target_pdf.label'))
        
        # 更新占位符文本
        self.txt_path.setPlaceholderText(self.get_text('ui.layout.watermark_content.placeholder'))
        self.pdf_path.setPlaceholderText(self.get_text('ui.layout.target_pdf.placeholder'))
        
        # 更新输出目录相关文本
        self.output_dir_label.setText(self.get_text('ui.layout.output_dir.label'))
        self.output_dir_edit.setPlaceholderText(self.get_text('ui.layout.output_dir.placeholder'))
        self.output_dir_btn.setText(self.get_text('ui.layout.output_dir.button'))
        
        # 更新版权信息
        self.copyright_label.setText(self.get_text('app.copyright'))

    def show_usage(self):
        usage_text = "\n".join(self.config['usage_steps'][self.current_language])
        QMessageBox.information(self, self.get_text('ui.menu.usage'), usage_text)

    def show_about(self):
        about_text = f"{self.get_text('app.name')}\n" \
                    f"{self.get_text('app.version')}\n" \
                    f"{self.get_text('app.copyright')}"
        QMessageBox.about(self, self.get_text('ui.menu.about'), about_text)

    def select_txt(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            self.get_text('ui.dialog.select_txt.title'), 
            "", 
            "Text Files (*.txt);;All Files (*.*)"
        )
        if path:
            self.txt_path.setText(path)

    def select_pdf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            self.get_text('ui.dialog.select_pdf.title'), 
            "", 
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        if path:
            self.pdf_path.setText(path)

    def choose_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, 
            self.get_text('ui.dialog.select_output_dir.title')
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)

    def get_font_path(self):
        """获取字体文件路径，支持打包后的应用和本地运行"""
        try:
            if hasattr(sys, '_MEIPASS'):
                # 如果是打包后的应用
                application_path = sys._MEIPASS
                font_path = os.path.join(application_path, 'STHeiti.ttc')
            else:
                # 如果是本地运行
                font_path = os.path.join(os.path.abspath("."), 'STHeiti.ttc')
            
            if not os.path.exists(font_path):
                # 如果找不到字体文件，尝试在系统字体目录中查找
                system_font_paths = [
                    '/System/Library/Fonts/STHeiti.ttc',  # macOS
                    '/Library/Fonts/STHeiti.ttc',         # macOS
                    'C:\\Windows\\Fonts\\STHeiti.ttc',    # Windows
                    '/usr/share/fonts/truetype/STHeiti.ttc'  # Linux
                ]
                for path in system_font_paths:
                    if os.path.exists(path):
                        font_path = path
                        break
                
                if not os.path.exists(font_path):
                    # 如果还是找不到字体文件，使用系统默认字体
                    self.log_text.append("警告：找不到 STHeiti.ttc 字体文件，将使用系统默认字体")
                    return None
            
            return font_path
        except Exception as e:
            self.log_text.append(f"警告：获取字体路径时出错：{str(e)}")
            return None

    def start_watermark(self):
        txt_path = self.txt_path.text()
        pdf_path = self.pdf_path.text()
        output_dir = self.output_dir_edit.text()
        
        # 验证输入
        if not txt_path or not pdf_path or not output_dir:
            QMessageBox.warning(self, self.get_text('ui.messages.error'), 
                               self.get_text('ui.messages.no_output_dir'))
            return
        
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, self.get_text('ui.messages.error'),
                                   f"无法创建输出目录：{str(e)}")
                return
        
        # 获取字体路径
        font_path = self.get_font_path()
        if not font_path:
            reply = QMessageBox.question(self, 
                                       self.get_text('ui.messages.warning'),
                                       "未找到指定字体，是否使用系统默认字体继续？",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        params = {
            'txt_path': txt_path,
            'pdf_path': pdf_path,
            'font_path': font_path,
            'water_x': self.x_spin.value(),
            'water_y': self.y_spin.value(),
            'water_r': self.r_spin.value(),
            'water_font_size': self.fontsize_spin.value(),
            'water_trans': self.trans_spin.value(),
            'output_dir': output_dir,
        }
        
        try:
            core = WatermarkCore(**params)
            
            # 读取名字文件
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    names = [line.strip() for line in f if line.strip()]
            except Exception as e:
                QMessageBox.critical(self, self.get_text('ui.messages.error'),
                                   f"无法读取名字文件：{str(e)}")
                return
            
            if not names:
                QMessageBox.warning(self, self.get_text('ui.messages.warning'),
                                  "名字文件为空")
                return
            
            # 对每个名字产生水印并加到 PDF
            for name in names:
                try:
                    # 直接使用 create_watermark 产生水印 PDF
                    mark_pdf = core.create_watermark(name)
                    # 组合输出文件路径
                    pdf_base = os.path.splitext(os.path.basename(pdf_path))[0]
                    output_pdf_name = f"{pdf_base}_{name}.pdf"
                    output_pdf_path = os.path.join(output_dir, output_pdf_name)
                    # 将水印加到原始 PDF
                    core.add_watermark(pdf_path, mark_pdf, output_pdf_path)
                    self.log_text.append(f"完成：{output_pdf_path}")
                except Exception as e:
                    self.log_text.append(f"处理 {name} 时出错：{str(e)}")
                    continue
            
            self.statusBar.showMessage(self.get_text('ui.status.complete'))
            QMessageBox.information(self, self.get_text('ui.messages.success'), 
                                  self.get_text('ui.messages.success'))
        except Exception as e:
            self.log_text.append(f"错误：{str(e)}")
            self.statusBar.showMessage(self.get_text('ui.status.error').format(str(e)))
            QMessageBox.critical(self, self.get_text('ui.messages.error'), str(e))

    def clear_log(self):
        self.log_text.clear()

def main():
    app = QApplication(sys.argv)
    window = WatermarkGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 