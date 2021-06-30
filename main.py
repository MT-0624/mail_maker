# coding:UTF-8
import yaml
import sys
import os
import datetime

FORMAT_PATH = r"./format.yaml"
SENDER_INFO = r"./personal/sender.yaml"
CODEC = "UTF-8"

# 設定の読み込み作業
try:
    with open(FORMAT_PATH, "r", encoding=CODEC) as f:
        word_format = yaml.safe_load(f)

    with open(SENDER_INFO, "r", encoding=CODEC) as f:
        sender = yaml.safe_load(f)

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print('Exception occurred while loading YAML...', file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)


def generator(d_belong, d_name, honor, _body, _cushion):
    message = ""

    # 先頭文
    message += f"{d_belong}\n{d_name} {honor}\n"
    message += word_format["greeting"]["first"] + "\n"
    # 名乗り
    message += sender["signature"]["belong"] + "\n"
    message += sender["signature"]["name"] + "です。\n"

    message += _cushion

    message += "\n\n"

    # 要件追加
    message += _body
    message += "\n"

    orn = word_format["ornament"]["grid"]
    grid = orn["char"] * orn["length"] + "\n"

    message += "\n" + grid
    for i in sender["signature"]:
        value = sender["signature"][i]
        message += value + "\n"
    message += grid
    return message


if __name__ == '__main__':

    args = sys.argv

    # 伝達内容のパスを予め指定する
    if len(args) == 2:
        # python3 main.py {txtファイルのパス}　を実行した場合
        MESSAGE_PATH = repr(args[1])
    elif len(args) == 1:
        # python3 main.py　を実行した場合
        os.system('cls')
        MESSAGE_PATH = input("伝達内容(txt形式)の絶対パス >>")

        if MESSAGE_PATH[0] == "\"" and MESSAGE_PATH[-1] == "\"":
            MESSAGE_PATH = MESSAGE_PATH[1:-1]

        try:
            with open(MESSAGE_PATH, "r", encoding=CODEC) as f:
                body = f.read()
        except FileNotFoundError as e:
            print(e)
    else:
        raise ValueError(repr(args))

    # message = generator("步華步華株式会社", "古賀", honor="様", _body=body, _cushion=word_format["greeting"]["night_apology"])

    while True:
        os.system('cls')
        dest_belong = input("宛先の企業・団体名 >>")
        dest_name = input("名前・部門名 >>")

        honorific = "敬称"

        while honorific not in ("様", "御中", ""):
            os.system('cls')
            print("敬称【様・御中】を設定します")
            honorific = input("人物ならpを、団体ならgを入力、nを押すと何も付けません >>")

            if honorific == "p":
                honorific = "様"
            if honorific == "g":
                honorific = "御中"
            if honorific == "n":
                honorific = ""
        os.system('cls')
        print("クッション文を設定します")
        cushion = input("送信予定時刻が夜間...[n]\n返信が遅れている...[l]\n[デフォルト値:なし] >>")

        if cushion == "n":
            cushion = word_format["greeting"]["night_apology"]
        elif cushion == "l":
            cushion = word_format["greeting"]["late_apology"]
        else:
            cushion = ""

        # 本文ファイルを開く

        message = generator(d_name=dest_name,
                            d_belong=dest_belong,
                            honor=honorific,
                            _body=body,
                            _cushion=cushion)
        break

    now = datetime.datetime.now()

    if not (os.path.exists(r"./output")):
        os.mkdir(r"./output")

    filename = "./output/" + now.strftime('%Y%m%d_%H%M%S') + '.txt'
    print(filename)

    with open(filename, "w", encoding=CODEC) as f:
        f.write(message)

    file = os.path.abspath(filename)
    os.system(f"notepad {file}")
