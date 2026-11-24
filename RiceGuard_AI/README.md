# RiceGuard AI – Rice Leaf Disease Detection System

Modular Streamlit + TensorFlow/Keras app. **This repo is a scaffold**: the UI runs today
with *mock* predictions; students implement the `# TODO` blocks in parallel.

## Quick start (VS Code, local)
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # shared-contract tests should pass
streamlit run main.py            # runs in mock mode by default
```

## Colab -> VS Code workflow
1. **Colab (Members 1-4):** clone the repo, mount Google Drive, keep `dataset/` on Drive
   (symlink or copy into `dataset/`). Run cleaning -> split -> training -> evaluation.
2. Training must export to `model/saved_models/`: `riceguard_model.keras` and `class_indices.json`.
3. Upload both files to the shared Drive folder (they are git-ignored).
4. **VS Code (Members 5-6):** download them into `model/saved_models/`, set
   `USE_MOCK_MODEL = False` in `config/settings.py` (or use the sidebar toggle), run the app.

## Rules to remember
- Class names, image size, split ratios, thresholds and paths come from `config/settings.py` only.
- Resize/normalisation lives only in `preprocessing/image_preprocessing.py` (train + inference).
- `main.py` and `app/` never import `model/train_model.py`, `model/evaluate_model.py` or `model/model_builder.py`.
- Never commit datasets or `.keras` files. Never report numbers you did not produce yourself.

## Git workflow
`main` is protected. Work on `feature/memberN-<topic>`, open a Pull Request, get one review, then merge.
See `docs/team_responsibilities.md`.
