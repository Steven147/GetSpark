import json, time
import re
import pandas as pd


# print(df['林绍钦']["0822"])
# 0xd7e4b94a54c74e1aaecebf4c7e20d645ac4539cfe1bc4dc9a25d4c4be9652333
timeStr = "0824"
cnt = 1091

# timeStr = str(time.strftime("%m%d", time.localtime()))
sparkDick = {}
# sparkDick[timeStr] = {}

fin = open("Chat_46cf6649760baa443cadf803d532e0d1.json", "r")
fout = open("spark.txt", "w")

results = json.load(fin)
nameDict = {'wxid_vrfl7oczl53122': '廖慧炫',
            'wxid_0982559824022': '杨雨霏', 
            'wxid_azqlbpx87tp312': '徐怡格', 
            'AmberCai': '蔡慧群', 
            'wxid_yjibowth7kja22': '欣雪', 
            'wxid_edh8glb48ncl22': '姜辰丽', 
            'wxid_ph1gz5mylsn422': '程浩原', 
            'wxid_h2ixckqehtde12': '程浩原', 
            'ninibaobeisheng': '周利静', 
            'wxid_4gfs3gywie1p22': '王彩燕', 
            'binABC': '王德彬', 
            'wxid_cdipxhhgoaa322': '朱静雯', 
            'wxid_cly783cbv6v922': '曾怡佳', 
            'wxid_dza4hkbg3dsb22': '黄鸿骞', 
            'wxid_gyms19vd4yvs22': '梁茵', 
            'wxid_optfgyvdjoug22': '卢迅舟', 
            'wxid_toalbrhss7z022': '邓欣', 
            'wxid_gws2keu7quaj12': '李博', 
            'wxid_w34xy2edbmlp11': '立平老师', 
            'wxid_f8jgnc0k3fb911': '丽鹏', 
            'wxid_8zjftmrhw5cz11': '黄斯奕', 
            'wxid_esylk9gfh40022': '尹航', 
            'a28436605': '唐清松', 
            'wxid_7tbnfgpysf6m22': '唐子涵', 
            'wxid_3404884048922': '英姿', 
            'wxid_k8enk5lhgw6z11': '吴雨聪', 
            'wxid_hjdd6ch5y7ye12': '李欣红', 
            'wxid_2105551055822': '贠轩冰',
            'wxid_bgykc0a4wosh21': '冯鹏尧'}


 
print("cnt = %s"%(len(results)))

for dic in results[cnt:]:
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
                realName = name
            
            msg = content.strip().replace("\n", " ").replace("\r", " ").replace(name+':', "")

        else:
            realName = '林绍钦'
            msg = content.strip().replace("\n", " ").replace("\r", " ")
            
        # if msg.startswith('火花' + timeStr):
        # print(msg)
        if realName+'火花'+timeStr in msg:
            # print(msg)
            if timeStr in sparkDick:
                sparkDick[timeStr][realName] = msg
            else:
                sparkDick[timeStr] = {realName: msg}
        elif '火花' in msg:
            print(msg)
            # tmpDict = {"名字": realName,}
            # tmpDict[timeStr] = msg
            # fout.write("{}:{}\n".format(name,msg))
df = pd.DataFrame(sparkDick)

tf = open("sparkList.json", "w")
json.dump(sparkDick,tf)
tf.close()

df.to_excel("sparkList2.xlsx")