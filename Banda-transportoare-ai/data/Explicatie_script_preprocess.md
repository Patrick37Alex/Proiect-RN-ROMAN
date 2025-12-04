Explicație Detaliată – “preprocess_simple.py”
Acest cod este un script de preprocesare a datelor. Scopul său este să ia un set de imagini brute și hărți termice (heatmaps), să le redimensioneze la o mărime standard și să le împartă aleatoriu în trei seturi: Train, Validation și Test.
1. Importuri
Aceste linii încarcă modulele necesare pentru lucrul cu fișiere, directoare, imagini și aleatoriu:
import os
import random
import shutil
from pathlib import Path
from PIL import Image
• **os** – interacțiune cu sistemul de fișiere.
• **random** – generare de valori și ordonări aleatorii.
• **shutil** – copiere fișiere.
• **Path** – manipulare modernă a căilor.
• **PIL.Image** – încărcare/redimensionare imagini.
2. Definirea directoarelor datasetului
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

• **BASE_DIR** – folderul principal al datasetului.
• **RAW_DIR** – folderul care conține imaginile brute și heatmap-urile.
• **OUT_TRAIN_IMG/VAL/TEST** – directoare pentru imaginile procesate.
• **OUT_TRAIN_HM/VAL/TEST** – directoare pentru heatmap-uri.
3. Parametrii de procesare
IMG_SIZE = (200, 200)
VAL_RATIO = 0.15
TEST_RATIO = 0.15
• **IMG_SIZE** – toate imaginile sunt redimensionate la 200×200.
• **VAL_RATIO / TEST_RATIO** – procentele pentru împărțirea datasetului.
4. Funcția ensure_dirs()
def ensure_dirs():
    for d in [OUT_TRAIN_IMG, OUT_VAL_IMG, OUT_TEST_IMG,
              OUT_TRAIN_HM, OUT_VAL_HM, OUT_TEST_HM]:
        d.mkdir(parents=True, exist_ok=True)
Creează toate directoarele necesare pentru dataset
parents=True: Dacă folderul data/train nu există, îl creează și pe el înainte de a crea images.
exist_ok=True: Dacă folderul există deja, nu dă eroare (doar continuă).
5. Funcția resize_and_save()
def resize_and_save(src, dst, size=(200, 200), mode="RGB"):
    img = Image.open(src)   # Deschide imaginea de la sursă
    img = img.convert(mode) # Convertește (ex: în color RGB sau alb-negru L)
    img = img.resize(size)  # Redimensionează la 200x200
    img.save(dst)           # Salvează rezultatul la destinație
6. Funcția main()
def main():
    ensure_dirs()

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
        src_hm = HEATMAPS_DIR / fname

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

    for aux in ["sensors.csv", "metadata.json"]:
        src = RAW_DIR / aux
        if src.exists():
            shutil.copy(src, BASE_DIR / aux)
            print(f"Copiat {aux} în data/{aux}")

    print("Gata. Imaginile & heatmap-urile sunt în:")
    print("  data/train, data/validation, data/test")
Aceasta este logica principală a scriptului:
• Creează directoarele.
• Listează imaginile brute.
• Amestecă random indicii cu seed fix (deterministic).
• Împarte imaginile în train/validation/test.
• Verifică dacă există heatmap aferent imaginii.
• Redimensionează și salvează în directoarele potrivite.
• Copiază fișierele auxiliare sensors.csv și metadata.json.
7. Execuția scriptului
if __name__ == "__main__":
    main()
Această condiție asigură că funcția **main()** rulează doar atunci când fișierul este executat direct, nu importat.
