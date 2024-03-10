<p align="center">
  <a href="https://docs.argonariod.tech/"><img src="https://docs.argonariod.tech/logo.svg" width="200" height="200" alt="hammer"></a>
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
    <a href="https://docs.argonariod.tech/maij">
    <img src="https://img.shields.io/badge/MaiJ API-3.2.0-blue" alt="maij">
  </a>
  <img src="https://img.shields.io/badge/Onebot-v11-lightgrey" alt="onebot11">
  <img src="https://img.shields.io/badge/nonebot-2.1.0-orange" alt="nonebot2">
  <a href="https://github.com/ArgonarioD/nonebot-plugin-hammer-core">
    <img src="https://img.shields.io/badge/hammer--core-0.3.3-green" alt="hammer-core">
  </a>
</p>

## 前言
本插件的本质是 [Hammer MaiJ API](https://docs.argonariod.tech/maij) 的 Nonebot2 前端，
可以令您的机器人与其它同样接入了 Hammer MaiJ API 的机器人以及机器人所面向的玩家共享该服务中已经存在的舞萌DX机厅信息。

## 使用包管理器安装本插件

1. 在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

    <details>
    <summary>pip</summary>

    ```sh
    pip install nonebot-plugin-hammer-maij
    ```
    </details>
    <details>
    <summary>pdm</summary>

    ```sh
    pdm add nonebot-plugin-hammer-maij
    ```
    </details>
    <details>
    <summary>poetry</summary>

    ```sh
    poetry add nonebot-plugin-hammer-maij
    ```
    </details>
    <details>
    <summary>conda</summary>

    ```sh
    conda install nonebot-plugin-hammer-maij
    ```
    </details>

2. 打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入
   
    ```toml
    plugins = ["nonebot_plugin_hammer_maij"]
    ```

## :warning:重要

> [!IMPORTANT]
> 使用本插件，必须要在 `.env` 文件中配置两个配置项：
> - SUPERUSERS：机器人超级用户，详情请看 [nonebot2 官方文档](https://nonebot.dev/docs/appendices/config#superusers) 中的解释。
> - MAIJ_API_TOKEN：你持有的 MaiJ API 的 API Token。如果你不知道这是什么，详情请看 [MaiJ API 文档](https://docs.argonariod.tech/maij/token.html) 。

## 命令

> [!NOTE]
>  - 没有通过 `maij.config` 指令设置地区的群聊不会响应任何有关命令。
>  - 在下文中，COMMAND_START代表`.env`文件配置中的`COMMAND_START`的值，默认情况下是`/`。
>  - 在下文中，`<arg>` 指 `arg` 参数必须填写，`[arg]` 指 `arg` 参数可选填写。
>  - 有关本插件的公告功能，其本意是服务于：
>    - 当机厅遇到机身损坏、断电、断网、举办比赛等特殊情况分享；
>    - 失物招领、机厅群宣传等非盈利性质信息的发布。
>
>    API管理员会不定时检查公告内容，如有违规内容（如色情内容、商业性质广告）或无意义灌水会删除，严重者禁用本功能使用权限。

| 命令                                           | 说明                                                                                                                                                                                                                                             |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<COMMAND_START>maij.config <城市名> [目标群号...]` | **只有机器人的超级用户才可以执行该指令！！！**<br/> 为目标群号设置固定地区，当不指定目标群号时目标群号为当前群聊的群号。<br/> 其中省市名必须为API中收录的省市，且必须为如`安徽省合肥市`的标准写法。<br/> 收录的省市列表请查看 [MaiJ API文档](https://docs.argonariod.tech/maij/#%E7%9B%AE%E5%89%8D%E6%94%AF%E6%8C%81%E7%9A%84%E5%8C%BA%E5%9F%9F)。 |
| `<COMMAND_START>maij.disable [目标群号...]`      | **只有机器人的超级用户才可以执行该指令！！！**<br/> 为目标群号清除地区设置，当不指定目标群号时目标群号为当前群聊的群号。                                                                                                                                                                              |
| `机厅列表/jtlb`                                  | 查询本城市中自当日 MaiJ API 重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表                                                                                                                                                                                            |
| `<机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡`            | 查询指定机厅中的排卡数                                                                                                                                                                                                                                    |
| `<机厅名称>+/-<数字>卡`                             | 为指定机厅添加/移除指定卡数                                                                                                                                                                                                                                 |
| `<机厅名称>++/--`                                | 为指定机厅添加/移除一张卡                                                                                                                                                                                                                                  |
| `<机厅名称>[=]<数字>卡`                             | 将指定机厅设置为指定卡数                                                                                                                                                                                                                                   |
| `<机厅名称>[都]有谁`                                | 查询指定机厅今日的卡数变更记录                                                                                                                                                                                                                                |
| `<机厅名称>有什么别名`                                | 查询指定机厅的别名列表                                                                                                                                                                                                                                    |
| `<机厅名称>[的本]周[的]出勤情况`                         | 发送由API记录的指定机厅七天以内的出勤情况折线图                                                                                                                                                                                                                      |
| `发[一](条/个)公告 <地名> <内容>`                      | 发送一条公告，内容支持换行；在不续期的情况下一周后会被自动删除                                                                                                                                                                                                                |
| `续[一](续/发/下)公告 <地名> <公告ID>`                  | 为指定公告续期一周                                                                                                                                                                                                                                      |
| `删[一](条/个)公告 <地名> <公告ID>`                    | 删除指定的公告                                                                                                                                                                                                                                        |

## 测试环境

- Python 3.9.7
- nonebot 2.1.0
- matcha 0.2.5

## 本插件所实现的API

- [Hammer MaiJ API](https://docs.argonariod.tech/maij)

## 更新日志

### v2.0.0 (*2024-01-27*)
重构插件，将项目管理工具从 Poetry 改为 PDM，全面对接 MaiJ API 3.0.0 版本。
#### Feature
- 现在只会在配置了地区的群聊中响应指令了
- 修改了配置地区的指令的用法
- 新增了删除某群的地区设置的指令
- 为机厅设置指定卡数指令可以省略等号了（机厅名称的结尾必须不能是数字，否则需要用等号或者空格分隔机厅名称和卡数）
- 新增了统计相关的指令

### v1.0.1 (*2023-07-10*)
#### Bugs Fixed
- 修复了续期公告请求体参数名错误的问题
- 修复了删除公告请求无法发送的问题
### v1.0.0 (*2023-07-10*)
发布本项目

## 鸣谢

- [onebot](https://github.com/botuniverse/onebot)
- [nonebot2](https://github.com/nonebot/nonebot2)
- [matcha](https://github.com/A-kirami/matcha)

---
~~*如果觉得有用的话求点个Star啵QwQ*~~