# 飞书 Agent 配置指南

> 让你的个人电脑变成飞书机器人的大脑，随时随地通过飞书对话控制你的电脑。

---

## 📋 目录

1. [前置条件](#前置条件)
2. [方案选择](#方案选择)
3. [企业用户配置](#企业用户配置)
4. [个人用户配置](#个人用户配置)
5. [项目配置](#项目配置)
6. [运行与测试](#运行与测试)
7. [常见问题](#常见问题)

---

## 前置条件

### 必需环境

- Python 3.8+
- 本项目完整代码
- LLM API 密钥（Claude/OpenAI 等，已在 `llmcore/mykeys` 中配置）

### 安装依赖

```bash
pip install lark-oapi
```

---

## 方案选择

| 你的情况           | 推荐方案                   | 预计耗时  |
| ------------------ | -------------------------- | --------- |
| 公司已有飞书企业版 | [企业用户配置](#企业用户配置) | 5-10分钟  |
| 个人用户/学习测试  | [个人用户配置](#个人用户配置) | 10-15分钟 |

---

## 企业用户配置

> 适用于：你的公司使用飞书，你有权限创建应用或联系管理员审批

### 步骤 1：创建应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录你的企业飞书账号
3. 点击右上角「创建应用」→「企业自建应用」
4. 填写应用信息：
   - 应用名称：`我的Agent助手`（可自定义）
   - 应用描述：`个人AI助手`
   - 应用图标：可选

### 步骤 2：添加机器人能力

1. 进入应用详情页
2. 左侧菜单选择「添加应用能力」
3. 找到「机器人」，点击「添加」
4. 配置机器人信息（可保持默认）

### 步骤 3：配置权限

1. 左侧菜单「权限管理」→「API 权限」
2. 搜索并开通以下权限：
   - `im:message` - 获取与发送单聊、群组消息
   - `im:message:send_as_bot` - 以应用身份发送消息
   - `contact:user.id:readonly` - 获取用户 ID

### 步骤 4：获取凭证

1. 左侧菜单「凭证与基础信息」
2. 记录以下信息：
   - **App ID**：`cli_xxxxxxxx`
   - **App Secret**：`xxxxxxxxxxxxxxxx`

### 步骤 5：发布应用

1. 左侧菜单「版本管理与发布」
2. 点击「创建版本」
3. 填写版本信息，提交审核
4. **联系企业管理员审批**（或自己是管理员直接审批）

### 步骤 6：获取你的 Open ID

1. 应用审批通过后，在飞书中搜索你的机器人
2. 给机器人发送任意消息
3. 运行以下代码获取你的 Open ID：

```python
# 临时运行一次，获取 open_id
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

client = lark.Client.builder().app_id("你的APP_ID").app_secret("你的APP_SECRET").build()

# 监听消息，打印发送者的 open_id
def handle(data):
    print(f"你的 Open ID: {data.event.sender.sender_id.open_id}")

# ... 或者查看 frontends/fsapp.py 运行时的日志输出
```

---

## 个人用户配置

> 适用于：没有企业飞书账号，想个人测试使用

### 步骤 1：创建测试企业

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 使用个人手机号注册/登录
3. 点击右上角头像 →「创建测试企业」
4. 填写企业名称（如：`我的测试工作区`）
5. 创建完成后，你就是这个测试企业的**管理员**

### 步骤 2：创建应用

> 与企业用户步骤相同

1. 点击「创建应用」→「企业自建应用」
2. 填写应用信息

### 步骤 3：添加机器人能力

1. 进入应用详情页
2. 「添加应用能力」→「机器人」→「添加」

### 步骤 4：配置权限

1. 「权限管理」→「API 权限」
2. 开通权限：
   - `im:message`
   - `im:message:send_as_bot`
   - `contact:user.id:readonly`

### 步骤 5：获取凭证

1. 「凭证与基础信息」
2. 复制 **App ID** 和 **App Secret**

### 步骤 6：发布应用（测试企业可自审批）

1. 「版本管理与发布」→「创建版本」
2. 提交后，进入 [飞书管理后台](https://feishu.cn/admin)
3. 「工作台」→「应用审核」→ 通过你的应用

### 步骤 7：在飞书客户端使用

1. 下载 [飞书客户端](https://www.feishu.cn/download)
2. 登录你的测试企业账号
3. 搜索你创建的机器人名称
4. 开始对话！

---

## 项目配置

### 配置飞书凭证

编辑项目根目录的 `mykey.py`，添加：

```python
# 飞书应用凭证
fs_app_id = "cli_xxxxxxxxxxxxxxxx"      # 替换为你的 App ID
fs_app_secret = "xxxxxxxxxxxxxxxx"       # 替换为你的 App Secret

# 允许使用的用户 Open ID 列表（留空则允许所有人，建议填写以限制访问权限）
fs_allowed_users = [
    "ou_xxxxxxxxxxxxxxxxxxxxxxxx",       # 你的 Open ID
]
```

### 确认 LLM 配置

确保 `llmcore/mykeys` 中已配置 LLM API 密钥：

```python
# 示例：Claude API
claude_config = {
    'apikey': 'sk-ant-xxxxx',
    'apibase': 'https://api.anthropic.com',
    'model': 'claude-sonnet-4-20250514'
}
```

---

## 运行与测试

### 启动服务

```bash
cd /path/to/pc-agent-loop
python frontends/fsapp.py
```

### 预期输出

```
========================
```
