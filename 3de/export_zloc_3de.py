#
#
# 3DE4.script.name:    Export ZLOC...
#
# 3DE4.script.version:    v0.1.0
#
# 3DE4.script.gui:    Main Window::3DE4::File::Export
# 3DE4.script.gui:    Object Browser::Context Menu Point
# 3DE4.script.gui:    Object Browser::Context Menu Points
# 3DE4.script.gui:    Object Browser::Context Menu PGroup
#
# 3DE4.script.comment:    Exports selected trackers to ZLOC file.
# 3DE4.script.comment:    Author: Hyuk Ko (kohyuk91@gmail.com)
#
# Original Script:    export_tracks.py(by Science-D-Visions)
#

from vl_sdv import *
import __builtin__ as builtin

import os
import tempfile

TEMPDIR = tempfile.gettempdir()

c = tde4.getCurrentCamera()
pg = tde4.getCurrentPGroup()
lens = tde4.getCameraLens(c)

if c!=None and pg!=None:
    n = tde4.getCameraNoFrames(c)
    p = tde4.getContextMenuObject() # check if context menu has been used, and retrieve point...
    if p!=None:
        pg = tde4.getContextMenuParentObject() # retrieve point's parent pgroup (not necessarily being the current one!)...
        l = tde4.getPointList(pg, 1)
    else:
        l = tde4.getPointList(pg, 1) # otherwise use regular selection...
    if len(l)>0:
        req = tde4.createCustomRequester()
        tde4.addFileWidget(req,"manual_path","Manual Path","*.zloc")
        tde4.addTextFieldWidget(req,"quick_path","Quick Path","*.zloc")
        tde4.addTextFieldWidget(req, "frame_offset_field", "Frame Offset","0")
        tde4.addToggleWidget(req,"remove_distortion","Remove Distortion",1)
        tde4.addToggleWidget(req,"2.5d","2.5D",1)

        tde4.setWidgetValue(req, "quick_path", os.path.join(TEMPDIR, "quick.zloc"))
        tde4.setWidgetSensitiveFlag(req, "quick_path", 0)
        tde4.setWidgetValue(req, "frame_offset_field", builtin.str(tde4.getCameraSequenceAttr(c)[0]-1))

        ret = tde4.postCustomRequester(req, "Export ZLOC...", 500, 0, "Manual", "Quick", "Cancel")
        if ret==1:
            path = tde4.getWidgetValue(req,"manual_path")
            if path.find(".zloc",len(path)-5)==-1: path += ".zloc"
        if ret==2:
            path = tde4.getWidgetValue(req,"quick_path")
        if ret==3:
            path = None

        offset = int(tde4.getWidgetValue(req,"frame_offset_field"))
        rd = tde4.getWidgetValue(req,"remove_distortion")
        twopointfive = tde4.getWidgetValue(req,"2.5d")

        if twopointfive==1:
            w_fb_inch = tde4.getLensFBackWidth(lens)/2.54
            h_fb_inch = tde4.getLensFBackHeight(lens)/2.54
        else:
            w_fb_inch = 1.0
            h_fb_inch = 1.0

        if offset<0:
            offset = 0
        if path!=None:
            #
            # main block...
            f = open(path,"w")
            if not f.closed:
                for point in l:
                    name = tde4.getPointName(pg,point)
                    c2d = tde4.getPointPosition2DBlock(pg,point,c,1,n)
                    if twopointfive==1:
                        color = tde4.getPointColor2D(pg,point)
                    else:
                        color = ""
                    n0 = 0
                    for v in c2d:
                        if v[0]!=-1.0 and v[1]!=-1.0: n0 += 1
                    frame = 1+offset
                    for v in c2d:
                        if v[0]!=-1.0 and v[1]!=-1.0:
                            if rd: v = tde4.removeDistortion2D(c, frame-offset, v)
                            f.write("%s %d %.15f %.15f %s\n"%("zloc"+name,frame,(v[0]-0.5)*w_fb_inch,(v[1]-0.5)*h_fb_inch,color))
                        frame += 1
                f.close()
            else:
                tde4.postQuestionRequester("Export ZLOC...","Error, couldn't open file.","Ok")

            # end main block...
            #
    else:
        tde4.postQuestionRequester("Export ZLOC...","There are no selected points.","Ok")
else:
    tde4.postQuestionRequester("Export ZLOC...","There is no current Point Group or Camera.","Ok")
