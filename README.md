# SiliconFlow 语音转文字（Windows 版）

把一段录音变成可编辑的文字，并可选地做**文本校准、智能摘要、学术笔记**。本项目把
[Qianxia666/siliconflow-speech-to-text](https://github.com/Qianxia666/siliconflow-speech-to-text)
的最新功能打包成了 Windows 上可以直接双击运行的 `exe`，不需要自己安装 Python。

- 想直接使用：看 [快速开始](#快速开始5-分钟上手)，下载 `exe` 即可。
- 想自己改代码或重新打包：看 [从源码打包](#从源码打包进阶)。

> 需要联网使用。程序会把音频发送到你自己配置的云端接口（默认是硅基流动 SiliconFlow），不会上传到其他任何地方。

## 这个仓库是什么

本仓库是上游项目的 **Windows 打包版**，代码与上游保持一致，只额外做了 3 处适配，方便普通用户在 Windows 上使用：

1. 启动时自动读取 **exe 同目录下的 `.env`**，不用再手动设置系统环境变量。
2. 兼容 PyInstaller 打包后的资源路径（`templates` / `static` 已打包进 exe）。
3. 启动后自动打开默认浏览器，访问 `http://127.0.0.1:5000`。

## 功能一览

- **语音转录**：上传音频，调用兼容 OpenAI 的转录接口，返回文字稿。
- **文本校准**：去掉口语停顿、重复和语气词，修正错别字与多音字。
- **智能摘要**：长文本自动分段、并发提炼，再整合成连贯摘要。
- **学术笔记**：按“草稿 → 自查 → 优化”三阶段生成结构化笔记。
- **长文本支持**：自动分块、上下文衔接、失败重试，避免超出模型长度限制。
- **专用模型**：转录、校准、摘要、笔记可分别指定不同模型。
- **OpenAI 兼容 API**：提供 `s2t-calibrated`、`s2t-summarized` 两个模型，可接入第三方客户端。
- **轻量网页界面**：启动后用浏览器操作，无需安装额外软件。

## 快速开始（5 分钟上手）

整个流程只有 4 步：**拿 API Key → 下载 exe → 写一个 `.env` → 双击运行**。

### 第 1 步：准备一个 API Key（必做）

语音转录必须有一个 API Key。默认使用硅基流动（SiliconFlow），它提供免费额度，注册即可。

1. 打开 [硅基流动控制台](https://cloud.siliconflow.cn/)，注册并登录。
2. 在左侧菜单或账号设置中找到 **API 密钥**。
3. 点击 **新建 API 密钥**，名称随意（例如 `speech-to-text`）。
4. 创建后**立刻复制**密钥（通常以 `sk-` 开头），稍后要填进配置文件。
5. 如果提示余额不足，按控制台提示充值即可。

> API Key 相当于账号密码，不要发给别人，也不要提交到 GitHub。

可选：如果还需要“文本校准 / 摘要 / 学术笔记”，需要再准备一个**对话模型**的 Key。
可以直接复用上面这个硅基流动账号，见 [启用可选功能](#启用可选功能校准--摘要--学术笔记)。

### 第 2 步：下载 exe

1. 打开本仓库页面：<https://github.com/Qianxia666/siliconflow-speech-to-text-windows>
2. 点进 `dist` 文件夹，点击 `SiliconflowSTT.exe`，再点右上角的 **Download raw file**（下载原始文件）。
3. 建议新建一个单独的文件夹（例如 `D:\SiliconflowSTT`），把 exe 放进去。

> 浏览器可能提示“此文件不常见”。这是 PyInstaller 打包程序常见的误报，选择保留即可。
> 如果 Windows 弹出“Windows 已保护你的电脑”，点 **更多信息 → 仍要运行**。

### 第 3 步：创建配置文件 `.env`

程序启动时会读取 **exe 同目录**下名为 `.env` 的文件。

1. 把仓库里的 [.env.example](.env.example) 复制到 exe 所在文件夹。
2. 将它重命名为 `.env`（注意开头有个点，不是 `env.txt`）。
3. 用记事本打开，至少填写下面 3 行：

   ```ini
   S2T_API_URL=https://api.siliconflow.cn/v1/audio/transcriptions
   S2T_API_KEY=sk-粘贴你的密钥
   S2T_MODEL=FunAudioLLM/SenseVoiceSmall
   ```

4. 保存。若使用记事本，请确认编码为 **UTF-8**（Windows 10/11 默认即是）。

最终目录结构应该像这样：

```text
D:\SiliconflowSTT\
├─ SiliconflowSTT.exe
└─ .env
```

### 第 4 步：双击运行

1. 双击 `SiliconflowSTT.exe`。
2. 会弹出一个黑色命令行窗口，显示配置检查和启动日志，**这个窗口不要关**。
3. 稍等片刻，默认浏览器会自动打开 `http://127.0.0.1:5000`。
4. 如果浏览器没有自动打开，手动在地址栏输入 `http://127.0.0.1:5000` 即可。
5. 页面顶部会显示各项功能是否“可用 / 未配置”，确认“语音转录”为可用后，上传音频开始使用。

> 首次启动若 Windows 防火墙询问是否允许网络访问，允许“专用网络”即可。

### 第 5 步：停止与修改配置

- **停止**：直接关闭那个黑色命令行窗口。
- **修改配置**：编辑 `.env` 后，关闭窗口再重新双击 exe 即可生效（正在运行的进程不会自动读取新配置）。

## 启用可选功能（校准 / 摘要 / 学术笔记）

只配置 `S2T_API_KEY` 时，只能使用「语音转录」。要解锁其余功能，在 `.env` 中追加对话模型配置：

```ini
OPT_API_URL=https://api.siliconflow.cn/v1/chat/completions
OPT_API_KEY=sk-你的密钥
OPT_MODEL=Qwen/Qwen2.5-7B-Instruct
```

- 硅基流动的 `OPT_API_URL` 用上面的地址；如使用 OpenAI，则为 `https://api.openai.com/v1/chat/completions`。
- `OPT_MODEL` 填控制台里可用的对话模型 ID（以控制台为准）。
- 想给不同功能用不同模型，可再分别设置 `CALIBRATION_MODEL`、`SUMMARY_MODEL`、`NOTES_MODEL`，不设置则默认使用 `OPT_MODEL`。

## 配置项说明

所有配置都写在 exe 同目录的 `.env` 中，格式为 `KEY=VALUE`，一行一项，`#` 开头为注释。

| 变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `S2T_API_URL` | 是 | `https://api.siliconflow.cn/v1/audio/transcriptions` | 语音转录接口地址 |
| `S2T_API_KEY` | 是 | 空 | 语音转录密钥 |
| `S2T_MODEL` | 是 | `FunAudioLLM/SenseVoiceSmall` | 转录模型 |
| `OPT_API_URL` | 否 | `https://api.openai.com/v1/chat/completions` | 文本处理（对话）接口地址 |
| `OPT_API_KEY` | 否 | 空 | 文本处理密钥，不填则禁用校准/摘要/笔记 |
| `OPT_MODEL` | 否 | 空 | 默认文本处理模型 |
| `CALIBRATION_MODEL` | 否 | 同 `OPT_MODEL` | 校准专用模型 |
| `SUMMARY_MODEL` | 否 | 同 `OPT_MODEL` | 摘要专用模型 |
| `NOTES_MODEL` | 否 | 同 `OPT_MODEL` | 笔记专用模型 |
| `API_ACCESS_TOKEN` | 否 | 空 | 开启 OpenAI 兼容 API 时需要，用于 Bearer 鉴权 |
| `PORT` | 否 | `5000` | 本地服务端口，被占用时可改成 `8080` 等 |
| `MAX_UPLOAD_MB` | 否 | `100` | 单个音频上传大小上限（MB） |
| `MAX_TEXT_CHARS` | 否 | `250000` | 单次处理的文本字符上限 |
| `API_TIMEOUT_SECONDS` | 否 | `300` | 单次上游请求超时（秒） |
| `RETRY_ATTEMPTS` | 否 | `3` | 上游请求失败重试次数 |
| `RETRY_BACKOFF_SECONDS` | 否 | `2` | 重试退避基数（秒） |
| `CHUNK_TARGET_SIZE` | 否 | `5000` | 长文本分块目标大小（字符） |
| `CHUNK_PROCESSING_THRESHOLD` | 否 | `5500` | 超过该字符数才启用分块 |
| `MAX_CONCURRENT_WORKERS` | 否 | `3` | 分块处理最大并发数 |
| `S2T_NO_BROWSER` | 否 | 空 | 设为 `1` 时不自动打开浏览器 |

## 常见问题（FAQ）

**双击后浏览器没有自动打开？**
手动访问 `http://127.0.0.1:5000`。也可以右键 exe →「以管理员身份运行」再试。

**页面显示“未配置”或音频无法转录？**
依次检查：`.env` 是否和 exe 在同一目录；文件名是否为 `.env`（不是 `.env.txt`）；`S2T_API_KEY` 是否已填写并保存；改完后是否重新启动了 exe。

**提示 401 / Token is invalid？**
密钥错误、失效或账户余额不足。重新复制密钥并确认控制台余额。

**端口 5000 被占用怎么办？**
在 `.env` 中加 `PORT=8080`，重新启动后访问 `http://127.0.0.1:8080`。

**杀毒软件报毒 / Windows 拦截？**
未签名的 PyInstaller 程序容易被误报。可加入信任；或按下方步骤从源码自行打包。

**能离线使用吗？**
不能。转录和文本处理都调用云端 API，必须联网。

**支持哪些音频格式？**
常见格式（如 mp3、wav、m4a 等）通常都可，建议先用小文件测试。超过 `MAX_UPLOAD_MB` 会被拒绝。

**公司网络有代理 / 连不上接口？**
请为系统或当前进程配置代理；若接口地址填错也会失败，检查 `S2T_API_URL`。

**修改了 `.env` 但没有生效？**
运行中的进程不会自动重载配置。关闭命令行窗口后重新双击 exe。

## 从源码打包（进阶）

若你想修改代码，或公司环境不允许运行下载的 exe，可以在 Windows 上自行打包。

### 1. 安装 Python

1. 打开 [Python 官方下载页](https://www.python.org/downloads/windows/)，下载 Windows 安装包。
2. 运行安装包，务必勾选 **Add python.exe to PATH**，然后点 **Install Now**。
3. 重新打开 PowerShell，验证：

   ```powershell
   python --version
   ```

   显示 `Python 3.9` 以上版本即可。

### 2. 获取代码

任选一种：

```powershell
git clone https://github.com/Qianxia666/siliconflow-speech-to-text-windows.git
cd siliconflow-speech-to-text-windows
```

或直接在仓库页面点 **Code → Download ZIP**，解压后进入该目录。

### 3. 一键打包

双击仓库中的 `build_windows.bat`，或在 PowerShell 中执行：

```powershell
.\build_windows.bat
```

脚本会自动安装依赖并调用 PyInstaller 打包，完成后产物在 `dist\SiliconflowSTT.exe`。

### 4. 手动打包（等价命令）

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --console --name SiliconflowSTT `
  --add-data "templates;templates" --add-data "static;static" app.py
```

> `--add-data` 的 `;` 分隔符仅适用于 Windows；在 macOS / Linux 上应使用 `:`。

## 目录结构

```text
app.py                 # 上游最新应用代码 + Windows 打包适配
templates/             # 网页模板
static/                # 前端资源（样式、脚本、图标）
requirements.txt       # 运行依赖
.env.example           # 配置模板（复制为 .env 后填写）
build_windows.bat      # Windows 一键打包脚本
dist/                  # 已编译的 exe
LICENSE                # MIT 许可证
```

## 安全与隐私

- API Key 只保存在你本机的 `.env` 中，仓库已通过 `.gitignore` 忽略 `.env`。
- 音频和文本只会发送到你配置的 API 地址。
- 本地服务监听 `0.0.0.0`，同一局域网内设备可能访问到该端口；请勿将其直接暴露到公网。如需对外提供 OpenAI 兼容接口，请设置 `API_ACCESS_TOKEN` 并放在可信网络后使用。

## 与上游同步

本仓库会跟随上游 [siliconflow-speech-to-text](https://github.com/Qianxia666/siliconflow-speech-to-text) 更新功能代码，并重新打包 `dist/SiliconflowSTT.exe`。

## 许可证

与上游一致，采用 [MIT](LICENSE) 许可证。
