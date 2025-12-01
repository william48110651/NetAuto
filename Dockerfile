# 使用官方 Python 3.12 輕量版
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴檔
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案所有檔案
COPY . .

# 設定 Flask 可外部訪問
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# 開放 5000 port
EXPOSE 5000

# 啟動 Flask
CMD ["python", "app.py"]
