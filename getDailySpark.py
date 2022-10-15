import json, datetime
import pandas as pd

# 打开数据库; 0xd927f690cd3943a7a9cd53765eca2ad61d54a286d8ca4da4a34b161a36bef05a
# 保存到json
# 运行程序
# 复制

# 获取四个字典数据：已处理的聊天记录字典、点位字典、名字字典、总聊天记录字典
def getData(): 
    # 保存成全局变量
    global sparkDict, pointDict, nameDict, chatDict
    with open("sparkDict.json", "r") as sDin:
        sparkDict = json.load(sDin)
    
    # Python3.6 版本以后的 dict 是有序的
    with open("pointDict.json", "r") as pDin:
        pointDict = json.load(pDin)
    
    with open("nameDict.json", "r") as nDin:
        nameDict = json.load(nDin)
        # 在此添加/更新人名：
        # nameDict['swt199614'] = '孙文韬'
        # nameDict['wxid_i711szwrnup922'] = '戚宇隆'
        # for i in nameDict:
        #     if nameDict[i] == '欣雪': nameDict[i] = '陈欣雪'
        
    with open("Chat_46cf6649760baa443cadf803d532e0d1.json", "r") as fDin:
        chatDict = json.load(fDin)

# 工具函数：根据今天的时间戳获取前一天时间戳
def getYstday(todayTimeStr):
    today = datetime.datetime.strptime(todayTimeStr, '%m%d')
    ystday = today - datetime.timedelta(days=1)
    ystdayTimeStr = ystday.strftime('%m%d')
    return ystdayTimeStr

# 插入没有定义的时间戳timeStr，直到程序运行当日，初始值设置为-1
def insertTimeStr():
    # 插入至当日=递归插入前一日+插入当日（当日已经插入便返回）
    def insertTilToday(todayTimeStr):
        # 设置一个初始化的值，防止无限递归，同时第一天设置为0（已经有值，代表当日已经识别完成）
        if '0821' not in pointDict: pointDict['0821'] = 0
        if todayTimeStr not in pointDict:
            # 顺序不能错，因为pointDict是按顺序读取
            insertTilToday(getYstday(todayTimeStr))
            pointDict[todayTimeStr] = -1 

    nowTimeStr = datetime.datetime.now().strftime("%m%d")
    insertTilToday(nowTimeStr)

# 工具函数：搜索这一天的火花，搜索范围是前一天火花的第一条至最后，搜索时间戳就是这一天
def getTodaySpark(todayTimeStr):
    if todayTimeStr in sparkDict: sparkDict.pop(todayTimeStr) # 清空当天火花
    ystdayTimeStr = getYstday(todayTimeStr)
    startPoint = pointDict[ystdayTimeStr]
    print("搜索%s火花，搜索起点为第%s条，终点为第%s条"%(todayTimeStr, startPoint, len(chatDict)))
    print("----")
    firstSparkPoint = -1
    for point, chat in enumerate(chatDict[startPoint:]):
        if chat["messageType"] == 1:
            content = chat["msgContent"]
            if chat["mesDes"] == 1:
                name = content.strip().split(":\n")[0]
                if name not in nameDict:
                    print('新名字:', name, msg)
                    nameDict[name] = name
                realName = nameDict[name]
                msg = content.strip().replace("\n", " ").replace("\r", " ").replace(name+':', "")
            else:
                realName = '林绍钦'
                msg = content.strip().replace("\n", " ").replace("\r", " ")

            if '火花' in msg and todayTimeStr in msg:
                if todayTimeStr in sparkDict: # 这天已经有火花
                    if realName in sparkDict[todayTimeStr]: # 这天这人已经发过火花，补充在后面
                        sparkDict[todayTimeStr][realName] = sparkDict[todayTimeStr][realName] + '\n---\n' + msg
                    else: sparkDict[todayTimeStr][realName] = msg # 这天这人第一次发火花
                else: # 这天第一个人发火花
                    firstSparkPoint = point + startPoint
                    sparkDict[todayTimeStr] = {realName: msg}
    
    return firstSparkPoint

# 从未初始化的那天开始，逐天初始化
def getSpark():
    for timeStr, point in pointDict.items():
        if point == -1:
            pointDict[timeStr] = getTodaySpark(timeStr)

# 保存数据：其中chatDict不需要修改，并且使用pd额外将火花保存成xlsx文件
def saveData():
    with open("sparkDict.json", "w") as fout:
        json.dump(sparkDict, fout)
    with open("pointDict.json", "w") as fout:
        json.dump(pointDict, fout)
    with open("nameDict.json", "w") as fout:
        json.dump(nameDict, fout)

    df = pd.DataFrame(sparkDict)
    df = df.sort_index(axis=1, ascending=False)
    df.to_excel("sparkList.xlsx")
    

if __name__ == "__main__":
    getData()
    insertTimeStr()
    getSpark()
    saveData()
    print("火花整理:https://cm0nlh86eu.feishu.cn/sheets/shtcnExX9jrUoIxaTaWU0dJIVnh")
    print("更新时间:%s"%(datetime.datetime.now().strftime("%m-%d %H:%M:%S")))
    print("----")

