# from collections import OrderedDict
# 现今只能在python3.6以及3.7使用。因为这两版本保证dict顺序
# 重复key操作 请用中划线-分割 比如success- or success--
testCase1 = {
    'type': 1,  # 0接口测试 1：webUI测试 2：APP
    'safe': 0,  # 是否测试注入
    'get': {  # get & post
        'url': 'https://sso.120ask.com/user/login',
        'params': {},
        'header': {},
        'cookie': {}
    },
    'interaction': [
        # {'element': '@手机快速登录', 'action': {'click': None}},
        {'element': '#username', 'action': {'write': 'xxxx'}},
        {'element': '#password', 'action': {'write': 'xxxx'}},
        {'element': '#submit', 'action': {'click': None}}
    ],
    'success': {
        # 'httpCode': 200,
        # 'text': '快速问医生',
        'element':'@我的提问'
    }
}

# testCase2 = {
#     'type': 0,  # 0接口测试 1：webUI测试 2：APP
#     'safe': 0,  # 是否测试注入
#     'get': {  # get & post
#         'url': 'https://www.120.net',
#         'params': {},
#         'header': {},
#         'cookie': {}
#     },
#     'success-':{
#         'httpCode': 200
#     },
#     # 'interaction': [
#     #     {'element': '#id .class', 'action': {'write': 'value'}}
#     # ],
#     # 'success': {
#         # 'text': '快速问医生'
#     # }
#     #
# }
