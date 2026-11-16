#!/bin/zsh
cd -- "${0:A:h}" || exit 1
if python3 tools/build.py; then
  open dist/index.html
else
  echo '未能生成预览；请查看上面的错误后再重试。'
  read '?按回车关闭窗口。'
  exit 1
fi
