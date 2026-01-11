import os
import zlib
import time
from . import data

def cat_file(sha1):
    dir_name = sha1[:2]
    file_name = sha1[2:]
    path = os.path.join(".git","objects",dir_name,file_name)

    try:
        with open(path,"rb") as f:
            compressed_data = f.read()
            full_data = zlib.decompress(compressed_data)
        raw_header,content = full_data.split(b'\x00',1)
        type_str,size_str = raw_header.split(b' ')
        print(content.decode())

    except FileNotFoundError:
        print(f"Error: Object {sha1} not found")

    except Exception as e:
        print(f"Error reading object {e}")

def write_tree(directory= "."):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full_path = os.path.join(directory,entry.name)

            if entry.name == ".git" or entry.name == "__pycache__":
                continue
            
            if entry.is_file(follow_symlinks=False):
                with open(full_path,"rb") as f:
                    file_data = f.read()
                sha1 = data.object_hash(file_data,fmt=b'blob',write=True)

                stat = os.stat(full_path)
                mode = b'100755' if (stat.st_mode & 0o100) else b'100644'
                entries.append((entry.name.encode(),mode,bytes.fromhex(sha1)))
            
            elif entry.is_dir(follow_symlinks=False):
                sha1 = write_tree(full_path)
                mode = b'40000'
                entries.append((entry.name.encode(),mode,bytes.fromhex(sha1)))

    def sort_key(item):
        name,mode, _ = item
        if mode == b'40000':
            return name + b'/'
        return name
    entries.sort(key=sort_key)
    tree_content = b""
    for name,mode,sha1 in entries:
        tree_content += mode + b' ' + name + b'\x00' + sha1
    return data.object_hash(tree_content,fmt=b'tree',write=True)

def commit_tree(tree_sha1,message,parent_sha1=None):
    seconds = int(time.time())
    timezone = "+0000"
    author = f"Prathamesh <prathamesh@example.com> {seconds} {timezone}"
    committer = f"Prathamesh <prathamesh@example.com> {seconds} {timezone}"
    lines = []
    lines.append(f"tree {tree_sha1}")
    if parent_sha1:
        lines.append(f"parent {parent_sha1}")
    lines.append(f"author {author}")
    lines.append(f"committer {committer}")
    lines.append("")
    lines.append(message)
    data_content = "\n".join(lines).encode()
    commit_sha1 = data.object_hash(data_content,fmt=b'commit',write=True)
    data.update_ref("HEAD",commit_sha1)
    return commit_sha1

def log_graph(commit_sha1=None):
    if not commit_sha1:
        commit_sha1 = data.get_ref("HEAD")

    while commit_sha1:
        dir_name = commit_sha1[:2]
        file_name = commit_sha1[2:]
        path = os.path.join(".git","objects",dir_name,file_name)

        try:
            with open(path,"rb") as f:
                raw_data = zlib.decompress(f.read())
            
            header_end = raw_data.find(b'\x00')
            content = raw_data[header_end+1:].decode()
            lines = content.split("\n")
            print(f"commit {commit_sha1}")

            parent = None
            for line in lines:
                if line.startswith("parent "):
                    parent = line.split(" ")[1]
                elif line.startswith("author "):
                    print(line)
            
            try:
                empty_idx = lines.index("")
                print("\n    " + "\n    ".join(lines[empty_idx+1:]))
            
            except ValueError:
                pass
            print("-"*40)
            commit_sha1 = parent

        except FileNotFoundError:
            break