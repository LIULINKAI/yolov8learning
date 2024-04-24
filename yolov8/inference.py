from ultralytics import YOLO

# Load a model
model = YOLO(r'runs\detect\train\weights\best.pt')  # build a new model from YAML
# Train the model
results = model.predict(source=r'E:\science\llk\助教\计算机视觉\实验资料\datasets\test_images', imgsz=512, conf=0.25, iou=0.6, save=True
                    #   device=0
                      )