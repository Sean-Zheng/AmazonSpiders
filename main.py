import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QRadioButton, QDesktopWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTextBrowser
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from AmazonSpiders.spiders.Commodities import CommoditiesSpider
from AmazonSpiders.spiders.JPAmazon import JpamazonSpider
from AmazonSpiders.spiders.USAmazon import UsamazonSpider
from AmazonSpiders.log import read_log


def start_crawl(search, website):
    process = CrawlerProcess(get_project_settings())
    if website == 'jp':
        process.crawl(JpamazonSpider, search)
    elif website == 'us':
        process.crawl(UsamazonSpider, search)
    else:
        return
    process.start()


class AppWindows(QWidget):
    def __init__(self):
        super().__init__()
        # 设置窗口标题及图标
        self.setWindowTitle('Amazon商品信息分析')
        self.setWindowIcon(QIcon('icon.ico'))
        # 设置窗口居中显示
        fg = self.frameGeometry()
        fg.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(fg.topLeft())
        # 固定窗口大小
        self.setFixedSize(1200, 675)
        # 添加水平主布局
        self.main_layout = QHBoxLayout(self)
        # 设置四周margin
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # 设置控件间间距
        self.main_layout.setSpacing(0)
        # 初始化控制窗口
        self.__init_control_widget()
        # 初始化显示窗口
        self.__init_show_widget()
        self.show()

    # 控制窗口控件
    def __init_control_widget(self):
        self.control_widget = QWidget()
        control_layout = QVBoxLayout(self.control_widget)
        self.control_widget.setFixedWidth(400)
        # self.control_widget.setStyleSheet('QWidget{background-color:blue}')
        self.main_layout.addWidget(self.control_widget, alignment=Qt.AlignLeft)

        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_label = QLabel()
        search_label.setText('搜索关键字')
        self.search_editer = QLineEdit()
        self.search_editer.setPlaceholderText('亚马逊搜索关键字')
        # self.search_editer.setFixedHeight(0)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_editer)

        keywords_widget = QWidget()
        keywords_layout = QHBoxLayout(keywords_widget)
        keywords_label = QLabel()
        keywords_label.setText('筛选关键字')
        self.keywords_editer = QLineEdit()
        self.keywords_editer.setPlaceholderText('请用;分隔搜索关键字')
        keywords_layout.addWidget(keywords_label)
        keywords_layout.addWidget(self.keywords_editer)

        # control_layout.addWidget(QLabel('请用;分割搜索关键字'))

        select_widget = QWidget()
        select_layout = QHBoxLayout(select_widget)
        self.jp_amazon = QRadioButton('日本亚马逊')
        self.us_amazon = QRadioButton('美国亚马逊')
        self.jp_amazon.setChecked(True)
        select_layout.addWidget(self.jp_amazon)
        select_layout.addWidget(self.us_amazon)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        self.clean_btn = QPushButton('清除')
        self.clean_btn.clicked.connect(self.__clean)
        self.search_btn = QPushButton('搜索')
        self.search_btn.clicked.connect(self.__search)
        button_layout.addWidget(self.search_btn)
        button_layout.addWidget(self.clean_btn)

        control_layout.addWidget(search_widget)
        control_layout.addWidget(keywords_widget)
        control_layout.addWidget(select_widget)
        control_layout.addWidget(button_widget)

    # 显示窗口控件

    def __init_show_widget(self):
        self.show_widget = QTabWidget()
        self.show_widget.setFixedWidth(800)
        # self.show_widget.setStyleSheet('QWidget{background-color:red}')
        self.main_layout.addWidget(self.show_widget, alignment=Qt.AlignLeft)
        self.__init_result_widget()
        self.__init_log_widget()

    # 日志窗口控件
    def __init_log_widget(self):
        self.log_widget = QWidget()
        self.log_text = QTextBrowser(self.log_widget)
        self.log_text.resize(793, 650)
        self.show_widget.addTab(self.log_widget, "日志")

    # 结果窗口控件
    def __init_result_widget(self):
        self.result_widget = QWidget()
        self.result_text = QTextBrowser(self.result_widget)
        self.result_text.resize(793, 650)
        # setStyleSheet("QTextBrowser{border-width:0;border-style:outset}");
        self.result_text.setText('sdfadsfdsa')
        self.show_widget.addTab(self.result_widget, "结果")

    @pyqtSlot()
    def __search(self):
        # 获取所要搜索的商品名称
        search = self.search_editer.text()
        # 判断选择的网址
        website = 'jp' if self.jp_amazon.isChecked() == True else 'us'
        print('开始搜索{}:{}'.format(search, website))
        start_crawl(search, website)
        print('OVER')
        self.log_text.setText(read_log())

    @pyqtSlot()
    def __clean(self):
        self.search_editer.setText('')
        self.keywords_editer.setText('')
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindows()
    sys.exit(app.exec_())
    pass
