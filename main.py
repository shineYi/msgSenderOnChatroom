import os
import pyautogui
import pyperclip
import platform
import subprocess


def run_kakao(kakao_path):
    print('Run KakaoTalk')
    try:
        subprocess.run(kakao_path)
    except Exception:
        print(f'[ERROR] Execute Kakaotalk path: {kakao_path}')
        raise


def enter_chatroom(chat_idx, retina_user):
    chat_imgs = ['chat.png', 'chat_with_msg.png']
    for chat_png in chat_imgs:
        try:
            click_img(chat_png, retina_user)
        except TypeError:
            pass
        except Exception:
            print(f'[ERROR] Click image: {chat_png}')
            raise

    # Focus on 1st chatroom
    pyautogui.hotkey('home')
    print(f"Enter the {chat_idx}th chatroom")
    for _ in range(1, chat_idx):
        pyautogui.press('down')
    pyautogui.press('enter')


# TODO: Return response to sending msg (Need Cursor check)
def send_msg(msg, cmd):
    pyperclip.copy(msg)
    pyautogui.hotkey(cmd, 'v')
    pyautogui.press('enter')


def click_img(png_name, retina_user):
    img_path = os.path.join('img', png_name)
    location = pyautogui.locateCenterOnScreen(img_path, confidence=0.9)
    x, y = location
    if retina_user:
        x = x / 2
        y = y / 2
    pyautogui.click(x, y)


# XXX: KakaoTalk path is set only to default install path
def config_by_os():
    user_os = platform.system()
    kakao_path = ['C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe']
    cmd = 'ctrl'
    retina_user = False
    if user_os == 'Darwin':
        kakao_path = ['open', '-a', 'KakaoTalk']
        cmd = 'command'
        if subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0:
            retina_user = True
    return kakao_path, cmd, retina_user


def talk_check():
    chatroom_idx = 3
    my_msg = '출근했습니다'
    kakao_path, cmd_key, retina_user = config_by_os()
    success = False

    try:
        run_kakao(kakao_path)
        enter_chatroom(chatroom_idx, retina_user)
        send_msg(my_msg, cmd_key)
        success = True
    except Exception as e:
        print(f'Error: {e}')

    return success


if __name__ == "__main__":
    pyautogui.PAUSE = 0.5
    python_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(python_path)

    talk_result = talk_check()
    if talk_result:
        exit(0)
    else:
        exit(1)
