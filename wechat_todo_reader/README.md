# 微信群待办助手（P0/P1 只读验证）

这个独立子项目只验证一件事：能否通过 Windows UI Automation 读取白名单中微信群的最近可见文本，并打印到终端。

## 安全边界

- 仅适用于 Windows 10/11、已登录且正在运行的微信 4.x。
- 仅使用 `uiautomation` 访问 Windows UI Automation；不使用 wx4py 作为运行时依赖。
- 只会对 `config.json` 中**精确匹配**的 `allowed_groups` 逐一查找和读取。
- 为显示某个允许群的当前消息，读取器可能仅通过 UIA 选择该允许的会话项；它不会向聊天输入框写入内容，也不会执行发送、自动回复、加好友、登录、群管理、DLL 注入、Hook、内存读取、修改微信或非官方协议登录。
- 未在白名单的群名会在调用 UIA 前被拒绝。

> 读取/打开某个聊天可能使微信本身将未读状态变为已读。这是微信客户端的界面行为；本项目不会发送任何消息。

## 安装与配置

在 Windows PowerShell 中使用真实的 Windows Python：

```powershell
cd "D:\download（D）\vscode practice\wechat_todo_reader"
py -m pip install -r requirements.txt
Copy-Item config.example.json config.json
```

编辑 `config.json`，只填写要读取的精确群名：

```json
{
  "allowed_groups": ["XXX课程群"],
  "recent_message_limit": 5
}
```

`config.json` 不会由程序自动创建或修改。

## 运行

先登录并打开 Windows 微信 4.x，然后运行：

```powershell
python .\test_reader.py
```

预期格式：

```text
微信窗口：找到
群聊：XXX课程群
最近消息：
1. 第一条
2. 第二条
```

## UI 树诊断

微信版本、语言和辅助功能状态会改变 UIA 树。出现“找不到群”或“找不到聊天区域”时，**先**运行：

```powershell
python .\inspect_ui_tree.py --depth 5
```

该诊断命令只打印当前 UIA 控件的 `ControlTypeName`、`Name`、`AutomationId` 与 `ClassName`，不会点击、聚焦、输入、保存或发送。请根据实际输出调整 `src\wechat_todo_reader\reader.py` 的选择器；不要用 OCR、坐标点击、Hook 或注入作为回退。

## 已知限制

- 微信 Qt UIA 通常不能稳定暴露发送者名称；P0/P1 只输出可见消息文本。
- 当前实现依据 wx4py 已公开的微信 4.x 观察，优先查找 `AutomationId="chat_message_list"` 和 `mmui::ChatTextItemView` / `mmui::ChatBubbleItemView`。真实版本必须以 `inspect_ui_tree.py` 输出为准。
- 仅读取当前可见消息，不滚动加载历史记录。
