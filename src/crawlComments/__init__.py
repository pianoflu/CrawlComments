#coding:utf-8
from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time


headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Referer': 'http://music.163.com/'
}

first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

def get_params(page):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1):
        first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = "{rid:\"\", offset:\"%s\", total:\"%s\", limit:\"20\", csrf_token:\"\"}"%(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey
    

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    return response.content


def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"用户id 用户昵称  用户头像地址  评论时间  点赞总数  评论内容\n")
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    hot_comments = json_dict['hotComments']
    print("共有%d条热门评论�" % len(hot_comments))
    for item in hot_comments:
        comment = item['content']
        likedCount = item['likeCount']
        comment_time = item['time']
        userID = item['user']['userID']
        nickname = item['user']['nickname']
        avatarUrl = item['user']['avatarUrl']
        comment_info = userID + " " +nickname + " " + avatarUrl + " " + comment_time + " " + likedCount + " " + comment +u"\n"
        hot_comments_list.append(comment_info)
        
    return hot_comments_list
    

#获取全部评论
def get_all_comments(url):
    all_comments_list = [] #全部评论
    all_comments_list.append(u"用户id 用户昵称  用户头像地址  评论时间  点赞总数  评论内容\n")
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])
    if(comments_num % 20 == 0 ):
        page = comments_num/20
    else:
        page = int(comments_num / 20) + 1 
    print("评论共有%dҳ页" % page)
    for i in range(page):
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text)
        if i==0:
            print("共有%d条评论" % comments_num)
        for item in json_dict['comments']:
            comment = item['content']
            likedCount = item['likedCount']
            comment_time = item['time']
            userID = item['user']['userId']
            nickname = item['user']['nickname']
            avatarUrl = item['user']['avatarUrl']
            comment_info = unicode(userID) + u"" + nickname + u"" + avatarUrl + u"" + unicode(comment_time) + u"" + unicode(likedCount) + u"" + comment +u"\n"
            all_comments_list.append(comment_info)
        print("第%d页抓取完毕" % (i+1))
    return all_comments_list
        
        
        
#将评论写入文件
def save_to_file(list,filename):
    with codecs.open(filename,'a',encoding='utf-8') as f:#文件位置在与此项目并列的文件夹下
        f.writelines(list)
    print("写入文件成功") 
     
    

if __name__ == "__main__":
    start_time = time.time()
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_481423070/?csrf_token="
    filename = u"评论.txt"
    all_comments_list = get_all_comments(url)
    save_to_file(all_comments_list,filename)
    end_time = time.time()
    print(end_time-start_time)

        
        
        
        
        