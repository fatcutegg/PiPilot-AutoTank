---
Notion_Parent_ID: 3590fc46777e80cea840f8f9b4833418
---

# 🐚 基础教程 08：Oh My Zsh 环境增强

在掌握了基础的 Shell 操作（02 篇）后，我们可以通过 Oh My Zsh 让终端更加好用。

## 1. 安装 Oh My Zsh
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## 2. 插件安装（推荐）
### 自动补全
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### 语法高亮
```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

## 3. 配置文件修改
编辑 `~/.zshrc`：
```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

## 4. Conda 自动激活
```bash
conda init zsh
```

---
**💡 总结：**
良好的终端环境是高效开发的第一步。
