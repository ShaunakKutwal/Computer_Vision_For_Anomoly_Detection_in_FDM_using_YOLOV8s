# src/merge_curves.py
import cv2
import os
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

def merge_curves():
    """
    Merge all box curve images into a single composite image
    """
    print("="*60)
    print("MERGING BOX CURVE RESULTS")
    print("="*60)
    
    # Path to your training session
    session_path = r'runs\detect\runs\train\training_session'
    
    if not os.path.exists(session_path):
        print(f" Session path not found: {session_path}")
        return
    
    # Find all box curve images
    curve_files = {
        'BoxF1_curve.png': 'F1-Confidence Curve',
        'BoxP_curve.png': 'Precision-Confidence Curve',
        'BoxPR_curve.png': 'Precision-Recall Curve',
        'BoxR_curve.png': 'Recall-Confidence Curve'
    }
    
    # Load images
    images = []
    titles = []
    
    for filename, title in curve_files.items():
        filepath = os.path.join(session_path, filename)
        if os.path.exists(filepath):
            img = cv2.imread(filepath)
            if img is not None:
                # Convert BGR to RGB for matplotlib
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img_rgb)
                titles.append(title)
                print(f" Loaded: {filename}")
            else:
                print(f" Could not read: {filename}")
        else:
            print(f" Not found: {filename}")
    
    if not images:
        print(" No curve images found!")
        return
    
    # Create a grid layout
    n_images = len(images)
    n_cols = 2
    n_rows = (n_images + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    fig.suptitle('Combined Training Curves', fontsize=16, fontweight='bold')
    
    # Flatten axes for easy indexing
    if n_rows == 1:
        axes = [axes]
    axes_flat = []
    for row in axes:
        if isinstance(row, (list, np.ndarray)):
            axes_flat.extend(row)
        else:
            axes_flat.append(row)
    
    # Plot each image
    for i, (img, title) in enumerate(zip(images, titles)):
        axes_flat[i].imshow(img)
        axes_flat[i].set_title(title, fontsize=12)
        axes_flat[i].axis('off')
    
    # Hide unused subplots
    for i in range(len(images), len(axes_flat)):
        axes_flat[i].axis('off')
    
    plt.tight_layout()
    
    # Save merged image
    output_path = os.path.join(session_path, 'merged_curves.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n Merged image saved to: {output_path}")
    
    # Also create a horizontal layout version
    fig_h, axes_h = plt.subplots(1, n_images, figsize=(5*n_images, 4))
    if n_images == 1:
        axes_h = [axes_h]
    
    for i, (img, title) in enumerate(zip(images, titles)):
        axes_h[i].imshow(img)
        axes_h[i].set_title(title, fontsize=10)
        axes_h[i].axis('off')
    
    plt.suptitle('Training Curves - Horizontal Layout', fontsize=14)
    plt.tight_layout()
    
    output_h = os.path.join(session_path, 'merged_curves_horizontal.png')
    plt.savefig(output_h, dpi=300, bbox_inches='tight')
    print(f" Horizontal merged image saved to: {output_h}")
    
    plt.show()
    
    print("\n" + "="*60)
    print("MERGING COMPLETE")
    print("="*60)

def merge_with_confusion():
    """
    Merge box curves with confusion matrix
    """
    print("="*60)
    print("MERGING ALL RESULTS (INCLUDING CONFUSION MATRIX)")
    print("="*60)
    
    session_path = r'runs\detect\runs\train\training_session'
    
    if not os.path.exists(session_path):
        print(f" Session path not found: {session_path}")
        return
    
    # Find all image files
    all_images = []
    
    # Add curve files
    curve_patterns = ['Box*.png', 'confusion*.png']
    for pattern in curve_patterns:
        files = glob.glob(os.path.join(session_path, pattern))
        for file in files:
            img = cv2.imread(file)
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                all_images.append((img_rgb, os.path.basename(file)))
                print(f" Loaded: {os.path.basename(file)}")
    
    if not all_images:
        print(" No images found!")
        return
    
    # Create a grid layout (3 columns)
    n_images = len(all_images)
    n_cols = 3
    n_rows = (n_images + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6*n_rows))
    fig.suptitle('Complete Training Results', fontsize=16, fontweight='bold')
    
    # Flatten axes
    if n_rows == 1:
        axes = [axes]
    axes_flat = []
    for row in axes:
        if isinstance(row, (list, np.ndarray)):
            axes_flat.extend(row)
        else:
            axes_flat.append(row)
    
    # Plot each image
    for i, (img, title) in enumerate(all_images):
        axes_flat[i].imshow(img)
        axes_flat[i].set_title(title.replace('_', ' ').replace('.png', ''), fontsize=10)
        axes_flat[i].axis('off')
    
    # Hide unused subplots
    for i in range(len(all_images), len(axes_flat)):
        axes_flat[i].axis('off')
    
    plt.tight_layout()
    
    output_path = os.path.join(session_path, 'complete_results.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n Complete results saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    print("\n CURVE MERGER MENU")
    print("="*40)
    print("1. Merge only box curves")
    print("2. Merge all results (including confusion matrix)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        merge_curves()
    elif choice == '2':
        merge_with_confusion()
    else:
        print("Invalid choice")