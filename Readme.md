### 部署 

#### 平台环境配置

```python
# 安装了anaconda的用户可以创建虚拟环境，方便部署
conda create -n NBADBA python=3.8 -y
conda activate NBADBA
# 也可以通过python 3.8, 跳过前面两步
pip install -r requirements.txt
```

#### 数据导入

```mysql
mysql -h localhost -u root -p
create schema NBADBA;
use NBADBA;
source 'path to final_project.sql'
```

#### 连接数据库

于文件 NBA\settings.py 第81行数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NBADBA',
        'USER':'root',
        'PASSWORD':'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

使用本机作为服务器的话，将数据库名字，用户和密码配置好即可。HOST和PORT可以继续使用上述配置。

#### 启动系统

以本机作为服务器，启动网页

```python
python manage.py runserver
```

会显示：

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

打开浏览器，访问http://127.0.0.1:8000/，即可进入数据库系统。
