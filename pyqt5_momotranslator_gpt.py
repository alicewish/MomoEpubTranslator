import os
import os.path
import re
import sys
from ast import Import, ImportFrom, parse, walk
from collections import Counter, OrderedDict
from copy import deepcopy
from datetime import datetime
from functools import wraps
from getpass import getuser
from hashlib import md5
from html import unescape
from locale import getdefaultlocale
from os.path import abspath, dirname, exists, expanduser, getsize, isfile
from pathlib import Path
from platform import machine, processor, system, uname, python_version
from pprint import pprint
from re import I, findall, match, IGNORECASE, sub, fullmatch, escape, search
from shutil import copy2, copytree
from subprocess import PIPE, Popen
from time import localtime, sleep, strftime, time
from traceback import print_exc
from urllib.parse import urlparse
from uuid import getnode
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

import Quartz
import osascript
import pkg_resources
import pyperclip
import validators
from PIL import Image
from bs4 import BeautifulSoup
from cv2 import COLOR_RGB2BGR, cvtColor, imencode
from deep_translator import GoogleTranslator
from html2text import HTML2Text
from loguru import logger
from lxml import etree as ET
from natsort import natsorted
from nltk.corpus import names
from numpy import array
from pathvalidate import sanitize_filename
from prettytable import PrettyTable
from psutil import virtual_memory
from pyautogui import locateOnScreen, locate, center, click, keyDown, keyUp
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import HtmlLexer
from pytz import UTC
from stdlib_list import stdlib_list
from tqdm import tqdm

good_names = set(names.words())


# ================================参数区================================
def a1_const():
    return


# Platforms
SYSTEM = ''
platform_system = system()
platform_uname = uname()
os_kernal = platform_uname.machine
if os_kernal in ['x86_64', 'AMD64']:
    if platform_system == 'Windows':
        SYSTEM = 'WINDOWS'
    elif platform_system == 'Linux':
        SYSTEM = 'LINUX'
    else:  # 'Darwin'
        SYSTEM = 'MAC'
else:  # os_kernal = 'arm64'
    if platform_system == 'Windows':
        SYSTEM = 'WINDOWS'
    elif platform_system == 'Darwin':
        SYSTEM = 'M1'
    else:
        SYSTEM = 'PI'

locale_tup = getdefaultlocale()
lang_code = locale_tup[0]

username = getuser()
homedir = expanduser("~")
homedir = Path(homedir)
DOWNLOADS = homedir / 'Downloads'
DOCUMENTS = homedir / 'Documents'
MOVIES = homedir / 'Movies'

mac_address = ':'.join(findall('..', '%012x' % getnode()))
node_name = platform_uname.node

current_dir = dirname(abspath(__file__))
current_dir = Path(current_dir)

dirpath = os.getcwd()
ProgramFolder = Path(dirpath)
UserDataFolder = ProgramFolder / 'MomoHanhuaUserData'

python_vs = f"{sys.version_info.major}.{sys.version_info.minor}"

APP_NAME = 'MomoTranslator'
MAJOR_VERSION = 2
MINOR_VERSION = 0
PATCH_VERSION = 0
APP_VERSION = f'v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}'

APP_AUTHOR = '墨问非名'

if SYSTEM == 'WINDOWS':
    encoding = 'gbk'
    line_feed = '\n'
    cmct = 'ctrl'
else:
    encoding = 'utf-8'
    line_feed = '\n'
    cmct = 'command'

if SYSTEM in ['MAC', 'M1']:
    import applescript
    from Quartz import CGEventCreateMouseEvent, CGEventPost, kCGEventLeftMouseDown, kCGEventLeftMouseUp, \
        kCGMouseButtonLeft, kCGHIDEventTap, CGEventSetType
    from Quartz.CoreGraphics import CGPoint
    from AppKit import NSApplicationActivateIgnoringOtherApps, NSWorkspace

    processor_name = processor()
else:
    processor_name = machine()

if SYSTEM == 'WINDOWS':
    import pytesseract

    # 如果PATH中没有tesseract可执行文件，请指定tesseract路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

line_feeds = line_feed * 2

lf = line_feed
lfs = line_feeds

DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'

ignores = ('~$', '._')

type_dic = {
    'xlsx': '.xlsx',
    'csv': '.csv',
    'pr': '.prproj',
    'psd': '.psd',
    'tor': '.torrent',
    'xml': '.xml',
    'audio': ('.aif', '.mp3', '.wav', '.flac', '.m4a', '.ogg'),
    'video': ('.mp4', '.mkv', '.avi', '.flv', '.mov', '.wmv'),
    'compressed': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
    'font': ('.ttc', '.ttf', '.otf'),
    'comic': ('.cbr', '.cbz', '.rar', '.zip', '.pdf', '.txt'),
    'pic': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'),
    'log': '.log',
    'json': '.json',
    'pickle': '.pkl',
    'python': '.py',
    'txt': '.txt',
    'doc': ('.doc', '.docx'),
    'ppt': ('.ppt', '.pptx'),
    'pdf': '.pdf',
    'html': ('.html', '.htm', '.xhtml'),
    'css': '.css',
    'js': '.js',
    'markdown': ('.md', '.markdown'),
}

ram = str(round(virtual_memory().total / (1024.0 ** 3)))

python_ver = python_version()

span_map = {}

google_max_chars = 5000

py_path = Path(__file__).resolve()

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
p_color = re.compile(r'([a-fA-F0-9]{6})-?(\d{0,3})', I)
p_issue_w_dot = re.compile(r'(.+?)(?!\d) (\d{2,5})', I)
p_ISBN = re.compile(r'(?:-13)?:?\s?(?:978|979)?[\-]?\d{1,5}[\-]?\d{1,7}[\-]?\d{1,7}[\-]?\d{1,7}[\-]?(?:\d|X)', I)
p_decimal_or_comma = re.compile(r'^\d*\.?\d*$|^\d*[,]?\d*$', I)
# p_en = re.compile(r"(?<![A-Za-z0-9@'-])[A-Za-z0-9@'-]+(?:'[A-Za-z0-9@'-]+)*(?![A-Za-z0-9@'-])")
# 正则表达式匹配连续英文单词、逗号、点和电子邮件
p_en = re.compile(r'（?[A-Za-z0-9äöüßÄÖÜéèêñçàìòùáíóúýė@,\.\'-]+(?:\s+[A-Za-z0-9äöüßÄÖÜéèêñçàìòùáíóúýė@,\.\'-]+)*）?')

# 标点符号，排除 '.com'
p_punct = re.compile(r'([,.:;?!，。：；？！、…])(?!\s|com)')

roman_numerals_upper = [
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV",
    "XVI", "XVII", "XVIII", "XIX", "XX"
]

roman_numerals_lower = [
    "i", "ii", "iii", "iv", "v",
    "vi", "vii", "viii", "ix", "x",
    "xi", "xii", "xiii", "xiv", "xv",
    "xvi", "xvii", "xviii", "xix", "xx"
]
roman_numerals = roman_numerals_upper + roman_numerals_lower

untranslatables = [
    'Pinterest',
    'Instagram',
    'Spotify',
    'Moleskine',
    'Snapchat',
    'TikTok',
    'Reddit',
    'DoorDash',
    'Target',
    'Uber',
    'iPhone',
    'Oral-B',
    'Zoom',
    'ID',
    'SUV',
    'CD',
    'DVD',
    'LED',
    'PX',
    'Uno',
    'Visa',
    'ChatGPT',
    'WAPA',
    'HGTV',
    'Brita',
    'FaceBook',
    'Meta',
    'IBM',
    # 'Wager',
]

# 英文到中文的章节映射字典
chapter_map = {
    "One": "一",
    "Two": "二",
    "Three": "三",
    "Four": "四",
    "Five": "五",
    "Six": "六",
    "Seven": "七",
    "Eight": "八",
    "Nine": "九",
    "Ten": "十",
    "Eleven": "十一",
    "Twelve": "十二",
    "Thirteen": "十三",
    "Fourteen": "十四",
    "Fifteen": "十五",
    "Sixteen": "十六",
    "Seventeen": "十七",
    "Eighteen": "十八",
    "Nineteen": "十九",
    "Twenty": "二十",
    "Twenty-One": "二十一",
    "Twenty-Two": "二十二",
    "Twenty-Three": "二十三",
    "Twenty-Four": "二十四",
    "Twenty-Five": "二十五",
    "Twenty-Six": "二十六",
    "Twenty-Seven": "二十七",
    "Twenty-Eight": "二十八",
    "Twenty-Nine": "二十九",
    "Thirty": "三十",
    "Thirty-One": "三十一",
    "Thirty-Two": "三十二",
    "Thirty-Three": "三十三",
    "Thirty-Four": "三十四",
    "Thirty-Five": "三十五",
    "Thirty-Six": "三十六",
    "Thirty-Seven": "三十七",
    "Thirty-Eight": "三十八",
    "Thirty-Nine": "三十九",
    "Forty": "四十",
    "Forty-One": "四十一",
    "Forty-Two": "四十二",
    "Forty-Three": "四十三",
    "Forty-Four": "四十四",
    "Forty-Five": "四十五",
    "Forty-Six": "四十六",
    "Forty-Seven": "四十七",
    "Forty-Eight": "四十八",
    "Forty-Nine": "四十九",
    "Fifty": "五十",
    "Fifty-One": "五十一",
    "Fifty-Two": "五十二",
    "Fifty-Three": "五十三",
    "Fifty-Four": "五十四",
    "Fifty-Five": "五十五",
    "Fifty-Six": "五十六",
    "Fifty-Seven": "五十七",
    "Fifty-Eight": "五十八",
    "Fifty-Nine": "五十九",
    "Sixty": "六十",
    "Sixty-One": "六十一",
    "Sixty-Two": "六十二",
    "Sixty-Three": "六十三",
    "Sixty-Four": "六十四",
    "Sixty-Five": "六十五",
    "Sixty-Six": "六十六",
    "Sixty-Seven": "六十七",
    "Sixty-Eight": "六十八",
    "Sixty-Nine": "六十九",
    "Seventy": "七十",
    "Seventy-One": "七十一",
    "Seventy-Two": "七十二",
    "Seventy-Three": "七十三",
    "Seventy-Four": "七十四",
    "Seventy-Five": "七十五",
    "Seventy-Six": "七十六",
    "Seventy-Seven": "七十七",
    "Seventy-Eight": "七十八",
    "Seventy-Nine": "七十九",
    "Eighty": "八十",
    "Eighty-One": "八十一",
    "Eighty-Two": "八十二",
    "Eighty-Three": "八十三",
    "Eighty-Four": "八十四",
    "Eighty-Five": "八十五",
    "Eighty-Six": "八十六",
    "Eighty-Seven": "八十七",
    "Eighty-Eight": "八十八",
    "Eighty-Nine": "八十九",
    "Ninety": "九十",
    "Ninety-One": "九十一",
    "Ninety-Two": "九十二",
    "Ninety-Three": "九十三",
    "Ninety-Four": "九十四",
    "Ninety-Five": "九十五",
    "Ninety-Six": "九十六",
    "Ninety-Seven": "九十七",
    "Ninety-Eight": "九十八",
    "Ninety-Nine": "九十九",
}

numbers = list(chapter_map.keys())
lower_numbers = [x.lower() for x in numbers]

ignore_texts = [
    'ePub r1.0',
    'ePub base r1.2',
    'A.B.',
    'itr.1',
    'con.1',
    'app.1',
]

ignore_texts += untranslatables

# 创建一个新的 KeyboardEvent，模拟按下回车键。
# 'keydown' 是事件类型，表示一个按键被按下。
# 'key' 和 'code' 属性分别表示按下的按键和按键代码。
# 'which' 属性表示按键的字符编码。
# 'bubbles' 和 'cancelable' 属性表示事件是否可以冒泡和被取消。
press_enter_js = '''
var event = new KeyboardEvent('keydown', {
    'key': 'Enter',
    'code': 'Enter',
    'which': 13,
    'bubbles': true,
    'cancelable': true
});
Array.from(document.querySelectorAll('textarea'))[0].dispatchEvent(event);
'''

as_paste = f'''
delay 0.5
tell application "System Events"
    key code 9 using command down
end tell
'''

as_paste_n_enter = f'''
delay 0.5
tell application "System Events"
    key code 9 using command down
    delay 0.5
    key code 36
end tell
'''

as_enter = f'''
delay 0.5
tell application "System Events"
    key code 36
end tell
'''

as_funk = """
set soundName to "Funk"
do shell script "afplay /System/Library/Sounds/" & soundName & ".aiff"
"""

as_submarine = """
set soundName to "Submarine"
do shell script "afplay /System/Library/Sounds/" & soundName & ".aiff"
"""

as_Tingting_uploaded = f"""
say "全部上传完毕" speaking rate 180
"""

gpt_user_str = ''

glossary_str = """
Desiree
黛丝蕾
"""

button_js_code = """
var buttons = Array.from(document.querySelectorAll('button[aria-label=\'附加文件\']'));
if (buttons.length > 0) {
    buttons[0].click();
}
console.log('找到按钮数量：', buttons.length);
"""

chatgpt_prefix = 'https://chatgpt.com/'

ForegroundWindow_as = """
global frontApp, frontAppName, windowTitle

set windowTitle to ""
tell application "System Events"
	set frontApp to first application process whose frontmost is true
	set frontAppName to name of frontApp
	tell process frontAppName
		tell (1st window whose value of attribute "AXMain" is true)
			set windowTitle to value of attribute "AXTitle"
		end tell
	end tell
end tell

return {frontAppName & "
" & windowTitle}
"""

activate_app_voice_str = '调用'

as_Tingting_activate = f"""
say "{activate_app_voice_str}" speaking rate 180
"""

# 定义自闭合标签列表
void_tags = {
    'img', 'input', 'br', 'meta', 'link', 'hr', 'base', 'col', 'command', 'embed', 'keygen', 'param',
    'source', 'track', 'wbr', 'area',
    # 'span',
}

replacements = {
    '@public@vhost@g@gutenberg@html@files@16464@16464-h@16464-h-': 'ψ',
    'Lowe_9780804137133_epub_': 'ω',
    'Gran_9780385534277_epub3_': 'Θ'
}


# ================================基础函数区================================
def a2_base():
    return


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        elapsed_time = time() - start_time

        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)

        if hours > 0:
            show_run_time = f"{int(hours)}时{int(minutes)}分{seconds:.2f}秒"
        elif minutes > 0:
            show_run_time = f"{int(minutes)}分{seconds:.2f}秒"
        else:
            show_run_time = f"{seconds:.2f}秒"

        logger.debug(f"{func.__name__} took: {show_run_time}")
        return result

    return wrapper


def is_decimal_or_comma(s):
    return bool(match(p_decimal_or_comma, s))


def is_valid_file(file_path, suffixes):
    if not file_path.is_file():
        return False
    if not file_path.stem.startswith(ignores):
        if suffixes:
            return file_path.suffix.lower() in suffixes
        else:
            return True
    return False


def printe(e):
    print(e)
    logger.error(e)
    print_exc()


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def reduce_list(input_list):
    try:
        # 尝试使用dict.fromkeys方法
        output_list = list(OrderedDict.fromkeys(input_list))
    except TypeError:
        # 如果发生TypeError（可能是因为列表包含不可哈希的对象），
        # 则改用更慢的方法
        output_list = []
        for input in input_list:
            if input not in output_list:
                output_list.append(input)
    return output_list


# ================创建目录================
def make_dir(file_path):
    if not exists(file_path):
        try:
            os.makedirs(file_path)
        except BaseException as e:
            print(e)


# ================获取文件夹列表================
def get_dirs(rootdir):
    dirs_list = []
    if rootdir and rootdir.exists():
        # 列出目录下的所有文件和目录
        lines = os.listdir(rootdir)
        for line in lines:
            filepath = Path(rootdir) / line
            if filepath.is_dir():
                dirs_list.append(filepath)
    dirs_list.sort()
    return dirs_list


def get_files(rootdir, file_type=None, direct=False):
    rootdir = Path(rootdir)
    file_paths = []

    # 获取文件类型的后缀
    # 默认为所有文件
    suffixes = type_dic.get(file_type, file_type)
    if isinstance(suffixes, str):
        suffixes = (suffixes,)

    # 如果根目录存在
    if rootdir and rootdir.exists():
        # 只读取当前文件夹下的文件
        if direct:
            files = os.listdir(rootdir)
            for file in files:
                file_path = Path(rootdir) / file
                if is_valid_file(file_path, suffixes):
                    file_paths.append(file_path)
        # 读取所有文件
        else:
            for root, dirs, files in os.walk(rootdir):
                for file in files:
                    file_path = Path(root) / file
                    if is_valid_file(file_path, suffixes):
                        file_paths.append(file_path)

    # 使用natsorted()进行自然排序，
    # 使列表中的字符串按照数字顺序进行排序
    file_paths = natsorted(file_paths)
    return file_paths


# ================读取文本================
def read_txt(file_path, encoding='utf-8'):
    """
    读取指定文件路径的文本内容。

    :param file_path: 文件路径
    :param encoding: 文件编码，默认为'utf-8'
    :return: 返回读取到的文件内容，如果文件不存在则返回None
    """
    file_content = None
    # 行分隔符（Line Separator, LS, \u2028）
    # 段落分隔符（Paragraph Separator, PS, \u2029）
    if file_path.exists():
        with open(file_path, mode='r', encoding=encoding) as file_object:
            file_content = file_object.read()
            file_content = file_content.replace('\u2028', '').replace('\u2029', '')
    return file_content


# ================写入文件================
def write_txt(file_path, text_input, encoding='utf-8', ignore_empty=True):
    """
    将文本内容写入指定的文件路径。

    :param file_path: 文件路径
    :param text_input: 要写入的文本内容，可以是字符串或字符串列表
    :param encoding: 文件编码，默认为'utf-8'
    :param ignore_empty: 是否忽略空内容，默认为True
    """
    if text_input:
        save_text = True
        if isinstance(text_input, list):
            otext = lf.join(text_input)
        else:
            otext = text_input
        file_content = read_txt(file_path, encoding)
        if file_content == otext or (ignore_empty and otext == ''):
            save_text = False
        if save_text:
            with open(file_path, mode='w', encoding=encoding, errors='ignore') as f:
                f.write(otext)


def generate_md5(img_array):
    img_data = imencode('.png', img_array)[1].tostring()
    file_hash = md5()
    file_hash.update(img_data)
    return file_hash.hexdigest()


# ================对文件算MD5================
def md5_w_size(path, blksize=2 ** 20):
    if isfile(path) and exists(path):  # 判断目标是否文件,及是否存在
        file_size = getsize(path)
        if file_size <= 256 * 1024 * 1024:  # 512MB
            with open(path, 'rb') as f:
                cont = f.read()
            hash_object = md5(cont)
            t_md5 = hash_object.hexdigest()
            return t_md5, file_size
        else:
            m = md5()
            with open(path, 'rb') as f:
                while True:
                    buf = f.read(blksize)
                    if not buf:
                        break
                    m.update(buf)
            t_md5 = m.hexdigest()
            return t_md5, file_size
    else:
        return None


@logger.catch
def write_pic(pic_path, picimg):
    pic_path = Path(pic_path)
    ext = pic_path.suffix
    temp_pic = pic_path.parent / f'{pic_path.stem}-temp{ext}'

    # 检查输入图像的类型
    if isinstance(picimg, bytes):
        # 如果是字节对象，直接写入文件
        with open(temp_pic, 'wb') as f:
            f.write(picimg)
    else:
        # 如果是PIL图像，转换为NumPy数组
        if isinstance(picimg, Image.Image):
            picimg = array(picimg)

            # 如果图像有三个维度，并且颜色为三通道，则进行颜色空间的转换
            if picimg.ndim == 3 and picimg.shape[2] == 3:
                picimg = cvtColor(picimg, COLOR_RGB2BGR)

        # 检查图像是否为空
        if picimg is None or picimg.size == 0:
            logger.error(f'{pic_path=}')
            # raise ValueError("The input image is empty.")
            return pic_path

        # 保存临时图像
        imencode(ext, picimg)[1].tofile(temp_pic)
    # 检查临时图像和目标图像的md5哈希和大小是否相同
    if not pic_path.exists() or md5_w_size(temp_pic) != md5_w_size(pic_path):
        copy2(temp_pic, pic_path)
    # 删除临时图像
    if temp_pic.exists():
        os.remove(temp_pic)
    return pic_path


# ================运行时间计时================
# @logger.catch
def run_time(start_time):
    rtime = time() - start_time
    show_run_time = ''
    if rtime >= 3600:
        show_run_time += f'{(rtime // 3600):.0f}时'
    if rtime >= 60:
        show_run_time += f'{(rtime % 3600 // 60):.0f}分'
    show_run_time += f'{(rtime % 60):.2f}秒'
    return show_run_time


# ================当前时间================
# @logger.catch
def current_time():
    now_time_str = strftime(DATE_FORMATTER, localtime())
    return now_time_str


# @logger.catch
def time_utcnow():
    """Returns a timezone aware utc timestamp."""
    return datetime.now(UTC)


def common_prefix(strings):
    """
    返回字符串列表中的共同前缀。

    :param strings: 字符串列表
    :return: 共同前缀
    """
    # pprint(strings)
    if not strings:
        return ""
    common_prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(common_prefix):
            common_prefix = common_prefix[:-1]
            if not common_prefix:
                return ""
    return common_prefix


def common_suffix(strings):
    """
    返回字符串列表中的共同后缀。

    :param strings: 字符串列表
    :return: 共同后缀
    """
    if not strings:
        return ""
    common_suffix = strings[0]
    for s in strings[1:]:
        while not s.endswith(common_suffix):
            common_suffix = common_suffix[1:]
            if not common_suffix:
                return ""
    return common_suffix


# ================================基础图像函数区================================
def a3_pic():
    return


def get_clipboard_data():
    """
    从剪贴板获取数据
    :return 如果没有错误，返回剪贴板数据；否则返回 None
    """
    process = Popen(['pbpaste'], stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()

    if not error:
        return output.decode('utf-8')
    else:
        print("Error:", error)
        return None


# ================================图像函数区================================
def a4_apple_script():
    return


def remove_common_indent(script):
    """
    删除脚本中每行开头的相同长度的多余空格
    :param script: 要处理的脚本
    :return: 删除多余空格后的脚本
    """
    lines = script.split('\n')
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    return '\n'.join(line[min_indent:] for line in lines)


@logger.catch
@timer_decorator
def run_apple_script(script):
    """
    执行 AppleScript 脚本
    :param script：要执行的 AppleScript 脚本
    :return 如果执行成功，返回执行结果；否则返回 None
    """
    if script:
        script = remove_common_indent(script)
        # logger.debug(f'{script.strip()}')
        result = applescript.run(script)
        if result.code == 0:
            return result.out
        else:
            print(f'{result.err=}')


def get_browser_current_tab_url(browser):
    """
    获取浏览器当前标签页的 URL
    :param browser：浏览器名称，可以是 'Safari' 或 'Google Chrome'
    :return 当前标签页的 URL
    """
    if browser == 'Safari':
        apple_script = f'''
        tell application "{browser}"
            set current_url to URL of front document
            return current_url
        end tell
        '''
    elif browser.startswith('Google Chrome'):
        apple_script = f'''
        tell application "{browser}"
            set current_url to URL of active tab of front window
            return current_url
        end tell
        '''
    else:
        print(f"Error: Unsupported browser {browser}.")
        return None
    return run_apple_script(apple_script)


def get_browser_current_tab_title(browser):
    """
    获取浏览器当前标签页的标题
    :param browser：浏览器名称，可以是 'Safari' 或 'Chrome'
    :return 当前标签页的标题
    """
    if browser == 'Safari':
        apple_script = f'''
        tell application "{browser}"
            set current_title to name of front document
            return current_title
        end tell
        '''
    elif browser.startswith('Google Chrome'):
        apple_script = f'''
        tell application "{browser}"
            set current_title to title of active tab of front window
            return current_title
        end tell
        '''
    else:
        print(f"Error: Unsupported browser {browser}.")
        return None

    return run_apple_script(apple_script)


def get_browser_current_tab_html(browser, activate_browser=False):
    """
    获取浏览器当前标签页的 HTML 内容
    :param browser：浏览器名称，可以是 'Safari' 或 'Chrome'
    :return 当前标签页的 HTML 内容
    """
    js_code = "document.documentElement.outerHTML;"

    # 如果需要激活浏览器，则设置 activate_command 为 "activate"，否则为空字符串。
    activate_command = "activate" if activate_browser else ""

    if browser == 'Safari':
        apple_script = f'''
        tell application "{browser}"
            {activate_command}
            set curr_tab to current tab of front window
            do JavaScript "{js_code}" in curr_tab
            set the clipboard to result
            return (the clipboard as text)
        end tell
        '''
    elif browser.startswith('Google Chrome'):
        apple_script = f'''
        tell application "{browser}"
            {activate_command}
            set curr_tab to active tab of front window
            execute curr_tab javascript "{js_code}"
            set the clipboard to result
            return (the clipboard as text)
        end tell
        '''
    else:
        print(f"Error: Unsupported browser {browser}.")
        return None

    return run_apple_script(apple_script)


def open_html_file_in_browser(file_path, browser):
    """
    在浏览器中打开 HTML 文件
    :param file_path：HTML 文件的路径
    :param browser：浏览器名称，可以是 'Safari' 或 'Chrome'
    """
    apple_script = f'''
    tell application "{browser}"
        activate
        open POSIX file "{file_path}"
    end tell
    '''
    return run_apple_script(apple_script)


@timer_decorator
@logger.catch
def save_from_browser(browser: str):
    """
    主函数
    :param browser：浏览器名称，可以是 'Safari' 或 'Chrome'
    """
    current_url = get_browser_current_tab_url(browser)
    title = get_browser_current_tab_title(browser)
    logger.debug(f'{current_url=}')
    logger.warning(f'{title=}')
    if current_url and title:
        if current_url.startswith(chatgpt_prefix):
            safe_title = title.replace('/', '／').replace('\\', '＼')
            chatgpt_html_stem = f'{sanitize_filename(safe_title)}-{Path(current_url).stem}'
            chatgpt_html = ChatGPT / f'{chatgpt_html_stem}.html'
            logger.info(f'{chatgpt_html_stem=}')
            content = get_browser_current_tab_html(browser)
            # logger.info(f'{content}')
            soup = BeautifulSoup(content, 'html.parser')
            pretty_html = soup.prettify()
            write_txt(chatgpt_html, pretty_html)
    return chatgpt_html


def as_proc(as_code):
    try:
        result = applescript.run(as_code)
        print(f"Script output: {result.out}")
    except Exception as e:
        print(f"Script error: {e}")


def mouse_click(x, y):
    mouse_event = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, CGPoint(x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, mouse_event)
    CGEventSetType(mouse_event, kCGEventLeftMouseUp)
    CGEventPost(kCGHIDEventTap, mouse_event)


@timer_decorator
def fill_textarea(browser, input_text, activate_browser=True, hit_enter=True):
    """
    使用 AppleScript 在指定浏览器中查找并填充页面上的第一个 textarea 元素，然后模拟回车键的按下。

    :param browser (str): 浏览器名称，支持 'Safari' 和 'Google Chrome'。
    :param input_text (str): 需要填入 textarea 的文本。
    :param activate_browser (bool): 是否激活（前台显示）浏览器。

    :return: AppleScript 执行结果，如果有错误返回 None。
    """
    input_lines = input_text.splitlines()
    # 将输入文本复制到剪贴板
    pyperclip.copy(input_text)

    # 如果需要激活浏览器，则设置 activate_command 为 "activate"，否则为空字符串。
    activate_command = "activate" if activate_browser else ""

    js_command = press_enter_js
    as_command = as_paste_n_enter
    if not hit_enter:
        js_command = ''
        as_command = as_paste

    if len(input_lines) == 1:
        # 单行提问
        if browser == 'Safari':
            apple_script = f'''
            tell application "{browser}"
                {activate_command}
                do JavaScript "Array.from(document.querySelectorAll('textarea'))[0].value = '{input_text}'; {js_command}" in front document
            end tell
            '''
        elif browser.startswith('Google Chrome'):
            apple_script = f'''
            tell application "{browser}"
                {activate_command}
                set js_code to "Array.from(document.querySelectorAll('textarea'))[0].value = '{input_text}'; {js_command}"
                execute active tab of front window javascript js_code
            end tell
            '''
        else:
            print(f"Error: Unsupported browser {browser}.")
            return None
    else:
        # 多行提问
        if browser == 'Safari':
            apple_script = f'''
            tell application "{browser}"
                {activate_command}
                do JavaScript "Array.from(document.querySelectorAll('textarea'))[0].focus();" in front document
                {as_command}
            end tell
            '''
        elif browser.startswith('Google Chrome'):
            apple_script = f'''
            tell application "{browser}"
                {activate_command}
                set js_code to "Array.from(document.querySelectorAll('textarea'))[0].focus();"
                execute active tab of front window javascript js_code
                {as_command}
            end tell
            '''
        else:
            print(f"Error: Unsupported browser {browser}.")
            return None
    return run_apple_script(apple_script)


@timer_decorator
@logger.catch
def get_QA(browser, local_name=None, div_type='code'):
    """
    从当前浏览器中提取问答对，并进行格式化和清理。

    :param browser: 当前使用的浏览器名称
    :return: 包含已清理和格式化问答对的列表
    """
    # ================保存当前浏览器内容================
    if local_name:
        chatgpt_html = ChatGPT / f'{local_name}.html'
    else:
        chatgpt_html = save_from_browser(browser)
    chatgpt_text = read_txt(chatgpt_html)
    # ================解析当前浏览器内容================
    soup = BeautifulSoup(chatgpt_text, 'html.parser')
    # 删除所有不需要的标签，如 meta、script、link 和 style
    extra_tags = [
        'meta',
        'script',
        'link',
        'style',
    ]
    for extra_tag in extra_tags:
        for meta in soup.find_all(extra_tag):
            meta.decompose()

    # 查找并删除具有特定 class 的 <div> 标签
    extra_classes = [
        'overflow-x-hidden',  # 历史聊天记录
        'bottom-0',  # 侧边对话
    ]
    for extra_class in extra_classes:
        for div in soup.find_all('div', class_=extra_class):
            div.decompose()

    # 格式化HTML并去除多余的空行
    pretty_html = soup.prettify()
    simple_chatgpt_text = '\n'.join([line for line in pretty_html.splitlines() if line.strip()])
    simple_chatgpt_html = chatgpt_html.parent / f'{chatgpt_html.stem}_simple.html'
    write_txt(simple_chatgpt_html, simple_chatgpt_text)

    # ================进行问答解析================
    simple_soup = BeautifulSoup(simple_chatgpt_text, 'html.parser')
    target_tups = []
    # class_ = "min-h-[20px]"
    class_ = '[.text-message+&]:mt-5'
    message_divs = simple_soup.find_all('div', class_=class_)

    # 模型名称
    class_ = "line-clamp-1 text-sm"
    style = "opacity: 0; padding-left: 0px; width: 0px;"
    model_spans = simple_soup.find_all('span', class_=class_, style=style)
    # 打印找到的所有符合条件的<span>标签
    model_names = []
    for m in range(len(model_spans)):
        model_span = model_spans[m]
        model_name = model_span.get_text().strip()
        model_names.append(model_name)

    handler_normal = HTML2Text()
    handler_no_link = HTML2Text()
    # 如果不需要处理Markdown中的链接可以设置为True
    handler_no_link.ignore_links = True

    model_i = 0
    for m in range(len(message_divs)):
        message_div = message_divs[m]
        raw_div_str = str(message_div)
        # 根据文本特征判断发送者身份
        if 'max-w-[70%]' in raw_div_str:
            text_role = '用户'
            model_name = ''
        else:
            text_role = 'chatGPT'
            if model_i < len(model_names):
                model_name = model_names[model_i]
                model_i += 1
            else:
                model_name = ''

        # 查找 code 标签
        code_tag = message_div.find('code')
        if code_tag and div_type == 'code':
            # 如果找到 code 标签，提取其内容
            # 用于文稿翻译
            target_div = str(code_tag).strip()
        elif text_role == '用户':
            # 用户提问
            # 查找所有的<code>标签
            code_tags = message_div.find_all('code')
            # 替换<code>标签内容，用反引号包围其文本
            for code in code_tags:
                code.string = f"`{code.get_text(strip=True)}`"
            # 提取整个文档的文本，此时<code>中的文本已被修改
            target_div = message_div.get_text(strip=True)

            # 提问转为Markdown
            target_md = handler_normal.handle(raw_div_str).strip()
        else:
            # 回答转为Markdown
            target_div = handler_no_link.handle(raw_div_str).strip()
        target_tup = (text_role, model_name, target_div)
        target_tups.append(target_tup)
    return target_tups


@logger.catch
def get_target_tups(browser, div_type='code'):
    all_target_tups = []
    if read_local:
        target_tups = get_QA(browser, local_name, div_type=div_type)
    else:
        target_tups = get_QA(browser, div_type=div_type)
    all_target_tups.extend(target_tups)
    if read_history:
        for h in range(len(history_names)):
            history_name = history_names[h]
            target_tups = get_QA(browser, history_name, div_type=div_type)
            all_target_tups.extend(target_tups)
    return all_target_tups


def pt_print(window_list):
    # 创建PrettyTable对象
    table = PrettyTable()
    table.field_names = ["Window Number", "Owner Name", "Window Name"]

    info_tups = []
    # 填充表格数据
    for window in window_list:
        window = dict(window)
        bounds = window['kCGWindowBounds']
        window_number = window.get('kCGWindowNumber', 'N/A')
        owner_name = window.get('kCGWindowOwnerName', 'N/A')
        # 某些窗口可能没有标题
        window_name = window.get('kCGWindowName', 'N/A')
        table.add_row([window_number, owner_name, window_name])
        info_tup = (window_number, owner_name, window_name, bounds)
        info_tups.append(info_tup)
    # print(table)
    return info_tups


@logger.catch
@timer_decorator
def get_window_list():
    # 获取本屏幕所有窗口的列表
    screen_window_list = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID
    )

    # 获取所有窗口的列表，包括最小化的窗口
    window_list = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionAll,
        Quartz.kCGNullWindowID
    )

    print_list = window_list
    info_tups = pt_print(print_list)
    # print_list = screen_window_list
    # info_tups = pt_print(print_list)
    return info_tups


@logger.catch
@timer_decorator
def capture_screen_main():
    # 创建一个全屏的屏幕截图
    main_display_id = Quartz.CGMainDisplayID()
    region = Quartz.CGRectInfinite
    image_ref = Quartz.CGWindowListCreateImage(region, Quartz.kCGWindowListOptionOnScreenOnly, main_display_id,
                                               Quartz.kCGWindowImageDefault)

    # 将CGImage转换为PIL可用的Image对象
    width = Quartz.CGImageGetWidth(image_ref)
    height = Quartz.CGImageGetHeight(image_ref)
    bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)
    pixel_data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image_ref))

    # 注意：在这里，图像的数据格式需要与Quartz的输出匹配
    image = Image.frombytes("RGBA", (width, height), pixel_data, "raw", "BGRA", bytes_per_row, 1)
    image.save('screenshot.png')  # 保存截图


@logger.catch
# @timer_decorator
def capture_window(window_id):
    # 创建窗口截图
    image_ref = Quartz.CGWindowListCreateImage(
        Quartz.CGRectNull,
        Quartz.kCGWindowListOptionIncludingWindow,
        window_id,
        Quartz.kCGWindowImageBoundsIgnoreFraming
    )
    width = Quartz.CGImageGetWidth(image_ref)
    height = Quartz.CGImageGetHeight(image_ref)
    bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)
    pixel_data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image_ref))
    image = Image.frombytes("RGBA", (width, height), pixel_data, "raw", "BGRA", bytes_per_row, 1)
    return image


@timer_decorator
@logger.catch
def get_active_app():
    act_prog_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
    # logger.debug(f'{act_prog_name=}')
    code, out, err = osascript.run(ForegroundWindow_as.strip())
    infos = out.splitlines()
    # logger.debug(f'{out=}')
    act_window_name = ''
    if len(infos) >= 2:
        act_window_name = infos[1]
        # logger.debug(f'{act_window_name=}')
    return act_prog_name, act_window_name


@timer_decorator
@logger.catch
def get_active_app_info():
    # 获取当前活动的应用程序
    active_app = NSWorkspace.sharedWorkspace().frontmostApplication()

    # 获取应用程序的基本信息
    app_name = active_app.localizedName()  # 应用程序的名称
    bundle_id = active_app.bundleIdentifier()  # Bundle Identifier
    pid = active_app.processIdentifier()

    # 获取图标
    icon = active_app.icon()  # 返回NSImage对象

    # 获取活动状态
    is_active = active_app.isActive()  # 应用是否处于活动状态

    # 获取启动时间
    launch_date = active_app.launchDate()  # 返回NSDate对象，需要转换
    if launch_date:
        # 转换NSDate对象为Python datetime对象
        launch_date = datetime.fromtimestamp(launch_date.timeIntervalSince1970())
        launch_date_str = launch_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        launch_date_str = "Not available"

    # 获取隐藏状态
    is_hidden = active_app.isHidden()

    # 打印收集的信息
    print(f"App Name: {app_name}")
    print(f"Bundle ID: {bundle_id}")
    print(f"PID: {pid}")
    print(f"Active: {'Yes' if is_active else 'No'}")
    print(f"Launch Date: {launch_date_str}")
    print(f"Hidden: {'Yes' if is_hidden else 'No'}")
    app_tup = (app_name, bundle_id, pid)
    return app_tup


@logger.catch
def activate_app_base(app_name):
    # 获取所有运行的应用程序实例
    running_apps = NSWorkspace.sharedWorkspace().runningApplications()
    # 查找特定名称的应用程序
    for app in running_apps:
        # print(f"{app.localizedName()=}")
        if app.localizedName() == app_name:
            # 将应用程序调到前台
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            logger.info(f"{app_name}已调到前台")
            return True
    print(f"{app_name} not found.")
    return False


@timer_decorator
@logger.catch
def activate_app(app_name, wait_time=0):
    if wait_time == 5:
        pre_activate_str = f'{wait_time}秒后调用'
        as_pre_activate = f"""
        say "{pre_activate_str}" speaking rate 180
        """
        as_proc(as_pre_activate)
        sleep(wait_time)
    act_prog_name, act_window_name = get_active_app()
    if act_prog_name == app_name:
        pass
    else:
        logger.warning(f'{act_prog_name=}, {app_name=}')
        if wait_time == 0:
            as_proc(as_Tingting_activate)
        elif wait_time != 5:
            pre_activate_str = f'{wait_time}秒后调用'
            as_pre_activate = f"""
            say "{pre_activate_str}" speaking rate 180
            """
            as_proc(as_pre_activate)
            sleep(wait_time)
        activate_app_base(app_name)
        sleep(1)
        act_prog_name, act_window_name = get_active_app()
        if act_prog_name == app_name:
            pass
        else:
            logger.warning(f'{act_prog_name=}, {app_name=}')
            activate_app_base(app_name)
            return True
    return False


@logger.catch
def find_n_click(roi_logo, click_it=False):
    roi_location = None
    if ask_mode == 'web':
        app_name = browser
    else:
        app_name = 'ChatGPT'
    try:
        if click_it:
            # 调取浏览器或应用到前台
            activate_app(app_name, 1)
            logger.debug(f'{roi_logo=}')
            # ================必须前台================
            roi_location = locateOnScreen(roi_logo.as_posix(), confidence=0.98)
            if roi_location:
                logger.info(f'{roi_location=}')
                # 获取图片中心点坐标
                ct = center(roi_location)
                pos_x = int(ct.x / 2)
                pos_y = int(ct.y / 2)
                pos = (pos_x, pos_y)
                # logger.info(f'{ct=}')
                # logger.info(f'{pos=}')
                if click_type == 'pyautogui':
                    # click(ct)
                    click(pos)
                else:
                    mouse_click(pos_x, pos_y)
        else:
            # ================可以后台================
            image = capture_window(window_id)
            write_pic(ChatGPTApp_png, image)
            roi_location = locate(roi_logo.as_posix(), ChatGPTApp_png.as_posix())
            if roi_location:
                logger.info(f'{roi_location=}')
                # 获取图片中心点坐标
                ct = center(roi_location)
                pos_x = int(ct.x / 2)
                pos_y = int(ct.y / 2)
                pos = (pos_x, pos_y)
                # logger.info(f'{ct=}')
                # logger.info(f'{pos=}')
    except Exception as e:
        pass
    return roi_location


@logger.catch
def warn_user(warn_str):
    logger.error(warn_str)
    as_proc(as_funk)
    voice_str = warn_str.replace('重', '虫')
    as_warn_Tingting = f"""
    say "{voice_str}" speaking rate 180
    """
    as_proc(as_warn_Tingting)


@logger.catch
def gpt_translate(roi_htmls, prompt_prefix):
    # ================排除已经翻译的部分================
    need2trans_lines = []
    roi_htmls = reduce_list(roi_htmls)
    for r in range(len(roi_htmls)):
        roi_html = roi_htmls[r]
        src_soup = BeautifulSoup(roi_html, 'html.parser')
        src_1st_tag = src_soup.find()
        src_opening = roi_html.split('>')[0] + '>'
        src_closing = f"</{src_1st_tag.name}>"
        src_content = roi_html.removeprefix(src_opening).removesuffix(src_closing)
        src_content = src_content.replace('\xa0', ' ').replace('\u2002', ' ')
        if src_content not in main_gpt_dic:
            need2trans_lines.append(roi_html)
            # logger.debug(f'{src_1st_tag=}')
            # logger.debug(f'{src_opening=}')
            # logger.debug(f'{src_closing=}')
            # logger.debug(f'{src_content=}')
    need2trans_lines = reduce_list(need2trans_lines)
    html_text = lf.join(need2trans_lines)
    split_lines_raw = get_split_lines(html_text)
    split_lines_raw = [x for x in split_lines_raw if x != []]
    split_lines = []
    # ================添加提示词================
    for s in range(len(split_lines_raw)):
        input_lines = split_lines_raw[s]
        input_text = lf.join(input_lines)
        full_prompt = f'{prompt_prefix}{lf}```html{lf}{input_text}{lf}```'
        possible_divs = [x for x in target_tups if x[0] == '用户' and full_prompt in x[-1]]
        if possible_divs and False:
            # ================已经提问的段落================
            logger.debug(full_prompt)
            possible_div = possible_divs[0]
            possible_ind = target_tups.index(possible_div)
            logger.warning(f'已经提问[{s + 1}/{len(split_lines_raw)}], {possible_ind=}')
        else:
            # ================尚未提问的段落================
            split_lines.append(input_lines)
            if len(split_lines) <= max_limit:
                logger.warning(f'尚未提问[{s + 1}/{len(split_lines_raw)}], {len(input_lines)=}, {len(input_text)=}')
                logger.info(full_prompt)
    if do_automate and split_lines:
        if ask_mode == 'web':
            for s in range(len(split_lines)):
                input_lines = split_lines[s]
                input_text = lf.join(input_lines)
                full_prompt = f'{prompt_prefix}{lf}```html{lf}{input_text}{lf}```'
                fill_textarea(browser, full_prompt, activate_browser, hit_enter)
                if s != len(split_lines):
                    stime = web_answer_time
                else:
                    # 最后一次等待时间
                    stime = int(0.6 * web_answer_time)
                break
                # 等待回答完成
                sleep(stime)
        else:
            for s in range(len(split_lines)):
                input_lines = split_lines[s]
                input_text = lf.join(input_lines)
                full_prompt = f'{prompt_prefix}{lf}```html{lf}{input_text}{lf}```'
                if s < max_limit:
                    logger.warning(
                        f'[{s + 1}/{len(split_lines_raw)}], {len(input_lines)=}, {len(input_text)=}')
                    logger.info(full_prompt)
                    if force_gpt4:
                        your_limit_location = find_n_click(your_limit_logo)
                        if your_limit_location:
                            logger.error(f'{your_limit_location=}')
                            warn_user('已到限额')
                            break
                        ChatGPT4o_location = find_n_click(ChatGPT4o_logo)
                        if ChatGPT4o_location:
                            logger.error(f'{ChatGPT4o_location=}')
                            warn_user('已变成GPT4o')
                            break
                    retry_location = find_n_click(retry_logo)
                    if retry_location:
                        logger.error(f'{retry_location=}')
                        warn_user('需重试')
                        break
                    reconnect_location = find_n_click(reconnect_logo)
                    if reconnect_location:
                        logger.error(f'{reconnect_location=}')
                        warn_user('需重连')
                        sleep(10)  # 等待用户手动处理
                        reconnect_location = find_n_click(reconnect_logo)
                        if reconnect_location:
                            logger.error(f'{reconnect_location=}')
                            warn_user('需重连')
                            break

                    # 调取浏览器或应用到前台
                    act_prog_name, act_window_name = get_active_app()
                    activate_app(app_name, 4)
                    sleep(0.2)
                    # 粘贴prompt
                    pyperclip.copy(full_prompt)
                    sleep(0.05)
                    as_proc(as_paste)
                    sleep(1)

                    if hit_enter:
                        # 按下回车键
                        keyDown('enter')
                        sleep(0.1)
                        keyUp('enter')

                        sleep(1)
                        activate_app_base(act_prog_name)
                        sleep(1)

                        up_arrow_location = find_n_click(up_arrow_logo)
                        if up_arrow_location:
                            logger.error(f'{up_arrow_location=}')
                            warn_user('没按出回车')
                            break

                        sleep(3)
                        retry_location = find_n_click(retry_logo)
                        if retry_location:
                            logger.error(f'{retry_location=}')
                            warn_user('需重试')
                            break

                        if s == max_limit - 1:
                            # ================所有图片上传完毕================
                            as_proc(as_submarine)
                            as_proc(as_Tingting_uploaded)
                            break

                        # 等待回答
                        for _ in tqdm(range(int(app_answer_time / 5)), desc="等待"):
                            sleep(5)
                        # sleep(app_answer_time)

                        # ================确保答案已经生成完毕================
                        headphone_location = None
                        for a in range(50):
                            # 找到屏幕上的图片位置
                            headphone_location = find_n_click(headphone_logo)
                            if headphone_location:
                                # 如果找到就不再等待
                                logger.info(f'{headphone_location=}')
                                break
                            else:
                                sleep(2)
                        if not headphone_location:
                            warn_user('答案未生成完毕')
                            break
                    else:
                        warn_user('用户设定不再继续')
                        break
    logger.warning(f'chatGPT翻译完成, {len(split_lines)=}')


@logger.catch
def count_tags(soup, tag_name):
    return len(soup.find_all(tag_name))


@logger.catch
def get_code_text(user_html):
    user_soup = BeautifulSoup(user_html, 'html.parser')
    # 查找 code 标签
    code_tag = user_soup.find('code')
    if code_tag is None:
        code_text = user_html
    else:
        code_text = code_tag.get_text().strip()
    # 对文本内容进行反向转义
    unescaped_text = unescape(code_text)
    return code_text


def check_tag_balance(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = {tag.name for tag in soup.find_all()}
    tag_balance = {}
    for tag in tags:
        if tag in void_tags:
            # 对于自闭合标签，我们假设它们总是平衡的
            tag_balance[tag] = True
        else:
            # 对于非自闭合标签，计算开始标签和结束标签的数量
            open_tags = len(soup.find_all(tag))
            close_tags = html_content.count(f"</{tag}>")
            tag_balance[tag] = (open_tags == close_tags)
    return tag_balance


@logger.catch
def line2dic(input_line, output_line, main_gpt_dic, sub_gpt_dic):
    input_line = input_line.replace('\xa0', ' ').replace('\u2002', ' ')
    output_line = output_line.replace('\xa0', ' ').replace('\u2002', ' ')
    input_soup = BeautifulSoup(input_line, 'html.parser')
    output_soup = BeautifulSoup(output_line, 'html.parser')
    input_text = input_soup.get_text()
    output_text = output_soup.get_text()

    input_1st_tag = input_soup.find()
    output_1st_tag = output_soup.find()
    if output_1st_tag is None:
        logger.error(f'{output_text=}')
    else:
        # 仅当内部a标签数量一致且span标签数量一致时加入翻译词典
        input_a_cnt = count_tags(input_soup, 'a')
        input_span_cnt = count_tags(input_soup, 'span')
        output_a_cnt = count_tags(output_soup, 'a')
        output_span_cnt = count_tags(output_soup, 'span')

        input_opening = input_line.split('>')[0] + '>'
        input_closing = f"</{input_1st_tag.name}>"
        input_content = input_line.removeprefix(input_opening).removesuffix(input_closing)
        output_opening = output_line.split('>')[0] + '>'
        output_closing = f"</{output_1st_tag.name}>"
        output_content = output_line.removeprefix(output_opening).removesuffix(output_closing)

        input_balanced = check_tag_balance(input_line)
        output_balanced = check_tag_balance(output_line)

        # 定义一个正则表达式，精确匹配含撇号、连字符和社交媒体用户名的英文短语
        matches = findall(p_en, output_text)
        # 过滤结果，确保每个匹配包含至少两个字母
        en_phrases = [m for m in matches if search('[A-Za-z]{2,}', m)]
        en_phrases = [x for x in en_phrases if x not in roman_numerals]
        en_phrases = [x for x in en_phrases if x not in untranslatables]
        en_phrases = [x for x in en_phrases if not x.startswith('@')]
        en_phrases = [x for x in en_phrases if not x.endswith('@')]
        en_phrases = [x for x in en_phrases if not check_url(x)]
        en_lowers = [x.lower() for x in en_phrases]
        en_somes = [x for x in en_lowers if x.startswith(('some', 'linger'))]
        en_names = [x for x in en_phrases if x in good_names]
        en_numbers = [x for x in en_lowers if x in lower_numbers]
        # if input_a_cnt == output_a_cnt and input_span_cnt == output_span_cnt:
        is_valid = False
        if output_content == input_content:
            # 未翻译
            # logger.warning(f'{input_content=}')
            pass
        elif all(output_balanced.values()):
            # 所有标签均有开闭
            if en_names:
                # 包含英文名
                logger.debug(f'{en_names=}')
                sub_gpt_dic[input_content] = output_content
                if allow_en_names:
                    is_valid = True
            elif en_numbers:
                logger.debug(f'{en_numbers=}')
                sub_gpt_dic[input_content] = output_content
                # is_valid = True
            elif en_somes:
                # 例如somehow等等
                logger.debug(f'{en_phrases=}')
                sub_gpt_dic[input_content] = output_content
                # is_valid = True
            elif en_phrases:
                logger.debug(f'{en_phrases=}')
                is_valid = True
            else:
                is_valid = True
        if is_valid:
            main_gpt_dic[input_content] = output_content
        else:
            # logger.debug(f'{input_line=}')
            logger.warning(f'{output_line=}')
    return main_gpt_dic, sub_gpt_dic


# @timer_decorator
@logger.catch
def get_gpt_dic(target_tups):
    main_gpt_dic = {}
    sub_gpt_dic = {}
    gpt_dic_user = str2dic(gpt_user_str, strip_tag=True)
    main_gpt_dic.update(gpt_dic_user)
    error_num = 0
    display_mode = 'side_by_side'
    display_mode = 'up_down'
    logger.warning(f'{len(target_tups)=}')
    for t in range(len(target_tups) - 1):
        target_tup = target_tups[t]
        next_target_tup = target_tups[t + 1]
        text_role, model_name, target_div = target_tup
        next_text_role, next_model_name, next_target_div = next_target_tup
        if text_role == '用户' and next_text_role == 'chatGPT' and target_div.startswith('<code'):
            user_html = target_div
            gpt_html = next_target_div
            user_code_text = get_code_text(user_html)
            gpt_code_text = get_code_text(gpt_html)
            if user_code_text.startswith('html'):
                user_code_text = user_code_text.removeprefix('html').strip()
            input_lines = user_code_text.strip().splitlines()
            output_lines = gpt_code_text.strip().splitlines()
            if len(input_lines) == len(output_lines) >= 1:
                ilines = input_lines
                olines = output_lines
            else:
                ilines = []
                olines = []
                # logger.warning(f'{len(input_lines)=}, {len(output_lines)=}')
                # logger.warning(f'{input_text}')
                # logger.error(f'{code_text}')
                error_num += 1
                # main_gpt_dic[input_text] = code_text
            if next_model_name in ignore_models:
                # 跳过GPT3.5的翻译
                # logger.error(f'{next_model_name=}')
                pass
            else:
                # logger.debug(f'{next_model_name=}')
                for c in range(len(ilines)):
                    input_line = ilines[c]
                    output_line = olines[c]
                    main_gpt_dic, sub_gpt_dic = line2dic(input_line, output_line, main_gpt_dic, sub_gpt_dic)

    for i in range(120):
        input_content = f'Chapter {i + 1}'
        output_content = f'第{i + 1}章'
        main_gpt_dic[input_content] = output_content
        main_gpt_dic[input_content.upper()] = output_content
        main_gpt_dic[input_content.lower()] = output_content
        input_content = f'Part {i + 1}'
        output_content = f'第{i + 1}部分'
        main_gpt_dic[input_content] = output_content
        main_gpt_dic[input_content.upper()] = output_content
        main_gpt_dic[input_content.lower()] = output_content
    for eng, chn in chapter_map.items():
        main_gpt_dic[eng] = chn
        main_gpt_dic[eng.upper()] = chn
        main_gpt_dic[eng.lower()] = chn
        input_content = f"Chapter {eng}"
        output_content = f"第{chn}章"
        main_gpt_dic[input_content] = output_content
        main_gpt_dic[input_content.upper()] = output_content
        main_gpt_dic[input_content.lower()] = output_content
        input_content = f"Part {eng}"
        output_content = f"第{chn}部分"
        main_gpt_dic[input_content] = output_content
        main_gpt_dic[input_content.upper()] = output_content
        main_gpt_dic[input_content.lower()] = output_content

    # logger.info(f'{error_num=}')

    # 将 main_gpt_dic 按键的长度排序
    sorted_gpt_dic = dict(sorted(main_gpt_dic.items(), key=lambda item: len(item[0])))
    # sorted_gpt_dic = dict(sorted(main_gpt_dic.items(), key=lambda item: -len(item[0])))

    # 如果是第一次调用函数，打印 PrettyTable
    if not hasattr(get_gpt_dic, "has_run") and show_dic:
        get_gpt_dic.has_run = True
        # 使用 PrettyTable 打印所有的键值对
        table = PrettyTable()
        table.align = "l"  # 设置所有列的对齐方式为左对齐
        if display_mode == 'side_by_side':
            table.field_names = ["Input", "Output"]
            for key, value in sorted_gpt_dic.items():
                table.add_row([key, value])
        else:
            table.field_names = ['Name', 'Content']
            for key, value in sorted_gpt_dic.items():
                table.add_row(['英文', key])
                table.add_row(['中文', value])
        print(table)
    return main_gpt_dic, sub_gpt_dic


@logger.catch
def is_valid_url(url):
    parsed_url = urlparse(url)
    # Check if the URL has either a scheme or a netloc part
    return bool(parsed_url.scheme or parsed_url.netloc)


@logger.catch
def is_extra_a_tag(para):
    # 提取p标签中所有直接的子节点
    children = list(para.children)
    # 剔除所有空白字符节点
    non_empty_children = [child for child in children if not (isinstance(child, str) and child.strip() == '')]

    # 查找所有a标签
    a_tags = [child for child in non_empty_children if child.name == 'a']
    # 检查是否只有一个a标签
    if len(a_tags) == 1:
        a_tag = a_tags[0]
        # 获取a标签的文本并去除空白
        a_text = a_tag.get_text(strip=True)
        # 获取a标签的href属性
        a_href = a_tag.get('href', '')
        a_href_simple = a_href.removeprefix('https://').removeprefix('http://')
        # 如果文本自身是有效URL或者href是有效URL且文本是URL去掉协议后的部分
        if is_valid_url(a_href) and (is_valid_url(a_text) or a_text == a_href_simple):
            # 检查除a标签外的所有文本是否不包含英文字母
            other_text = ''.join(str(child) for child in children if child != a_tag)
            # print(f'{other_text=}')
            if not search(r'[a-zA-Z]', other_text):
                return True
    return False


@logger.catch
def is_page_notation(text):
    # 复杂页码正则表达式，处理复杂的文档和页码引用
    patterns = [
        r'((Stowe|LU|YBL|LL|Eg|fo|H|Add)\.?\s+[\w\s.,&-]*\d+[ab]?\,?\s*\d*[-\d]*\s*(and\s+)?)+\.?',
        r'(Stowe|LU|YBL|LL|Eg|fo|H|Add)\.?\s+[\w\s.,&-]*\d+[ab]?\,?\s*\d*[-\d]*\s*(;|,)\s*((Stowe|LU|YBL|LL|Eg|fo|H|Add)\.?\s+)?[\w\s.,&-]*\d+[ab]?\,?\s*\d*[-\d]*\.?',
        r'((Stowe|Add|H|YBL)\.?\s*,?\s*and\s+)?(Stowe|Add|H|YBL)\.?\s+[\d.]+,\s*(Stowe|Add|H|YBL)\.?\s+[\d.]+'
    ]
    for pattern in patterns:
        if fullmatch(pattern, text):
            return True
    return False


@logger.catch
def check_url(roi_text):
    if validators.url(roi_text):
        # 检查文本是否为网址
        return True
    elif fullmatch(r'(?:http://|https://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9.-]+)*', roi_text):
        # 检查文本是否为网址
        return True
    return False


@logger.catch
def check2ignore(para):
    inner_html = str(para).removeprefix(f'<{para.name}>').removesuffix(f'</{para.name}>').strip()
    roi_text = para.get_text(strip=True)

    if roi_text.strip() == '':
        # 检查文本是否为空
        return True
    elif is_extra_a_tag(para):
        # 检查是否是一个特殊的a标签
        return True
    elif fullmatch(r'[\d\W_-]+', roi_text):
        # 检查是否只包含数字、符号
        return True
    elif fullmatch(r'\[?[a-zA-Z]\]?', roi_text):
        # 检查是否只包含单个字母，包括被括号包围的情况
        return True
    elif fullmatch(r'Page \d+', inner_html):
        # 检查Page页码
        # print(f'{inner_html=}')
        return True
    elif check_page_notation and is_page_notation(inner_html):
        # 检查表示页码的特殊格式
        return True
    elif check_url(roi_text):
        # 检查文本是否为网址
        return True
    elif roi_text.startswith('»') and check_url(roi_text.removeprefix('»').strip()):
        # 检查文本是否为网址
        return True
    elif fullmatch(r'[a-zA-Z0-9\W_]+', roi_text) and not search(r'\b[a-zA-Z]{2,}\b', roi_text):
        # 检查文本由英文、数字、符号组成，且不包含有意义的英文单词
        return True
    elif roi_text in roman_numerals:
        # 检查文本是否只包含罗马数字 1～10
        return True
    elif roi_text.startswith('ISBN') and fullmatch(p_ISBN, roi_text.removeprefix('ISBN').strip()):
        # 检查文本是否为ISBN
        return True
    elif fullmatch(r'[A-Z0-9]+(?:-[A-Z0-9]+)+', roi_text):
        # 检查文本是否为非标准书号
        return True
    elif roi_text in ignore_texts:
        return True
    elif 'index-nav-bar-letter' in str(para):
        return True
    return False


@logger.catch
def get_roi_tags(soup):
    # 标题标签
    titles = soup.find_all('title')
    # 标题h1到h6标签
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    # 段落标签
    paragraphs = soup.find_all('p')

    soup4lis = deepcopy(soup)
    titles4lis = soup4lis.find_all('title')
    headers4lis = soup4lis.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs4lis = soup4lis.find_all('p')
    for tag in titles4lis:
        tag.decompose()
    for header in headers4lis:
        header.decompose()
    for paragraph in paragraphs4lis:
        paragraph.decompose()

    # 列表标签
    lis = soup4lis.find_all('li')
    # 查找所有li标签，但排除那些包含子li标签的li标签
    sel_lis = [li for li in lis if not li.find('li')]

    soup4divs = deepcopy(soup4lis)
    lis4divs = soup4divs.find_all('li')
    for li in lis4divs:
        if not li.find('li'):
            li.decompose()
    divs = soup4divs.find_all('div')
    # 查找所有div标签，但排除那些包含子div标签的div标签
    sel_divs = [div for div in divs if not div.find('div')]

    # 总集
    roi_tags = titles + headers + paragraphs + sel_lis + sel_divs
    return roi_tags


# @timer_decorator
@logger.catch
def get_dst_line(gpt_dic, src_line, bilingual=False):
    src_soup = BeautifulSoup(src_line, 'html.parser')
    src_1st_tag = src_soup.find()
    src_opening = src_line.split('>')[0] + '>'
    src_closing = f"</{src_1st_tag.name}>"
    src_content = src_line.removeprefix(src_opening).removesuffix(src_closing)
    src_content = src_content.replace('\xa0', ' ').replace('\u2002', ' ')
    dst_content = gpt_dic[src_content]
    if bilingual:
        if src_opening.startswith('<p'):
            # 添加换行
            dst_line = f'{src_opening}{src_content}<br>{dst_content}{src_closing}'
        else:
            dst_line = f'{src_opening}{src_content}{dst_content}{src_closing}'
    else:
        dst_line = f'{src_opening}{dst_content}{src_closing}'
    return dst_line


@logger.catch
def str2dic(dic_str, strip_tag=False):
    spec_dic = {}
    manual_lines = dic_str.strip().splitlines()
    for m in range(len(manual_lines) - 1):
        manual_line = manual_lines[m]
        next_manual_line = manual_lines[m + 1]
        if m % 2 == 0:
            if strip_tag:
                input_line = manual_line
                output_line = next_manual_line

                input_soup = BeautifulSoup(input_line, 'html.parser')
                output_soup = BeautifulSoup(output_line, 'html.parser')

                input_1st_tag = input_soup.find()
                output_1st_tag = output_soup.find()

                input_opening = input_line.split('>')[0] + '>'
                input_closing = f"</{input_1st_tag.name}>"
                input_content = input_line.removeprefix(input_opening).removesuffix(input_closing)
                output_opening = output_line.split('>')[0] + '>'
                output_closing = f"</{output_1st_tag.name}>"
                output_content = output_line.removeprefix(output_opening).removesuffix(output_closing)

                spec_dic[input_content] = output_content
            else:
                spec_dic[manual_line] = next_manual_line
    return spec_dic


@logger.catch
@timer_decorator
def google_translate(simple_lines, target_lang, strip_empty=True):
    """
    将 .docx 文档翻译成指定的目标语言，并将翻译后的文本保存到一个 .txt 文件中。

    :param simple_lines: 要翻译的文本列表
    :param target_lang: 目标语言的代码，例如 'zh-CN' 或 'en'
    """
    chunks = []
    current_chunk = ""

    # 将文本分成多个块，以便在翻译时遵守最大字符数限制
    for line in simple_lines:
        # 检查将当前行添加到当前块后的长度是否超过最大字符数
        if len(current_chunk) + len(line) + 1 > google_max_chars:  # 加1是为了考虑换行符
            chunks.append(current_chunk.strip())
            current_chunk = ""
        current_chunk += line + "\n"

    # 添加最后一个块（如果有内容的话）
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # ================分段翻译================
    translated_chunks = []
    # 对每个块使用谷歌翻译 API 进行翻译
    for chunk in chunks:
        translated_chunk = GoogleTranslator(source='auto', target=target_lang).translate(chunk)
        translated_chunks.append(translated_chunk)
    # 将翻译后的块连接成一个字符串
    translated_text = lf.join(translated_chunks)
    if strip_empty:
        translated_lines = translated_text.splitlines()
        translated_lines = [x for x in translated_lines if x.strip() != '']
        translated_text = lf.join(translated_lines)
    return translated_text


@logger.catch
def get_split_lines(html_text):
    # 将输入的HTML文本按行分割存入html_lines列表
    html_lines = html_text.splitlines()

    # ================对网页内容进行分段================
    # 初始化split_lines列表，用于存储最终的分段结果，每个元素是一个包含多行文本的列表
    split_lines = []
    # 初始化current_lines列表，用于暂存当前处理的段落
    input_lines = []
    # 初始化当前段落的行数计数器
    cur_line_cnt = 0
    # 初始化当前段落的字符数计数器
    cur_char_cnt = 0

    # 遍历每一行HTML文本
    for i in range(len(html_lines)):
        html_line = html_lines[i]
        # 获取当前行的长度
        line_len = len(html_line)

        # 判断是否可以将当前行添加到current_lines中
        if cur_line_cnt + 1 <= gpt_line_max and cur_char_cnt + line_len + 80 * cur_line_cnt <= gpt_char_max:
            # 添加当前行到段落中
            input_lines.append(html_line)
            # 行数计数器加一
            cur_line_cnt += 1
            # 字符数计数器增加当前行的字符数
            cur_char_cnt += line_len
        else:
            # 如果当前行不能添加到current_lines中，则将current_lines作为一个完成的段落添加到split_lines中
            split_lines.append(input_lines)
            # 重置current_lines，开始新段落
            input_lines = [html_line]
            # 重置行数计数器
            cur_line_cnt = 1
            # 重置字符数计数器
            cur_char_cnt = line_len
        # print()

    # 循环结束后，如果current_lines中有数据，也添加到split_lines中
    if input_lines:
        split_lines.append(input_lines)

    # 返回分段后的所有段落列表
    return split_lines


@logger.catch
def get_roi_html(para, span_classes):
    preserved_tags = {}
    if del_all_attrs:
        # 删除para的所有属性，除了内容
        for attr in list(para.attrs):
            del para[attr]
    else:
        # 删除`class`和`id`属性
        if para.has_attr('class'):
            del para['class']
        if para.has_attr('id'):
            del para['id']

    # ================处理span标签================
    # 删除内容为空的span标签
    for span in para.find_all('span'):
        if not span.get_text(strip=True):
            span.decompose()

    span_classes_ignore = ['koboSpan']
    # 处理所有具有指定class的span标签，将它们转化为纯文本
    for span_class in span_classes_ignore:
        target_spans = para.find_all('span', class_=span_class)
        for span in target_spans:
            span.replace_with(span.get_text())

    # 获取para内的所有文本
    para_text = para.get_text(strip=True)

    if flat_span:
        # 检查para内的span标签数量和内容
        visible_spans = para.find_all('span')
        if len(visible_spans) == 1:
            span = visible_spans[0]
            span_text = span.get_text(strip=True)
            # 确认span标签包含para标签的全部文本
            if span_text.strip() == para_text.strip():
                preserved_tags['span'] = deepcopy(span)
                # 提取span的文本到p中
                para.string = span_text
                # 删除span标签
                span.decompose()

    if flat_samp:
        # 检查para内的samp标签数量和内容
        visible_samps = para.find_all('samp')
        if len(visible_samps) == 1:
            samp = visible_samps[0]
            samp_text = samp.get_text(strip=True)
            # 确认samp标签包含para标签的全部文本
            if samp_text.strip() == para_text.strip():
                preserved_tags['samp'] = deepcopy(samp)
                # 提取samp的文本到p中
                para.string = samp_text
                # 删除samp标签
                samp.decompose()

    if flat_a:
        # 检查para内的a标签数量和内容
        visible_as = para.find_all('a')
        if len(visible_as) == 1:
            a = visible_as[0]
            a_text = a.get_text(strip=True)
            # 确认a标签包含para标签的全部文本
            if a_text.strip() == para_text.strip():
                preserved_tags['a'] = deepcopy(a)
                # 提取a的文本到p中
                para.string = a_text
                # 删除a标签
                a.decompose()

    # 处理剩余的span标签，映射类名
    for span in para.find_all('span'):
        span_class = ' '.join(span.get('class', []))
        if span_class in span_map:
            # 应用自定义映射
            span['class'] = span_map[span_class]
        else:
            # 记录未映射的类名
            span_classes.append(span_class)

    # ================处理a标签================
    # 处理a标签的属性，如果包含id则只保留id
    if simple_a_id:
        links = para.find_all('a')
        for link in links:
            if link.has_attr('id'):
                attr_value = link['id']
                link.attrs = {'id': attr_value}

    # 清理两端的空a标签
    if rip_edge_a:
        links = para.find_all('a')
        inner_html = str(para).removeprefix(f'<{para.name}>').removesuffix(f'</{para.name}>').strip()
        if links:
            link = links[0]
            if link.get_text(strip=True) == '' and inner_html.startswith(str(link)):
                preserved_tags['left_a'] = str(link)
                links[0].decompose()
            if len(links) >= 2:
                link = links[-1]
                if link.get_text(strip=True) == '' and inner_html.endswith(str(link)):
                    preserved_tags['right_a'] = str(link)
                    links[-1].decompose()

        # 清理最左端的无需翻译的a标签
        links = para.find_all('a')
        inner_html = str(para).removeprefix(f'<{para.name}>').removesuffix(f'</{para.name}>').strip()
        if links:
            link = links[0]
            link_text = link.get_text(strip=True)
            # 文本内容由数字和符号构成
            if match(r'^[\d\W]+$', link_text) and inner_html.startswith(str(link)):
                preserved_tags['left_inner_a'] = str(link)
                links[0].decompose()

    # 简化pginternal等
    links = para.find_all('a')
    for l in range(len(links)):
        link = links[l]
        if link.has_attr('class'):
            class_attr = link['class']
            # logger.warning(f'{class_attr=}')
            if class_attr == ['pginternal']:
                if link.has_attr('tag'):
                    del link['tag']
        if link.has_attr('href'):
            new_href = link['href']
            # 应用所有替换规则
            for old, new in replacements.items():
                new_href = new_href.replace(old, new)
            link['href'] = new_href

    samps = para.find_all('samp')
    for s in range(len(samps)):
        samp = samps[s]
        if samp.has_attr('class'):
            class_attr = samp['class']
            if len(class_attr) == 1 and class_attr[0].startswith('SANS_TheSansMonoCd_'):
                new_class = class_attr[0].removeprefix('SANS_TheSansMonoCd_')
                samp['class'] = [new_class]

    roi_html = str(para).replace('\n', '')
    if use_censor:
        # 自定义词汇表替换
        for word in censor_words:
            if keep_1st_letter:
                roi_html = sub(r'\b' + escape(word) + r'\b',
                               lambda m: m.group()[0] + '*' * (len(m.group()) - 1), roi_html,
                               flags=IGNORECASE)
            else:
                roi_html = sub(r'\b' + escape(word) + r'\b', '*' * len(word), roi_html, flags=IGNORECASE)
    return roi_html, span_classes, preserved_tags


@logger.catch
def restore_tag(dst_para, preserved_tags, roi):
    # 获取标签头（包括属性）
    dst_opening = str(dst_para).split('>')[0] + '>'
    # 获取标签尾
    dst_closing = f"</{dst_para.name}>"
    # 获取标签内容
    dst_content = str(dst_para).removeprefix(dst_opening).removesuffix(dst_closing)
    if roi in preserved_tags:
        roi_tag = preserved_tags[roi]
        # 获取标签头（包括属性）
        roi_opening = str(roi_tag).split('>')[0] + '>'
        # 获取标签尾
        roi_closing = f"</{roi_tag.name}>"
        dst_html = f'{dst_opening}{roi_opening}{dst_content}{roi_closing}{dst_closing}'
        dst_soup = BeautifulSoup(dst_html, 'lxml')
        dst_para = dst_soup.find(dst_para.name)
    return dst_para


@logger.catch
def restore_para(dst_para, preserved_tags):
    if 'left_inner_a' in preserved_tags:
        dst_para.insert(0, BeautifulSoup(preserved_tags['left_inner_a'], 'lxml').a)
    if 'left_a' in preserved_tags:
        dst_para.insert(0, BeautifulSoup(preserved_tags['left_a'], 'lxml').a)
    if 'right_a' in preserved_tags:
        dst_para.append(BeautifulSoup(preserved_tags['right_a'], 'lxml').a)
    rois = ['span', 'samp', 'a']
    for roi in rois:
        dst_para = restore_tag(dst_para, preserved_tags, roi)
    return dst_para


@timer_decorator
@logger.catch
def process_epub(all_html_files):
    all_htmls = []
    roi_htmls = []
    roi_texts = []
    console_htmls = []
    span_classes = []
    all_md = ''
    all_words = []
    handler_normal = HTML2Text()

    # ================生成中文翻译目录================
    if epub_dir.exists() and not cn_epub_dir.exists():
        logger.debug(f'复制: {epub_dir} → {cn_epub_dir}')
        copytree(epub_dir, cn_epub_dir)
        all_cn_html_files = get_files(cn_epub_dir, 'html')
        # ================删除网页文件================
        for a in range(len(all_cn_html_files)):
            cn_html = all_cn_html_files[a]
            if cn_html.exists():
                os.remove(cn_html)

    for a in range(len(all_html_files)):
        src_html_file = all_html_files[a]
        html_content = read_txt(src_html_file)
        logger.warning(f'[{a + 1}/{len(all_html_files)}]{src_html_file=}')

        target_md = handler_normal.handle(html_content).strip()
        all_md += f"{lf}{target_md}{lf}"

        soup = BeautifulSoup(html_content, 'lxml')

        text = soup.get_text(separator=' ')
        words = findall(r'\b\w+\b', text.lower())
        all_words.extend(words)

        roi_htmls_chapter = []
        roi_texts_chapter = []
        roi_tags = get_roi_tags(soup)
        for p in range(len(roi_tags)):
            para = roi_tags[p]
            roi_raw_html = str(para)
            roi_text = para.get_text(strip=True)
            if p_format == 'raw':
                roi_html = roi_raw_html
            elif p_format == 'text':
                roi_html = roi_text
            else:  # if p_format == 'raw_simple'
                roi_html, span_classes, preserved_tags = get_roi_html(para, span_classes)
            all_htmls.append(roi_raw_html)

            if check2ignore(para):
                pass
            else:
                roi_htmls_chapter.append(roi_html)
                roi_texts_chapter.append(roi_text)

                console_html = sub(r'(<\/?[\w\s="]+>)', r'\033[1;31m\1\033[0m', roi_html)
                console_html = highlight(roi_html, HtmlLexer(), TerminalFormatter())
                console_htmls.append(console_html)
        roi_htmls.extend(roi_htmls_chapter)
        roi_texts.extend(roi_texts_chapter)

    # 打印提取的文本
    for c in range(len(console_htmls)):
        console_html = console_htmls[c]
        print(f"---[{c + 1}]{lf}{lf}{console_html.strip()}{lf}")
    logger.debug(f'{len(roi_htmls)=}')

    span_classes = reduce_list(span_classes)
    span_classes.sort()
    for s in range(len(span_classes)):
        span_class = span_classes[s]
        # logger.warning(f'{span_class}')

    word_count = Counter(all_words)
    total_word_count = sum(word_count.values())

    average_reading_speed = 250
    est_time = total_word_count / average_reading_speed

    # 输出统计结果
    print(f"总词数: {total_word_count}")
    print(f"不重复词数: {len(word_count)}")
    print(f"预计阅读时间: {est_time:.2f}分钟")
    write_txt(md_file, all_md)


def get_para_segments(para):
    # 用于存储原始和替换后的片段
    para_segments = []
    # 当前处理的文本片段
    current_text = ''
    for element in para.contents:
        if isinstance(element, str):
            # 直接添加字符串到当前文本
            current_text += element
        else:
            # 处理前一个累积的文本
            if current_text:
                # 这里可以进行翻译或其他处理
                para_segments.append(current_text)
                # 重置文本累积
                current_text = ''
            # 添加HTML元素
            element_html = str(element)
            para_segments.append(element_html)
    # 确保最后一段文本被处理
    if current_text:
        para_segments.append(current_text)
    if show_list:
        pprint(para_segments)
    return para_segments


@logger.catch
def get_seg_htmls_chapter(para_segments):
    seg_roi_htmls = [f'<p>{x}</p>' for x in para_segments]
    seg_htmls_chapter = []
    for s in range(len(seg_roi_htmls)):
        # ================网页转soup================
        seg_roi_html = seg_roi_htmls[s]
        seg_soup = BeautifulSoup(seg_roi_html, 'lxml')
        seg_p_tags = seg_soup.find_all('p')
        if seg_p_tags:
            seg_roi_tag = seg_p_tags[0]
            if check2ignore(seg_roi_tag):
                pass
            else:
                seg_htmls_chapter.append(seg_roi_html)
    return seg_htmls_chapter


@timer_decorator
@logger.catch
def translate_epub(all_html_files, do_convert=False):
    all_opfs = get_files(epub_dir, '.opf')
    all_ncxs = get_files(epub_dir, '.ncx')
    # content_opf = all_opfs[0]

    activate_browser = True
    all_htmls = []
    roi_htmls = []
    roi_texts = []
    span_classes = []

    # ================目录================
    if all_ncxs:
        toc_ncx = all_ncxs[0]
        dst_dir = Path(toc_ncx.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        cn_toc_ncx = dst_dir / toc_ncx.name
        src_txt = dst_dir / f'{toc_ncx.stem}-en.txt'
        dst_txt = dst_dir / f'{toc_ncx.stem}.txt'

        tree = ET.parse(toc_ncx)
        root = tree.getroot()

        # 定义命名空间，如果你的NCX文件有命名空间
        namespaces = {
            'ncx': 'http://www.daisy.org/z3986/2005/ncx/'
        }

        # 查找所有的文本元素，例如<navLabel>下的<text>
        roi_htmls_chapter = []
        roi_texts_chapter = []
        for text_element in root.findall('.//ncx:navLabel/ncx:text', namespaces):
            original_text = text_element.text
            original_text = original_text.replace('\xa0', ' ').replace('\u2002', ' ')
            roi_html = f'<p>{original_text}</p>'
            text_soup = BeautifulSoup(roi_html, 'lxml')
            text_roi_tags = text_soup.find_all('p')
            if text_roi_tags:
                text_roi_tag = text_roi_tags[0]
                if check2ignore(text_roi_tag):
                    pass
                else:
                    roi_htmls_chapter.append(roi_html)
                    roi_texts_chapter.append(original_text)
        roi_htmls.extend(roi_htmls_chapter)
        roi_texts.extend(roi_texts_chapter)

        src_text = lf.join(roi_texts_chapter)
        # print(src_text)
        # logger.debug(f'{src_txt=}')
        write_txt(src_txt, src_text)

        # ================谷歌翻译================
        if do_google_translate and not dst_txt.exists():
            translated_text = google_translate(roi_texts_chapter, target_lang)
            write_txt(dst_txt, translated_text)

    # ================所有网页================
    for a in range(len(all_html_files)):
        src_html_file = all_html_files[a]
        dst_dir = Path(src_html_file.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        src_txt = dst_dir / f'{src_html_file.stem}-en.txt'
        dst_txt = dst_dir / f'{src_html_file.stem}.txt'

        html_content = read_txt(src_html_file)
        # logger.warning(f'{src_html_file=}')

        soup = BeautifulSoup(html_content, 'lxml')

        roi_htmls_chapter = []
        roi_texts_chapter = []
        roi_tags = get_roi_tags(soup)
        for p in range(len(roi_tags)):
            para = roi_tags[p]
            roi_raw_html = str(para)
            roi_text = para.get_text(strip=True)
            if p_format == 'raw':
                roi_html = roi_raw_html
            elif p_format == 'text':
                roi_html = roi_text
            else:  # if p_format == 'raw_simple':
                roi_html, span_classes, preserved_tags = get_roi_html(para, span_classes)
            all_htmls.append(roi_raw_html)

            if check2ignore(para):
                pass
            elif len(str(para)) >= 2000:
                # ================段落过长必须切割================
                para_segments = get_para_segments(para)
                seg_roi_htmls = [f'<p>{x}</p>' for x in para_segments]
                seg_htmls_chapter = []
                for s in range(len(seg_roi_htmls)):
                    # ================网页转soup================
                    seg_roi_html = seg_roi_htmls[s]
                    seg_soup = BeautifulSoup(seg_roi_html, 'lxml')
                    seg_p_tags = seg_soup.find_all('p')
                    for s in range(len(seg_p_tags)):
                        # ================soup转tag================
                        seg_roi_tag = seg_p_tags[s]
                        if check2ignore(seg_roi_tag):
                            pass
                        else:
                            seg_htmls_chapter.append(seg_roi_html)
                roi_htmls_chapter.extend(seg_htmls_chapter)
                roi_texts_chapter.append(roi_text)
            else:
                # ================根据链接所占比例决定是否切割================
                para_segments = get_para_segments(para)
                segments_as = [x for x in para_segments if x.startswith('<a')]
                if segments_as and len(str(para)) <= len(segments_as) * 100:
                    #  说明链接含量比较多
                    seg_htmls_chapter = get_seg_htmls_chapter(para_segments)
                    roi_htmls_chapter.extend(seg_htmls_chapter)
                else:
                    roi_htmls_chapter.append(roi_html)
                roi_texts_chapter.append(roi_text)

        roi_htmls.extend(roi_htmls_chapter)
        roi_texts.extend(roi_texts_chapter)

        src_text = lf.join(roi_texts_chapter)
        # print(src_text)
        # logger.debug(f'{src_txt=}')
        write_txt(src_txt, src_text)

        # ================谷歌翻译================
        if do_google_translate and not dst_txt.exists():
            logger.debug(f'[{a + 1}/{len(all_html_files)}]{src_html_file=}]')
            translated_text = google_translate(roi_texts_chapter, target_lang)
            write_txt(dst_txt, translated_text)

    # ================GPT4翻译================
    if do_gpt_translate:
        gpt_translate(roi_htmls, prompt_prefix)

    if do_convert:
        if all_ncxs:
            tree = ET.parse(toc_ncx)
            root = tree.getroot()

            # 定义命名空间，如果你的NCX文件有命名空间
            namespaces = {
                'ncx': 'http://www.daisy.org/z3986/2005/ncx/'
            }

            # 查找所有的文本元素，例如<navLabel>下的<text>
            for text_element in root.findall('.//ncx:navLabel/ncx:text', namespaces):
                original_text = text_element.text
                original_text = original_text.replace('\xa0', ' ').replace('\u2002', ' ')
                if original_text in main_gpt_dic:
                    dst_content = main_gpt_dic[original_text]
                elif original_text in sub_gpt_dic:
                    dst_content = sub_gpt_dic[original_text]
                else:
                    logger.error(f'{original_text=}')
                    dst_content = original_text
                text_element.text = dst_content

            # 保存修改后的NCX文件
            tree.write(cn_toc_ncx, encoding='utf-8', xml_declaration=True, pretty_print=True)

        # ================转换成翻译好的网页================
        if do_gpt_translate:
            for a in range(len(all_html_files)):
                src_html_file = all_html_files[a]
                dst_dir = Path(src_html_file.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
                dst_html_file = dst_dir / f'{src_html_file.stem}.html'
                html_content = read_txt(src_html_file)
                # logger.warning(f'{src_html_file=}')
                soup = BeautifulSoup(html_content, 'lxml')

                # ================生成翻译好的网页================
                roi_htmls_chapter = []
                roi_tags = get_roi_tags(soup)
                dst_lines = []
                trans_len = 0
                for p in range(len(roi_tags)):
                    para = roi_tags[p]
                    roi_raw_html = str(para)
                    roi_text = para.get_text(strip=True)
                    if p_format == 'raw':
                        roi_html = roi_raw_html
                    elif p_format == 'text':
                        roi_html = roi_text
                    else:  # if p_format == 'raw_simple':
                        roi_html, span_classes, preserved_tags = get_roi_html(para, span_classes)
                    all_htmls.append(roi_raw_html)

                    if check2ignore(para):
                        pass
                    else:
                        roi_htmls_chapter.append(roi_html)
                        do_split = False
                        para_segments = get_para_segments(para)
                        if len(str(para)) >= 2000:
                            # ================段落过长必须切割================
                            if len(para_segments) >= 2:
                                do_split = True
                        else:
                            # ================根据链接所占比例决定是否切割================
                            segments_as = [x for x in para_segments if x.startswith('<a')]
                            if segments_as and len(str(para)) <= len(segments_as) * 100:
                                do_split = True
                        src_soup = BeautifulSoup(roi_html, 'html.parser')
                        src_1st_tag = src_soup.find()
                        src_opening = roi_html.split('>')[0] + '>'
                        src_closing = f"</{src_1st_tag.name}>"
                        src_content = roi_html.removeprefix(src_opening).removesuffix(src_closing)
                        src_content = src_content.replace('\xa0', ' ').replace('\u2002', ' ')
                        if do_split:
                            trans_segments = []
                            for s in range(len(para_segments)):
                                segment = para_segments[s]
                                trans_segment = main_gpt_dic.get(segment, segment)
                                trans_segments.append(trans_segment)
                            dst_content = ''.join(trans_segments)
                            dst_line = f'{src_opening}{dst_content}{src_closing}'
                            trans_len += 1
                        else:
                            src_line = roi_html
                            if src_content in main_gpt_dic:
                                dst_line = get_dst_line(main_gpt_dic, src_line)
                                trans_len += 1
                            elif src_content in sub_gpt_dic:
                                dst_line = get_dst_line(sub_gpt_dic, src_line)
                                trans_len += 1
                            else:
                                logger.error(f'{src_line=}')
                                dst_line = src_line
                        dst_lines.append(dst_line)
                # ================确定翻译完再生成================
                if trans_len >= 0.996 * len(roi_htmls_chapter):
                    dst_html_text = lf.join(dst_lines)
                    print(dst_html_text)
                    write_txt(dst_html_file, dst_html_text)


@logger.catch
def get_dst_html_text(src_html_file, bilingual=False):
    # logger.warning(f'{src_html_file=}')
    html_content = read_txt(src_html_file)
    span_classes = []
    soup = BeautifulSoup(html_content, 'lxml')
    replace_tups = []
    roi_htmls_chapter = []
    roi_texts_chapter = []
    roi_tags = get_roi_tags(soup)
    # ================电子书翻译================
    for p in range(len(roi_tags)):
        para = roi_tags[p]
        roi_raw_html = str(para)
        roi_text = para.get_text(strip=True)
        preserved_tags = {}
        if p_format == 'raw':
            roi_html = roi_raw_html
        elif p_format == 'text':
            roi_html = roi_text
        else:  # if p_format == 'raw_simple'
            roi_html, span_classes, preserved_tags = get_roi_html(para, span_classes)

        if check2ignore(para):
            pass
        else:
            do_split = False
            para_segments = get_para_segments(para)
            if len(str(para)) >= 2000:
                # ================段落过长必须切割================
                if len(para_segments) >= 2:
                    do_split = True
            else:
                # ================根据链接所占比例决定是否切割================
                segments_as = [x for x in para_segments if x.startswith('<a')]
                if segments_as and len(str(para)) <= len(segments_as) * 100:
                    do_split = True
            src_soup = BeautifulSoup(roi_html, 'html.parser')
            src_1st_tag = src_soup.find()
            src_opening = roi_html.split('>')[0] + '>'
            src_closing = f"</{src_1st_tag.name}>"
            src_content = roi_html.removeprefix(src_opening).removesuffix(src_closing)
            src_content = src_content.replace('\xa0', ' ').replace('\u2002', ' ')
            if do_split:
                trans_segments = []
                for s in range(len(para_segments)):
                    segment = para_segments[s]
                    trans_segment = main_gpt_dic.get(segment, segment)
                    trans_segments.append(trans_segment)
                src_closing = f"</{src_1st_tag.name}>"
                dst_content = ''.join(trans_segments)
                dst_html = f'{src_opening}{dst_content}{src_closing}'
            else:
                if src_content in main_gpt_dic or src_content in sub_gpt_dic:
                    if src_content in main_gpt_dic:
                        dst_html = get_dst_line(main_gpt_dic, roi_html, bilingual)
                    else:
                        dst_html = get_dst_line(sub_gpt_dic, roi_html, bilingual)
                else:
                    dst_html = roi_html
            if dst_html != roi_html:
                # 解析目标HTML
                dst_soup = BeautifulSoup(dst_html, 'lxml')
                # 寻找与原标签同类型的标签
                dst_para = dst_soup.find(para.name)
                # 恢复完整
                dst_para = restore_para(dst_para, preserved_tags)
                if not do_split and para.name == 'li':
                    replace_tup = (roi_raw_html, str(dst_para))
                    replace_tups.append(replace_tup)
                para.replace_with(dst_para)
            roi_htmls_chapter.append(roi_html)
            roi_texts_chapter.append(roi_text)

    dst_html_text = str(soup)
    dst_html_text = dst_html_text.replace('</p><p>', '</p>\n<p>')
    for replace_tup in replace_tups:
        roi_raw_html, dst_para_str = replace_tup
        logger.info(f'{roi_raw_html}')
        logger.debug(f'{dst_para_str}')
        dst_html_text = dst_html_text.replace(roi_raw_html, dst_para_str, 1)
    return dst_html_text, roi_htmls_chapter


@timer_decorator
@logger.catch
def format_epub(all_html_files):
    all_opfs = get_files(epub_dir, '.opf')
    all_ncxs = get_files(epub_dir, '.ncx')

    # ================允许用户修改翻译================
    if source_html.exists() and user_dest_htm.exists():
        # ================原文================
        source_text = read_txt(source_html)
        source_lines = source_text.splitlines()
        # ================译文================
        user_dest_text = read_txt(user_dest_htm)
        user_destlines = user_dest_text.splitlines()
        # ================一行行对比================
        for s in range(len(source_lines)):
            source_line = source_lines[s]
            destline = user_destlines[s]
            main_gpt_dic[source_line] = destline

    all_translated_lines = []
    roi_htmls = []

    # ================目录================
    if all_ncxs:
        toc_ncx = all_ncxs[0]
        dst_dir = Path(toc_ncx.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        cn_toc_ncx = dst_dir / toc_ncx.name
        dst_txt = dst_dir / f'{toc_ncx.stem}.txt'

        tree = ET.parse(toc_ncx)
        root = tree.getroot()

        # 定义命名空间，如果你的NCX文件有命名空间
        namespaces = {
            'ncx': 'http://www.daisy.org/z3986/2005/ncx/'
        }

        # 查找所有的文本元素，例如<navLabel>下的<text>
        roi_texts_chapter = []
        for text_element in root.findall('.//ncx:navLabel/ncx:text', namespaces):
            original_text = text_element.text
            original_text = original_text.replace('\xa0', ' ').replace('\u2002', ' ')
            roi_html = f'<p>{original_text}</p>'
            text_soup = BeautifulSoup(roi_html, 'lxml')
            text_roi_tags = text_soup.find_all('p')
            if text_roi_tags:
                text_roi_tag = text_roi_tags[0]
                if check2ignore(text_roi_tag):
                    pass
                else:
                    roi_texts_chapter.append(roi_html)
        roi_htmls.extend(roi_texts_chapter)

        translated_text = read_txt(dst_txt)
        if translated_text:
            translated_lines = translated_text.splitlines()
            translated_lines = [x for x in translated_lines if x.strip() != '']
            all_translated_lines.extend(translated_lines)
        else:
            logger.error(f'{dst_txt=}')

    # ================所有网页================
    for a in range(len(all_html_files)):
        src_html_file = all_html_files[a]
        dst_dir = Path(src_html_file.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        dst_xhtml_file = dst_dir / f'{src_html_file.stem}.xhtml'
        dst_bi_xhtml_file = dst_dir / f'{src_html_file.stem}-bilingual.xhtml'
        dst_txt = dst_dir / f'{src_html_file.stem}.txt'
        translated_text = read_txt(dst_txt)
        if translated_text:
            translated_lines = translated_text.splitlines()
            translated_lines = [x for x in translated_lines if x.strip() != '']
            all_translated_lines.extend(translated_lines)
        else:
            logger.error(f'{dst_txt=}')
        dst_html_text, roi_htmls_chapter = get_dst_html_text(src_html_file)
        dst_bi_html_text, roi_htmls_chapter = get_dst_html_text(src_html_file, bilingual=True)
        roi_htmls.extend(roi_htmls_chapter)
        write_txt(dst_xhtml_file, dst_html_text)
        write_txt(dst_bi_xhtml_file, dst_bi_html_text)

    # ================原文================
    # roi_htmls = reduce_list(roi_htmls)
    all_html = lf.join(roi_htmls)
    write_txt(source_html, all_html)

    # ================谷歌翻译================
    all_text = lf.join(all_translated_lines)
    write_txt(dest_txt, all_text)

    # ================GPT翻译================
    dst_lines = []
    for i in range(len(roi_htmls)):
        src_line = roi_htmls[i]
        src_soup = BeautifulSoup(src_line, 'html.parser')
        src_1st_tag = src_soup.find()
        src_opening = src_line.split('>')[0] + '>'
        src_closing = f"</{src_1st_tag.name}>"
        src_content = src_line.removeprefix(src_opening).removesuffix(src_closing)
        src_content = src_content.replace('\xa0', ' ').replace('\u2002', ' ')
        if src_content in main_gpt_dic:
            dst_line = get_dst_line(main_gpt_dic, src_line)
        elif src_content in sub_gpt_dic:
            dst_line = get_dst_line(sub_gpt_dic, src_line)
        else:
            dst_line = src_line
        dst_lines.append(dst_line)
    dst_htm_text = lf.join(dst_lines)
    write_txt(dest_htm, dst_htm_text)

    if not user_dest_htm.exists():
        copy2(dest_htm, user_dest_htm)


@logger.catch
def review_epub():
    glossary_dic = str2dic(glossary_str)
    # ================原文================
    source_text = read_txt(source_html)
    source_lines = source_text.splitlines()
    # ================译文================
    dest_text = read_txt(user_dest_htm)
    destlines = dest_text.splitlines()
    # ================一行行对比================
    for s in range(len(source_lines)):
        source_line = source_lines[s]
        destline = destlines[s]
        has_error = False
        for key in glossary_dic:
            val = glossary_dic[key]
            if search(r'\b' + escape(key.lower()) + r'\b', source_line.lower()):
                if val not in destline:
                    has_error = True
                    logger.warning(f'{key=}')
        if has_error:
            logger.info(source_line)
            logger.debug(destline)


@timer_decorator
@logger.catch
def generate_epub(epub_name, bilingual=False):
    epub_dir = BookHTML / epub_name
    cn_epub_file = BookHTML / f'{epub_name}-GPT4翻译.epub'
    bi_epub_file = BookHTML / f'{epub_name}-双语.epub'

    if bilingual:
        output_epub_file = bi_epub_file
    else:
        output_epub_file = cn_epub_file

    all_files = get_files(epub_dir)
    all_html_files = get_files(epub_dir, 'html')
    mimetype_file = epub_dir / 'mimetype'

    all_opfs = get_files(epub_dir, '.opf')
    all_ncxs = get_files(epub_dir, '.ncx')
    # content_opf = all_opfs[0]

    other_files = [x for x in all_files if x != mimetype_file]
    other_files = [x for x in other_files if x not in all_html_files]

    if show_list:
        pprint(all_files)
        pprint(other_files)

    if all_ncxs:
        toc_ncx = all_ncxs[0]
        dst_dir = Path(toc_ncx.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        cn_toc_ncx = dst_dir / toc_ncx.name
        other_files = [x for x in other_files if x != toc_ncx]

    if not output_epub_file.exists():
        with ZipFile(output_epub_file, 'w') as epub_file:
            # ================文件类型头================
            epub_file.write(mimetype_file.as_posix(), 'mimetype', compress_type=ZIP_STORED)
            # ================其他文件================
            for o in range(len(other_files)):
                file_path = other_files[o]
                archive_path = os.path.relpath(file_path, epub_dir)
                logger.debug(f'{file_path}->{archive_path}')
                epub_file.write(file_path, archive_path, compress_type=ZIP_DEFLATED)
            # ================网页文件================
            for a in range(len(all_html_files)):
                src_html_file = all_html_files[a]
                archive_path = os.path.relpath(src_html_file, epub_dir)
                dst_dir = Path(src_html_file.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
                if bilingual:
                    dst_xhtml = dst_dir / f'{src_html_file.stem}-bilingual.xhtml'
                else:
                    dst_xhtml = dst_dir / f'{src_html_file.stem}.xhtml'
                if dst_xhtml.exists():
                    file_path = dst_xhtml
                else:
                    logger.error(f'{dst_xhtml}')
                    file_path = src_html_file
                logger.debug(f'{file_path}->{archive_path}')
                epub_file.write(file_path, archive_path, compress_type=ZIP_DEFLATED)
            # ================目录================
            if all_ncxs:
                toc_ncx = all_ncxs[0]
                archive_path = os.path.relpath(toc_ncx, epub_dir)
                dst_dir = Path(toc_ncx.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
                cn_toc_ncx = dst_dir / toc_ncx.name
                logger.debug(f'{cn_toc_ncx}->{archive_path}')
                epub_file.write(cn_toc_ncx, archive_path, compress_type=ZIP_DEFLATED)
        logger.warning(f'已生成{output_epub_file.name}')


@timer_decorator
@logger.catch
def html2epub(epub_name):
    epub_dir = BookHTML / epub_name
    # cn_epub_dir = BookHTML / f'{epub_name}-中文'

    logger.warning(f'{epub_dir=}')

    all_files = get_files(epub_dir)
    all_html_files = get_files(epub_dir, 'html')
    mimetype_file = epub_dir / 'mimetype'

    all_opfs = get_files(epub_dir, '.opf')
    all_ncxs = get_files(epub_dir, '.ncx')

    other_files = [x for x in all_files if x != mimetype_file]
    other_files = [x for x in other_files if x not in all_html_files]

    if all_ncxs:
        toc_ncx = all_ncxs[0]
        dst_dir = Path(toc_ncx.parent.as_posix().replace(epub_name, f'{epub_name}-中文', 1))
        cn_toc_ncx = dst_dir / toc_ncx.name
        other_files = [x for x in other_files if x != toc_ncx]

    if show_list:
        pprint(all_files)
        pprint(other_files)

    if all_opfs:
        content_opf = all_opfs[0]
        # 读取OPF文件
        tree = ET.parse(content_opf)
        root = tree.getroot()
        # 命名空间，必须匹配OPF文件中的命名空间定义
        namespaces = {
            'opf': 'http://www.idpf.org/2007/opf'
        }
        # 获取命名空间映射
        namespaces_from_file = dict([
            node for _, node in ET.iterparse(content_opf, events=['start-ns'])
        ])
        # 打印所有命名空间
        print("Namespaces in the document:", namespaces_from_file)

        # 读取manifest元素下的所有item元素
        for item in root.findall('./opf:manifest/opf:item', namespaces):
            item_id = item.get('id')  # 获取item的id属性
            item_href = item.get('href')  # 获取item的href属性，即文件路径
            item_type = item.get('media-type')  # 获取item的media-type属性
            logger.debug(f'Item ID: {item_id}, HREF: {item_href}, Media Type: {item_type}')

    generate_epub(epub_name)
    generate_epub(epub_name, bilingual=True)


@logger.catch
def get_roi_dir(epub_dir):
    OEBPS = epub_dir / 'OEBPS'
    OPS = epub_dir / 'OPS'
    ops = epub_dir / 'ops'
    outer_sub_dirs = get_dirs(epub_dir)
    ignore_names = ['META-INF', 'images']
    roi_outer_sub_dirs = [x for x in outer_sub_dirs if x.name not in ignore_names]
    if OEBPS.exists():
        ops_dir = OEBPS
    elif OPS.exists():
        ops_dir = OPS
    elif ops.exists():
        ops_dir = ops
    elif roi_outer_sub_dirs:
        ops_dir = roi_outer_sub_dirs[0]
    else:
        ops_dir = epub_dir

    xhtml = ops_dir / 'xhtml'
    text = ops_dir / 'text'
    Text = ops_dir / 'Text'
    if xhtml.exists():
        src_dir = xhtml
    elif text.exists():
        src_dir = text
    elif Text.exists():
        src_dir = Text
    else:
        src_dir = ops_dir
    logger.debug(f'{ops_dir=}')
    return src_dir


# @logger.catch
@timer_decorator
def generate_requirements(py_path, python_vs):
    """
    生成给定Python文件中使用的非标准库的列表。

    :param py_path: 要分析的Python文件的路径。
    :param python_vs: Python版本的元组，默认为当前Python版本。
    :return: requirements文本内容
    """
    # 获取已安装的包及其版本
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    # 获取标准库模块列表
    stdlib_modules = set(stdlib_list(python_vs))

    # 读取Python文件并解析语法树
    py_text = read_txt(py_path)
    root = parse(py_text)

    imports = []
    # 遍历语法树，提取import语句
    for node in walk(root):
        if isinstance(node, Import):
            imports.extend([alias.name for alias in node.names])
        elif isinstance(node, ImportFrom):
            if node.level == 0:
                imports.append(node.module)
    imported_modules = set(imports)
    requirements = []

    # 对于导入的每个模块，检查是否为非标准库模块
    for module in imported_modules:
        if module in installed_packages and module not in stdlib_modules:
            requirements.append(module)
    requirements.sort()
    requirements_text = lf.join(requirements)
    return requirements_text


def z():
    pass


browser = 'Google Chrome'

# ask_mode = 'web'
ask_mode = 'app'

sleep_minute = 3
web_answer_time = sleep_minute * 60
app_answer_time = 10
wait_range = 60

censor_words = [
    'naked',
    'rape',
    'pedophile',
    'pedophiles',
    'virginity',
]

computer_marker = f'{processor_name}_{ram}GB'
logger.info(f'{computer_marker=}')

prompt_prefix = '您是一位专业翻译家，精通中文和英文。您的任务是翻译英文小说，请把下列html翻译成中文，保留原格式，并以html格式输出。在翻译过程中，请仔细分析文本的上下文和情感色彩，确保翻译准确无误。人名和专有名词也要翻译成中文。翻译时要连贯、自然且符合中文表达习惯。翻译后的段落数量需和原文段落数量一致且一一对应，不能多段变成一段。'

epub_name = 'your_epub_name'

ignore_models = [
    '3.5',
    '4o mini',
]

browser = 'Google Chrome'
browser_type = 'Chrome'

# do_automate = True
do_automate = False

# hit_enter = True
hit_enter = False

allow_en_names = True
# allow_en_names = False

force_gpt4 = True
# force_gpt4 = False

gpt_line_max = 30
gpt_char_max = 3600
# max_limit = 75
max_limit = 275

local_name = 'your_html_name'

history_names = [
]

if __name__ == "__main__":
    MomoBook = DOCUMENTS / '默墨书籍'
    BookHTML = MomoBook / 'BookHTML'
    Log = MomoBook / 'Log'

    MomoYolo = DOCUMENTS / '默墨智能'
    ChatGPT = MomoYolo / 'ChatGPT'
    ChatGPTPic = MomoYolo / 'ChatGPTPic'

    AutomateUserDataFolder = ProgramFolder / 'MomoAutomateUserData'
    ChatGPTApp = AutomateUserDataFolder / 'ChatGPTApp'
    upload_logo = ChatGPTApp / '回形针上传文件.png'
    gray_up_arrow_logo = ChatGPTApp / '灰色上箭头.png'
    up_arrow_logo = ChatGPTApp / '上箭头.png'
    down_arrow_logo = ChatGPTApp / '下箭头.png'
    stop_logo = ChatGPTApp / '停止.png'
    send_message_logo = ChatGPTApp / '发送消息.png'
    white_x_logo = ChatGPTApp / '白叉.png'
    microphone_logo = ChatGPTApp / '话筒.png'
    headphone_logo = ChatGPTApp / '耳机.png'
    retry_logo = ChatGPTApp / '重试.png'
    reconnect_logo = ChatGPTApp / '重连.png'
    continue_logo = ChatGPTApp / '继续生成.png'
    your_limit_logo = ChatGPTApp / '您的限额.png'
    ChatGPT4o_logo = ChatGPTApp / 'ChatGPT 4o >.png'

    ChatGPTApp_png = ChatGPTPic / 'ChatGPTApp.png'

    make_dir(BookHTML)
    make_dir(Log)

    make_dir(MomoYolo)
    make_dir(ChatGPT)
    make_dir(ChatGPTPic)

    date_str = strftime('%Y_%m_%d')
    log_path = Log / f'日志-{date_str}.log'
    logger.add(
        log_path.as_posix(),
        rotation='500MB',
        encoding='utf-8',
        enqueue=True,
        compression='zip',
        retention='10 days',
        # backtrace=True,
        # diagnose=True,
        # colorize=True,
        # format="<green>{time}</green> <level>{message}</level>",
    )


    def steps():
        pass


    logger.warning(f'{os.cpu_count()=}')
    logger.warning(f'{force_gpt4=}')
    logger.warning(f'{gpt_line_max=}')
    logger.warning(f'{gpt_char_max=}')
    logger.warning(f'{max_limit=}')

    click_type = 'pyautogui'

    read_local = True
    read_local = False

    read_history = True
    read_history = False

    show_list = True
    show_list = False

    target_lang = 'zh-CN'

    # p_format = 'raw'
    p_format = 'raw_simple'

    do_google_translate = True
    # do_google_translate = False

    do_gpt_translate = True
    # do_gpt_translate = False

    del_all_attrs = True
    # del_all_attrs = False

    flat_span = True
    # flat_span = False

    flat_samp = True
    # flat_samp = False

    flat_a = True
    # flat_a = False

    use_censor = True
    # use_censor = False

    show_dic = True
    show_dic = False

    keep_1st_letter = True
    keep_1st_letter = False

    check_page_notation = True
    # check_page_notation = False

    simple_a_id = True
    # simple_a_id = False

    rip_edge_a = True
    # rip_edge_a = False

    global_start_time = time()

    requirements_text = generate_requirements(py_path, python_vs)
    print(requirements_text)

    info_tups = get_window_list()
    app_name = 'ChatGPT'
    ChatGPT_tups = [x for x in info_tups if x[1] == x[2] == app_name]
    if ChatGPT_tups:
        ChatGPT_tup = ChatGPT_tups[0]
        bounds = ChatGPT_tup[-1]
        window_id = ChatGPT_tup[0]
        logger.debug(f'{window_id=}, {bounds=}')

        prompt_prefix = prompt_prefix.replace('英文小说', '英文书籍', 1)

        # read_history = True
        do_automate = True
        hit_enter = True

        epub_dir = BookHTML / epub_name
        cn_epub_dir = BookHTML / f'{epub_name}-中文'
        src_dir = get_roi_dir(epub_dir)
        dst_dir = Path(src_dir.as_posix().replace(epub_name, f'{epub_name}-中文', 1))

        md_file = BookHTML / f'{epub_name}.md'
        source_html = BookHTML / f'{epub_name}.html'
        dest_htm = BookHTML / f'{epub_name}.htm'
        user_dest_htm = BookHTML / f'{epub_name}-用户.htm'
        dest_txt = BookHTML / f'{epub_name}.txt'
        all_html_files = get_files(epub_dir, 'html')

        if show_list:
            pprint(all_html_files)

        if SYSTEM in ['MAC', 'M1']:
            target_tups = get_target_tups(browser)
            if target_tups:
                main_gpt_dic, sub_gpt_dic = get_gpt_dic(target_tups)

                logger.warning(f'{epub_name=}')
                logger.warning(f'{browser=}')

                if not md_file.exists():
                    process_epub(all_html_files)
                translate_epub(all_html_files, do_convert=False)
                # format_epub(all_html_files)
                # html2epub(epub_name)
                # review_epub()

    show_run_time = run_time(global_start_time)
    logger.info(f'总耗时{show_run_time}')

    now_time_str = current_time()
    logger.info(now_time_str)
