## Inpainting to remove unwanted information from training data

## Tips

### Get list of bounding boxes for predictions

Useful way to get coordinates to perform inpainting step
```python
output_pred_boxes = outputs["instances"].pred_boxes
for i in output_pred_boxes.__iter__():
print(i.cpu().numpy())
```
![source](https://github.com/facebookresearch/detectron2/issues/1519)

### Crop images

![Crop images using PIL](https://stackoverflow.com/questions/9983263/how-to-crop-an-image-using-pil)