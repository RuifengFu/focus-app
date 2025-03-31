# 专注助手 (Focus Assistant)

一款帮助您提高工作效率、管理时间和增强行动力的桌面应用。专注助手集成了番茄工作法、待办事项管理、以及时间可视化等功能，让您清晰了解时间的宝贵，从而更有动力地规划和利用每一天。

## 主要功能

*   **番茄工作法计时器**：自定义工作时间和休息时间，帮助您保持专注
*   **待办事项管理**：简单直观的任务管理界面
*   **时间统计**：直观展示今日流逝时间、年度进度和生命进度
*   **激励名言**：随机展示富有哲理的名言，提升动力
*   **工作时间追踪**：记录并可视化您的工作时间

## 技术栈

*   **前端**：Vue.js 3
*   **后端**：Rust (Tauri 框架)
*   **构建工具**：Vite

## 从零开始部署指南

### 1. 开发环境准备

**安装必要的系统依赖**

*   **对于 Windows 用户**:
    *   安装 Visual Studio 2019 (或更新版本) 并勾选 "Desktop development with C++"
    *   安装 nvm npm Node.js (推荐使用 v16 或更高版本)
    *   安装 Rust
    *   安装 Git
*   **对于 macOS 用户**:
    ```bash
    # 安装 Homebrew (如果尚未安装)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # 安装 Xcode 命令行工具
    xcode-select --install

    # 安装 Node.js
    brew install node

    # 安装 Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

    # 安装 Tauri 依赖
    brew install wget
    ```
*   **对于 Linux 用户 (Ubuntu/Debian)**:

    ```bash
    # 更新软件包列表
    sudo apt update

    # 安装必要的依赖
    sudo apt install libwebkit2gtk-4.0-dev \
        build-essential \
        curl \
        wget \
        libssl-dev \
        libgtk-3-dev \
        libayatana-appindicator3-dev \
        librsvg2-dev

    # 安装 Node.js
    curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # 安装 Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

### 2. 克隆项目

```bash
git clone https://github.com/yourusername/focus-assistant.git
cd focus-assistant
```

### 3. 安装项目依赖

```bash
# 安装前端依赖
npm install

# 安装 Tauri CLI
npm install -g @tauri-apps/cli
```

### 4. 项目结构说明

```
focus-assistant/
├── src/                  # 前端 Vue 代码
│   ├── components/       # Vue 组件
│   ├── App.vue           # 主应用组件
│   └── main.js           # Vue 入口文件
├── src-tauri/            # Rust 后端代码
│   ├── src/              # Rust 源代码
│   │   ├── main.rs       # 主入口文件
│   │   ├── timer.rs      # 番茄计时器实现
│   │   ├── todo.rs       # 待办事项管理
│   │   └── quotes.rs     # 名言管理
│   ├── resources/        # 资源文件
│   │   └── quotes.json   # 名言数据
│   ├── Cargo.toml        # Rust 依赖配置
│   └── tauri.conf.json   # Tauri 配置文件
├── package.json          # 项目配置与依赖
└── README.md             # 项目说明文档
```

### 5. 开发模式运行

```bash
# 启动开发服务器
npm run tauri dev
```

这将启动一个带有热重载功能的开发服务器，您可以实时看到代码修改的效果。

### 6. 自定义功能

**修改名言库**

编辑 `src-tauri/resources/quotes.json` 文件，添加或修改励志名言：

**调整番茄钟默认时间**

修改 `src-tauri/src/timer.rs` 文件中的默认设置：

```rust
pub fn new() -> Self {
    Self {
        work_duration: Mutex::new(Duration::minutes(25)), // 修改默认工作时间
        break_duration: Mutex::new(Duration::minutes(5)), // 修改默认休息时间
        // ...其他设置
    }
}
```

### 7. 构建应用程序

```bash
# 构建生产版本
npm run tauri build
```

构建完成后，可执行文件将位于以下目录：

*   Windows: `src-tauri/target/release/focus-assistant.exe`
*   macOS: `src-tauri/target/release/bundle/macos/Focus Assistant.app`
*   Linux: `src-tauri/target/release/focus-assistant`

### 8. 打包与发布

Tauri 会自动为不同平台生成安装包：

*   Windows: `src-tauri/target/release/bundle/msi/` 目录下的 `.msi` 文件
*   macOS: `src-tauri/target/release/bundle/dmg/` 目录下的 `.dmg` 文件
*   Linux:
    *   `src-tauri/target/release/bundle/deb/` 目录下的 `.deb` 文件
    *   `src-tauri/target/release/bundle/appimage/` 目录下的 `.AppImage` 文件

## 9. 使用指南

### 番茄工作法

*   在设置面板中调整工作时间、休息时间和每日工作时长
*   点击"开始"按钮启动计时器
*   专注工作直到休息时间
*   短暂休息后继续下一个工作周期

### 待办事项管理

*   在输入框中输入新任务，按回车添加
*   点击任务前的复选框标记完成
*   点击删除按钮移除任务

### 时间统计

查看三种进度条，了解：

*   今日时间流逝百分比
*   年度进度百分比
*   生命进度百分比

## 10. 常见问题

*   **Q: 应用无法启动怎么办？**
    *   A: 检查是否安装了所有必要的系统依赖，并确保 Node.js 和 Rust 的版本是最新的。
*   **Q: 名言不显示或显示默认名言怎么办？**
    *   A: 确保 `quotes.json` 文件格式正确，且位于正确的目录位置。
*   **Q: 如何修改默认设置？**
    *   A: 您可以修改源代码中的默认值，或者在应用的设置界面中进行调整。

## 许可证

MIT License

## 贡献

欢迎提交 Pull Request 或提出 Issues 帮助改进项目。

---

希望"专注助手"能够帮助您提高工作效率和行动力！如有任何问题，请随时联系我们。

本项目全部由Claude-3.7编写