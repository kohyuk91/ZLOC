#
#
# 3DE4.script.name:    Import ZLOC...
#
# 3DE4.script.version:    v0.1.0
#
# 3DE4.script.gui:    Main Window::3DE4::File::Export
# 3DE4.script.gui:    Object Browser::Context Menu Point
# 3DE4.script.gui:    Object Browser::Context Menu Points
# 3DE4.script.gui:    Object Browser::Context Menu PGroup
#
# 3DE4.script.comment:    Imports 2D tracking curves from ZLOC file.
# 3DE4.script.comment:    Author: Hyuk Ko (kohyuk91@gmail.com)
#
# Original Script:    import_tracks.py(by Science-D-Visions)
#

import os
import tempfile

TEMPDIR = tempfile.gettempdir()

#
# main script...

c = tde4.getCurrentCamera()
pg = tde4.getCurrentPGroup()
if c!=None and pg!=None:

    req = tde4.createCustomRequester()
    tde4.addFileWidget(req,"manual_path","Manual Path","*.zloc")
    tde4.addTextFieldWidget(req,"quick_path","Quick Path")
    tde4.addTextFieldWidget(req,"frame_offset_field","Frame Offset","0")

    tde4.setWidgetValue(req, "quick_path", os.path.join(TEMPDIR, "quick.zloc"))
    tde4.setWidgetSensitiveFlag(req, "quick_path", 0)

    ret = tde4.postCustomRequester(req,"Import ZLOC...",500,0,"Manual","Quick","Cancel")
    if ret==1:
        path = tde4.getWidgetValue(req,"manual_path")
    if ret==2:
        path = tde4.getWidgetValue(req,"quick_path")
    if ret==3:
        path = None

    if path!=None:
        offset = int(tde4.getWidgetValue(req,"frame_offset_field"))
        with open(path,'r') as f:
            word_list = [word for line in f for word in line.split()]

        zloc_list = sorted(set(word_list[0::4]),key=word_list.index)
        group_word_by_four_list = [word_list[i:i+4] for i in range(0, len(word_list), 4)]

        for zloc in zloc_list:
            p = tde4.createPoint(pg)
            tde4.setPointName(pg,p,zloc)

            for i in range(len(group_word_by_four_list)):
                if group_word_by_four_list[i][0] == zloc:
                    tde4.setPointPosition2D(pg,p,c,int(group_word_by_four_list[i][1])+offset,[float(group_word_by_four_list[i][2])+0.5,float(group_word_by_four_list[i][3])+0.5])
    else:
        tde4.postQuestionRequester("Import ZLOC...","Error, couldn't open file.","Ok")
