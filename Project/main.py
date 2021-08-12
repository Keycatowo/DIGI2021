from threading import Timer # 多執行緒
import time 
from fysom import Fysom # 有限狀態
import argparse
###################自定模組####################
from IFTTT import send_msg #傳送訊息
from voice_detect import get_command # 辨認語音指令
from voice_output import praise, ans_is_wrong, say_welcome # 讚美語句
from object_detect import get_object # 辨認物體
###################自定模組####################

def timer_msg():
    time.sleep(5)
    print("Send IFTTT message")
    # send_msg("1","2","3")
    Timer(100, timer_msg).start()  # 每100秒执行一次

def args_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model', help='File path of .tflite file.', required=False,
        default='mobilenet_ssd_v2_coco_quant.tflite')
    parser.add_argument(
        '--labels', help='File path of labels file.', required=False,
        default='coco_labels.txt')
    parser.add_argument(
        '--threshold',
        help='Score threshold for detected objects.',
        required=False,
        type=float,
        default=0.7)
    parser.add_argument(
        '--video',
        help='Video number',
        required=False,
        type=int,
        default=0)
    parser.add_argument(
        '--debug',
        help='Debug without some info reading',
        required=False,
        type=bool,
        default=0)
    parser.add_argument(
      '--file', help='File path of video(.mp4) file.', required=False,default="")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    
    args = args_parser() # 讀取參數

    # timer_msg() # 定時傳送IFTTT訊息
    
    # 定義有限狀態機
    state = Fysom(initial = "start",
            events=[("welcome", "start", "listen"),
                ("select_what", "listen", "camera_get"),
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
    if args.debug == True:
        state.welcome()


    while True :
        print("Now state = %s" % state.current)
        # 歡迎詞
        if state.current == "start":
            say_welcome()
            state.welcome()
            continue

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
            label = get_object(args) # TODO: 一個改多個
            state.show_ans()
            continue

        # 顯示答案
        if state.current == "Answer":
            # TODO: 顯示結果
            praise(label)
            state.what_end()
            continue

        # 物品探索模式
        if state.current == "Question":
            Q = "bottle" # TODO 隨機產生問題
            state.to_find()
            continue

        
        # 檢查是否符合
        if state.current == "camera_check":
            label = get_object(args)
            if label == Q:
                state.check_yes()
            else:
                
                ans_is_wrong(label, Q)
            continue
        
        # 讚美
        if state.current == "praise":
            praise(label)
            state.where_end()
            continue

        # 結束
        if state.current == "end":
            print("結束學習相機")
            exit()
        
    
    