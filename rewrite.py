import os
import zipfile
import argparse
import requests
import shutil

# 设置代理
proxies = {
    'http': 'http://192.168.10.4:10809',
    'https': 'http://192.168.10.4:10809',
}

# 解析命令行参数
parser = argparse.ArgumentParser(description='处理游戏ZIP文件和生成Lua脚本')
parser.add_argument('id', type=str, help='游戏ID')
parser.add_argument('list', type=str, help='密钥列表，使用空格分隔')
parser.add_argument('--path', type=str, help='ZIP文件的路径或URL', default=None)
args = parser.parse_args()

# 尝试创建目录
try:
    os.makedirs(args.id, exist_ok=True)
except Exception as e:
    print(f"创建目录失败: {e}")

lua_script_content = f"addappid({args.id})\n"

# 辅助函数：下载文件
def download_file(url, local_filename):
    with requests.get(url, proxies=proxies, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename

# 清理指定的目录
def cleanup_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"已删除目录: {directory}")
    except Exception as e:
        print(f"删除目录失败: {e}")

# 下载并解压ZIP文件
zip_filename = None
if args.path and args.path.startswith('http') and args.path.endswith('.zip') and 'vdf' not in args.path and 'txt' not in args.path:
    zip_filename = download_file(args.path, f"{args.id}.zip")
elif args.path and args.path.startswith('http') and args.path.endswith('.txt'):
    cleanup_directory(args.id)
    exit()
elif args.path:
    zip_filename = args.path

if zip_filename and os.path.exists(zip_filename):
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(args.id)
    except zipfile.BadZipFile:
        print(f"文件 {zip_filename} 不是有效的ZIP文件或已损坏。")
        cleanup_directory(args.id)
        exit()
    except Exception as e:
        print(f"解压文件 {zip_filename} 时发生错误: {e}")
        cleanup_directory(args.id)
        exit()
    finally:
        os.remove(zip_filename)
        
        # if os.listdir(args.id):
        
# 处理每个密钥
for entry in args.list.split(" "):
    zip_id, zip_key = entry.split(";")
    if os.path.exists(args.id):
        for file_name in os.listdir(f'./{args.id}'):
            if file_name.endswith('.manifest'):
                j = file_name.split("_")[0]
                k = file_name.split("_")[1].split(".")[0]
                lua_script_content += f"addappid({j},1,'{zip_key}')\n"
                lua_script_content += f"setManifestid({j},'{k}',0)\n"

# 写入Lua文件
lua_file_path = os.path.join(args.id, f"{args.id}.lua")
with open(lua_file_path, 'w') as lua_file:
    lua_file.write(lua_script_content)
print(f"Lua file created at {lua_file_path}")


