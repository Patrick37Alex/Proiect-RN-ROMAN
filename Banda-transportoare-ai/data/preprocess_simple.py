import os
import random
import shutil
from pathlib import Path
from PIL import Image

BASE_DIR = Path("data")
RAW_DIR = BASE_DIR / "raw"
IMAGES_DIR = RAW_DIR / "images"
HEATMAPS_DIR = RAW_DIR / "heatmaps"

OUT_TRAIN_IMG = BASE_DIR / "train" / "images"
OUT_VAL_IMG = BASE_DIR / "validation" / "images"
OUT_TEST_IMG = BASE_DIR / "test" / "images"

OUT_TRAIN_HM = BASE_DIR / "train" / "heatmaps"
OUT_VAL_HM = BASE_DIR / "validation" / "heatmaps"
OUT_TEST_HM = BASE_DIR / "test" / "heatmaps"

IMG_SIZE = (200, 200)
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def ensure_dirs():
    for d in [OUT_TRAIN_IMG, OUT_VAL_IMG, OUT_TEST_IMG,
              OUT_TRAIN_HM, OUT_VAL_HM, OUT_TEST_HM]:
        d.mkdir(parents=True, exist_ok=True)

def resize_and_save(src, dst, size=(200, 200), mode="RGB"):
    img = Image.open(src)
    img = img.convert(mode)
    img = img.resize(size)
    img.save(dst)

def main():
    ensure_dirs()
    
    # listăm imaginile
    files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    files.sort()
    n = len(files)
    print(f"Am găsit {n} imagini brute.")

    idx = list(range(n))
    random.seed(42)
    random.shuffle(idx)

    n_test = max(1, int(TEST_RATIO * n))
    n_val = max(1, int(VAL_RATIO * n))

    test_idx = set(idx[:n_test])
    val_idx = set(idx[n_test:n_test + n_val])

    for i, fname in enumerate(files):
        src_img = IMAGES_DIR / fname
        src_hm = HEATMAPS_DIR / fname  # presupunem același nume

        if not src_hm.exists():
            print(f"[WARN] Nu există heatmap pentru {fname}, sar peste.")
            continue

        if i in test_idx:
            img_out_dir = OUT_TEST_IMG
            hm_out_dir = OUT_TEST_HM
        elif i in val_idx:
            img_out_dir = OUT_VAL_IMG
            hm_out_dir = OUT_VAL_HM
        else:
            img_out_dir = OUT_TRAIN_IMG
            hm_out_dir = OUT_TRAIN_HM

        dst_img = img_out_dir / fname
        dst_hm = hm_out_dir / fname

        resize_and_save(src_img, dst_img, IMG_SIZE, mode="RGB")
        resize_and_save(src_hm, dst_hm, IMG_SIZE, mode="L")

    # copiem sensors.csv și metadata.json în data/
    for aux in ["sensors.csv", "metadata.json"]:
        src = RAW_DIR / aux
        if src.exists():
            shutil.copy(src, BASE_DIR / aux)
            print(f"Copiat {aux} în data/{aux}")

    print("Gata. Imaginile & heatmap-urile sunt în:")
    print("  data/train, data/validation, data/test")

if __name__ == "__main__":
    main()
