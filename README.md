# tar-scope

解压前离线查看 tar、tar.gz、tar.xz 等归档的条目名称、声明体积、链接和可能越界的路径。工具只读取归档，不提取或改写文件。

## 使用

需要 Python 3.8+，不安装依赖。

~~~sh
python tar_scope.py ./backup.tar.gz
python tar_scope.py ./backup.tar --list
~~~

默认显示条目数量、普通文件声明的展开体积和需要留意的绝对路径、盘符路径、`..` 路径段、重复名称、链接或特殊文件类型。`--list` 会列出全部条目名称和声明大小。名称与链接目标以转义形式输出，避免归档中的控制字符影响终端。

此工具不会解压文件，也不会读取普通文件内容。归档格式、展开器和目标系统之间仍可能存在差异；摘要检查不能证明归档安全。gzip、xz 等压缩格式的目录扫描可能需要读取整个压缩流。

## 许可

MIT，见 [LICENSE](LICENSE)。

## Linux x86_64 下载

- [单文件版](https://github.com/506058115-cmd/tar-scope/releases/download/v1.0.0/tar-scope-linux-x86_64-onefile.tar.gz)
- [目录版](https://github.com/506058115-cmd/tar-scope/releases/download/v1.0.0/tar-scope-linux-x86_64-onedir.tar.gz)
- [v1.0.0 Release 页面](https://github.com/506058115-cmd/tar-scope/releases/tag/v1.0.0)

压缩包附带构建信息和依赖许可证；Release 另附 SHA-256 校验文件。构建目标为 GNU/Linux x86_64。较旧 Linux 发行版可能需要兼容的 glibc。
