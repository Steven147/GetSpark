# string="nhooo is a great site"
# echo `expr index "$string" io`  # 输出 4


#ps -axu bytedance | grep /Applications/WeChat.app
arr=(`ps -axu bytedance | grep /Applications/WeChat.app | tr ' ' ' '`)
echo ${arr[1]}
kill -9 ${arr[1]}
sleep 0.15
open -a "WeChat"