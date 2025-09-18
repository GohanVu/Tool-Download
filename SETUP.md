# Hướng dẫn Setup Video Downloader Tool

## Yêu cầu hệ thống
- macOS (đã test trên macOS 14+)
- Python 3.11.9 (cụ thể)
- Homebrew (để cài đặt pyenv)

## Cài đặt môi trường

### 1. Cài đặt pyenv (nếu chưa có)
```bash
brew install pyenv
```

### 2. Cấu hình pyenv trong shell
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

### 3. Reload shell hoặc chạy:
```bash
source ~/.zshrc
```

### 4. Cài đặt Python 3.11.9
```bash
pyenv install 3.11.9
```

### 5. Thiết lập Python 3.11.9 cho project
```bash
cd /path/to/Tool-Download
pyenv local 3.11.9
```

### 6. Tạo môi trường ảo
```bash
python -m venv venv
```

### 7. Kích hoạt môi trường ảo
```bash
source venv/bin/activate
```

### 8. Cài đặt dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 9. Chạy ứng dụng
```bash
python main.py
```

## Các lệnh hữu ích

### Kích hoạt môi trường ảo (mỗi lần mở terminal mới)
```bash
cd /path/to/Tool-Download
source venv/bin/activate
```

### Kiểm tra phiên bản Python
```bash
python --version
# Kết quả mong đợi: Python 3.11.9
```

### Kiểm tra các package đã cài đặt
```bash
pip list
```

### Deactivate môi trường ảo
```bash
deactivate
```

## Troubleshooting

### Nếu gặp lỗi "command not found: python"
- Đảm bảo đã kích hoạt môi trường ảo: `source venv/bin/activate`
- Kiểm tra pyenv đã được cấu hình: `pyenv versions`

### Nếu gặp lỗi khi cài đặt PyQt6
- Đảm bảo đang sử dụng Python 3.11.9
- Thử cài đặt lại: `pip uninstall PyQt6 && pip install PyQt6==6.9.1`

### Nếu ứng dụng không chạy
- Kiểm tra tất cả dependencies: `pip install -r requirements.txt`
- Đảm bảo đang trong thư mục project và đã kích hoạt venv
