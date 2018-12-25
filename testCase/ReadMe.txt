# 现今只能在python3.6以及3.7使用。因为这两版本保证dict顺序
# 重复key操作 请用中划线-分割 比如success- or success--


测试用例名称 = {
    'type': 0,  # 0接口测试 1：webUI测试 2：APP
    'safe': 0,  # 是否测试注入
    'get': {  # get & post
        'url': 'https://xxxx',
        'params': {},
        'header': {},
        'cookie': {}
    },
    'success-':{
        'httpCode': 300
    },

  
    #和页面交互动作 列表。可以多个会按照列表顺序依次执行
    #如果没有找到元素，比如ajax加载的页面，会等待5秒再查找，还没有找到会报错
    'interaction':[ 

        {
            #除了本身的# & . 还提供  
            #"!": "xpath",
            #"@": "link text",
            #"$": "name",
            #"%": "tag name"
            #action有 
            #write 写入数据
            #clear 清空 value为None
            #click 点击 value为None
            #execute 执行js value为可执行的js代码

            'element':'需要查找的元素，结构和jquey一样','action':{'write':'value'},

            #操作完成是否会开新页面，有开新页后续操作都会在新页面执行
            'newpage':'yes/no'
        },
        {
            'element':'需要查找的元素，结构和jquey一样','action':{'write':'value'},
            #操作完成是否会开新页面
            'newpage':'yes/no' 
        }
    ],
    #断言是否成功
    'success':{
        'httpCode':200, #http状态码 
        'content':'成功' #页面源码是否包含文字
        'element':'#id .class' #页面是否包含特定的元素 暂未实现
    },
    #出错之后的处理 暂未实现
    'error':{}
}
