# Inference protocol

Before inference, ensure that the trained nnU-Net model is available under `nnUNet_results`.

## Predict the venous mask

```bash
bash scripts/07_predict_upper_final.sh \
  --input /path/to/imagesTs \
  --output outputs/pred_venous_mask
```

## Generate venous-suppressed and venous-highlighted outputs

```bash
python scripts/08_postprocess_suppression_highlighting.py \
  --image /path/to/case_0000.nii.gz \
  --mask outputs/pred_venous_mask/case.nii.gz \
  --out-dir outputs/postprocessed_case \
  --mode both
```

## Create MIP or cine outputs

```bash
python scripts/10_make_mip_cine.py \
  --image outputs/postprocessed_case/suppressed.nii.gz \
  --out-dir outputs/postprocessed_case/mip_cine \
  --axis 0 \
  --make-gif
```
