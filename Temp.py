from urllib.request import *
from urllib.error import *
from json import *
from ssl import *
def GetOpenRouterResponse():
    Url="https://openrouter.ai/api/v1/chat/completions"
    Headers={"Authorization":"Bearer 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","Content-Type":"application/json","HTTP-Referer":"<YOUR_SITE_URL>","X-Title":"<YOUR_SITE_NAME>"}
    Payload={"model":"deepseek/deepseek-r1-0528:free","messages":[{"role":"user","content":input("请输入问题:")}],"temperature":0.7,"max_tokens":1000}
    try:
        Data=dumps(Payload).encode('utf-8')
        Req=Request(Url,data=Data,headers=Headers,method='POST')
        Context=create_default_context()
        with urlopen(Req,timeout=15,context=Context)as Response:
            StatusCode=Response.status
            ResponseData=Response.read().decode('utf-8')
        if StatusCode != 200:
            return f"HTTP错误({StatusCode})\n响应内容:\n{ResponseData[:500]}"
        try:
            Result=loads(ResponseData)
        except JSONDecodeError as Error:
            return f"JSON解析失败(位置:{Error.pos})\n原始数据:\n{ResponseData[:500]}"
        if 'choices' not in Result or not Result['choices']:
            raise ValueError("无效的响应结构")
        Answer=Result['choices'][0].get('message',{}).get('content','')
        return f"✅ API响应成功\n\n回答内容:\n{Answer}\n"
    except HTTPError as Error:
        return f"HTTP错误({Error.code})\n原因:{Error.reason}\n详情:{Error.read()}"
    except URLError as Error:
        return f"网络错误:{Error.reason}\n建议检查网络连接"
    except TimeoutError:
        return "⚠️ 请求超时\n建议:检查网络或增大超时时间"
    except Exception as Error:
        return f"未知错误:\n{str(Error)}"
print("="*60)
print("API请求结果:")
print(GetOpenRouterResponse())
print("="*60)