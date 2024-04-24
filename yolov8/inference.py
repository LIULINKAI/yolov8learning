from ultralytics import YOLO

# Load a model
model = YOLO(r'../runs\detect\train\weights\best.pt')  # build a new model from YAML
# Train the model
results = model.predict(source=r'../datasets\test_images', 
                        imgsz=512, 
                        conf=0.25, 
                        iou=0.6, 
                        save=True,
                        device=0
                      )