# Team Responsibilities (6 members)

| # | Role | Owns | Environment | Branch |
|---|---|---|---|---|
| 1 | Dataset | `preprocessing/image_loader.py`, `dataset_split.py`, `docs/dataset_notes.md` | Colab | `feature/member1-dataset` |
| 2 | Preprocessing | `preprocessing/image_preprocessing.py`, `config/settings.py` review | Colab + local | `feature/member2-preprocessing` |
| 3 | Model training | `model/model_builder.py`, `train_model.py` | Colab (GPU) | `feature/member3-training` |
| 4 | Evaluation & inference | `model/evaluate_model.py`, `model/predict.py` | Colab + local | `feature/member4-inference` |
| 5 | UI & app logic | `main.py`, `app/detection.py`, `results.py`, `history.py`, `utils/validators.py`, `history_manager.py` | VS Code | `feature/member5-ui` |
| 6 | QA, docs, knowledge | `utils/disease_information.py`, `app/disease_library.py`, `tests/`, `requirements.txt`, README | VS Code | `feature/member6-qa-docs` |

## Interface rules
- Changing a contract in `docs/architecture.md` needs agreement from every affected owner (post in the team chat first).
- Members 1-3 work offline (no dependency on the UI). Members 5-6 use mock mode until Member 3/4 deliver a real model.

## Git workflow
1. `git checkout -b feature/memberN-topic` from latest `main`.
2. Small commits with clear messages; push often.
3. Open a Pull Request; one teammate reviews; `pytest` must pass.
4. Never commit datasets, `.keras` files, or `data/*.csv`.

## Integration milestones
1. Scaffold merged (done).  2. Dataset cleaned + split + leakage check passed.
3. Model trained, `.keras` + `class_indices.json` on Drive.  4. `real_predict` working, mock off.
5. Test-set evaluation (once).  6. Final QA + report.
