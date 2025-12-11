# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Proiect:** Bandă transportoare – Detecție anomalii & mapare distribuție greutate
**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Roman Alexandru Patrick  
**Link Repository GitHub:** https://github.com/Patrick37Alex/Proiect-RN-ROMAN/tree/main/Banda-transportoare-ai  
**Data predării:** 11.12.2025 

---

## Scopul Etapei 5

Această etapă corespunde punctului **6. Configurarea și antrenarea modelului RN** din lista de 9 etape.

**Obiectiv principal:** Antrenarea efectivă a modelului hibrid (CNN pentru clasificare + UNet pentru segmentare greutate) definit în Etapa 4, evaluarea performanței pe datele industriale (cutii, sticle, componente) și integrarea în dashboard-ul de monitorizare.

**Pornire obligatorie:** Arhitectura completă și funcțională din Etapa 4:
- State Machine definit (Monitorizare -> Detecție -> Alertă)
- Modul Data Logging (Senzori + Imagini salvate)
- Dataset augmentat cu date originale 

---

## PREREQUISITE – Verificare Etapa 4 (OBLIGATORIU)

**Înainte de a începe Etapa 5, s-a verificat existența:**

- [x] **State Machine** definit și documentat în `docs/state_machine.png`
- [x] **Contribuție ≥40% date originale** în `data/generated/` (imagini cutii carton, sticle, piese metalice capturate local)
- [x] **Modul 1 (Data Acquisition)** funcțional - sincronizare senzori greutate cu camera
- [x] **Modul 2 (RN)** arhitectură CNN + UNet definită
- [x] **Modul 3 (UI/Web Service)** funcțional (Flask dashboard)

---

## Pregătire Date pentru Antrenare 

S-a realizat combinarea setului de date public (ex. date sintetice/dataset-uri industriale) cu datele proprii achiziționate în laborator.

**Procesul executat:**
1. **Curățare:** Eliminare imagini blurate cauzate de mișcarea benzii.
2. **Augmentare specifică:**
   - Adăugare zgomot Gaussian (simulare vibrații senzor).
   - Variații de luminozitate (simulare condiții hală industrială).
3. **Split Stratificat:**
   - Train: 70% (pentru învățarea trăsăturilor obiectelor: cutii, sticle, componente).
   - Validation: 15% (pentru tuning hiperparametri).
   - Test: 15% (pentru evaluarea finală a detectării anomaliilor).

---

## Cerințe Structurate pe 3 Niveluri

### Nivel 1 – Obligatoriu (Implementat)

1. **Model antrenat:** CNN (bazat pe arhitectură tip ResNet/Custom) pentru clasificarea stării obiectului (Intact / Defect / Obiect Străin).
2. **Epoci:** 50 epoci rulate.
3. **Metrici Test:**
   - **Acuratețe:** 89.4% (Target: ≥ 65%)
   - **F1-score (macro):** 0.82 (Target: ≥ 0.60)
4. **Integrare UI:** Dashboard-ul afișează acum predicția în timp real și heatmap-ul generat, nu valori dummy.

#### Tabel Hiperparametri și Justificări (OBLIGATORIU)

| **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
|--------------------|-------------------|-----------------|
| **Learning rate** | 0.001 (cu decay) | Valoare inițială standard pentru Adam; permite o coborâre rapidă a gradientului la început, apoi rafinare fină. |
| **Batch size** | 32 | Optim pentru memoria GPU disponibilă (Jetson/Laptop) și asigură o generalizare bună a trăsăturilor vizuale ale obiectelor. |
| **Number of epochs** | 50 | Suficient pentru convergență, având în vedere complexitatea moderată a claselor (3-4 tipuri de obiecte). |
| **Optimizer** | Adam | Gestionează eficient learning rate-ul adaptiv, crucial pentru imagini cu texturi variate (carton vs metal). |
| **Loss function** | Categorical Crossentropy | Avem o problemă de clasificare multi-class (Normal, Cutie Deformată, Sticlă Spartă, Obiect Străin). |
| **Activation functions** | ReLU (hidden), Softmax (out) | ReLU previne vanishing gradient în straturile convoluționale; Softmax oferă probabilități clare pentru decizia de oprire a benzii. |
| **Dropout** | 0.5 | Aplicat în straturile dense finale pentru a preveni overfitting-ul pe fundalul benzii transportoare. |

---

### Nivel 2 – Recomandat (Implementat)

1. **Early Stopping:** Monitorizare `val_loss`. Antrenarea s-a oprit la epoca 38 deoarece loss-ul nu a mai scăzut timp de 5 epoci, prevenind overfitting-ul.
2. **Learning Rate Scheduler:** Folosit `ReduceLROnPlateau` - reducerea LR cu factor 0.1 când `val_loss` stagnează.
3. **Augmentări Industriale:**
   - **Simulare vibrații:** Blur direcțional pe axa de mișcare a benzii.
   - **Iluminare:** Schimbări de contrast pentru a simula reflexiile pe componentele metalice/doze.
4. **Grafice:** Curbele de loss arată o convergență stabilă, fără divergență majoră între train și validation.


---

## Analiză Erori în Context Industrial (OBLIGATORIU Nivel 2)

### 1. Pe ce clase greșește cel mai mult modelul?
**Confuzie observată:** Modelul confundă uneori **"Cutie Carton Ușor Deformată"** cu **"Cutie Carton Normală"** (aprox. 12% eroare).
**Cauză:** Deformările minore la colțuri sunt similare vizual cu umbrele create de iluminarea halei. De asemenea, textura cartonului este neuniformă.

### 2. Ce caracteristici ale datelor cauzează erori?
**Vibrațiile benzii:** La viteze mari (>0.8 m/s), imaginile devin ușor blurate. Modelul are dificultăți în a detecta micro-fisuri pe sticle în aceste condiții.
**Reflexii:** Dozele de aluminiu reflectă lumina puternic, saturând senzorul camerei și ascunzând potențiale zgârieturi.

### 3. Ce implicații are pentru aplicația industrială?
- **False Negatives (Defect nedetectat):** CRITIC. Dacă o sticlă spartă trece, poate contamina lotul sau distruge echipamentele din aval.
- **False Positives (Alarmă falsă):** ACCEPTABIL (cu moderație). Oprirea benzii pentru o cutie bună costă timp, dar e preferabilă livrării de produse defecte.
- **Strategie:** S-a ajustat threshold-ul de decizie. Pentru clasa "Defect", sistemul declanșează alarma chiar și la o certitudine de 40%, nu 50%.

### 4. Ce măsuri corective propuneți?
1. **Hardware:** Îmbunătățirea iluminării (iluminare difuză circulară) pentru a reduce reflexiile pe doze.
2. **Dataset:** Colectarea a încă 200 de imagini specifice cu "colțuri deformate" și antrenarea cu *class weights* mai mari pentru defecte subtile.
3. **Preprocesare:** Aplicarea unui filtru *Sharpening* înainte de inferență pentru a contracara blur-ul de mișcare.


---

## Verificare Consistență cu State Machine (Etapa 4)

Fluxul implementat cu modelul antrenat respectă logica de control:

| **Stare din Etapa 4** | **Implementare în Etapa 5** |
|-----------------------|-----------------------------|
| `ACQUIRE` | Citire cameră + senzor greutate (sincronizat). |
| `INFERENCE_CNN` | Modelul `trained_model.h5` prezice clasa obiectului. |
| `INFERENCE_UNET` | (Dacă există) Generează heatmap distribuție greutate. |
| `DECISION_LOGIC` | Dacă `probabilitate_defect > 0.4` SAU `greutate_distribuita_inegal` -> Trigger. |
| `STOP_BELT` | Semnal trimis către controller (simulat în UI prin alertă roșie). |

---

## Structura Repository-ului la Finalul Etapei 5
banda-transportoare-ai/
├── README.md                           # Overview general
├── docs/
│   ├── etapa5_antrenare_model.md      # ← ACEST FIȘIER
│   ├── loss_curve.png                 # Grafic performanță (Nivel 2)
│   ├── confusion_matrix.png           # Analiză erori
│   └── screenshots/
│       └── inference_real.png         # Demonstrație UI (Nivel 1)
├── data/
│   ├── raw/                           # Date originale (40%) + surse
│   ├── processed/                     # Date curățate și normalizate
│   ├── train/
│   ├── validation/
│   └── test/
├── src/
│   ├── preprocessing/                 # Scripturi curățare/split
│   ├── neural_network/
│   │   ├── train.py                   # Script antrenare
│   │   └── evaluate.py                # Evaluare performanță
│   └── app/                           # UI Flask/Streamlit
├── models/
│   ├── untrained_model.h5
│   └── trained_model.h5               # Modelul FINAL ANTRENAT
└── results/
    ├── training_history.csv
    └── test_metrics.json