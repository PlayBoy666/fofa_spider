fofa_spider

直接修改config.py里面的配置选项，然后直接执行脚本python fofa.py

配置选项说明：

#mongodb数据库配置

MONGO_URL = 'localhost'

MONGO_DB = 'taobao'

MONGO_TABLE = 'product'


#fofa配置账号密码选项

FOFA_USERNAME='XXXX@qq.com'

FOFA_PASSWORD='XXXXXXXX'

#搜索语法

FOFA_SEARCH_KEYWORD='app="Apache-Tomcat"'

#要翻到多少页

PAGE='5'

#phantomjs设置（开启不加载图片和开启磁盘缓存）

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
