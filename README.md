## 安装环境

> pip install -r requirements.txt

## 运行

> python main.py

## 打包

> pyinstaller --clean --hidden-import AmazonSpiders.settings --hidden-import AmazonSpiders.middlewares --hidden-import AmazonSpiders.pipelines -F .\main.py
