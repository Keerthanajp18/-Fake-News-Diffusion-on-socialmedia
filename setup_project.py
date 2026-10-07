import os
import shutil

def setup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    dirs = [
        "data/raw/twitter15/tree",
        "data/raw/twitter16/tree",
        "data/processed/twitter15",
        "data/processed/twitter16",
        "src/ndtl_engine",
        "src/kg_engine",
        "experiments",
        "models"
    ]
    
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)
        print(f"Created: {d}")
        
    ndtl_src = os.path.join(base_dir, "NDTL")
    engine_dest = os.path.join(base_dir, "src", "ndtl_engine")
    
    core_files = [
        "ndtl.py",
        "ndtl_grammar.lark",
        "ndtl_parser.py",
        "NDTL_discovery.py",
        "Dataset.py",
        "NetworkGenerator.py"
    ]
    
    for f in core_files:
        src_path = os.path.join(ndtl_src, f)
        if os.path.exists(src_path):
            shutil.copy(src_path, engine_dest)
            print(f"Copied core engine file: {f} -> src/ndtl_engine/")
            
    raw_source = os.path.join(base_dir, "fake-news-analysis", "rumor_detection_acl2017")
    
    for ds in ["twitter15", "twitter16"]:
        ds_src = os.path.join(raw_source, ds)
        ds_dest = os.path.join(base_dir, "data", "raw", ds)
        
        for f in ["label.txt", "source_tweets.txt"]:
            src_file = os.path.join(ds_src, f)
            dest_file = os.path.join(ds_dest, f)
            if os.path.exists(src_file):
                shutil.copy(src_file, dest_file)
                print(f"Copied {ds}/{f}")
                
        tree_src = os.path.join(ds_src, "tree")
        tree_dest = os.path.join(ds_dest, "tree")
        if os.path.exists(tree_src):
            tree_files = os.listdir(tree_src)
            for tf in tree_files:
                shutil.copy(os.path.join(tree_src, tf), os.path.join(tree_dest, tf))
            print(f"Copied {len(tree_files)} tree files for {ds}")

    print("\nPhase 1 directory setup & dataset transfer complete!")

if __name__ == "__main__":
    setup()
