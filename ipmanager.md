环境： Python 3.6.8, Centos7.6
1、创建 venv
```
mkdir ipmanager
cd ipmanager
python3 -m venv venv
```
2、安装 flask
```
source venv/bin/activate
pip install flask
```
3、设置 flask 环境变量，在 .flaskenv 文件中写入 flask 环境变量
```
pip install python-dotenv
```
4、引入 Flask-WTF 插件来处理表单
```
pip install flask-wtf
```
5、数据库 ORM、迁移插件
```
pip install flask-sqlalchemy
pip install flask-migrate
```
6、登录
```
pip install flask-login
```
7、开启调试模式，生产环境禁用
```
export FLASK_DEBUG=1
```
8、使用 bootstrap 美化
```
pip install flask-bootstrap
```
9、使用 elasticsearch 提供搜索服务
```
pip install elasticsearch
```


注意事项：
1、.flaskenv 文件中写入 FLASK_RUN_PORT != 6000，否则不会生效，无法访问 web
```
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=8050
```
2、多个 flask 应用在同一 server、同一浏览器访问，会出现登录失败问题 