from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from Line_App.models import *
from ptt import *
import os, urllib
import requests
import json
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import g4f

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                type=event.message.type
                messages=[]
                message=[]
                content=""
                uid_notify=''
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=''
                if type=='text':
                    mtext=event.message.text
                    if mtext=='加入會員':
                        if User_Info.objects.filter(uid=uid).exists()==False:
                            User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                            content='會員資料新增完畢 請連動Line_Bot 選Tese_gpt'
                            message.append(TextSendMessage(text=content))
                            message.append(TextSendMessage(text=create_auth_link(uid)))
                        elif User_Info.objects.filter(uid=uid,isDelete=0).exists()==False:
                            User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                            content='會員資料新增完畢 請連動Line_Bot 選Tese_gpt'
                            message.append(TextSendMessage(text=content))
                            message.append(TextSendMessage(text=create_auth_link(uid)))
                        else :
                            content='已經有建立會員資料囉'
                            message.append(TextSendMessage(text=content))
                            user_info = User_Info.objects.filter(uid=uid)
                            for user in user_info:
                                info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
                            message.append(TextSendMessage(text=info))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif mtext=='移除':
                        User_Info.objects.filter(uid=uid,isDelete=0).update(isDelete=1,mtext='移除會員')
                        message.append(TextSendMessage(text='移除會員'))
                        content='移除會員'
                        line_bot_api.reply_message(event.reply_token,message)
                    elif mtext=='連動URL':
                        content='連動URL'
                        message.append(TextSendMessage(text=create_auth_link(uid)))
                        line_bot_api.reply_message(event.reply_token,message)
                    content=mtext
                    user_info = User_Info.objects.filter(uid=uid,isDelete=0)
                    for user in user_info:
                        uid_notify=str(user.uid_notify)
                    if User_Info.objects.filter(uid=uid).exists()==False:
                        content='請先輸入 加入會員'
                        message.append(TextSendMessage(text=content))
                        line_bot_api.reply_message(event.reply_token,message)

                    elif uid_notify=='':
                        content='請先連動Line_Bot  選Tese_gpt'
                        message.append(TextSendMessage(text=content+'\n'+create_auth_link(uid)))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif uid_notify!='':
                        api_key = 'aaaa'
                        content=""
                        if mtext == '!reset':
                                    last_message=''
                                    messages.clear()    # 如果收到 !reset 的訊息，表示清空資料庫內容
                                    content = '對話歷史紀錄已經清空！'
                        else:    
                            user_info = User_Info.objects.filter(uid=uid,isDelete=0)
                            # for user in user_info:
                            #     Info_ID=str(user.id)
                            #     uid_notify=str(user.uid_notify)
                            #     jons_len=0
                            #     arr=user.last_message
                                # for jons_str in arr.split('##'):
                                #     if jons_str!='' and jons_len<20:
                                #         jons_len=jons_len+1
                                #         last_message+=jons_str.strip()+'##'
                                #         print("jons_str="+jons_str.replace('\n','').replace('\\','/'))
                                #         j = json.loads(jons_str.replace('\n','').replace('\\','/'))
                                #         messages.append(j)

                            # last_message+='{"role": "user", "content": "'+mtext+'"}##'
                            # messages.append({"role": "user", "content": mtext})  # 将消息添加到列表      
                        messages.append({"role": "system", "content": '''你是專業的分類器，
                                請判斷是維修問題還是其他問題，
                                如果是維修的話，我們只能回答維修。
                                永遠不要解釋它。
                                切勿使用「維修」和「其他」以外的答案來回答。'''
                            },)  # 将消息添加到列表
                        # # # Set with provider
                        messages.append({"role": "user", "content": '''我的燈泡壞了'''
                            },)  # 将消息添加到列表
                        messages.append({"role": "assistant", "content":  '維修'
                            },)  # 将消息添加到列表
                        messages.append({"role": "user", "content": mtext})  # 将消息添加到列表      
                        response = g4f.ChatCompletion.create(
                            # model="gpt-4",
                            model="gpt-3.5-turbo",
                            provider=g4f.Provider.GptGo	,
                            # provider=g4f.Provider.ChatForAi,
                            messages=messages,
                            #proxy="http://host:port",
                            # or socks5://user:pass@host:port
                            #timeout=120, # in secs
                        )
                        content=""
                        for message in response:
                            print(message)
                            content+=message
                        messages.append({"role": "assistant", "content": content.replace('"','\'').replace('\\','/')})
                        # last_message+='{"role": "assistant", "content": "'+content.replace('"','\'').replace('\\','/')+'"}##'
                        print("last_message="+str(content))
                        send_message(uid_notify, content)
                        # User_Info.objects.filter(uid=uid,isDelete=0).update(last_message=last_message)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
def create_auth_link(user_id):
    
    data = {
        'response_type': 'code', 
        'client_id': settings.CLIENT_ID, 
        'redirect_uri': settings.REDIRECT_URI, 
        'scope': 'notify', 
        'state': user_id,
        'response_mode': 'from_post'
    }
    query_str = urllib.parse.urlencode(data)
    
    return f'https://notify-bot.line.me/oauth/authorize?{query_str}'

def text_Log(Info_ID,uid,uid_notify,name,mtext,content):
    User_text_Log.objects.create(Info_ID=Info_ID,L_uid=uid,L_uid_notify=uid_notify,L_name=name,L_mtext=mtext,L_Rmtext=content)

def send_message(token, text_message):
    url = 'https://notify-api.line.me/api/notify'
    token = token
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    data = {
        'message':text_message     # 設定要發送的訊息
    }
    data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法

def notify(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    access_token = get_token(code, settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)
    #抓取user的info
    user_info_url = 'https://notify-api.line.me/api/status'
    headers = {'Authorization':'Bearer '+access_token}
    get_user_info = requests.get(user_info_url,headers=headers)
    # get_user_info={'status': 200, 'message': 'ok', 'targetType': 'GROUP', 'target': 'Tese_gpt'}
    notify_user_info = get_user_info.json()
    name_Str= '恭喜完成 LINE Notify 連動！請把LINE Notify加'+notify_user_info['target']
    # User_Info.objects.filter(uid=state).update(uid_notify=access_token)
    if notify_user_info['target']==settings.LINE_BOT_NAME:
        name_Str= '恭喜完成 LINE Notify 連動！'
        User_Info.objects.filter(uid=state).update(uid_notify=access_token)
    else:
        name_Str= '請選'+settings.LINE_BOT_NAME
    return HttpResponse(name_Str)
# 取得token
def get_token(code, client_id, client_secret, redirect_uri):
    url = 'https://notify-bot.line.me/oauth/token'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()
    res = json.loads(page.decode('utf-8'))
    #print(data)
    return res['access_token']

def testdb(request):
    # 初始化
    response = ""
    response1 = ""

    test1 = Test(name='test01')
    #test1.save()
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    # list = Test.objects.all()

    # # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response2 = Test.objects.filter(id=1) 

    # # 获取单个对象
    # response3 = Test.objects.get(id=1) 

    # # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    # list = Test.objects.all()
        
    # # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response2 = Test.objects.filter(id=1) 
    
    # # 获取单个对象
    # response3 = Test.objects.get(id=1) 
    
    # # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    # Test.objects.order_by('name')[0:2]
    
    # #数据排序
    # Test.objects.order_by("id")
    
    # # 上面的方法可以连锁使用
    # Test.objects.filter(name="runoob").order_by("id")
    
    # # 输出所有数据
    # for var in list:
    #     response1 += var.name + " "
    # response = response1

    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    # test1 = Test.objects.get(id=1)
    # test1.name = 'Google'
    # test1.save()
     # 另外一种方式
    #Test.objects.filter(id=1).update(name='Google')

    return HttpResponse("<p>" + response + "</p>")