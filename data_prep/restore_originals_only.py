# src/restore_originals_only.py
import os
import glob
import shutil

def restore_originals():
    print("="*60)
    print("RESTORING ONLY ORIGINAL IMAGES")
    print("="*60)
    
    defects = ['stringing', 'cracking', 'off_platform']
    total_restored = 0
    
    for defect in defects:
        print(f"\n Processing {defect}...")
        
        # Get all label files (these are your trusted originals)
        label_folder = f'dataset/labels/{defect}'
        if not os.path.exists(label_folder):
            print(f"  No labels folder for {defect}")
            continue
            
        label_files = glob.glob(f'{label_folder}/*.txt')
        print(f"  Found {len(label_files)} trusted labels")
        
        # Create image folder if it doesn't exist
        img_folder = f'dataset/images/{defect}'
        os.makedirs(img_folder, exist_ok=True)
        
        restored = 0
        missing = 0
        
        for label_file in label_files:
            # Get image name from label
            img_name = os.path.basename(label_file).replace('.txt', '.jpg')
            
            # Check multiple possible source locations
            possible_sources = [
                f'dataset/images/{defect}_backup/{img_name}',
                f'backup_images/{defect}/{img_name}',
                f'original_labels_backup/../images/{defect}/{img_name}'
            ]
            
            found = False
            for src in possible_sources:
                if os.path.exists(src):
                    dst = os.path.join(img_folder, img_name)
                    shutil.copy2(src, dst)
                    print(f"   Restored: {img_name}")
                    restored += 1
                    found = True
                    break
            
            if not found:
                print(f"   Missing image for: {img_name}")
                missing += 1
        
        print(f"  Restored: {restored}, Missing: {missing}")
        total_restored += restored
    
    print(f"\n{'='*60}")
    print(f" Total images restored: {total_restored}")
    print("="*60)

if __name__ == "__main__":
    restore_originals()