# cvat.py

Alex Beng's validation scripts(mainly python) for [cvat](https://github.com/GengGode/cvAutoTrack)

## setup

This repo needs the opencv-python with `BUILD_opencv_python3`, `OPENCV_ENABLE_NONFREE` and `OPENCV_EXTRA_MODULES_PATH` enabled and manually installed.

## GI visual odometer
- [ ] simple 2d frame-frame
- [ ] frame-map


## Filter-based Multi-source GI location

- [ ] capture/video/other source
- [ ] feature-match GI location
- [ ] template-match-based GI location
- [ ] odemeter
- [ ] filter-based or optimization-based location
    - [ ] filter-based, simple KF
    - [ ] with non-linear mouse model, ESKF.
    - [ ] frameSLAM, only opt the pose without loop closure. opt in se(2) space.

## sequence to path/trajectory

- [ ] reused the Filter-based location
- [ ] path/trajectory generation (algorithm needed)
  
## anchor-based big map location

- [ ] GI anchor detection
- [ ] anchor data parser
- [ ] RANSAC-based loaction

## SLAM-based 3D-2D fusion

- [ ] run the SLAM 
- [ ] ground finding (RANSAC may be used)
- [ ] 3D-2D fusion
