# LympClear

**Cross-Anatomic Transfer Learning for Sample-Efficient, Task-Specific Venous Postprocessing at Upper-Extremity MR Lymphangiography**

LympClear is an nnU-Net-based research pipeline for venous segmentation and postprocessing in dynamic contrast-enhanced upper-extremity MR lymphangiography (MRL). The repository includes code for:

- lower-extremity source-domain pretraining;
- upper-extremity fine-tuning and training from scratch;
- venous-mask inference with 3D nnU-Net;
- venous suppression and highlighting;
- MIP/cine generation;
- Dice evaluation and learning-curve analysis.

## Installation

```bash
conda env create -f environment.yml
conda activate lympclear
pip install -e .
```

Set the nnU-Net v2 paths:

```bash
export nnUNet_raw=/path/to/nnUNet_raw
export nnUNet_preprocessed=/path/to/nnUNet_preprocessed
export nnUNet_results=/path/to/nnUNet_results
```

For Windows PowerShell:

```powershell
$env:nnUNet_raw="<path-to-nnUNet_raw>"
$env:nnUNet_preprocessed="<path-to-nnUNet_preprocessed>"
$env:nnUNet_results="<path-to-nnUNet_results>"
```

## Data preparation

Input data follow the nnU-Net v2 convention. For a single-channel postcontrast MRL volume:

```text
DatasetXXX_name/
├── dataset.json
├── imagesTr/
│   └── case001_0000.nii.gz
├── labelsTr/
│   └── case001.nii.gz
└── imagesTs/
    └── case101_0000.nii.gz
```

All phases from the same patient should remain in the same data partition to prevent information leakage. See `docs/data_format.md` for details.

## Preprocessing

```bash
bash scripts/02_plan_and_preprocess.sh --dataset-id 29 --config 3d_fullres
```

## Training from scratch

```bash
bash scripts/03_train_scratch.sh \
  --dataset-id 29 \
  --fold 0 \
  --config 3d_fullres
```

## Fine-tuning from the lower-extremity model

```bash
bash scripts/04_finetune_from_lower_limb.sh \
  --target-dataset-id 38 \
  --fold 0 \
  --config 3d_fullres \
  --pretrained-checkpoint "$nnUNet_results/Dataset025_leg/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/checkpoint_best.pth"
```

## Inference

The trained nnU-Net model must be available under `nnUNet_results`.

```bash
bash scripts/07_predict_upper_final.sh \
  --input /path/to/imagesTs \
  --output outputs/pred_venous_mask
```

## Venous postprocessing

```bash
python scripts/08_postprocess_suppression_highlighting.py \
  --image /path/to/case_0000.nii.gz \
  --mask outputs/pred_venous_mask/case.nii.gz \
  --out-dir outputs/postprocessed_case \
  --mode both
```

Venous suppression replaces each mask-positive voxel with the median intensity of nonvenous voxels in a local `3 × 3 × 3` neighborhood.

## MIP and cine generation

```bash
python scripts/10_make_mip_cine.py \
  --image outputs/postprocessed_case/suppressed.nii.gz \
  --out-dir outputs/postprocessed_case/mip_cine \
  --axis 0 \
  --make-gif
```

## Segmentation evaluation

```bash
python scripts/09_evaluate_dice.py \
  --pairs-csv /path/to/prediction_label_pairs.csv \
  --output-csv outputs/patient_level_dice.csv \
  --summary-csv outputs/dice_summary.csv
```

The aggregate learning-curve results are provided in `results/learning_curve_table2.csv`.

## Repository structure

```text
configs/       Configuration templates
docs/          Data, training, inference, and deployment documentation
examples/      Synthetic example data generator
lympclear/     Python package for I/O, metrics, postprocessing, and visualization
scripts/       Training, inference, postprocessing, and evaluation scripts
tests/         Unit tests
results/       Aggregate segmentation results
```

## Data and model availability

Clinical images, manual masks, and patient-level metadata are not distributed because of privacy and institutional data-governance restrictions. Trained model weights are not included in this repository.

## Intended use

This software is intended for research use. It is not a standalone diagnostic, surgical-planning, or treatment-decision system.

## License

Apache License 2.0. See `LICENSE`.

## Citation

Citation metadata are provided in `CITATION.cff`.
