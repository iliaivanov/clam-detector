# Clam detector
This script was inspired by my family travel to Italy. I collected a lot of beautiful clams on the beach and got an idea to create kinda board with these shells ordered by size. Measure them manually was to durty, so that's how this script was created :)

# Usage
1. Clone project `git clone git@github.com:iliaivanov/clam-detector.git`.
2. Install required Python libraries (_argparse_, _imutils_, _cv2_).
3. Copy your images to the desired directory inside the project (you can replace existing images in `clam_shelter` directory and use it, or create your own).
4. Execute script.

Parameters:
- `-d` Clams directory to look images from.
- `-v` Eather display clam image or not (true, false)? Clams will be displayed desc. Defaul false.

`python3 order_clams.py -d clam_shelter -v true`
