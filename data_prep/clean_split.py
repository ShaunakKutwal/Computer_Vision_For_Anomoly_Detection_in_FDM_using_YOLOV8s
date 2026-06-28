# src/clean_split.py
import os
import shutil
import random
import glob

def clean_split():
    print("="*60)
    print("CLEAN DATASET SPLIT")
    print("="*60)
    
    # First, clear existing split folders
    print("\n🧹 Cleaning existing split folders...")
    for split in ['train', 'val', 'test']:
        for folder in [f'dataset/images/{split}', f'dataset/labels/{split}']:
            if os.path.exists(folder):
                for file in glob.glob(f'{folder}/*'):
                    os.remove(file)
                print(f"  Cleared: {folder}")
    
    # Create fresh folders
    for split in ['train', 'val', 'test']:
        os.makedirs(f'dataset/images/{split}', exist_ok=True)
        os.makedirs(f'dataset/labels/{split}', exist_ok=True)
    
    defects = ['stringing', 'cracking', 'off_platform']
    total_images = 0
    
    for defect in defects:
        print(f"\n Processing {defect}...")
        
        # Get all images for this defect
        img_folder = f'dataset/images/{defect}'
        label_folder = f'dataset/labels/{defect}'
        
        # Get all image files
        images = [f for f in os.listdir(img_folder) 
                 if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        # Sort to ensure consistency
        images.sort()
        
        print(f"  Found {len(images)} images")
        total_images += len(images)
        
        # Shuffle for random split
        random.shuffle(images)
        
        # Calculate split sizes
        total = len(images)
        train_count = int(total * 0.7)
        val_count = int(total * 0.15)
        
        # Split the images
        train_images = images[:train_count]
        val_images = images[train_count:train_count + val_count]
        test_images = images[train_count + val_count:]
        
        print(f"  Train: {len(train_images)}")
        print(f"  Val: {len(val_images)}")
        print(f"  Test: {len(test_images)}")
        
        # Copy files to respective split folders
        for split_name, split_images in [
            ('train', train_images),
            ('val', val_images),
            ('test', test_images)
        ]:
            for img_file in split_images:
                # Copy image
                src_img = os.path.join(img_folder, img_file)
                dst_img = os.path.join(f'dataset/images/{split_name}', f'{defect}_{img_file}')
                shutil.copy2(src_img, dst_img)
                
                # Copy label
                label_file = img_file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
                src_label = os.path.join(label_folder, label_file)
                
                if os.path.exists(src_label):
                    dst_label = os.path.join(f'dataset/labels/{split_name}', f'{defect}_{label_file}')
                    shutil.copy2(src_label, dst_label)
                else:
                    print(f"   Warning: No label for {img_file}")
    
    print("\n" + "="*60)
    print("VERIFICATION:")
    print("="*60)
    
    total_images = 0
    total_labels = 0
    
    for split in ['train', 'val', 'test']:
        images = len(glob.glob(f'dataset/images/{split}/*.jpg'))
        labels = len(glob.glob(f'dataset/labels/{split}/*.txt'))
        total_images += images
        total_labels += labels
        
        print(f"\n{split.upper()}:")
        print(f"  Images: {images}")
        print(f"  Labels: {labels}")
        
        if images == labels:
            print(f"   MATCH")
        else:
            print(f"   MISMATCH: {images - labels} missing labels")
    
    print("\n" + "="*60)
    print(f"TOTAL IMAGES: {total_images}")
    print(f"TOTAL LABELS: {total_labels}")
    print(f"ORIGINAL TOTAL: {311 + 94 + 90} = 495")
    print("="*60)

if __name__ == "__main__":
    clean_split()