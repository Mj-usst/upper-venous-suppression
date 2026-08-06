# Synthetic demo case

Generate the synthetic image and mask:

```bash
python scripts/11_generate_synthetic_demo.py
```

Run venous postprocessing:

```bash
python scripts/08_postprocess_suppression_highlighting.py \
  --image examples/synthetic_case/imagesTs/synthetic_upper_mrl_0000.nii.gz \
  --mask examples/synthetic_case/labelsTs/synthetic_upper_mrl.nii.gz \
  --out-dir outputs/synthetic_postprocess \
  --mode both
```

The synthetic example contains no clinical or patient-derived data.
