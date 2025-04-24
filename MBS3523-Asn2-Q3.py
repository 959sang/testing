# YOLO v3
import cv2
import numpy as np

confThreshold = 0.8

cam = cv2.VideoCapture(0)

classesFile = 'coco80.names'            # point classesFile to 'coco80.names'
classes = []                            # create empty list - classes[]
with open(classesFile, 'r') as f:       # load all classes in coco80.names into classes[]
    classes = f.read().splitlines()
    print(classes)
    print(len(classes))

# You need to download the weights and cfg files from https://pjreddie.com/darknet/yolo/
net = cv2.dnn.readNetFromDarknet('yolov3-608.cfg','yolov3-608.weights')     # load configuration and weights files

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)    # use OpenCV as backend
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)         # use CPU as target

while True:
    success , img = cam.read()
    height, width, ch = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (320, 320), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)

    layerNames = net.getLayerNames()
    print(layerNames)

    output_layers_names = net.getUnconnectedOutLayersNames()
    print(output_layers_names)

    LayerOutputs = net.forward(output_layers_names)
    print(len(LayerOutputs))

    number = 0
    price = 0

    bboxes = []         # array for all bounding boxes of detected classes
    confidences = []    # array for all confidence values of matching detected classes
    class_ids = []      # array for all class IDs of matching detected classes

    for output in LayerOutputs:
        for detection in output:
            scores = detection[5:]       # omit the first 5 values
            class_id = np.argmax(scores) # find the highest score ID from 80 values with the highest confidence value
            confidence = scores[class_id]
            if confidence > confThreshold:
                center_x = int(detection[0]*width)  # YOLO predicts centers of image
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                bboxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)
                # cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)

    print(len(bboxes))
    indexes = cv2.dnn.NMSBoxes(bboxes, confidences, confThreshold, 0.3) # Non-maximum suppression
    #print(indexes)
    #print(indexes.flatten())

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(bboxes), 3))

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = bboxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i] * 100))
            color = colors[i]

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                # print label with confidence level in percentage
            cv2.putText(img, label + " " + confidence + "%", (x, y + 12), font, 0.9,
                        (255, 255, 255), 1)

    # Count fruit detected
    fruit_counts = {}
    for i in range(len(bboxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            confidence = confidences[i]

            # Update fruit count
            if label in fruit_counts:
                fruit_counts[label] += 1
            else:
                fruit_counts[label] = 1

    # Print total counts per fruit
    for fruit, count in fruit_counts.items():
        print(f"{fruit}: {count} detected")

        # print total number of apple
        cv2.putText(img, f"{fruit} no. = {count}", (420, 20), font, 1, (255, 255, 255), )

        price = count * 2
        # print total price of apple
        cv2.putText(img, f"price = $2 x {count} = ${price}", (420, 40), font, 1,
                            (255, 255, 255), 1)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == 27:
        break

cam.release()
cv2.destroyAllWindows()