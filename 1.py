import os
import zipfile
import argparse

# 设置解析器
parser = argparse.ArgumentParser(description='处理游戏ZIP文件和生成Lua脚本')
parser.add_argument('id', type=str, help='游戏ID')
parser.add_argument('list', type=str, help='密钥列表，使用空格分隔')
parser.add_argument('--path', type=str, help='ZIP文件的路径', default=None)

# 解析命令行参数
args = parser.parse_args()

# 获取游戏id和密钥列表
i_id = args.id
input_keys = args.list
entries = input_keys.split(" ")  # 用空格分隔每个条目

# 尝试创建目录
try:
    os.makedirs(i_id, exist_ok=True)
except Exception as e:
    print(f"创建目录失败: {e}")

lua_script_content = f"addappid({i_id})\n"

def find_zip_file(zip_id):
    """寻找允许1-3偏差的zip文件"""
    start_id = int(zip_id) - 3
    end_id = int(zip_id) + 3
    for filename in os.listdir('.'):
        # 提取数字ID用于比较
        try:
            file_id = int(filename.split('_')[0])
        except ValueError:
            continue  # 如果文件名不符合预期格式，跳过
        if file_id >= start_id and file_id <= end_id and filename.endswith('.zip'):
            return filename
    return None

for i in entries:
    zip_id, zip_key = i.split(";")
    extracted = False
    # 检查是否指定了路径
    if args.path:
        zip_filename = args.path
    else:
        zip_filename = find_zip_file(zip_id)

    if zip_filename and os.path.exists(zip_filename):
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(i_id)
            extracted = True
    else:
        print(f"未找到或无法访问ZIP文件: {zip_filename}")

    # 处理目录中的每个文件，生成Lua脚本内容
    if extracted:
        for file_name in os.listdir(f'./{i_id}'):
            print(file_name)
            if file_name.endswith('.manifest'):
                j = file_name.split("_")[0]
                k = file_name.split("_")[1].split(".")[0]
                lua_script_content += f"addappid({j},1,'{zip_key}')\n"
                lua_script_content += f"setManifestid({j},'{k}',0)\n"

# 写入Lua文件
lua_file_path = os.path.join(i_id, f"{i_id}.lua")
with open(lua_file_path, 'w') as lua_file:
    lua_file.write(lua_script_content)
print(f"Lua file created at {lua_file_path}")
