'''
Author: gumpcpy gumpcpy@gmail.com
Date: 2023-02-11 12:46:23
LastEditors: gumpcpy gumpcpy@gmail.com
LastEditTime: 2023-07-21 16:56:38
Description: 
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys,time
import layout

# Author: Chen Pei Yu @2023       
        
StyleSheet = """

#label_11{
    background-color: #D5EFEB; /*背景颜色*/
    border-radius: 5px;
    color: #000;
    
}

#label{
    background-color: #D5EFEB; /*背景颜色*/
    border-radius: 5px;
    color: #000;
    
}

QPushButton{
    border: 1px solid #555;
    border-radius: 6px;
    background-color: #D5EFEB; /*背景颜色*/
    margin:2px;
    color: #000;
}
QPushButton:hover {
    background-color: #B0CFDE; /*鼠标悬停时背景颜色*/
    color: #000;
}

QPushButton:pressed {
    background-color: #AFDCEC; /*鼠标按下不放时背景颜色*/
    color: #000;
}


#progressBar {
    border: 1px solid grey;
    border-radius: 3px;
    background-color: transparent;
    text-align: center;
    qproperty-textVisible: false; /* 文本可见属性设为false，即为不可见 */
    height: 8px;
    margin:2px;
    color: #000;
}

#progressBar::chunk {
  background-color: #83E800;
  width: 8px; /* 进度块宽度，垂直进度条则使用height */
  margin: 0.5px; /* 进度块间隔 */
  /* width与margin同时使用，可显示进度块 */
  color: #000;
}

"""

class PluginApp(QtWidgets.QMainWindow, layout.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PluginApp, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    form = PluginApp()
    form.show()
    app.exec_()
    

    

if __name__ == '__main__':
        
    main()