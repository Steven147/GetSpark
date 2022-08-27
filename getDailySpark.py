import json, datetime
import pandas as pd

# 打开数据库;0xd7e4b94a54c74e1aaecebf4c7e20d645ac4539cfe1bc4dc9a25d4c4be9652333
# 保存到json
# 运行程序（在第二天中午运行）
# 复制

# 自动获取：firstTimeStr（第一天），timeStr（昨天），nowTimeStr（今天）

# 扫描标签范围，当日为0827时，扫描0825，0826，0827三日标签
delta = 2

def getTimeStr():    

    now = datetime.datetime.now()

    
    
    # 重新开始扫描 startTimeStr=0822
    # 增量扫描 startTimeStr=nowTimeStr
    nowTimeStr = now.strftime("%m%d")
    # startTimeStr = "0822"
    startTimeStr = nowTimeStr


    # 读取天内标签 ------------------------- 
    deltaDays = now - datetime.timedelta(days=delta)
    # deltaDays = datetime.datetime.strptime("0822", '%m%d')
    deltaStartDay = deltaDays.strftime("%m%d")

    nowActStr = now.strftime("%m-%d %H:%M:%S")

    return nowTimeStr, startTimeStr, deltaStartDay, nowActStr

def getData(): 
    # 读取数据：总聊天记录、已处理的聊天记录字典、点位字典
    with open("sparkDict.json", "r") as sDin:
        nowTimeStr, startTimeStr, _, _ = getTimeStr()
        if nowTimeStr == startTimeStr :
            sparkDict = json.load(sDin)
        elif startTimeStr == "0822":# 重新开始扫描，清空
            sparkDict = {}
    
    # Python3.6 版本以后的 dict 是有序的
    with open("pointDict.json", "r") as pDin:
        pointDict = json.load(pDin)

    
    with open("nameDict.json", "r") as nDin:
        nameDict = json.load(nDin)
        # nameDict['wxid_h2ixckqehtde12'] = '姚泽雄'
        # for i in nameDict:
        #     if nameDict[i] == '欣雪':
        #         nameDict[i] = '陈欣雪'

        
    with open("Chat_46cf6649760baa443cadf803d532e0d1.json", "r") as fDin:
        results = json.load(fDin)

    return sparkDict, pointDict, nameDict, results
    
def getDailySpark(inp):
    
    sparkDict, pointDict, nameDict, results = inp

    nowTimeStr, startTimeStr, deltaStartDay, _ = getTimeStr()
    durationDays = [str(i) for i in pointDict]
    durationDays = durationDays[durationDays.index(deltaStartDay):]

    # 重新开始扫描 startTimeStr=0822
    # 增量扫描 startTimeStr=nowTimeStr
    startPoint = pointDict[startTimeStr]
    pointDict[nowTimeStr] = len(results) - 1
    if startPoint == pointDict[nowTimeStr]:
        print("————\n从%s日消息读取第%s条消息到第%s条消息，已经是最新"%(startTimeStr, startPoint, pointDict[nowTimeStr]))
    else:
        print("————\n从%s日消息读取第%s条消息到第%s条消息，扫描日期字段包括%s"%(startTimeStr, startPoint, pointDict[nowTimeStr],durationDays))
        for dic in results[startPoint:]:
            if dic["messageType"] == 1:
                content = dic["msgContent"]
                name = ''
                realName = ''

                if dic["mesDes"] == 1:
                    name = content.strip().split(":\n")[0]
                    if name in nameDict: 
                        realName = nameDict[name]
                    else:
                        print('新名字:', name, msg)
                        name = nameDict[name]
                        realName = name
                    
                    msg = content.strip().replace("\n", " ").replace("\r", " ").replace(name+':', "")

                else:
                    realName = '林绍钦'
                    msg = content.strip().replace("\n", " ").replace("\r", " ")
                    
                # if msg.startswith('火花' + timeStr):
                # if '姚泽雄火花 ' in msg: print(name)
                
                for ptime in durationDays:
                    if '火花' in msg and ptime in msg:
                        if ptime in sparkDict: #这天有人发过火花
                            if realName in sparkDict[ptime]: #这天已经发过火花，补充在后面
                                sparkDict[ptime][realName] = sparkDict[ptime][realName] + '\n---\n' + msg
                            else: #这天第一次发火花
                                sparkDict[ptime][realName] = msg
                        else: #这天第一个人发火花
                            sparkDict[ptime] = {realName: msg}
                
                # elif '火花' in msg:
                #     print('未收入消息：', msg)

    return sparkDict, pointDict, nameDict, results


def saveData(inp):
    sparkDict, pointDict, nameDict, results = inp
    with open("sparkDict.json", "w") as fout:
        json.dump(sparkDict, fout)

    # pointDict.to_json("pointDict.json")
    with open("pointDict.json", "w") as fout:
        json.dump(pointDict, fout)
    with open("nameDict.json", "w") as fout:
        json.dump(nameDict, fout)

    df = pd.DataFrame(sparkDict)
    df = df.sort_index(axis=1, ascending=False)
    df.to_excel("sparkList.xlsx")
    

if __name__ == "__main__":
    saveData(getDailySpark(getData()))
    _, _, _, nowActTimeStr = getTimeStr()
    print("————\n火花整理:https://cm0nlh86eu.feishu.cn/sheets/shtcnExX9jrUoIxaTaWU0dJIVnh\n更新时间:%s\n————"%(nowActTimeStr))
    

