# MomoEpubTranslator

epub翻译器

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

首先，将'your_epub_name'改成你想翻译的电子书文件的名称（不带后缀名）。

确保你已将epub文件放到`/Users/your_username/Documents/默墨书籍/BookHTML`目录下。

接着运行`pyqt5_momotranslator_gpt.py`文件：

```bash
python pyqt5_momotranslator_gpt.py
```

不断运行程序即可，当一个步骤完成时，下次运行会进入下一个步骤，直到生成翻译好的epub。

## 许可证

本项目根据MIT许可证授权。有关更多信息，请查看[LICENSE](https://github.com/alicewish/MomoEpubTranslator/blob/main/LICENSE)文件。