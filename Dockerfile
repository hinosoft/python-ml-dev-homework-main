# Sử dụng Python làm base image
FROM python:3.9

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép mã nguồn vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng ứng dụng
EXPOSE 8000

# Lệnh chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
