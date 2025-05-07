"# DL---detection-of-birds-in-drone-images" 

[Google Drive](https://drive.google.com/drive/u/0/folders/1s-2uJSHty12oKUNlqSL-MHXkW62AAV0E)

Packages

## Searching and linking articles:
https://www.connectedpapers.com/ 

## Steps to be taken by our group (Done By monday)
- Baseline model of current data with Yolo - Research papers about what is useful (Eugene)
- Preprocessing & data understanding (Mathijs)
    - Shuffling data is probably necessary since same kind of images seem to be clustered. For example, same kind of agriculture or the same field
- 
- Data collection of open source data - Research available frameworks (Mehdi & Cas & Flynn)
- Explore TuE computing environment 

## Second stage
- Optimizing the baseline
- Experimentation of the different suggested models
- 



Weights and biases (wandb.ai)


## Meeting this monday at 1230

---
## Meeting 5  may
[Harmful Birds Detection Object Detection Dataset (v2, 2024-08-21 9:52am) by Yaelym Hong](https://universe.roboflow.com/yaelym-hong/harmful-birds-detection/dataset/2)

- Use bounding boxes to only find small objects in a larger field

Find cropped images and insert them randomly on a farmfield. 

You can divide the picture into the prefered 640x640 boxes. If there is a sliced bounding box. You just move it pixels to the oppposite direction until there is no issue anymore with the bounding box.

First model was shit, but then changed to 1280 and it seemed to be doing much better.

Freeze first and last layer and change these layerss with finetuning for our dataset

Wikipedia page about small object detection - feature pyramid network

Gamma correction fixes the brightness difference

Superresolution → make small birds much bigger

GIve it a try to insert cropped birds into the field - (Do it with the yoloflow data format)

- Find cropped images.
- Crop the image
- Add on the same height level as other birds that are placed on the same colored background
    - Or use the model that can detect rows of crops I found this model when looking up a picture with reverse image search
    - Try to scale it in different ways also
        - try to use the cropped images from our own dataset. Only issue is that cropping is hard in this regard
- Make the augmented bounding box the same size
- reduce the image size pixels to be similar to the other birds in the picture
- 

Mathijs will look into tiling 

- Try it first with 640x640 images
- Then try 320x320

Eugen

- Roboflow
- Keep testing with current data
- pruning & quantitatioztion at the end

Cas

- Send the data from mehdi to cas
- Make a pipeline from mehdi’s dataset to find the right size of images

### Questions to ask in Q&A

What type of drone is it?

What is the computing power of the drone? So how much can we use for computing for inference?
