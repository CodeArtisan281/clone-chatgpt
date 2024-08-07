from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

# # 测试所需要用到的库
# from langchain.memory import ConversationBufferMemory

def get_chat_response(model,api_key,base_url,prompt,memory):

    # 选择模型并设置好参数
    modle = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
    )

    # 创建一个自动添加保存记忆的链
    chain = ConversationChain(llm = modle,memory = memory)

    # 对AI进行问答
    response = chain.invoke({'input':prompt})

    # 返回AI的回答结果
    return response

# # 进行一个简单的小测试
#
# memory = ConversationBufferMemory(return_messages=True)
#
# print(get_chat_response('请输入自己的OpenAI的API密钥',
#                         '请输入自己的API密钥接口网址',
#                         '牛顿提出哪些知名的定律？',
#                         memory))

"""测试通过"""