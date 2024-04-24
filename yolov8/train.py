from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO('yolov8n.yaml')  # build a new model from YAML
    # Train the model
    results = model.train(data=r'yolov8\configs\mydata.yaml',
                          epochs=100, 
                          imgsz=512, 
                          optimizer='SGD',
                          device=0, 
                          batch=2,
                          lr0=0.01
                        )