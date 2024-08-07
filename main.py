import streamlit as st
from utils import get_chat_response
from langchain.memory import ConversationBufferWindowMemory
import pandas as pd

# 创建一个侧边栏
with st.sidebar:
    # 侧边栏中要让用户输入自己的api密钥，并才用密码的形式展示
    api_key = st.text_input('请输入OpenAI API密钥：',type='password')
    # 侧边栏中要让用户输入api接口网址
    base_url = st.text_input('请输入您的API_Key的接口网址')
    # 给用户提供一个获取中转API网址，使国内用户也能够通过中转API使用到GPT
    st.markdown('[获取OpenAI API密钥](https://api.aigc369.com/)')
    # 在网页中展示链接中的接口网址
    st.write('链接中的接口网址：https://api.aigc369.com/v1')
    # 侧边栏中要让用户选择自己的聊天模型
    model = st.selectbox('请选择您的聊天模型😘',['gpt-3.5-turbo','gpt-3.5-turbo-0125','gpt-3.5-turbo-1106',
                                        'gpt-3.5-turbo-16k','gpt-3.5-turbo-instruct','gpt-4o-mini',
                                        'gpt-4o-mini-2024-07-18','gpt-4o','gpt-4o-2024-05-13',
                                        'gpt-4-turbo','gpt-4-turbo-2024-04-09','gpt-4',
                                        'gpt-4-0613','gpt-4-0125-preview','gpt-4-1106-preview',
                                        'gpt-4-turbo-preview','gpt-4-all','gpt-4-gizmo-*',
                                        'gpt-4-dalle'])
    # 创建一个DataFrame展示模型的价格
    df = pd.DataFrame({
        '模型名称':['gpt-3.5-turbo(推荐，便宜😉)','gpt-3.5-turbo-0125','gpt-3.5-turbo-1106','gpt-3.5-turbo-16k',
                    'gpt-3.5-turbo-instruct','gpt-4o-mini','gpt-4o-mini-2024-07-18',
                    'gpt-4o','gpt-4o-2024-05-13','gpt-4-turbo',
                    'gpt-4-turbo-2024-04-09','gpt-4','gpt-4-0613',
                    'gpt-4-0125-preview','gpt-4-1106-preview','gpt-4-turbo-preview',
                    'gpt-4-all','gpt-4-gizmo-*','gpt-4-dalle'
                    ],
        '提问价格（RMB / 1K tokens）':[
            0.00125,0.00125,0.00375,0.00375,0.0075,0.000375,0.000375,0.0125,0.0125,
            0.025,0.025,0.075,0.075,0.025,0.025,0.025,0.075,0.075,0.075
        ],
        '回答价格（RMB / 1K tokens）':[
            0.00375,0.00375,0.01125,0.01125,0.0225,0.0015,0.0015,0.0375,0.0375,
            0.075,0.075,0.225,0.225,0.075,0.075,0.075,0.15,0.15,0.15
        ]
    })

    # 侧边栏用DataFrame展示模型价格
    st.dataframe(df,hide_index=True)

    # 设置一个按钮能够清除历史消息
    submit = st.button('清空所有对话')
    if submit:
        st.session_state.memory = st.session_state.memory = ConversationBufferWindowMemory(k=15, return_messages=True)
        st.session_state.messages = [{'role': 'ai', 'content': '你好，我是你的AI小助手，有什么可以帮助你的吗？'}]

# 给网站写一个标题
st.header('💬🤯 克隆ChatGPT——私人定制版')


# 给AI聊天小助手初始一下聊天记忆
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=15,return_messages=True)
    st.session_state.messages = [{'role':'ai','content':'你好，我是你的AI小助手，有什么可以帮助你的吗？'}]

# 使用streamlit中的chat_message函数展示消息角色和内容
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

# 创建一个聊天输入框，用户可以输入聊天消息
prompt = st.chat_input()

# 当用户输入聊天消息后
if prompt:
    # 如果用户没有输入API密钥
    if not api_key:
        st.info('请输入您的OpenAI API密钥')
        st.stop()

    # 如果用户没有输入接口网址
    if not base_url:
        st.info('请输入您的OpenAI API接口网址')
        st.stop()

    # 以上两个条件都满足后用户已输入聊天消息就展示在网页上
    st.session_state.messages.append({'role':'human','content':prompt})
    st.chat_message('human').write(prompt)

    # 创建一个加载中的小提示
    with st.spinner('AI正在思考中，可以先去敲敲🫎🏄‍♂️🐠的脑瓜子🤪'):
        # 将加载中较慢的代码放进来(AI正在生成回答)
        response = get_chat_response(model,api_key,base_url,prompt,st.session_state.memory)
        print(response)

    # 将AI的回答展示在网页上
    st.session_state.messages.append({'role':'ai','content':response['response']})
    st.chat_message('ai').write(response['response'])