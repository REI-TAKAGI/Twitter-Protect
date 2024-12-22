from datetime import datetime, timedelta
from sikuli import *
import shutil
import os

# Chromeが起動して、Googleのロゴが表示されるまで待つ
App.open("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")  # Chromeの起動
sleep(3)  # Chromeが完全に起動するまで待機
wait("google_search.png", 30)

# アドレスバーにフォーカス
type("l", Key.CTRL)
sleep(1)

# URLを書き換え、アクセス
paste("https://x.com/pilotmryo/followers")
sleep(1)
type(Key.ENTER)
sleep(3)

# ページにアクセスしてフォロワー一覧が表示されるまで待つ
wait("follower-menu.png", 30)
sleep(1)

# グローバル変数としてフォロワー1行分の検索範囲を定義
follower_row_region = Region(597,230,592,98)  # フォロワー1行分の検索範囲

# 各フォロワーを順番にブロックする関数
def block_followers():
    global follower_row_region  # 関数内でグローバル変数を使用することを宣言

    follower_count = 1  # ブロックしたアカウント数を追跡
    max_blocks = 2000  # 最大ブロック数を設定
    timeout_duration = timedelta(seconds=3)  # タイムアウト時間（4秒）を設定
    start_time = datetime.now()  # タイマーの初期化

    while follower_count <= max_blocks:  # 最大ブロック数に達したら終了
        print("フォロワーエリアを処理中...")

        try:
            # メニューアイコンを範囲内で直接探索
            if follower_row_region.exists(Pattern("menu_icon.png").similar(0.80)):
                menu_icon = follower_row_region.find(Pattern(Pattern("menu_icon.png").targetOffset(52,0)).similar(0.80).targetOffset(52, 1))
                print("Menu icon found at: x=" + str(menu_icon.getX()) + ", y=" + str(menu_icon.getY()))
                click(menu_icon)
                sleep(0.1)
                start_time = datetime.now()  # タイマーをリセット

                if exists("block_option.png"):
                    click("block_option.png")
                    sleep(0.1)

                    if exists("confirm_block.png"):
                        click("confirm_block.png")
                        sleep(0.1)
                        print("Blocked follower number: " + str(follower_count))
                        follower_count += 1
                        start_time = datetime.now()  # タイマーをリセット

                        if follower_count > max_blocks:
                            print("Reached maximum block count: " + str(max_blocks))
                            return
                    else:
                        print("Confirmation dialog not found. Skipping.")
                else:
                    print("Block option not found. Skipping.")
            else:
                print("Menu icon not found. Skipping.")

        except FindFailed:
            print("Error: Failed to find menu icon or related elements.")

        # タイムアウト処理：4秒以上経過した場合
        if datetime.now() - start_time > timeout_duration:
            print("Timeout (" + str(timeout_duration.seconds) + "s). Forcing scroll arrow click.")
            if exists(Pattern("scroll_arrow.png").similar(0.80)):
                arrow = find(Pattern(Pattern("scroll_arrow.png").targetOffset(69,32)).similar(0.8).targetOffset(69, 30))
                print("Clicking scroll arrow at: x=" + str(arrow.getX()) + ", y=" + str(arrow.getY()))
                click(arrow)
                start_time = datetime.now()  # タイマーをリセット
            else:
                print("Scroll arrow not found. Skipping forced scroll.")

        # 「ブロック中」のアイコンを確認してスクロール
        while follower_row_region.exists(Pattern("blocked_icon.png").similar(0.80)):
            print("Blocked icon detected. Scrolling...")
            wheel(WHEEL_DOWN, 1)  # スクロールホイールで1段階下にスクロール
            sleep(0.1)

        print("Blocked icon not found. Proceeding to the next operation.")

# メイン処理の実行
block_followers()