# 更新
将所有页面爬取下来
<p>因为这个是玩家自己上传的 千奇百怪 总有些人上传的格式怪怪的 处理起来也是很累，</p>
<p>有的上传的还不是zip的，或者是zip解压不了的，这些都是少数 所有直接扔掉了，不想为这些再加代码量</p>
有的zip包解压还有后里面还有一层目录的
更新改修的py文件rewrite.py 如果--path后面是http开头 zip结尾的就会自动下载 然后解压
添加了get_all_manifest_txt.py文件 获取所有清单信息并保存，
添加了call_rewrite_file.py文件  调用rewrite.py，将获取的清单信息全部处理
添加了delete_error_dir.sh文件 这个是shell脚本，将有问题的清单目录删除， 这个就是前面说的zip的问题。
最后处理效果