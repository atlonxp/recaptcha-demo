#!/bin/bash
./darknet detector test coco.data yolo-cutoff-18.cfg yolo-cutoff-18_600.weights data/payload.jpg
