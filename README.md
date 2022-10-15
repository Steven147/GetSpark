# Get Spark // 获取火花脚本

> Author：linshaoqin // 作者：林绍钦

- [Get Spark // 获取火花脚本](#get-spark--获取火花脚本)
  - [Feature // 功能简述](#feature--功能简述)
  - [Workflow // 工作流程](#workflow--工作流程)
  - [Todo // 待改进](#todo--待改进)
  - [Version // 代码版本与内容](#version--代码版本与内容)
  - [Requirement // 环境需求与复现](#requirement--环境需求与复现)
  - [Reference // 参考资料](#reference--参考资料)

## Feature // 功能简述
***获取微信群中群成员每日火花，储存到飞书在线文档中并统计***。

## Workflow // 工作流程

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

## Todo // 待改进

- [ ] 更安全的python代码（一些限制输入输出的方式，让全局变量的获取和实现更加安全）
  - [ ] python全局变量实现原理以及使用
- [ ] 优化递归函数，采用datetime库更优雅的轮子
- [ ] 提供指定范围内的重新扫描功能，应对较远时间的补交
- [ ] 自动获取聊天备注人名，实现对名字的更新
- [ ] 实现GUI
- [ ] 实现不同电脑的迁移，在新分支上线通用版本！

## Version // 代码版本与内容

v2.0.0
- [x] 根据程序数据处理特性，使用全局变量传递四个参数，让代码更加简洁
- [x] 时间戳实现自动更新，根据datetime库的特点，使用递归方式逐步初始化
  - [x] 明确了pointDict的内容和使用方式：保存每一天对应第一条火花的内容
  - [x] 在扫描时，从某一天开始，先清空此前的dict，识别str也是从当天开始
  - [x] 只在完全扫描结束后进行赋值，赋值后也代表这一天已经搜索完毕
- [x] 搜索方式从原来的一遍多timeStr，更改到了现在的单次只扫描一个timeStr，进行多次扫描
  - [x] 抽象出getTodaySpark函数，封装了扫描单日的逻辑

v1.0.1
- [x] 修复bug：第二天条目如果为空无法生成数据，设置为读取前一天的值为初始值
- [x] 数据添加进.gitignore，不再更新数据
- [x] 仓库中数据删除


v1.0.0
- [x] 代码将“读取消息范围”和“日期关键词范围”分离，实现增量更新，降低复杂度
  - [x] “读取消息范围”根据point字典储存的消息index确定，实现了增量更新，不需要每一次都从头开始读取。
  - [x] “日期关键词范围”设置为昨日、今日、明日三天，即在0827日更新0826日的火花，同时扫描0825，0826，0827这三个标签，考虑补发和提前发的情况。不需要每次都从第一天关键字开始扫描，复杂度从 $O(N^2)$ 下降到 $O(N)$
    > Python3.6 版本以后的 dict 是有序的，因此不需要考虑字典的顺序，可以直接当做有序处理
- [x] 完善代码输出、注释和文档

v0.0.3
- [x] 实现单日单人多条火花的补充更新（而不是覆盖）
- [x] 实现扫描所有日期关键词
- [x] 实现一定容错的关键词搜索（只要包含火花和日期就可以识别，只写“火花“那可能需要NLP救驾了）

v0.0.2
- [x] 自动化生成时间标签，并将消息index储存成pointDict字典
- [x] 将人名和id保存成nameDict字典，并且实现提示新人名
- [x] 将火花储存成sparkDict字典，每次都从头读取并保存
  
v0.0.1
- [x] 代码实现基础功能，从当日聊天记录json文件中，提取出火花数据，储存为xlsx文件



## Requirement // 环境需求与复现

复现可以直接下载代码，建议使用anaconda配置python环境，依赖模块和版本如下。

[Getting Started - pip documentation v22.2.2](https://pip.pypa.io/en/stable/getting-started/#install-multiple-packages-using-a-requirements-file)

```s
~ git clone
~ conda create -n getSpark-py37 python=3.7.2
~ conda activate getSpark-py37
~ pip install -r .backup/requirement.txt #pip freeze > requirement.txt
~ python getDailySpark.py
```

```
numpy==1.21.6
openpyxl==3.0.10
pandas==1.3.5
python-dateutil==2.8.2
```

配置python环境流程较为简单，不再赘述。
> 注意，OP is on osx-arm64 platform. There are only Python v3.8 and v3.9 builds for that.

然后是根据附录中方法解密。能够打开 msg_1.db就算成功。
> 注意，涉及到的读取内存的机器指令和cpu架构(arm64-M1)有关，需要调整命令

当然，为了脱敏，我没有上传人员信息的字典，有需要可以dd我或者在issue中提。   

## Reference // 参考资料

附录1: 解密方法参考

下载DB Browser for SQLite数据库浏览器：https://sqlitebrowser.org/dl/
。解密方法参考链接：https://blog.csdn.net/god_weiyang/article/details/120264189 
。获取解密密钥。经过解密后，进入数据库，查看数据表定位到对应群聊数据：msg_1/Chat_46cf6649760baa443cadf803d532e0d1。

本机命令行运行记录：
```sh
% sudo lldb -p $(pgrep WeChat) # 打开微信（不登陆）的情况下才可以获取进程信息
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
------ 旧架构情况
WCDB\`sqlite3_key:
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
------ 新架构情况
Architecture set to: arm64e-apple-macosx-.
...
WCDB\`sqlite3_key:
->  0x10930bfd4 <+0>:  mov    x3, x2
    0x10930bfd8 <+4>:  mov    x2, x1
    0x10930bfdc <+8>:  adr    x1, #0x2c215              ; "main"
    0x10930bfe0 <+12>: nop    
Target 0: (WeChat) stopped.
(lldb) memory read --size 1 --format x --count 32
error: memory read takes a start address expression with an optional end address expression.
warning: Expressions should be quoted if they contain spaces or other special characters.
(lldb) memory read --size 1 --format x --count 32 $x1
0x600002657ce0: 0xd9 0x27 0xf6 0x90 0xcd 0x39 0x43 0xa7
0x600002657ce8: 0xa9 0xcd 0x53 0x76 0x5e 0xca 0x2a 0xd6
0x600002657cf0: 0x1d 0x54 0xa2 0x86 0xd8 0xca 0x4d 0xa4
0x600002657cf8: 0xa3 0x4b 0x16 0x1a 0x36 0xbe 0xf0 0x5a
```

python代码格式化输出密码：

旧架构：
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
新架构：
```py
source = """
0x600002657ce0: 0xd9 0x27 0xf6 0x90 0xcd 0x39 0x43 0xa7
0x600002657ce8: 0xa9 0xcd 0x53 0x76 0x5e 0xca 0x2a 0xd6
0x600002657cf0: 0x1d 0x54 0xa2 0x86 0xd8 0xca 0x4d 0xa4
0x600002657cf8: 0xa3 0x4b 0x16 0x1a 0x36 0xbe 0xf0 0x5a
"""

key = '0x' + ''.join(i.partition(":")[2].replace('0x', '').replace(' ', '') for i in source.split('\n')[1:5])

print(key)
# 0xd927f690cd3943a7a9cd53765eca2ad61d54a286d8ca4da4a34b161a36bef05a
```

附录2：参考资料

虚拟环境构建miniconda：https://formulae.brew.sh/cask/miniconda

pysqlcipher3：https://github.com/rigglemania/pysqlcipher3

con = sqlite3.connect('/Users/bytedance/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/3a4f5181fdafb7b9b9c2bed2aac1897f/Message/msg_1.db')

数据路径：/Users/bytedance/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/3a4f5181fdafb7b9b9c2bed2aac1897f/Message/msg_1.db

表格路径：Chat_46cf6649760baa443cadf803d532e0d1

附录3：github上传
➜  getSpark git:(develop) ✗ git remote add origin git@github.com:Steven147/GetSpark.git
➜  getSpark git:(main) ✗ git branch -M main
➜  getSpark git:(main) ✗ git push -u origin main

➜  getSpark git:(main) ✗ git branch -M develop

附录4：[关于gitignore](https://segmentfault.com/q/1010000000430426)

