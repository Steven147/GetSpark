# Get Spark // 获取火花脚本

> Author：linshaoqin // 作者：林绍钦

## Feature // 功能简述：
***获取微信群中群成员每日火花，储存到飞书在线文档中并统计***。

## Workflow // 工作流程：

聊天数据在工作流程中，经过以下转化：

- 生成 msg_1.db：macOS版本微信将所有的聊天记录储存为.db的加密数据库文件。
  - 每次获取时，重新登陆账户，数据会自动保存到数据库中
  - 【可扩展】脚本实现自动退出并重新登陆
- msg.db -> chat.json：
  - DB Browser for SQLite数据库浏览器将对应群聊数据导出为json格式文件。
- chat.json -> sparkList.xlsx：
  - 代码自动从当日聊天记录json文件中，提取出火花数据，储存为xlsx文件。
- sparkList.xlsx -> [火花整理 - 飞书云文档](https://cm0nlh86eu.feishu.cn/sheets/shtcnExX9jrUoIxaTaWU0dJIVnh)：
  - 手动将sparkList.xlsx内容复制到飞书云文档中，并进行换行
  - 将消息发送到群里
  - 【可扩展】对接workflow，自动将消息发送到群里
  - 【可扩展】对接到飞书云文档api，利用云函数，自动储存到在线表格中

## Version // 代码版本与内容

v1.0.0
- 代码将“读取消息范围”和“日期关键词范围”分离，实现增量更新，降低复杂度
  - “读取消息范围”根据point字典储存的消息index确定，实现了增量更新，不需要每一次都从头开始读取。
  - “日期关键词范围”设置为昨日、今日、明日三天，即在0827日更新0826日的火花，同时扫描0825，0826，0827这三个标签，考虑补发和提前发的情况。不需要每次都从第一天关键字开始扫描，复杂度从 $O(N^2)$ 下降到 $O(N)$
    > Python3.6 版本以后的 dict 是有序的，因此不需要考虑字典的顺序，可以直接当做有序处理
- 完善代码输出、注释和文档



v0.0.3
- 实现单日单人多条火花的补充更新（而不是覆盖）
- 实现扫描所有日期关键词
- 实现一定容错的关键词搜索（只要包含火花和日期就可以识别，只写“火花“那可能需要NLP救驾了）

v0.0.2
- 自动化生成时间标签，并将消息index储存成pointDict字典
- 将人名和id保存成nameDict字典，并且实现提示新人名
- 将火花储存成sparkDict字典，每次都从头读取并保存
  
v0.0.1
- 代码实现基础功能，从当日聊天记录json文件中，提取出火花数据，储存为xlsx文件


## Requirement // 环境需求与复现

复现可以直接下载代码，建议使用anaconda配置python环境，依赖模块和版本如下。

下载后，根据附录中解密方法参考实现工作流程的第一步：生成 msg_1.db，然后交给getDailySpark.py就行。

```
% getSpark pip freeze > requirement.txt

numpy==1.21.6
pandas==1.3.5
python-dateutil==2.8.2
python==3.7.2
```

## Reference // 参考资料

附录1: 解密方法参考

下载DB Browser for SQLite数据库浏览器：https://sqlitebrowser.org/dl/
。解密方法参考链接：https://blog.csdn.net/god_weiyang/article/details/120264189 
。获取解密密钥。经过解密后，进入数据库，查看数据表定位到对应群聊数据：msg_1/Chat_46cf6649760baa443cadf803d532e0d1。

本机命令行运行记录：
```sh
% sudo lldb -p $(pgrep WeChat)
(lldb) process attach --pid 1797
Process 1797 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGSTOP
    frame #0: 0x00007ff8067ff97a libsystem_kernel.dylib`mach_msg_trap + 10
libsystem_kernel.dylib`mach_msg_trap:
->  0x7ff8067ff97a <+10>: retq   
    0x7ff8067ff97b <+11>: nop    

libsystem_kernel.dylib`mach_msg_overwrite_trap:
    0x7ff8067ff97c <+0>:  movq   %rcx, %r10
    0x7ff8067ff97f <+3>:  movl   $0x1000020, %eax          ; imm = 0x1000020 
Target 0: (WeChat) stopped.
Executable module set to "/Applications/WeChat.app/Contents/MacOS/WeChat".
Architecture set to: x86_64h-apple-macosx-.
(lldb) br set -n sqlite3_key
Breakpoint 1: 2 locations.
(lldb) c
Process 1797 resuming
Process 1797 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000107aa4854 WCDB`sqlite3_key
WCDB`sqlite3_key:
->  0x107aa4854 <+0>: pushq  %rbp
    0x107aa4855 <+1>: movq   %rsp, %rbp
    0x107aa4858 <+4>: movl   %edx, %ecx
    0x107aa485a <+6>: movq   %rsi, %rdx
Target 0: (WeChat) stopped.
(lldb) memory read --size 1 --format x --count 32 $rsi
0x60000062d6a0: 0xd7 0xe4 0xb9 0x4a 0x54 0xc7 0x4e 0x1a
0x60000062d6a8: 0xae 0xce 0xbf 0x4c 0x7e 0x20 0xd6 0x45
0x60000062d6b0: 0xac 0x45 0x39 0xcf 0xe1 0xbc 0x4d 0xc9
0x60000062d6b8: 0xa2 0x5d 0x4c 0x4b 0xe9 0x65 0x23 0x33
```

python代码格式化输出密码：
```py
source = """
0x60000062d6a0: 0xd7 0xe4 0xb9 0x4a 0x54 0xc7 0x4e 0x1a
0x60000062d6a8: 0xae 0xce 0xbf 0x4c 0x7e 0x20 0xd6 0x45
0x60000062d6b0: 0xac 0x45 0x39 0xcf 0xe1 0xbc 0x4d 0xc9
0x60000062d6b8: 0xa2 0x5d 0x4c 0x4b 0xe9 0x65 0x23 0x33
"""
key = '0x' + ''.join(i.partition(":")[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:5])
print(key)
# 0xd7e4b94a54c74e1aaecebf4c7e20d645ac4539cfe1bc4dc9a25d4c4be9652333
```

--- 
附录2：参考资料

虚拟环境构建miniconda：https://formulae.brew.sh/cask/miniconda

pysqlcipher3：https://github.com/rigglemania/pysqlcipher3

con = sqlite3.connect('/Users/bytedance/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/3a4f5181fdafb7b9b9c2bed2aac1897f/Message/msg_1.db')

数据路径：/Users/bytedance/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/3a4f5181fdafb7b9b9c2bed2aac1897f/Message/msg_1.db

表格路径：Chat_46cf6649760baa443cadf803d532e0d1


