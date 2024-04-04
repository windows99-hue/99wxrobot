**使用内置的 `venv` 模块**

1. 打开终端并进入你想要创建虚拟环境的目录。

2. 运行以下命令来创建虚拟环境（假设你的项目将使用Python 3）：

   ```
   bashCopy code
   python3 -m venv venv_name
   ```

   其中，`venv_name` 是你想要为虚拟环境指定的名称。

3. 激活虚拟环境。在Windows上，使用以下命令：

   ```
   bashCopy code
   venv_name\Scripts\activate
   ```

   在 macOS 和 Linux 上，使用以下命令：

   ```
   bashCopy code
   source venv_name/bin/activate
   ```

   当虚拟环境激活后，你会看到命令行前面出现了虚拟环境的名称。

4. 安装依赖项。你可以使用 `pip` 安装项目所需的依赖项，这些依赖项将仅在虚拟环境中可用。

5. 在虚拟环境中运行你的项目。