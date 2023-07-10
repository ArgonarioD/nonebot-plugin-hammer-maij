<p align="center">
  <a href="https://docs.hammer-hfut.tk:233/"><img src="https://docs.hammer-hfut.tk:233/logo.svg" width="200" height="200" alt="hammer"></a>
</p>

<div align="center">

# Nonebot Plugin Hammer MaiJ

✨ 基于 onebot、nonebot2 与 Hammer MaiJ API 的 舞萌DX机厅信息共享插件 ✨
</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/ArgonarioD/nonebot-plugin-hammer-maij/main/LICENSE">
    <img src="https://img.shields.io/github/license/ArgonarioD/nonebot-plugin-hammer-core" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-hammer-maij">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-hammer-maij.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9-blue.svg" alt="python">
    <a href="https://docs.hammer-hfut.tk:233/maij">
    <img src="https://img.shields.io/badge/MaiJ API-2.1.0-blue" alt="maij">
  </a>
  <img src="https://img.shields.io/badge/Onebot-v11-lightgrey" alt="onebot11">
  <img src="https://img.shields.io/badge/nonebot-2.0.0-orange" alt="nonebot2">
  <a href="https://github.com/ArgonarioD/nonebot-plugin-hammer-core">
    <img src="https://img.shields.io/badge/hammer--core-0.1.3-green" alt="hammer-core">
  </a>
</p>

## 前言
本插件的本质是 [Hammer MaiJ API](https://docs.hammer-hfut.tk:233/maij) 的 Nonebot2 前端，
可以令您的机器人与其它同样接入了 Hammer MaiJ API 的机器人以及机器人所面向的玩家共享该服务中已经存在的舞萌DX机厅信息。

## 使用本插件

1. 用包管理器在你的 Bot 项目中安装本包，以 Poetry（Nonebot2.0.0 使用的默认包管理器）为例，在命令行中执行

```shell
poetry add nonebot-plugin-hammer-maij
```

2. 修改配置，令 Nonebot2.0.0 能够加载本插件：
    1. 使用 `pyproject.toml` 管理插件加载的情况：

       修改你的 `pyproject.toml` 的以下属性：
       ```toml
       [tool.nonebot]
       plugin = ["nonebot_plugin_hammer_maij"]
       ```
    2. 使用 Python 入口文件管理插件加载的情况：

       在你的 `bot.py` 中添加以下内容：
       ```python
       nonebot.load_plugin("nonebot_plugin_hammer_maij")
       ```

## 命令

> 注：
>  - 在下文中，COMMAND_START代表`.env`文件配置中的`COMMAND_START`的值，默认情况下是`/`。
>  - 有关本插件的公告功能，其本意是服务于：
>    - 当机厅遇到机身损坏、断电、断网、举办比赛等特殊情况分享；
>    - 失物招领、机厅群宣传等非盈利性质信息的发布。
>
>    API管理员会不定时检查公告内容，如有违规内容（如色情内容、商业性质广告）或无意义灌水会删除，严重者禁用本功能使用权限。

| 命令                               | 说明                                                                                 |
|----------------------------------|------------------------------------------------------------------------------------|
| <COMMAND_START>maij.设置本群地区 <省市名> | 为该群设置固定地区，若不设置则下列指令都无法执行；其中省市名必须为API中收录的省市，且必须为如`安徽省合肥市`的标准写法，对于收录省市列表相关信息请查看API文档 |
| 机厅列表                             | 查询本城市中自当日API重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表                                       |
| <机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡  | 查询指定机厅中的排卡数                                                                        |
| <机厅名称>+/-<数字>卡                   | 为指定机厅添加/移除指定卡数                                                                     |
| <机厅名称>++/--                      | 为指定机厅添加/移除一张卡                                                                      |
| <机厅名称>=<数字>卡                     | 将指定机厅设置为指定卡数                                                                       |
| <机厅名称>\[都]有谁                     | 查询指定机厅今日的卡数变更记录                                                                    |
| 发\[一](条/个)公告 <地名> <内容>           | 发送一条公告，内容支持换行；在不续期的情况下一周后会被自动删除                                                    |
| 续\[一](续/ 发/下)公告 <地名> <公告ID>      | 为指定公告续期一周                                                                          |
| 删\[一](条/个)公告 <地名> <公告ID>         | 删除指定的公告，只有发布者可以删除                                                                  |

## 测试环境

- Python 3.9.7
- go-cqhttp v1.1.0
- nonebot 2.0.0

## 本插件所实现的API

- [Hammer MaiJ API](https://docs.hammer-hfut.tk:233/maij)

## 更新日志

### v1.0.1 (*2023-07-10*)
#### Bugs Fixed
- 修复了续期公告请求体参数名错误的问题
- 修复了删除公告请求无法发送的问题
### v1.0.0 (*2023-07-10*)
发布本项目

## 鸣谢

- [onebot](https://github.com/botuniverse/onebot)
- [nonebot2](https://github.com/nonebot/nonebot2)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

---
~~*如果觉得有用的话求点个Star啵QwQ*~~