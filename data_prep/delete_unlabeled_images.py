# src/delete_unlabeled_images.py
import os
import glob
import shutil

def delete_unlabeled_images():
    """
    Delete all images that don't have matching label files
    """
    print("="*70)
    print("DELETE IMAGES WITHOUT LABELS")
    print("="*70)
    
    defects = ['stringing', 'cracking', 'off_platform']
    total_deleted = 0
    total_kept = 0
    
    # Ask for confirmation
    print("\n  WARNING: This will DELETE images that don't have matching label files!")
    print("This action CANNOT be undone!")
    confirm = input("\nType 'YES' to confirm deletion: ")
    
    if confirm != 'YES':
        print("Operation cancelled.")
        return
    
    # Ask about backup
    backup = input("\nCreate backup of deleted files? (y/n): ").lower()
    
    for defect in defects:
        print(f"\n Processing {defect.upper()}...")
        
        img_folder = f'dataset/images/{defect}'
        label_folder = f'dataset/labels/{defect}'
        
        if not os.path.exists(img_folder):
            print(f"   Image folder not found: {img_folder}")
            continue
        
        # Get all images
        images = glob.glob(f'{img_folder}/*.jpg') + glob.glob(f'{img_folder}/*.jpeg') + glob.glob(f'{img_folder}/*.png')
        
        if not images:
            print(f"  No images found")
            continue
        
        # Get all label filenames (without extension)
        if os.path.exists(label_folder):
            labels = glob.glob(f'{label_folder}/*.txt')
            label_names = {os.path.splitext(os.path.basename(f))[0] for f in labels}
        else:
            print(f"   No labels folder found! All images will be deleted.")
            label_names = set()
        
        print(f"  Found {len(images)} images, {len(label_names)} labels")
        
        # Create backup folder if needed
        if backup == 'y':
            backup_folder = f'dataset/backup_deleted_{defect}'
            os.makedirs(backup_folder, exist_ok=True)
            print(f"  Backup folder: {backup_folder}")
        
        # Check each image
        deleted = 0
        kept = 0
        
        for img_path in images:
            img_name = os.path.basename(img_path)
            img_without_ext = os.path.splitext(img_name)[0]
            
            if img_without_ext not in label_names:
                # Image has no label - DELETE IT
                if backup == 'y':
                    # Move to backup instead of delete
                    shutil.move(img_path, os.path.join(backup_folder, img_name))
                    print(f"   Moved to backup: {img_name}")
                else:
                    # Permanently delete
                    os.remove(img_path)
                    print(f"   Deleted: {img_name}")
                deleted += 1
            else:
                kept += 1
        
        print(f"\n   {defect} summary:")
        print(f"     Kept: {kept} images (have labels)")
        print(f"     Deleted: {deleted} images (no labels)")
        
        total_deleted += deleted
        total_kept += kept
    
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f" Kept: {total_kept} images (have labels)")
    print(f" Deleted: {total_deleted} images (no labels)")
    print("="*70)

def quick_delete_no_backup():
    """
    Quick delete without backup (no questions asked after initial confirmation)
    """
    print("="*70)
    print("QUICK DELETE - NO BACKUP")
    print("="*70)
    
    defects = ['stringing', 'cracking', 'off_platform']
    total_deleted = 0
    
    print("\n  WARNING: This will PERMANENTLY DELETE all images without labels!")
    print("No backup will be created.")
    confirm = input("\nType 'YES' to confirm permanent deletion: ")
    
    if confirm != 'YES':
        print("Operation cancelled.")
        return
    
    for defect in defects:
        print(f"\n Processing {defect.upper()}...")
        
        img_folder = f'dataset/images/{defect}'
        label_folder = f'dataset/labels/{defect}'
        
        if not os.path.exists(img_folder):
            continue
        
        images = glob.glob(f'{img_folder}/*.jpg')
        
        if os.path.exists(label_folder):
            labels = glob.glob(f'{label_folder}/*.txt')
            label_names = {os.path.splitext(os.path.basename(f))[0] for f in labels}
        else:
            label_names = set()
        
        deleted = 0
        for img_path in images:
            img_name = os.path.basename(img_path)
            img_without_ext = os.path.splitext(img_name)[0]
            
            if img_without_ext not in label_names:
                os.remove(img_path)
                deleted += 1
                print(f"   Deleted: {img_name}")
        
        print(f"  Deleted {deleted} images from {defect}")
        total_deleted += deleted
    
    print("\n" + "="*70)
    print(f" COMPLETE: Deleted {total_deleted} images")
    print("="*70)

def preview_only():
    """
    Preview what would be deleted without actually deleting
    """
    print("="*70)
    print("PREVIEW - NO DELETIONS")
    print("="*70)
    
    defects = ['stringing', 'cracking', 'off_platform']
    total_unlabeled = 0
    
    for defect in defects:
        print(f"\n {defect.upper()}:")
        
        img_folder = f'dataset/images/{defect}'
        label_folder = f'dataset/labels/{defect}'
        
        if not os.path.exists(img_folder):
            print(f"  No images folder")
            continue
        
        images = glob.glob(f'{img_folder}/*.jpg')
        labels = glob.glob(f'{label_folder}/*.txt') if os.path.exists(label_folder) else []
        
        img_names = {os.path.splitext(os.path.basename(f))[0] for f in images}
        label_names = {os.path.splitext(os.path.basename(f))[0] for f in labels}
        
        unlabeled = img_names - label_names
        
        if unlabeled:
            print(f"  Found {len(unlabeled)} images without labels:")
            for i, img in enumerate(sorted(list(unlabeled))[:10]):
                print(f"    {i+1}. {img}.jpg")
            if len(unlabeled) > 10:
                print(f"    ... and {len(unlabeled)-10} more")
            total_unlabeled += len(unlabeled)
        else:
            print(f"   All images have labels")
    
    print("\n" + "="*70)
    print(f" TOTAL: {total_unlabeled} images would be deleted")
    print("="*70)

if __name__ == "__main__":
    print("\n  IMAGE CLEANUP MENU")
    print("="*40)
    print("1. Preview only (see what would be deleted)")
    print("2. Delete with backup (move to backup folder)")
    print("3. Quick delete (permanent, no backup)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        preview_only()
    elif choice == '2':
        delete_unlabeled_images()
    elif choice == '3':
        quick_delete_no_backup()
    else:
        print("Invalid choice")