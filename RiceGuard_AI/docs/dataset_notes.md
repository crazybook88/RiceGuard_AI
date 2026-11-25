# Dataset Notes (fill in – do not invent)

| Field | Value |
|---|---|
| Dataset name | A Rice Leaf Disease Image Dataset for Multi-Class Disease Classification |
| Source URL | https://data.mendeley.com/datasets/n8jpkpfz5p/1 |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Citation | Hasan, M. M. (2026). A rice leaf disease image dataset for multi-class disease classification. Mendeley Data, 1. https://doi.org/10.17632/n8jpkpfz5p.1 |
| Date downloaded | 2026-11-25 |

## Inspection report (computed by `audit_class_distribution`, not typed by hand)

1. Dataset Selection
Four classes were selected from the original dataset:
- Healthy
- Bacterial Leaf Blight
- Brown Spot
- Rice Blast

2. Image Validation
- Total images: 2820
- Valid images: 2820
- Corrupt files removed: 0
- All images passed image validation using Pillow.

3. Duplicate Detection
- Exact duplicates detected: 1 pair
- Exact duplicates images removed: 1
- Near duplicates detection method: Perceptual Hash (pHash)
- pHash Hamming distance threshold: 5
- Near-uplicate groups detected after exact duplicate removal: 44
- Near-duplicate images were retained and grouped to prevent data leakage.

4. Cleaned Dataset
Total images after cleaning: 2819

| Class | Image Count |
|---|---|
| Healthy | 753 |
| Bacterial Leaf Blight | 785 |
| Brown Spot | 760 |
| Rice Blast | 521 |
| Total | 2819 |

5. Class Imbalance
The dataset has a moderate class imbalance.

- Largest class: Bacterial Leaf Blight (785 images)
- Smallest class: Rice Blast (521 images)
- Minimum-to-maximum class ratio: approximately 0.66

Stratified splitting was used to maintain similar class proportions across the three datasets.

6. Leaf IDs and Grouping
No explicit leaf IDs were identified in the image filenames.

Near-duplicate images were grouped using perceptual hash (pHash) similarity. Images within the same detected group were assigned to the same dataset split to reduce data leakage.

Images without detected near-duplicates were assigned individual group IDs based on their file paths.

7. Dataset Splitting
The cleaned dataset was divided into three subsets:

| Split | Image Count | Percentage |
|---|---|---|
| Training | 1974 | 70.02% |
| Validation | 423 | 15.01% |
| Testing | 422 | 14.97% |
| Total | 2819 | 100% |

8. Class Distribution After Splitting
| Class | Training | Validation | Testing |
|---|---|---|---|
| Healthy | 527 | 114 | 112|
| Bacterial Leaf Blight | 550 | 117 | 118|
| Brown Spot | 532 | 114 | 114 |
| Rice Blast | 365 | 78 | 78|

9. Leakage Check
- Exact duplicate leakage: Not detected
- Near-duplicate leakage: Not detected
- Leakage check result: PASS

All checks passed before the dataset was copied into the training, validation and testing folders.