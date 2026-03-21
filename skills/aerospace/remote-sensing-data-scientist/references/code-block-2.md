# python Example

```
import torch.nn.functional as F

def predict_with_uncertainty(model, image_patches, mc_passes=20):
    """Monte Carlo Dropout for epistemic uncertainty estimation."""
    model.train()  # Enable dropout at inference for MC sampling
    predictions = []

    with torch.no_grad():
        for _ in range(mc_passes):
            logits = model(image_patches)
            probs = F.softmax(logits, dim=1)
            predictions.append(probs.cpu().numpy())

    pred_stack = np.stack(predictions)        # [passes, B, C, H, W]
    mean_probs = pred_stack.mean(axis=0)      # [B, C, H, W]
    epistemic_unc = pred_stack.std(axis=0).max(axis=1)  # [B, H, W]

    class_map = mean_probs.argmax(axis=1)     # Hard classification
    confidence = mean_probs.max(axis=1)       # Max class probability

    # Deliver all three products: class, confidence, uncertainty
    export_geotiff(class_map, 'land_cover_class.tif')
    export_geotiff(confidence, 'land_cover_confidence.tif')
    export_geotiff(epistemic_unc, 'land_cover_uncertainty.tif')
    return class_map, confidence, epistemic_unc
```
