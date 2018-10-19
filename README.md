# unittest_model
基于 unittest 实现的简单的通过配置自动实现自动化测试代码
还有很多功能没有实现。
现在实现的接口测试，是为了校长作业o(╥﹏╥)o 
欢迎补充
------
##python版本
3.0+
------
##安装依赖
```python
pip3 install requests
ppi3 install selenium
```
##安装chrome headless 【centos 7】
```bash
yum -y install libappindicator-gtk3
yum -y install libXss
yum -y install xdg-utils
yum -y install libXScrnSaver
rpm -ivh google-chrome-stable-69.0.3497.100-1.x86_64.rpm ##rpm包在driver下
yum install bitmap-fonts bitmap-fonts-cjk ##不安装截图无法显示中文
```

#目录结构
* config  -- 配置文件
* data    -- 数据文件，测试截图一类的
* pubTest -- 公共方法
* report  -- 测试结果文件
* testCase-- 测试实例配置文件 程序会自动读取 后缀为_test的Py文件
* main.py -- 运行入口

#testCase配置文件
请查看testCase目录下的ReadMe.txt
