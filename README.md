# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale
**Proiect:** *Bandă transportoare – Detecție anomalii & mapare distribuție greutate*  
**Disciplina:** Rețele Neuronale – FIIR / UPB  
**Student:** Roman Alexandru Patrick  
**Data:** 20.11.2025

---

## 0. Introducere
Această etapă documentează analiza și pregătirea setului de date necesar instruirii modelului AI utilizat pentru:
- detecția anomaliilor pe banda transportoare  
- maparea distribuției greutății  
Modelul folosește CNN pentru detecție și UNet pentru segmentare.

---

## 1. Structura Repository-ului (Etapa 3)
```
banda-transportoare-ai/
├── README.md
├── docs/
│   ├── dataset_description.md
│   ├── diagrams/
│   └── examples/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── train/
│   ├── validation/
│   └── test/
├── src/
│   ├── preprocessing/
│   ├── data_acquisition/
│   └── ai_models/
├── config/
└── requirements.txt
```

---

## 2. Descrierea Setului de Date

### 2.1 Sursa datelor
- Imagini RGB/IR  
- Date senzori (greutate, vibrații)  
- Metadate: timestamp, product_id, speed_belt  

### 2.2 Obiecte transportate
- cutii carton, componente metalice/plastice  
- recipiente (sticle, doze), produse electronice  

### 2.3 Caracteristici
| Tip | Format | Descriere |
|-----|--------|-----------|
| Imagini RGB | JPG/MP4 | detecție vizuală |
| Imagini IR | JPG | analiza deformărilor |
| Senzori | CSV/JSON | greutate & vibrații |
| Metadate | JSON | info suplimentară |

---

## 3. Analiza Exploratorie a Datelor (EDA)
- statistici descriptive  
- verificare iluminare și claritate  
- analiză vibrații (rms, fft peaks)  
- class imbalance pentru anomalii  

---

## 4. Preprocesarea Datelor

### 4.1 Curățare
- eliminare cadre blur  
- corectare valori lipsă  
- filtrare vibrații  

### 4.2 Transformare
- resize imagini  
- normalizare  
- augmentare (rotire, luminozitate, deformări sintetice)  
- generare heatmap greutate  

### 4.3 Split
Train 70% / Val 15% / Test 15%  
Principii: stratificare, fără leakage, normalizare pe train.

### 4.4 Salvare
- imagini procesate → data/processed  
- senzori → data/processed/sensors  
- heatmap → PNG/NumPy  
- config → config/preprocessing.json  

---

## 5. Intrări / Ieșiri

### Intrări
- Imagini RGB/IR  
- Date senzori  
- Timestamp & ID  

### Ieșiri
- alerte JSON  
- heatmap-uri  
- clasificări obiecte  
- rapoarte CSV/PDF  

---

## 6. Tehnologii utilizate
- PyTorch, OpenCV, NumPy, Pandas, TensorRT  
- Flask pentru UI  
- Jetson Nano / Orin / Raspberry Pi 5  
- SQLite / TimescaleDB  

---

## 7. Stare Etapă
- [x] Structură repo  
- [x] Analiză dataset  
- [ ] Preprocesare  
- [ ] Structură train/val/test  
- [ ] Upload date finale

