# 使用官方 Python 镜像作为基础镜像
FROM python:3.12.4-alpine

# 设置工作目录
WORKDIR /home

# 复制项目的依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露应用运行的端口
EXPOSE 8000

# 运行 Django 服务器
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wallhaven_project.wsgi:application"]
