# MomoEpubTranslator

`MomoEpubTranslator`是`epub翻译器`， 一个自动化工具，用于将EPUB电子书从英文翻译成中文，支持`中文`和`双语`两种输出格式。兼容
`ChatGPT`和`Claude`，可以在保持原始EPUB格式的同时提供高质量翻译。

![Commit activity](https://img.shields.io/github/commit-activity/m/alicewish/MomoEpubTranslator)
![License](https://img.shields.io/github/license/alicewish/MomoEpubTranslator)
![Contributors](https://img.shields.io/github/contributors/alicewish/MomoEpubTranslator)

简体中文 | [English](README_EN.md)

## 安装

首先，确保您的计算机上已安装Python 3.10。您可以通过在命令行输入以下命令来检查Python版本：

```bash
python --version
```

克隆此存储库或下载ZIP文件并解压缩。

使用以下命令安装必需的Python库：

```bash
pip install -r requirements.txt
```

## 使用

```python
epub_name = '你的EPUB文件名'  # EPUB文件名（不含扩展名）
ai_app_name = 'ChatGPT'     # 或者选择'Claude'
do_automate = True         # 启用自动翻译
do_enter = True           # 自动按回车键
allow_en_names = False    # 允许英文名
allow_en_numbers = False  # 允许英文数字
allow_quotes = True       # 不考虑引号问题
use_gpt4 = False       # 使用GPT4
```

确保你已将epub文件放到`/Users/your_username/Documents/默墨书籍/BookHTML`目录下。

接着运行`pyqt5_momotranslator_gpt.py`文件：

```bash
python pyqt5_momotranslator_gpt.py
```

不断运行程序即可，当一个步骤完成时，下次运行会进入下一个步骤，直到生成翻译好的epub。

## 其他

### 输出文件

- `{epub_name}-ChatGPT翻译.epub`：中文翻译版本
- `{epub_name}-ChatGPT双语.epub`：双语版本
- `{epub_name}.md`：提取的markdown格式文本
- `{epub_name}.html`：HTML格式源文本
- `{epub_name}.htm`：HTML格式翻译文本
- `{epub_name}-用户.htm`：用户可编辑的翻译文件

## 使用门槛

1. 需要一台装有openai桌面应用的电脑，可以是win或mac。
2. 需要登录开通会员的openai账号。
3. 如果只是想用于Claude，则需要一台电脑和一个账号（可以是没开会员的）。

## 许可证

本项目根据MIT许可证授权。有关更多信息，请查看[LICENSE](https://github.com/alicewish/MomoEpubTranslator/blob/main/LICENSE)
文件。