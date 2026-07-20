# Heart Anatomy and the Cardiac Conduction System

## 1. Introduction

The human heart is a marvel of biological engineering — a muscular organ roughly the size of a fist, weighing approximately 250–350 grams, that beats over 100,000 times per day to pump roughly 7,500 liters of blood through approximately 100,000 kilometers of vasculature. For engineers designing implantable pacemaker chips (iPACE-CHIP), a deep understanding of cardiac anatomy and its intrinsic electrical conduction system is not merely academic — it is foundational. The pacemaker chip must interface with, replicate, or supplement the heart's own electrical system, and doing so requires intimate knowledge of the structures it aims to support.

This chapter provides a comprehensive treatment of cardiac anatomy, the specialized conduction system, cardiac muscle ultrastructure, and the electrophysiological principles that govern the heartbeat. This knowledge forms the bedrock upon which all subsequent chapters on pacemaker design are built.

---

## 2. Gross Anatomy of the Heart

### 2.1 Position and Orientation

The heart resides in the mediastinum, nestled between the lungs, posterior to the sternum, and anterior to the vertebral column. Its long axis (base-to-apex) is oriented obliquely, running from the right posterior-superior direction to the left anterior-inferior direction. The apex of the heart normally points toward the left hip, while the base (where the great vessels emerge) is oriented superiorly and posteriorly.

Key anatomical landmarks:

| Landmark | Description | Clinical Relevance |
|----------|-------------|-------------------|
| **Right border** | Formed by the right atrium | Leads placed via right subclavian vein enter the RA |
| **Left border** | Formed by the left ventricle | LV lead positioning for CRT |
| **Inferior border** | Formed mainly by the right ventricle | Diaphragmatic stimulation risk |
| **Superior border (base)** | Great vessels: SVC, aorta, PA | Venous access for lead implantation |
| **Apex** | Formed by the left ventricle | RV apex is traditional pacing site |

### 2.2 The Pericardium

The heart is enclosed in a double-layered fibroserous sac called the pericardium:

- **Fibrous pericardium**: The outer layer, a tough, inelastic connective tissue layer that anchors the heart to the diaphragm, great vessels, and sternum. It prevents acute cardiac dilation.
- **Serous pericardium**: A thinner, inner layer consisting of:
  - **Parietal layer**: Lines the inner surface of the fibrous pericardium
  - **Visceral layer (epicardium)**: Covers the outer surface of the heart
  - **Pericardial cavity**: Contains 15–50 mL of serous fluid that reduces friction during cardiac cycles

The pericardium has direct relevance to pacemaker implantation. During device placement, the lead must traverse the pericardial space (via the venous system and into the cardiac chambers). Pericardial effusion, though rare during implantation, is a recognized complication that can lead to cardiac tamponade.

### 2.3 Heart Chambers

The heart contains four chambers — two superior receiving chambers (atria) and two inferior pumping chambers (ventricles) — separated by the interatrial and interventricular septa.

#### 2.3.1 Right Atrium (RA)

The right atrium receives deoxygenated blood from the systemic circulation via three veins:

- **Superior vena cava (SVC)**: Drains blood from the head, neck, upper limbs, and thorax
- **Inferior vena cava (IVC)**: Drains blood from the abdomen, pelvis, and lower limbs
- **Coronary sinus**: Drains myocardial venous blood

The RA has three anatomical subdivisions:

1. **Venous part (sinus venarum)**: Derived embryologically from the sinus venosus; smooth-walled; contains the openings of the SVC and IVC
2. **Anterior part (auricle)**: A muscular, trabeculated appendage that overlaps the aortic root; contains pectinate muscles
3. **Septal part**: Contains the fossa ovalis (remnant of the foramen ovale)

**Clinical significance for pacing**: The right atrium is the primary site for atrial lead placement. The lateral wall of the RA appendage is the preferred site for atrial lead fixation due to its accessibility and lower perforation risk. The SA node, located at the junction of the SVC and RA, is the natural pacemaker of the heart.

#### 2.3.2 Right Ventricle (RV)

The right ventricle receives blood from the RA through the tricuspid valve and pumps it into the pulmonary artery through the pulmonary valve. It is crescent-shaped in cross-section, wrapping around the left ventricle.

Internal structures include:

- **Trabeculae carneae**: Irregular muscular ridges on the internal surface
- **Papillary muscles**: Three muscles (anterior, posterior, septal) that anchor the tricuspid valve chordae tendineae
- **Moderator band (septomarginal trabecula)**: Contains part of the right bundle branch; connects the interventricular septum to the base of the anterior papillary muscle
- **Conus arteriosus (infundibulum)**: The smooth, funnel-shaped outflow tract leading to the pulmonary valve

Wall thickness: 3–5 mm (significantly thinner than the LV)

**Pacing relevance**: The RV apex is the most traditional and historically common site for ventricular lead placement. The RV septum is increasingly favored as an alternative site to provide more physiological activation. Lead perforation of the thin RV wall is a recognized complication.

#### 2.3.3 Left Atrium (LA)

The left atrium receives oxygenated blood from the lungs via four pulmonary veins (two from each lung). It is smaller in volume than the RA but has a thicker wall (approximately 3 mm).

Internal features:

- **Smooth posterior wall**: Derived from incorporation of the pulmonary veins
- **Left atrial appendage (LAA)**: A small, ear-shaped muscular extension; common site of thrombus formation in atrial fibrillation
- **Interatrial septum**: Visible from the LA side as a fossa; important for transseptal catheter procedures

#### 2.3.4 Left Ventricle (LV)

The left ventricle is the most muscular chamber, with a wall thickness of 12–15 mm (approximately three times that of the RV). It receives oxygenated blood from the LA through the mitral (bicuspid) valve and pumps it into the aorta through the aortic valve.

Internal structures:

- **Two large papillary muscles** (anterolateral and posteromedial): Anchor the mitral valve via chordae tendineae
- **Trabeculae carneae**: Less prominent than in the RV
- **Smooth outflow tract (aortic vestibule)**: Superior portion leading to the aortic valve

The LV generates systemic blood pressure (typically 120 mmHg systolic) and must generate approximately 5–6 times the pressure of the RV, which explains its significantly greater wall thickness.

### 2.4 Heart Valves

The heart contains four valves that ensure unidirectional blood flow:

| Valve | Location | Type | Orifice Diameter | Opening Mechanism |
|-------|----------|------|-----------------|-------------------|
| **Tricuspid** | RA → RV | Atrioventricular (AV) | 4–5 cm² | AV pressure gradient; annulus contraction |
| **Mitral (Bicuspid)** | LA → LV | Atrioventricular (AV) | 4–6 cm² | AV pressure gradient; annulus contraction |
| **Pulmonary** | RV → PA | Semilunar | 2.5–3.5 cm² | RV pressure exceeds PA diastolic pressure |
| **Aortic** | LV → Aorta | Semilunar | 3.0–4.0 cm² | LV pressure exceeds aortic diastolic pressure |

The AV valves (tricuspid and mitral) are anchored by chordae tendineae to papillary muscles, which prevent valve prolapse during systole. The semilunar valves (pulmonary and aortic) have pocket-like cusps that fill with blood during diastole, sealing the valve.

**Relevance to pacing**: Valve function depends on coordinated electrical activation and mechanical contraction. Abnormal pacing (e.g., RV apex pacing creating dyssynchronous activation) can impair tricuspid valve function, potentially causing tricuspid regurgitation. This is one reason why physiological pacing and His-bundle/Left Bundle Branch Area Pacing (LBBAP) have gained interest.

---

## 3. The Cardiac Conduction System

The cardiac conduction system is a specialized network of modified cardiac muscle cells that generates and propagates electrical impulses, coordinating the rhythmic contraction of the heart. This system is the direct target and reference for pacemaker technology.

### 3.1 Overview of the Conduction Pathway

```
SA Node (60-100 bpm)
    │
    ├── Internodal pathways (anterior, middle, posterior)
    ├── Bachmann's bundle (to left atrium)
    │
    ▼
Atrial Myocardium (contraction)
    │
    ▼
AV Node (40-60 bpm)
    │
    ▼
Bundle of His
    │
    ├── Right Bundle Branch
    │       │
    │       ▼
    │   Purkinje Fibers → Right Ventricular Myocardium
    │
    └── Left Bundle Branch
            │
            ├── Left Anterior Fascicle
            │       │
            │       ▼
            │   Purkinje Fibers → Anterolateral LV Wall
            │
            └── Left Posterior Fascicle
                    │
                    ▼
                Purkinje Fibers → Posteroinferior LV Wall
```

### 3.2 Sinoatrial (SA) Node

The SA node is the primary pacemaker of the heart, located at the junction of the SVC and the right atrium, subepicardially, along the sulcus terminalis. It is approximately 15 mm long and 5 mm wide, spindle-shaped, and contains approximately 10,000–20,000 specialized cells.

**Key properties:**

- **Intrinsic rate**: 60–100 beats per minute (bpm)
- **Dominance**: Its rate is faster than all other pacemaker sites, so it normally suppresses all subsidiary pacemakers through a mechanism called overdrive suppression
- **Blood supply**: Primarily from the SA nodal artery (which arises from the right coronary artery in 60% of individuals, or from the left circumflex artery in 40%)
- **Innervation**: Richly innervated by both sympathetic (T1–T4) and parasympathetic (vagus nerve, CN X) fibers
- **Response to autonomic tone**: Vagal stimulation decreases heart rate (negative chronotropy); sympathetic stimulation increases heart rate (positive chronotropy)

**Histological composition:**

- **P cells (pacemaker cells)**: Small, pale-staining cells with few myofibrils and organelles; responsible for impulse generation
- **T cells (transitional cells)**: Intermediate cells that connect P cells to the working atrial myocardium; provide transitional conduction
- **Fibroblasts and collagen**: The SA node has a high fibrous tissue content (approximately 60–70% of nodal volume), which electrically isolates the node from the surrounding atrial myocardium, allowing it to fire independently

**Clinical significance**: Dysfunction of the SA node is the most common indication for permanent pacemaker implantation (sick sinus syndrome). The SA node's location and blood supply make it vulnerable to ischemic injury (right coronary artery occlusion), surgical trauma, and fibrotic degeneration with aging.

### 3.3 Internodal Pathways and Bachmann's Bundle

Three internodal pathways conduct impulses from the SA node to the AV node:

1. **Anterior (Bachmann's) pathway**: Runs anteriorly along the interatrial septum; gives off Bachmann's bundle, which conducts to the left atrium, enabling coordinated biatrial depolarization
2. **Middle (Wenckebach's) pathway**: Runs along the posterior aspect of the crista terminalis
3. **Posterior (Thorel's) pathway**: Runs along the posterior wall of the right atrium

These pathways contain specialized conducting cells (similar to Purkinje fibers but smaller) embedded within the atrial myocardium. They ensure rapid and coordinated atrial activation, which is essential for efficient atrial contraction ("atrial kick") that contributes 15–30% of ventricular filling.

**Pacing relevance**: Loss of coordinated atrial activation (as in atrial fibrillation) eliminates atrial kick, reducing cardiac output by 15–30%. Dual-chamber pacemakers (DDD mode) aim to preserve AV synchrony and atrial contribution to ventricular filling.

### 3.4 Atrioventricular (AV) Node

The AV node is located in the posterior-inferior region of the interatrial septum, within the triangle of Koch, bounded by:
- The tendon of Todaro (posteriorly)
- The tricuspid valve annulus (anteriorly)
- The orifice of the coronary sinus (posteriorly)

**Key properties:**

- **Intrinsic rate**: 40–60 bpm (if the SA node fails)
- **Critical function — AV delay**: The AV node introduces a physiological delay of approximately 120–200 milliseconds between atrial and ventricular depolarization. This delay allows:
  - Complete atrial contraction before ventricular systole
  - Optimal ventricular filling ("atrial kick")
  - Time for the ventricles to relax and fill
- **Decremental conduction**: The AV node exhibits a unique property where faster atrial rates lead to progressively slower conduction through the node (decremental conduction). This acts as a protective "gatekeeper" mechanism, preventing excessively rapid atrial rates (e.g., atrial flutter at 300 bpm) from being conducted 1:1 to the ventricles.
- **Vulnerable to ischemia**: The AV node is typically supplied by the AV nodal artery (a branch of the right coronary artery in 85–90% of cases)

**Dual-pathway physiology**: The AV node contains two functionally distinct pathways:
- **Fast pathway (β pathway)**: Faster conduction, longer refractory period
- **Slow pathway (α pathway)**: Slower conduction, shorter refractory period

This dual-pathway model is the substrate for AV nodal reentrant tachycardia (AVNRT), the most common form of paroxysmal supraventricular tachycardia.

**Clinical significance for pacing**: 
- In complete heart block (3rd-degree AV block), the AV node fails to conduct any impulses from the atria to the ventricles, necessitating pacemaker implantation
- His-bundle pacing (HBP) and Left Bundle Branch Area Pacing (LBBAP) are emerging pacing modalities that target structures immediately distal to the AV node, aiming to preserve the native conduction system and provide more physiological ventricular activation

### 3.5 Bundle of His

The Bundle of His is a slender (approximately 1–2 mm diameter) bundle of specialized conducting fibers that passes from the AV node through the central fibrous body (the fibrous skeleton of the heart) and along the superior portion of the interventricular septum. It is approximately 20 mm long.

**Key properties:**

- **Intrinsic rate**: 40–60 bpm (ventricular escape rhythm if the bundle is intact but AV node is diseased)
- **Rapid conduction**: Conducts at velocities of 1.0–1.5 m/s, significantly faster than the AV node (0.02–0.05 m/s)
- **Protected location**: The Bundle of His is embedded within fibrous tissue, making it relatively resistant to surgical trauma but vulnerable to fibrotic degeneration and calcification

**Branching**: The Bundle of His bifurcates into the right and left bundle branches at the level of the membranous septum (approximately 5–10 mm below the aortic valve).

**Pacing relevance**: His-bundle pacing (HBP) involves placing a pacing lead directly at the Bundle of His. This technique, pioneered by Dr. Maurits Allessie and refined by Dr. Vijayaraman and Dr. Della Bella, provides:
- Activation of the native conduction system
- More physiological ventricular activation compared to RV apex pacing
- Narrow QRS duration (ideally <120 ms)
- Reduction in pacing-induced cardiomyopathy

However, HBP has technical challenges including higher pacing thresholds, lower R-wave sensing amplitudes, and lead stability issues, which have motivated the development of LBBAP as an alternative.

### 3.6 Bundle Branches

#### 3.6.1 Right Bundle Branch (RBB)

The right bundle branch is a continuation of the Bundle of His that courses along the right side of the interventricular septum, beneath the endocardium, toward the apex and the base of the anterior papillary muscle of the RV.

- **Diameter**: Approximately 1–2 mm
- **Conduction velocity**: 1.0–2.0 m/s
- **Blood supply**: Primarily from the left anterior descending (LAD) artery via septal perforators
- **Arrangement**: A single, discrete fascicle

The RBB terminates by giving rise to Purkinje fibers that distribute throughout the RV endocardium.

#### 3.6.2 Left Bundle Branch (LBB)

The left bundle branch is broader and shorter than the RBB, arising as a fan-shaped structure from the left side of the Bundle of His. It divides into two (or sometimes three) fascicles:

1. **Left anterior fascicle**: Courses anteriorly and superiorly toward the anterior papillary muscle; supplies the anterolateral wall of the LV
2. **Left posterior fascicle**: Courses posteriorly and inferiorly toward the posterior papillary muscle; supplies the posteroinferior wall of the LV
3. **Left septal fascicle** (sometimes considered a third fascicle): Supplies the mid-septum

**Key differences from RBB:**

| Property | Right Bundle Branch | Left Bundle Branch |
|----------|-------------------|-------------------|
| Anatomy | Single, discrete fascicle | Broad, fan-shaped; 2–3 fascicles |
| Length | ~50 mm | ~25 mm |
| Blood supply | LAD (septal perforators) | LAD + posterior descending artery (dual supply) |
| Vulnerability | More vulnerable to mechanical trauma | Less vulnerable due to broader structure |
| Fascicular block | RBBB pattern | LAFB, LPFB, or combined |

**Pacing relevance**: Left bundle branch area pacing (LBBAP) targets the region of the LBB on the left side of the interventricular septum. The lead is deployed through the RV septum, deep into the septum, approaching (or crossing into) the LV subendocardium to pace the LBB directly. This technique, pioneered by Dr. Huang and colleagues, has shown promising results in achieving narrow QRS with lower thresholds than HBP.

### 3.7 Purkinje Fibers

The Purkinje fibers form the terminal portion of the conduction system, arising from the bundle branches and spreading extensively throughout the ventricular endocardium.

**Key properties:**

- **Diameter**: 70–80 μm (the largest fibers in the conduction system; approximately 10× the diameter of working ventricular myocytes)
- **Conduction velocity**: 2.0–4.0 m/s (the fastest in the heart)
- **Arrangement**: Form a subendocardial plexus that penetrates approximately one-third of the way through the ventricular wall
- **Automaticity**: Possess latent pacemaker capability (intrinsic rate: 20–40 bpm), though normally suppressed by the faster SA and AV node rates
- **Gap junctions**: Rich in Connexin 40 (Cx40), which provides low-resistance electrical coupling for rapid conduction

**Function**: The extensive Purkinje fiber network ensures that the entire ventricular myocardium is activated within approximately 20–30 ms, producing the rapid, coordinated contraction necessary for efficient systolic ejection.

**Activation sequence**: The ventricles are activated from endocardium to epicardium and from the apex to the base (due to the Purkinje fiber distribution). This sequence ensures:
- The apex and septum contract first, directing blood toward the outflow tracts
- The LV free wall contracts slightly after the septum, creating a wringing motion
- Total ventricular activation time: 80–100 ms (corresponding to the QRS complex duration on ECG)

---

## 4. Cardiac Muscle Structure

### 4.1 Working Myocardium

The cardiac muscle (myocardium) consists of striated muscle cells (cardiomyocytes) with unique structural and functional properties:

**Cellular characteristics:**

- **Shape**: Branching, cylindrical cells approximately 50–100 μm long and 10–25 μm in diameter
- **Nuclei**: Typically 1–2 centrally located nuclei per cell
- **Sarcomeres**: Organized in series and parallel, with the same A-band, I-band, and Z-line structure as skeletal muscle
- **T-tubules**: Transverse tubules that penetrate the cell, allowing rapid electrical excitation to reach the interior
- **Sarcoplasmic reticulum (SR)**: Less extensive than in skeletal muscle; stores and releases calcium for excitation-contraction coupling

### 4.2 Intercalated Discs

Cardiomyocytes are connected end-to-end by intercalated discs, which contain three types of cell-to-cell junctions:

1. **Fasciae adherentes**: Anchor actin filaments; transmit mechanical force between cells
2. **Desmosomes (maculae adherentes)**: Prevent cells from pulling apart during contraction
3. **Gap junctions**: Provide low-resistance electrical pathways between cells

**Gap junction composition in the heart:**

| Connexin | Location | Function |
|----------|----------|----------|
| **Cx43** | Working ventricular myocytes | Primary ventricular gap junction protein |
| **Cx40** | Atrial myocytes, Purkinje fibers | Fast conduction in atria and conduction system |
| **Cx45** | AV node, SA node, ventricular myocytes | Slow conduction in nodal tissue |
| **Cx30.2** | AV node | Slow conduction, AV delay |

Gap junctions allow the heart to function as a functional syncytium — an electrically interconnected network where an action potential initiated at one point spreads rapidly throughout the entire myocardium.

### 4.3 Functional Syncytium Concept

The heart operates as two functional syncytia in series:

1. **Atrial syncytium**: Composed of both atria connected by Bachmann's bundle and atrial myocardial continuity
2. **Ventricular syncytium**: Composed of both ventricles connected by the interventricular septum and Purkinje fiber network

The two syncytia are electrically isolated from each other by the fibrous skeleton of the heart, with the only electrical connection being through the Bundle of His. This arrangement ensures that:
- Atrial activation is complete before ventricular activation begins
- The AV delay is preserved
- Abnormal electrical activity in one chamber does not immediately spread to the other

---

## 5. Electrical Properties of Cardiac Tissue

### 5.1 Resting Membrane Potential

The resting membrane potential (RMP) of cardiac cells varies by cell type:

| Cell Type | RMP (mV) | Primary Ionic Basis |
|-----------|----------|-------------------|
| Atrial/Ventricular myocytes | -85 to -90 | IK1 (inward rectifier K⁺ current) |
| SA node cells | -60 to -65 | Dominated by IK, ICa |
| AV node cells | -60 to -70 | Similar to SA node |
| Purkinje fibers | -90 to -95 | Strong IK1 |
| Contractile atrial myocytes | -80 to -85 | IK1 |

The less negative RMP of nodal cells (compared to working myocytes) is due to the lower density of IK1 channels, which makes nodal cells more excitable and capable of spontaneous diastolic depolarization.

### 5.2 Action Potential Morphology

#### 5.2.1 Fast-Response Action Potential (Working Myocardium, Purkinje Fibers)

```
Phase 0: Rapid depolarization (Na⁺ influx through Nav1.5)
    │     Overshoot to +20 to +30 mV
    │
Phase 1: Early repolarization (transient outward K⁺ current, Ito)
    │     Notch formation
    │
Phase 2: Plateau (L-type Ca²⁺ current, ICaL balanced by IKr, IKs)
    │     Sustained depolarization (~200 ms)
    │     Essential for contraction (excitation-contraction coupling)
    │
Phase 3: Repolarization (outward K⁺ currents: IKr, IKs, IK1)
    │     Return to resting potential
    │
Phase 4: Resting state (maintained by IK1)
         Stable RMP at -85 to -90 mV
```

#### 5.2.2 Slow-Response Action Potential (SA Node, AV Node)

```
Phase 4: Spontaneous diastolic depolarization
    │     If current (funny current, HCN channels) — primary pacemaker mechanism
    │     ICa-T (T-type Ca²⁺ current) contributes
    │     NCX (Na⁺/Ca²⁺ exchanger) contributes
    │     Gradual depolarization from -60 to -40 mV
    │
Phase 0: Slow depolarization (L-type Ca²⁺ influx, ICaL)
    │     No Na⁺ current contribution (voltage too positive for Nav1.5 activation)
    │     Overshoot to 0 to +10 mV
    │
Phase 3: Repolarization (IK, IKr, IKs)
    │     Return toward maximum diastolic potential
    │
Phase 4: Return to MDP and new spontaneous depolarization cycle begins
```

### 5.3 Refractory Periods

Understanding refractory periods is critical for pacemaker design, as the device must sense and pace without colliding with the heart's intrinsic refractory state.

| Period | Duration (ventricular) | Definition | Pacemaker Implication |
|--------|----------------------|------------|----------------------|
| **Absolute refractory period** | ~200 ms | No stimulus can elicit a response | Pacing pulse during this period is ineffective |
| **Effective refractory period** | ~250 ms | No propagated response possible | Sensing during this period may miss signals |
| **Relative refractory period** | ~50 ms | Stronger-than-normal stimulus needed | Premature pacing possible but risky |
| **Supranormal period** | ~10 ms | Weaker-than-normal stimulus can elicit response | Risk of unintended capture |

### 5.4 Conduction Velocity

Conduction velocity varies dramatically across cardiac tissue types:

| Tissue Type | Conduction Velocity (m/s) | Basis for Velocity |
|-------------|--------------------------|-------------------|
| Purkinje fibers | 2.0–4.0 | Large diameter, high Cx40 density |
| Atrial/Ventricular myocytes | 0.3–1.0 | Moderate diameter, Cx43 |
| Bundle of His | 1.0–1.5 | Specialized conduction cells |
| SA node | 0.02–0.05 | Small cells, high fibrous tissue, Cx45 |
| AV node | 0.02–0.05 | Small cells, decremental conduction |

---

## 6. Coronary Blood Supply

Understanding coronary anatomy is essential because:
1. Ischemia from coronary artery disease is a major cause of conduction system disease requiring pacemaker implantation
2. The blood supply to the conduction system determines its vulnerability to ischemic injury
3. Lead placement must avoid coronary structures

### 6.1 Coronary Arteries

**Left coronary artery (LCA)**:
- Left anterior descending (LAD): Supplies anterior wall of LV, anterior two-thirds of septum, apex
  - Septal perforators supply the Bundle of His, RBB, and anterior fascicle of LBB
- Left circumflex (LCx): Supplies lateral and posterior walls of LV, left atrium
  - May supply the SA node (40% of cases)

**Right coronary artery (RCA)**:
- Supplies right atrium, right ventricle, inferior wall of LV
- AV nodal artery (in 85–90% of cases): Supplies the AV node
- SA nodal artery (in 60% of cases): Supplies the SA node

### 6.2 Conduction System Blood Supply

| Structure | Primary Blood Supply | Clinical Consequence of Occlusion |
|-----------|---------------------|----------------------------------|
| SA node | RCA (60%) or LCx (40%) | Sinus bradycardia, sinus arrest |
| AV node | RCA (85–90%) | AV block (1st, 2nd, or 3rd degree) |
| Bundle of His | Septal perforators from LAD | His bundle disease |
| RBB | LAD septal perforators | RBBB |
| LBB (anterior fascicle) | LAD septal perforators | Left anterior fascicular block |
| LBB (posterior fascicle) | Posterior descending (RCA or LCx) | Left posterior fascicular block (rare due to dual supply) |

---

## 7. Cardiac Autonomic Innervation

The heart is innervated by the autonomic nervous system, which modulates heart rate, conduction velocity, and contractility. Understanding this innervation is critical for rate-responsive pacemaker design.

### 7.1 Sympathetic Innervation

- **Origin**: Preganglionic neurons from T1–T4 spinal segments; postganglionic fibers from the superior, middle, and inferior cervical ganglia (stellate ganglion)
- **Neurotransmitter**: Norepinephrine
- **Receptors**: β1-adrenergic receptors on cardiomyocytes
- **Effects**:
  - Increased heart rate (positive chronotropy)
  - Increased conduction velocity (positive dromotropy)
  - Increased contractility (positive inotropy)
  - Decreased AV nodal refractory period

### 7.2 Parasympathetic Innervation

- **Origin**: Vagus nerve (CN X)
- **Neurotransmitter**: Acetylcholine (ACh)
- **Receptors**: M2 muscarinic receptors
- **Effects**:
  - Decreased heart rate (negative chronotropy)
  - Decreased AV nodal conduction velocity (negative dromotropy)
  - Minimal effect on ventricular contractility (sparse vagal innervation of ventricles)

### 7.3 Implications for Rate-Responsive Pacing

Rate-responsive pacemakers must mimic the heart's natural chronotropic response to physiological demands. Sensors used in rate-responsive pacemakers include:

| Sensor | Physiological Parameter Measured | Mimics |
|--------|--------------------------------|--------|
| Accelerometer | Body motion/activity | Sympathetic response to exercise |
| Minute ventilation | Respiratory rate and tidal volume | Respiratory sinus arrhythmia |
| QT interval | Sympathetic modulation of repolarization | Direct sympathetic effect on myocardium |
| Mixed venous O₂ saturation | Metabolic demand | Overall metabolic response |
| Contractility (dP/dt) | Myocardial contractility | Sympathetic inotropic effect |

---

## 8. The Fibrous Skeleton of the Heart

The fibrous skeleton is a framework of dense connective tissue that:

1. **Provides structural support** for the valve rings (annuli)
2. **Electrophically insulates** the atria from the ventricles (except at the Bundle of His)
3. **Anchors** cardiac muscle fibers and valve leaflets

Key components:
- **Four fibrous rings** (annuli fibrosi) surrounding each valve orifice
- **Right and left fibrous trigones** (dense connective tissue masses at the junction of the aortic and mitral rings)
- **Membranous septum** (a thin fibrous sheet separating the RV outflow tract from the LV, through which the Bundle of His passes)
- **Central fibrous body** (where the membranous septum, the right fibrous trigone, and the AV rings meet; the Bundle of His passes through this structure)

**Pacing relevance**: The fibrous skeleton is the site of lead fixation for His-bundle pacing. The central fibrous body and the membranous septum are critical anatomical landmarks for lead placement. Calcification of the fibrous skeleton (common in elderly patients) can make lead placement more challenging.

---

## 9. Embryological Considerations

Understanding cardiac embryology provides insight into:
- Congenital conduction system abnormalities
- Anatomical variants that may affect lead placement
- The developmental origins of pacemaker cells

### 9.1 Development of the Conduction System

- The SA node develops from the right sinus venosus
- The AV node develops from the endocardial cushions of the AV canal
- The Bundle of His develops from the ventricular portion of the AV canal
- The bundle branches and Purkinje fibers develop from the ventricular myocardium

During embryonic development, the entire primitive ventricle has automaticity. As the heart matures, the conduction system becomes specialized, and most ventricular cells lose their automaticity, retaining it only in the specialized Purkinje network.

### 9.2 Clinical Relevance

Congenital heart defects (e.g., Ebstein's anomaly, corrected transposition of the great arteries) frequently involve conduction system abnormalities due to disrupted embryological development. Patients with these conditions may require pacemaker implantation at a young age.

---

## 10. Biomechanical Considerations for Device Design

### 10.1 Cardiac Motion and Lead Stress

The heart undergoes complex three-dimensional motion during each cardiac cycle:

- **Translation**: The heart moves 1–2 cm inferiorly and anteriorly during systole
- **Rotation**: The apex rotates counterclockwise (when viewed from the apex) during systole
- **Compression**: The ventricles shorten by 15–25% of their end-diastolic length during systole

This motion imposes mechanical stress on pacemaker leads, particularly at:
- The lead-myocardial interface (fixation point)
- The lead-tricuspid valve interface (leads crossing the tricuspid valve)
- The lead-subclavian vein junction (where the lead bends during arm movement)

Lead fracture is a well-recognized complication, and modern lead design must account for these biomechanical stresses.

### 10.2 Tissue Response to Implants

When a foreign body (such as a pacemaker lead) is placed in cardiac tissue, the following response occurs:

1. **Acute phase** (hours–days): Inflammation, thrombus formation on the lead surface
2. **Subacute phase** (weeks–months): Fibrous encapsulation, organization of thrombus
3. **Chronic phase** (months–years): Mature fibrous capsule formation, typically 100–200 μm thick

The fibrous capsule can increase pacing thresholds over time (the "exit block" phenomenon), which is why modern pacemaker output is programmable and must be periodically adjusted.

---

## 11. Summary

A thorough understanding of cardiac anatomy and the conduction system is essential for the design and development of implantable pacemaker chips. Key takeaways:

1. The heart is a four-chambered muscular pump with a specialized conduction system
2. The SA node is the primary pacemaker (60–100 bpm), with the AV node as a subsidiary pacemaker (40–60 bpm)
3. The conduction pathway (SA node → AV node → Bundle of His → Bundle branches → Purkinje fibers) ensures coordinated cardiac activation
4. The electrical properties of cardiac tissue (resting membrane potential, action potential morphology, refractory periods, conduction velocities) define the constraints within which a pacemaker must operate
5. The coronary blood supply to the conduction system determines its vulnerability to ischemic injury
6. Cardiac autonomic innervation provides the regulatory framework that rate-responsive pacemakers must replicate
7. Biomechanical factors (cardiac motion, tissue response to implants) influence lead design and longevity

These concepts will be revisited throughout this book as we progress from the fundamentals of cardiac electrophysiology to the design of the iPACE-CHIP.

---

## References

1. Guyton AC, Hall JE. *Textbook of Medical Physiology*. 14th ed. Elsevier; 2020.
2. Kumar V, Abbas AK, Aster JC. *Robbins & Cotran Pathologic Basis of Disease*. 10th ed. Elsevier; 2020.
3. Katz AM. *Physiology of the Heart*. 5th ed. Lippincott Williams & Wilkins; 2011.
4. Mohrman DE, Heller LJ. *Cardiovascular Physiology*. 9th ed. McGraw-Hill; 2018.
5. Tse HF, Lau CP. "Long-term outcome of right ventricular outflow tract pacing." *Pacing Clin Electrophysiol*. 2010;33(5):627-636.
6. Vijayaraman P, et al. "His bundle pacing: Current status and future directions." *J Cardiovasc Electrophysiol*. 2019;30(12):2524-2534.
7. Huang W, et al. "A beginner's guide to permanent left bundle branch area pacing." *J Cardiovasc Electrophysiol*. 2019;30(12):2535-2541.
8. Anderson RH, et al. "The clinical anatomy of the conduction system." *Cardiol J*. 2018;25(4):432-437.
9. Derval N, et al. "Anatomy of the conduction system." *Herzschrittmacherther Elektrophysiol*. 2017;28(4):314-320.
10. ISO 14708-1:2014. Implants for surgery — Active implantable medical devices — Part 1: General requirements for safety, marking and for information to be provided by the manufacturer.
