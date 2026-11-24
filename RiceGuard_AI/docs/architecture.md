# Architecture & Data Flow

```
OFFLINE (Colab/local)                              ONLINE (Streamlit)
raw/ -> image_loader (validate, dedupe)            main.py -> app/detection.py
     -> cleaned/ -> dataset_split (group-aware)         -> utils/validators.py   (checks upload)
     -> train|validation|test/                          -> model/predict.py      (mock OR real)
     -> train_model.py  --exports-->  saved_models/         -> preprocessing/image_preprocessing.py (SHARED)
     -> evaluate_model.py (test set, once)              -> utils/history_manager.py (CSV)
                                                        -> app/results.py + utils/disease_information.py
```

## Contracts
| Boundary | Contract |
|---|---|
| `predict_image(image, use_mock)` | dict: `predicted_class, confidence, probabilities, is_low_confidence, is_mock` |
| `preprocess_pil_image(image, mode)` | float32 array `(1, 224, 224, 3)` |
| `validate_uploaded_file(file)` | `ValidationResult(ok, message, image)` |
| `append_record(filename, result)` | writes one row with `HISTORY_COLUMNS` |
| `get_disease_info(class_name)` | `DiseaseInfo` dict (never raises) |
| Model artefacts | `riceguard_model.keras` + `class_indices.json` ({name: index}) |

## Separation of concerns
The online side imports only `config`, `preprocessing/image_preprocessing`, `model/predict`, `utils`, `app`.
It must not import anything from the offline side.
