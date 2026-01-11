import sys
import os 
from lib import data, base

def main():

    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python main.py <command> [<args>]")
        return
    
    command = args[0]

    if command == "init":
        data.init(os.getcwd())
    elif command == "hash-object":
        if len(args) < 2:
            print("Usage: python main.py hash-object <file>")
            return
        file_path = args[1]

        with open(file_path,"rb") as f:
            file_data = f.read()

        sha1 = data.object_hash(file_data,write=True)
        print(sha1)

    elif command == "cat-file":
        if len(args)<3 or args[1] != "-p":
            print("Usage: python main.py cat-file -p <hash>")
            return
        base.cat_file(args[2])

    elif command == "write-tree":
        sha1 = base.write_tree(os.getcwd())
        print(sha1)

    elif command == "commit-tree":
        if len(args) < 4 or args[2] != "-m":
            print("Usage: python main.py commit-tree <tree_sha> -m <message>")
            return
        
        tree_sha = args[1]
        message = args[3]
        parent = None
        if len(args)>5 and args[4] == "-p":
            parent = args[5]
        else:
            parent = data.get_ref("HEAD")
        commit_sha = base.commit_tree(tree_sha, message,parent)
        print(commit_sha)
    
    elif command == "log":
        start_sha = args[1] if len(args)>1 else None 
        base.log_graph(start_sha)
    else:
        print(f"Unknown command: {command}")
    
if __name__ == "__main__":
    main()