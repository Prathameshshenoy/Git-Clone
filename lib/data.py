import os
import hashlib
import zlib

def init(repo):
    try:
        os.makedirs(os.path.join(repo,".git"),exist_ok=True)
        os.makedirs(os.path.join(repo, ".git", "objects"), exist_ok=True)
        os.makedirs(os.path.join(repo, ".git", "refs"), exist_ok=True)

        with open(os.path.join(repo,".git","HEAD"),"w") as f:
            f.write("ref: refs/heads/main\n")
        
        print(f"Initialized empty Git repository in {os.path.abspath(repo)}/.git/")

    except OSError as e:
        print(f"Error initializing repository: {e}")

def object_hash(data, fmt=b'blob',write=False):
    header = fmt + b' ' + str(len(data)).encode() + b'\x00'
    store = header + data
    sha1 = hashlib.sha1(store).hexdigest()

    if write:
        dir_name = sha1[:2]
        file_name = sha1[2:]
        path = os.path.join(".git", "objects",dir_name)

        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,file_name),"wb") as f:
            f.write(zlib.compress(store))
    
    return sha1

def update_ref(ref,commit_sha1):
    full_path = os.path.join(".git",ref)

    if os.path.exists(full_path):
        with open(full_path,"r") as f:
            data = f.read().strip()
            if data.startswith("ref: "):
                ref = data.split(" ")[1]
    ref_path = os.path.join(".git",ref)
    os.makedirs(os.path.dirname(ref_path),exist_ok=True)
    with open(ref_path,"w") as f:
        f.write(commit_sha1)

def get_ref(ref="HEAD"):
    path = os.path.join(".git",ref)
    if not os.path.exists(path):
        return None
    
    with open(path,"r") as f:
        data = f.read().strip()
        if data.startswith("ref: "):
            return get_ref(data.split(" ")[1])
        return data
    