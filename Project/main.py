from threading import Timer # 多執行緒
import time 
from fysom import Fysom # 有限狀態

###################自定模組####################
from IFTTT import send_msg #傳送訊息
from voice_detect import get_command # 辨認語音指令

###################自定模組####################

def timer_msg():
    time.sleep(5)
    print("Send IFTTT message")
    # send_msg("1","2","3")
    Timer(100, timer_msg).start()  # 每100秒执行一次

if __name__ == "__main__":
    
    timer_msg() # 定時傳送IFTTT訊息
    
    # 定義有限狀態機
    state = Fysom(initial = "listen",
            events=[("select_what", "listen", "camera_get"),
                ("select_where", "listen", "Question"),
                ("show_ans", "camera_get", "Answer"),
                ("what_end", "Answer", "listen"),
                ("to_find", "Question", "camera_check"),
                ("check_yes", "camera_check", "praise"),
                ("check_no", "camera_check", "camera_check"),
                ("where_end", "praise", "listen"),
                ("select_end","listen", "end")
        ]
    )
    while state.current != "end":

        # 辨認語音指令
        if state.current == "listen":
            select = get_command()
            if select == "select_what":
                state.select_what()
            elif select == "select_where":
                state.select_where()
            elif select == "select_end":
                state.select_end()
            continue

        # 自由探索模式
        if state.current == "camera_get":
            label = get_object() // TODO: 包
            state.show_ans()
            continue

        # 顯示答案
        if state.current == "Answer":
            // TODO: 顯示結果
            state.what_end()

        # 物品探索模式
        if state.current == "Question":
            Q = \\ TODO: 
            state.to_find()

        
        # 檢查是否符合
        if state.current == "camera_check":
            label = get_object()
            if label == Q:
                state.check_yes()
        
        # 讚美
        if state.current == "praise":
            // TODO: 讚美內容
            state.where_end()

        # 結束
        if state.current == "end":
            break
            exit()
        
    
    