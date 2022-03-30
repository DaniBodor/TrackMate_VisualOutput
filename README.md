# TrackMate_VisualOutput

This code runs [TrackMate](https://imagej.net/plugins/trackmate/) through FiJi/ImageJ on a set of images and exports xml files that can be read by back in FiJi/ImageJ to show the visual output of tracking.

Output files (\*.xml) need to be loaded using the 'Load a TrackMate file' plugin in ImageJ (Plugins>Tracking>Load a TrackMate file). 

Settings can be adjusted in the first few lines of the code and are explained there and correspons to settings that would have been set manually in TrackMate (see paragraph 1.14 of the [TrackMate manual](https://imagej.net/plugins/trackmate/#documentation-and-tutorials))


## Source
The code is largely copied from https://imagej.net/plugins/trackmate/scripting#a-full-example. A few adjustments are:
- Cell detection is done via the [StarDist integration of TrackMate](https://imagej.net/plugins/trackmate/trackmate-stardist).
- The code is looped over a set of images and saves the visual output rather than running on a single image.
- Tracking and visual output settings are changed.


## Before first run
For this code to work, you must have the following update sites activated in your FiJi (check [here](https://imagej.net/update-sites/following) to see how to do this):
- CSBDeep
- StarDist
- TrackMate-Stardist


## Citation
#### For TrackMate, please cite:  
Ershov, D., Phan, M.-S., Pylvänäinen, J. W., Rigaud, S. U., Le Blanc, L., Charles-Orszag, A., … Tinevez, J.-Y. (2021, September 3). Bringing TrackMate into the era of machine-learning and deep-learning. Cold Spring Harbor Laboratory. https://doi.org/10.1101/2021.09.03.458852

and / or

Tinevez, J.-Y., Perry, N., Schindelin, J., Hoopes, G. M., Reynolds, G. D., Laplantine, E., … Eliceiri, K. W. (2017). TrackMate: An open and extensible platform for single-particle tracking. Methods, 115, 80–90. https://doi.org/10.1016/j.ymeth.2016.09.016


#### For StarDist, please cite:
Uwe Schmidt, Martin Weigert, Coleman Broaddus, and Gene Myers. Cell Detection with Star-convex Polygons. International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI), Granada, Spain, September 2018. https://doi.org/10.1007/978-3-030-00934-2_30