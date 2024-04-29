import os
import subprocess

def call_script(game_id, key_list, zip_url):
    """构建命令并调用2.py脚本"""
    cmd = [
        'python', 'rewrite.py', game_id, f'{key_list}', '--path', zip_url
    ]
    subprocess.run(cmd, check=True)
    print(f"Processed {game_id} with keys and zip at {zip_url}")

def process_manifest_files():
    manifest_dir = './Manifest'
    # 读取目录并按文件名排序
    files = sorted(os.listdir(manifest_dir))  # 对文件名进行字母排序

    for filename in files:
        print(filename)
        if filename.endswith('.txt'):
            file_path = os.path.join(manifest_dir, filename)
            with open(file_path, 'r') as file:
                lines = file.read().splitlines()
                if len(lines) >= 3:
                    game_id = lines[0].strip()
                    key_list = lines[1].strip()
                    zip_url = lines[2].strip()
                    print(game_id,key_list,zip_url)
                    call_script(game_id, key_list, zip_url)
        
                    

if __name__ == '__main__':
    process_manifest_files()
