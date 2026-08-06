# Model Card: LympClear Upper-Extremity Venous Segmentation Model

## Model

- Architecture: 3D nnU-Net
- Source-domain pretraining: lower-extremity MR lymphangiography
- Target-domain fine-tuning: upper-extremity MR lymphangiography
- Final configuration: `Dataset038_finetune127`, `fold_0`, `checkpoint_best.pth`
- Fine-tuning method: `nnUNetv2_train ... -pretrained_weights`

## Intended use

The model is intended for research use in venous segmentation and postprocessing of contrast-enhanced upper-extremity MR lymphangiography. The predicted venous mask can be used to generate venous-suppressed images and venous-highlighted visualizations.

## Input

- Fat-suppressed 3D T1-weighted postcontrast MR lymphangiography
- NIfTI format following the nnU-Net v2 convention
- Single input channel with the filename suffix `_0000.nii.gz`

## Output

- Binary venous mask: `0 = background`, `1 = vein`
- Optional venous-suppressed NIfTI image
- Optional venous-highlighted MIP visualization

## Limitations

- Residual errors may occur near injection sites.
- Superficial venous clusters may cause over-suppression or residual artifact.
- Motion, metal artifact, field inhomogeneity, or different acquisition protocols may reduce performance.
- Performance outside upper-extremity MRL requires independent evaluation.

## Out-of-scope use

The model is not intended for standalone diagnosis, treatment selection, autonomous surgical planning, or replacement of radiologist review. Venous-highlighted outputs should not replace clinical confirmation of venous caliber, depth, or patency.
