# SiliconFlow Speech-To-Text（Windows 打包版）

本项目是 [Qianxia666/siliconflow-speech-to-text](https://github.com/Qianxia666/siliconflow-speech-to-text) 最新代码的 Windows 打包版本。

功能与上游保持一致：语音转录、文本校准、量子速读摘要、学术笔记生成、长文本分块处理，以及 OpenAI 兼容 API。
相对于上游，本仓库只做了三处 Windows 打包适配：

1. 启动时读取 **exe 同目录下的 `.env`**，双击即可配置 API Key（优先级低于系统环境变量）。
2. 兼容 PyInstaller 打包后的资源路径（`templates` / `static` 打包进 exe）。
3. 启动后自动打开默认浏览器访问 `http://127.0.0.1:5000`。

## 直接使用

1. 下载 `dist/SiliconflowSTT.exe`，放到任意目录。
2. 在同一目录下放一个 `.env` 文件（可复制仓库中的 `.env.example` 后改名）。
3. 至少填写语音转录密钥：

   ```ini
   S2T_API_URL=https://api.siliconflow.cn/v1/audio/transcriptions
   S2T_API_KEY=sk-你的密钥
   S2T_MODEL=FunAudioLLM/SenseVoiceSmall
   ```

   如需校准 / 摘要 / 笔记，再补充：

   ```ini
   OPT_API_URL=https://api.siliconflow.cn/v1/chat/completions
   OPT_API_KEY=sk-你的密钥
   OPT_MODEL=Qwen/Qwen2.5-7B-Instruct
   ```

4. 双击 `SiliconflowSTT.exe`，程序会启动本地服务并自动打开浏览器。
5. 关闭命令行窗口即停止服务；修改 `.env` 后重新双击即可生效。

常用可选配置（完整清单见 `.env.example`）：

- `PORT`：服务端口，默认 `5000`。
- `S2T_NO_BROWSER=1`：不自动打开浏览器（脚本或远程部署时使用）。
- `MAX_UPLOAD_MB` / `MAX_TEXT_CHARS` / `API_TIMEOUT_SECONDS` 等运行参数。

## 自行编译

需要 Windows + Python 3.9 及以上版本：

```bat
build_windows.bat
```

脚本会安装依赖、调用 PyInstaller 打包，产物位于 `dist\SiliconflowSTT.exe`。
等价的手动命令：

```bat
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --console --name SiliconflowSTT ^
  --add-data "templates;templates" --add-data "static;static" app.py
```

## 目录结构

```text
app.py                 # 上游最新应用代码 + Windows 打包适配
templates/             # 页面模板
static/                # 前端资源
requirements.txt       # 运行依赖
.env.example           # 配置模板
build_windows.bat      # Windows 一键打包脚本
dist/                  # 已编译的 exe
```

## 许可证

与上游一致，采用 [MIT](LICENSE) 许可证。
