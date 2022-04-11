## the vast majority of this code is copied from https://imagej.net/plugins/trackmate/scripting#a-full-example


#### PARAMETERS
# input
input_dir = r"C:\Users\dani\Documents\MyCodes\TrackMate_VisualOutput\TEST\LongTracking_1"	# make sure to start with r before the quotation marks
filetype = "tif"	# extension of files to analyze (empty includes all extensions)
namefilter = ""	# only include files with this in the name (empty includes all files)

# tracking settings
linking_distance = 30	# max distance (in image units) by which spots can be linked into a track
gap_closing_frames = 5	# max number of frames over which a spot can be lost and still linked to a track (set to 0 to turn off)
gap_closing_distance = linking_distance # max distance (in image units) by which spots can be linked into a track after losing a spot for at least 1 frame
allow_splitting = False	# must be True or False (watch the capitalization)
splitting_distance = linking_distance	# max distance (in image units) by which spots can be linked into a single split track
allow_merging = False	# must be True or False
merging_distance = linking_distance	# max distance (in image units) from spots can be merge into a single track

# display settings
spot_transparency = 0.25	# transparency of spot color overlay
track_fade_range = 10	# number of frames over which tracks fade in time
track_direction = "both"	# options are "forward", "backward", or "both"; make sure to put in quotation marks


#### IMPORT LIBRARIES
import sys
import os
import java.io.File as File

from ij import IJ
from ij import WindowManager

from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.stardist import StarDistDetectorFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettings
from fiji.plugin.trackmate.gui.displaysettings.DisplaySettings import TrackMateObject
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.io.TmXmlWriter as TmXmlWriter



# clear memory
for x in range(3):
	IJ.run("Collect Garbage", "");


# ensure that are values are floats rather than ints (don't change these)
linking_distance = float(linking_distance)
gap_closing_distance = float(gap_closing_distance)
splitting_distance = float(splitting_distance)
merging_distance = float(merging_distance)
spot_transparency = float(spot_transparency)


#### DEFINE TRACKMATE FUNCTION, MAIN BODY OF CODE
def doTrackMate(path):

	# Open image from file
	imp = IJ.openImage(path)
#	imp.show()	# displays image on screen (kinda useless, especially because TrackMate progress is not seen on image)


	# Get currently selected image
	# DB: keeping this for troubleshooting purposes
#	imp = WindowManager.getCurrentImage()


	# Set to grayscale and Convert Z-stack to T-stack
	IJ.run(imp, "Grays", "");
	width, height, nChannels, nSlices, nFrames = imp.getDimensions()
	if nFrames == 1 and nSlices > 1:
		imp.setDimensions( nChannels, nFrames, nSlices)
		IJ.log("swapped T and Z dimensions")
		IJ.run(imp, "Save", "");


	#----------------------------
	# Create the model object now
	#----------------------------

	# Some of the parameters we configure below need to have a reference to the model at creation. So we create an empty model now.
	model = Model()
	# Send all messages to ImageJ log window.
	model.setLogger(Logger.IJ_LOGGER)


	#------------------------
	# Prepare settings object
	#------------------------
	settings = Settings(imp)

	#### Configure detector
	settings.detectorFactory = StarDistDetectorFactory()
	settings.detectorSettings = {'TARGET_CHANNEL' : 1}

	# Configure spot filters - Classical filter on quality
	# DB: not using any filters on these
#	filter1 = FeatureFilter('QUALITY', 30, True)
#	settings.addSpotFilter(filter1)


	#### Configure tracker and settings
	settings.trackerFactory = SparseLAPTrackerFactory()
	settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() # almost good enough; can't find what defaults are anywhere
	settings.trackerSettings['LINKING_MAX_DISTANCE'] = linking_distance
	settings.trackerSettings['ALLOW_GAP_CLOSING'] = True
	settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = gap_closing_distance
	settings.trackerSettings['MAX_FRAME_GAP'] = gap_closing_frames
	settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = allow_splitting
	settings.trackerSettings['SPLITTING_MAX_DISTANCE'] = splitting_distance
	settings.trackerSettings['ALLOW_TRACK_MERGING'] = allow_merging
	settings.trackerSettings['MERGING_MAX_DISTANCE'] = merging_distance


	# Add ALL the feature analyzers known to TrackMate. They will yield numerical features for the results, such as speed, mean intensity etc.
	settings.addAllAnalyzers()
	# Configure track filters - minimum displacement
	#DB: not using any track filters either
#	filter2 = FeatureFilter('TRACK_DISPLACEMENT', 10, True)
#	settings.addTrackFilter(filter2)


	#-------------------
	# Instantiate plugin
	#-------------------

	trackmate = TrackMate(model, settings)

	#--------
	# Process
	#--------

	ok = trackmate.checkInput()
	if not ok:
	    sys.exit(str(trackmate.getErrorMessage()))

	ok = trackmate.process()
	if not ok:
	    sys.exit(str(trackmate.getErrorMessage()))


	#----------------
	# Display results
	#----------------

	# A selection.
	selectionModel = SelectionModel( model )

	# Read the default display settings.
	ds = DisplaySettingsIO.readUserDefault()
	# adjust settings
	ds.setSpotFilled(True)
	ds.setSpotTransparencyAlpha(spot_transparency)
	ds.setSpotColorBy(TrackMateObject.TRACKS, "TRACK_INDEX")
	ds.setTrackColorBy(TrackMateObject.TRACKS, "TRACK_INDEX")
	ds.setFadeTracks(True)
	ds.setFadeTrackRange(track_fade_range)
	if track_direction == "forward":
		ds.setTrackDisplayMode(ds.TrackDisplayMode.LOCAL_FORWARD)
	elif track_direction == "backward":
		ds.setTrackDisplayMode(ds.TrackDisplayMode.LOCAL_BACKWARD)
	elif track_direction == "both":
		ds.setTrackDisplayMode(ds.TrackDisplayMode.LOCAL)

	# Save display settings to default
#	DisplaySettingsIO.saveToUserDefault(ds)


	#----------------
	# Show results on screen
	#----------------

	#displayer = HyperStackDisplayer( model, selectionModel, imp, ds )
	#displayer.render()
	#displayer.refresh()

	# Echo results with the logger we set at start:
	#DB: this prints all the excess info we don't need
#	model.getLogger().log( str( model ) )


	#----------------
	# Export results to file
	#----------------

	if filetype:
		outFile = File(path[:-ext_len] + ".xml")
	else:
		outFile = File(path + ".xml")

	writer = TmXmlWriter(outFile)
	writer.appendModel(model)
	writer.appendSettings(settings)
	writer.appendDisplaySettings(ds)
	writer.writeToFile()


	# free up memory
	imp.close()
	for x in range(3):
		IJ.run("Collect Garbage", "");


######## RUN CODE ON FOLDER

IJ.log("\\Clear")
# We have to do the following to avoid errors with UTF8 chars generated in TrackMate that will mess with our Fiji Jython.
reload(sys)
sys.setdefaultencoding('utf-8')


im_list = os.listdir(input_dir)
ext_len = len(filetype)+1
if filetype:	# only analyze files with correct extension
	im_list = [x for x in im_list if x[-ext_len:] == "." + filetype ]
if namefilter:	# only analyze files with correct filename filter
	im_list = [x for x in im_list if namefilter in x]


IJ.log("start")

for i, image in enumerate(im_list):
	path = os.path.join(input_dir,image)
	IJ.log("####### running TrackMate on " + image + " (image "+str(i+1)+" of "+str(len(im_list)) + ") #######" )
	doTrackMate(path)
	IJ.log("finished " + image + "\n")

# remind to cite trackmate and stardist papers
IJ.log("")
IJ.log("if using this in a publication, be sure to cite the following papers: ")
papers = [	"https://doi.org/10.1016/j.ymeth.2016.09.016 (2017 Methods - TrackMate: An open and extensible platform for single-particle tracking)",
			"https://doi.org/10.1101/2021.09.03.458852 (2021 bioRxiv - Bringing TrackMate into the era of machine-learning and deep-learning)",		# 2021 bioRxiv: Bringing TrackMate into the era of machine-learning and deep-learning
		  	"https://doi.org/10.1007/978-3-030-00934-2_30 (2018 MICCAI - Cell Detection with Star-Convex Polygons)",								# 2018 MICCAI: Cell Detection with Star-Convex Polygons
		 ]
for p in papers:
	IJ.log("- " + p)


IJ.log("\nALL DONE")
