import xml.etree.ElementTree as ET
import os
import glob

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_file, classes):
    in_file = open(xml_file)
    out_file = open(xml_file.replace(".xml", ".txt"), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    in_file.close()
    out_file.close()

# Define your classes here (they must match your dataset's labels)
classes = ["With Helmet", "Without Helmet"]

# Path to your VOC dataset folder containing XML files
voc_annotations_path = "C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\dataset\\annotations\\"

# Convert each XML annotation to YOLO format
xml_files = glob.glob(os.path.join(voc_annotations_path, "*.xml"))
print((len(xml_files)))
for xml_file in xml_files:
    convert_annotation(xml_file, classes)
