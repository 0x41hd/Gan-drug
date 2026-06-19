# FeedbackGAN — De Novo Drug Discovery via WGAN-GP

> Generate novel drug-like molecules optimized for potency against the
> **Kappa Opioid Receptor (KOR)**, using a Wasserstein GAN that operates in the
> latent space of a BiLSTM Autoencoder and is steered by an LSTM-predictor
> feedback loop.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/0x41hd/GAN-Drug-Generator/blob/main/FeedbackGAN_Colab.ipynb)

![Architecture](framework.jpg)

---

## Quick Start (Google Colab — recommended)

The easiest way to run this project is the included notebook. It trains
everything from scratch on a free Colab GPU.

1. Click the **Open in Colab** badge above (after pushing this repo to GitHub).
2. **Runtime → Change runtime type → GPU**.
3. Run **Section 2** (installs dependencies), then **Runtime → Restart session**.
4. Run the remaining sections top to bottom.

That's it — you only run the notebook. It clones this repo, builds the
vocabulary and configs, then trains the Autoencoder → Predictor → WGAN-GP →
FeedbackGAN in sequence.

---

## What it does

Traditional drug discovery is slow and expensive. This project uses generative
deep learning to propose molecules that are simultaneously:

- **Valid** — parseable by RDKit
- **Drug-like** — LogP between 1–5
- **Synthesizable** — SA score < 6 (of 10)
- **Potent** — predicted KOR pIC50 above a threshold

The core idea is a **feedback loop**: after each training epoch, the GAN's
training data is updated by swapping the weakest real molecules for the best
newly generated ones. Over many epochs the training distribution drifts toward
higher-potency molecules.

---

## Architecture

| Block | Component           | Role                                    |
| ----- | ------------------- | --------------------------------------- |
| A     | BiLSTM Encoder      | SMILES → 256-D latent vector            |
| B     | LSTM Decoder        | latent vector → SMILES                  |
| C     | WGAN-GP Critic      | Wasserstein distance + gradient penalty |
| D     | Generator           | noise z(64) → latent(256)               |
| F     | LSTM Predictor (×5) | predict KOR pIC50 from SMILES           |
| G     | Pareto Front        | rank by pIC50 ↑ and SA score ↓          |

---

## Repository structure

```
GAN-Drug-Generator/
├── FeedbackGAN_Colab.ipynb     ← run THIS in Colab
│
├── main_feedbackGAN.py         ← local entry point (alternative to notebook)
├── WGAN_4.py                   ← WGAN-GP model
├── Autoencoder2_emb.py         ← BiLSTM autoencoder
├── predictor.py                ← LSTM predictor ensemble
├── utils.py                    ← utilities (validity, scoring, feedback update)
├── Vocabulary2.py              ← SMILES tokenizer/encoder
├── tokens.py                   ← token table (predictor dependency)
├── sascorer_calculator.py      ← synthetic accessibility score (Ertl 2009)
├── pareto_front.py             ← post-hoc multi-objective ranking
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── framework.jpg               ← architecture diagram
│
└── data/
    └── data_clean_kop.csv      ← KOR dataset (smiles,pIC50) — YOU PROVIDE
```

---

## What to put in the repo

Push **everything above**, including:

- All 9 `.py` files
- `FeedbackGAN_Colab.ipynb`
- `README.md`, `LICENSE`, `.gitignore`, `requirements.txt`
- `framework.jpg`
- **`data/data_clean_kop.csv`** — yes, include it, because the notebook clones
  the repo to get the data. (If your dataset is private or huge, instead upload
  it manually in the notebook's Section 3.)

**Do NOT commit** (the `.gitignore` already excludes these):

- Trained weights (`*.h5`, `*.hdf5`, `*.weights.h5`) — too large for git
- Generated outputs (`GAN_model/run_*/`, `*.png`, prediction CSVs)
- `fpscores.pkl.gz` — the notebook downloads it automatically

---

## The dataset

`data/data_clean_kop.csv` must be a CSV with SMILES in column 0 and pIC50 in
column 1:

```
smiles,pIC50
COc1ccc2c(c1)CC(N)C2,6.3
CC(=O)Nc1ccc(O)cc1,5.1
```

To build it from [ChEMBL](https://www.ebi.ac.uk/chembl/):

1. Search the Kappa opioid receptor target (`CHEMBL218`).
2. Filter activities: type = IC50, assay = binding, units = nM.
3. Convert: `pIC50 = -log10(IC50_nM × 1e-9)`.
4. Keep `smiles,pIC50` and save to `data/data_clean_kop.csv`.

---

## Running locally (instead of Colab)

```bash
git clone https://github.com/0x41hd/GAN-Drug-Generator.git
cd GAN-Drug-Generator

conda create -n feedbackgan python=3.10
conda activate feedbackgan
pip install -r requirements.txt

# IMPORTANT: this project uses the Keras 2 API.
export TF_USE_LEGACY_KERAS=1        # Windows: set TF_USE_LEGACY_KERAS=1

python main_feedbackGAN.py
```

> Note: `main_feedbackGAN.py` assumes pre-trained weights exist. If you're
> training from scratch, the **notebook** is the supported path — it runs the
> three training stages in the right order.

---

## A note on Keras 2 vs Keras 3

This code targets the **Keras 2 API**. Modern TensorFlow ships Keras 3, which
changes the model-config format, stateful-RNN handling, and weight-file naming.
To stay compatible without rewriting the model code, set
`TF_USE_LEGACY_KERAS=1` **before importing TensorFlow** and install `tf-keras`
(both handled by the notebook and `requirements.txt`).

---

## Results

The feedback loop progressively shifts the predicted pIC50 distribution of
generated molecules upward. After training you get:

- A KDE plot comparing pIC50 **before vs after** the feedback loop
- A CSV of generated molecules ranked by predicted potency
- A Pareto front (pIC50 vs SA score) via `pareto_front.py`

---

## References

1. Ertl, P. & Schuffenhauer, A. (2009). _Estimation of synthetic accessibility
   score of drug-like molecules._ J. Cheminformatics 1(8).
2. Gulrajani, I. et al. (2017). _Improved Training of Wasserstein GANs._ NeurIPS.
3. Gómez-Bombarelli, R. et al. (2018). _Automatic Chemical Design Using a
   Data-Driven Continuous Representation of Molecules._ ACS Central Science.

---

## License

MIT — see [LICENSE](LICENSE). The SA-score module retains its original BSD
3-Clause license from Novartis (see file header).

---

_Built by [0x41hd](https://github.com/0x41hd)_
