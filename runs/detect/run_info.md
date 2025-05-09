# Information what each run means

- train11 -> The model runned with gamma correction and tiling of 1280x1280
  - val2 -> The validation run of train11
    ![Alt text](val2/confusion_matrix_normalized.png)

- train6 -> The model runned with gamma correction and tiling of 1280x1280 with 1 added bird in each tile
  - train62 -> The validation run of train6
    ![Alt text](train62/confusion_matrix_normalized.png)


- train8 -> The model runned with gamma correction and tiling of 1280x1280 with 2 added birds in each tile
  - train82 -> The validation run of train8
  ![Alt text](train82/confusion_matrix_normalized.png)

- train9 -> The model runned with gamma correction and tiling of 1280x1280 with 2 added birds in each tile
    - With paramters:
        # Hyperparameters
    epochs=100,                    # Number of epochs
    batch=16,                     # batch size
    imgsz=1280,                    # Image size
    single_cls=True,
    weight_decay=0.0003,
    warmup_epochs=5.0,
    warmup_momentum=0.75,
    freeze=10,                     # Freeze first 10 layers
    patience=12,
    dropout=0.1,
    # Reproducability
    seed = 42
  - train92 -> The validation run of train9
  ![Alt text](train92/confusion_matrix_normalized.png)

- train10 -> The model run with gamma correction and tiling 640x640 with 2 added birds in each tile
  - train102 -> Validation run of train10
  ![Alt text](train102/confusion_matrix_normalized.png)
