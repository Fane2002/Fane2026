from PIL import Image
import os
import shutil

def optimize_images():
    # 创建备份文件夹
    backup_dir = "images_backup"
    if not os.path.exists(backup_dir):
        shutil.copytree("images", backup_dir)
        print("已创建原始图片备份到：images_backup")
    
    # 统计原始大小
    original_size = 0
    for root, dirs, files in os.walk("images"):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                original_size += os.path.getsize(path)
    
    total_saved = 0
    
    # 优化图片
    for root, dirs, files in os.walk("images"):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                original_file_size = os.path.getsize(path)
                
                try:
                    img = Image.open(path)
                    width, height = img.size
                    
                    # 如果图片太大，降低分辨率
                    if width > 1920 or height > 1080:
                        ratio = min(1920 / width, 1080 / height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 保存优化后的图片
                    if file.lower().endswith(('.jpg', '.jpeg')):
                        img.save(path, quality=85, optimize=True)
                    elif file.lower().endswith('.png'):
                        img.save(path, optimize=True)
                    
                    new_size = os.path.getsize(path)
                    saved = original_file_size - new_size
                    total_saved += saved
                    
                    if saved > 0:
                        print(f"优化: {file} - 节省: {saved/1024:.2f}KB")
                    
                except Exception as e:
                    print(f"跳过: {file} - {e}")
    
    print(f"\n优化完成！")
    print(f"原始大小: {original_size/1024/1024:.2f}MB")
    print(f"节省空间: {total_saved/1024/1024:.2f}MB")

if __name__ == "__main__":
    print("开始优化图片...")
    print("="*50)
    optimize_images()
    print("\n视频压缩建议：")
    print("1. 使用在线工具：https://convertio.co/zh/mp4-compressor/")
    print("2. 或者下载 HandBrake 压缩到 720p")
