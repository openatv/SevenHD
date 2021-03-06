# -*- coding: UTF-8 -*-
#######################################################################
#
# SevenHD by Team Kraven
# 
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#######################################################################
from GlobalImport import *
#######################################################################
lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SevenHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SevenHD/locale/"))

def _(txt):
	t = gettext.dgettext("SevenHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block
########################################################################
class MenuSettings(ConfigListScreen, Screen):
    skin = """
                  <screen name="SevenHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
                         <widget name="buttonRed" font="Regular; 20" foregroundColor="#00f23d21" backgroundColor="#00000000" halign="left" valign="center" position="64,662" size="148,48" transparent="1" />
                         <widget name="buttonGreen" font="Regular; 20" foregroundColor="#00389416" backgroundColor="#00000000" halign="left" valign="center" position="264,662" size="148,48" transparent="1" />
                         <widget name="buttonYellow" font="Regular; 20" foregroundColor="#00e5b243" backgroundColor="#00000000" halign="left" valign="center" position="464,662" size="148,48" transparent="1" />
                         <widget name="buttonBlue" font="Regular; 20" foregroundColor="#000064c7" backgroundColor="#00000000" halign="left" valign="center" position="664,662" size="148,48" transparent="1" />
                         <widget name="config" position="18,72" size="816,575" scrollbarMode="showOnDemand" transparent="1" zPosition="1" backgroundColor="#00000000" />
                         <widget name="titel" position="70,12" size="708,46" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget name="colorthump" position="891,220" size="372,30" zPosition="1" backgroundColor="#00000000" alphatest="blend" />
                         <widget name="helperimage" position="891,274" size="372,209" zPosition="1" backgroundColor="#00000000" />
                         <widget name="description" position="891,490" size="372,200" font="Regular; 22" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
                         <widget backgroundColor="#00000000" font="Regular2; 34" foregroundColor="#00ffffff" position="70,12" render="Label" size="708,46" source="Title" transparent="1" halign="center" valign="center" noWrap="1" />
                         <eLabel backgroundColor="#00000000" position="6,6" size="842,708" transparent="0" zPosition="-9" foregroundColor="#00ffffff" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="842,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,714" size="844,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="6,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="848,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,64" size="816,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="18,656" size="816,2" zPosition="2" />
                         <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="ClockToText">Default</convert>
                         </widget>
                         <eLabel backgroundColor="#00000000" position="878,6" size="396,708" transparent="0" zPosition="-9" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="396,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,714" size="398,2" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="878,6" size="2,708" zPosition="2" />
                         <eLabel backgroundColor="#00ffffff" position="1274,6" size="2,708" zPosition="2" />
                         <widget source="session.CurrentService" render="Label" position="891,88" size="372,46" font="Regular2;35" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
                                 <convert type="SevenHDUpdate">Version</convert>
                         </widget>
                         <widget source="session.CurrentService" render="Label" position="891,134" size="372,28" font="Regular;26" halign="center" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00B27708">
                                 <convert type="SevenHDUpdate">Update</convert>
                         </widget>
                         <eLabel position="891,274" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,481" size="372,2" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="891,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                         <eLabel position="1261,274" size="2,208" backgroundColor="#00ffffff" zPosition="5" />
                  </screen>
               """

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self.ColorLoad = ePicLoad()
        self["colorthump"] = Pixmap()
        self["helperimage"] = Pixmap()
        self["description"] = Label()
        self["buttonRed"] = Label()
        self["buttonGreen"] = Label()
        self["buttonYellow"] = Label()
        self["buttonBlue"] = Label()
        self["titel"] = Label()
        self["buttonRed"].setText(_("Cancel"))
        self["buttonGreen"].setText(_("Save"))
        self["buttonYellow"].setText(_("Defaults"))
        self["titel"].setText(_("Menu Settings"))
        
        if config.plugins.SevenHD.grabdebug.value:
           self["buttonBlue"].setText('Screenshot')
           
        ConfigListScreen.__init__(
            self,
            self.getMenuItemList(),
            session = session,
            on_change = self.__selectionChanged
        )

        self["actions"] = ActionMap(
        [
            "OkCancelActions",
            "DirectionActions",
            "InputActions",
            "ColorActions"
        ],
        {
            "left": self.keyLeft,
            "down": self.keyDown,
            "up": self.keyUp,
            "right": self.keyRight,
            "red": self.exit,
            "yellow": self.defaults,
            "green": self.save,
            "blue": self.grab_png,
            "cancel": self.exit
        }, -1)

        self.onLayoutFinish.append(self.UpdatePicture)

    def getMenuItemList(self):
        
        list = []
        list.append(getConfigListEntry(_('_____________________________background________________________________________'), ))
        list.append(getConfigListEntry(_("main window"),        config.plugins.SevenHD.BackgroundLeft,             'Stellt die Farbe des linken Fenster ein.',                         '4',     'Main'))
        if config.plugins.SevenHD.BackgroundLeft.value=="back_gradient_main":
            list.append(getConfigListEntry(_("gradient top"),       config.plugins.SevenHD.GradientMenuTop,        'Stellt die obere Farbe vom Farbverlauf des linken Fenster ein.',   '4',     'Main'))
            list.append(getConfigListEntry(_("gradient bottom"),    config.plugins.SevenHD.GradientMenuBottom,     'Stellt die untere Farbe vom Farbverlauf des linken Fenster ein.',  '4',     'Right'))
        list.append(getConfigListEntry(_("main window right"),  config.plugins.SevenHD.BackgroundRight,        'Stellt die Farbe des rechten Fenster ein.',                        '4',     'Right'))
        if config.plugins.SevenHD.BackgroundRight.value=="back_gradient_right":
            list.append(getConfigListEntry(_("gradient top"),       config.plugins.SevenHD.GradientMenuRightTop,   'Stellt die obere Farbe vom Farbverlauf des rechten Fenster ein.',  '4',     'Main'))
            list.append(getConfigListEntry(_("gradient bottom"),    config.plugins.SevenHD.GradientMenuRightBottom,'Stellt die untere Farbe vom Farbverlauf des rechten Fenster ein.', '4',     'Right'))
        list.append(getConfigListEntry(_('_____________________________sytem menu________________________________________'), ))
        list.append(getConfigListEntry(_("show icons"),          config.plugins.SevenHD.Logo,                   'Auswahl der Darstellung von den Systemmen\xc3\xbcs.',             '1',     ''))
        list.append(getConfigListEntry(_('__________________________________transparency_____________________________________________'), ))
        list.append(getConfigListEntry(_("main window"),        config.plugins.SevenHD.BackgroundLeftColorTrans,      'Stellt die Transparenz des linken Fenster ein.',                '4',      'transparency'))
        list.append(getConfigListEntry(_("main window right"),  config.plugins.SevenHD.BackgroundRightColorTrans, 'Stellt die Transparenz des rechten Fenster ein.',               '4',      'transparencyright'))
        list.append(getConfigListEntry(_('_____________________________color lines_______________________________________'), ))
        list.append(getConfigListEntry(_("line leftside"),      config.plugins.SevenHD.Line,                   'Stellt die Farbe der Linie f\xc3\xbcr die linke Seite ein.',       '4',     'Line'))
        list.append(getConfigListEntry(_("line rightside"),     config.plugins.SevenHD.LineRight,              'Stellt die Farbe der Linie f\xc3\xbcr die rechte Seite ein.',      '4',     'Line'))
        list.append(getConfigListEntry(_("border leftside"),    config.plugins.SevenHD.Border,                 'Stellt die Rahmenfarbe f\xc3\xbcr die linke Seite ein.',           '4',     'Border'))
        list.append(getConfigListEntry(_("border rightside"),   config.plugins.SevenHD.BorderRight,            'Stellt die Rahmenfarbe f\xc3\xbcr die rechte Seite ein.',          '4',     'Border'))
        list.append(getConfigListEntry(_("progressbar"),        config.plugins.SevenHD.Progress,               'Stellt die Farbe des Fortschrittbalkens ein.',                     '4',     'Progress'))
        list.append(getConfigListEntry(_("progressbar line"),   config.plugins.SevenHD.ProgressLinePlug,       'Stellt die Farbe der Linie unter des Fortschrittbalkens ein.',     '4',     'Progress'))
        list.append(getConfigListEntry(_('______________________________color font________________________________________'), ))
        list.append(getConfigListEntry(_("primary font"),       config.plugins.SevenHD.Font1,                  'Stellt die Schriftfarbe der Liste ein.',                           '4',     'Font1'))
        list.append(getConfigListEntry(_("secondary font"),     config.plugins.SevenHD.Font2,                  'Stellt die Schriftfarbe der Beschreibung ein.',                    '4',     'Font2'))
        list.append(getConfigListEntry(_("button text"),        config.plugins.SevenHD.ButtonText,             'Stellt die Schriftfarbe der Farbtastenbeschreibung ein.',          '4',     'Buttontext'))
        return list

    def __selectionChanged(self):
        self["config"].setList(self.getMenuItemList())

    def GetPicturePath(self):
        returnValue = self["config"].getCurrent()[3]		
           		
        if returnValue == '4':
           returnValue = self["config"].getCurrent()[int(returnValue)]
        else:
           returnValue = self["config"].getCurrent()[int(returnValue)].value
         
        path = MAIN_IMAGE_PATH + str(returnValue) + str(".jpg")
        
        self["description"].setText(self["config"].getCurrent()[2])
        
        if fileExists(path):
           return path
        else:
           self.debug('Missing Picture: ' + str(path) + '\n')
           return MAIN_IMAGE_PATH + str("924938.jpg")

    def UpdatePicture(self):
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.UpdateColor()
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        self["description"].setText(self["config"].getCurrent()[4])
        self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.PicLoad.startDecode(self.GetPicturePath())

    def DecodePicture(self, PicInfo = ""):
        ptr = self.PicLoad.getData()
        self["helperimage"].instance.setPixmap(ptr)

    def UpdateColor(self):
        self.ColorLoad.PictureData.get().append(self.DecodeColor)
        self.onLayoutFinish.append(self.ShowColor)

    def ShowColor(self):
        self.ColorLoad.setPara([self["colorthump"].instance.size().width(),self["colorthump"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
        self.ColorLoad.startDecode(self.getFontColor())

    def DecodeColor(self, PicInfo = ""):
        ptr = self.ColorLoad.getData()
        self["colorthump"].instance.setPixmap(ptr)
    
    def getFontColor(self):   
        returnValue = self["config"].getCurrent()[1]
        
        self["colorthump"].instance.show()
        preview = ''
        
        if returnValue == config.plugins.SevenHD.Line:
              preview = self.generate(config.plugins.SevenHD.Line.value)
        elif returnValue == config.plugins.SevenHD.LineRight:
              preview = self.generate(config.plugins.SevenHD.LineRight.value)
        elif returnValue == config.plugins.SevenHD.BackgroundLeft:
              preview = self.generate(config.plugins.SevenHD.BackgroundLeft.value)
        elif returnValue == config.plugins.SevenHD.BackgroundRight:
              preview = self.generate(config.plugins.SevenHD.BackgroundRight.value)
        elif returnValue == config.plugins.SevenHD.Border:
              preview = self.generate(config.plugins.SevenHD.Border.value)
        elif returnValue == config.plugins.SevenHD.BorderRight:
              preview = self.generate(config.plugins.SevenHD.BorderRight.value)
        elif returnValue == config.plugins.SevenHD.Progress:
              preview = self.generate(config.plugins.SevenHD.Progress.value)
        elif returnValue == config.plugins.SevenHD.Font1:
              preview = self.generate(config.plugins.SevenHD.Font1.value)
        elif returnValue == config.plugins.SevenHD.Font2:
              preview = self.generate(config.plugins.SevenHD.Font2.value)
        elif returnValue == config.plugins.SevenHD.ButtonText:
              preview = self.generate(config.plugins.SevenHD.ButtonText.value)
        elif returnValue == config.plugins.SevenHD.ProgressLinePlug:
              preview = self.generate(config.plugins.SevenHD.ProgressLinePlug.value)
        elif returnValue == config.plugins.SevenHD.GradientMenuTop:
              preview = self.generate(config.plugins.SevenHD.GradientMenuTop.value)
        elif returnValue == config.plugins.SevenHD.GradientMenuBottom:
              preview = self.generate(config.plugins.SevenHD.GradientMenuBottom.value)
        elif returnValue == config.plugins.SevenHD.GradientMenuRightTop:
              preview = self.generate(config.plugins.SevenHD.GradientMenuRightTop.value)
        elif returnValue == config.plugins.SevenHD.GradientMenuRightBottom:
              preview = self.generate(config.plugins.SevenHD.GradientMenuRightBottom.value)
        else:
              self["colorthump"].instance.hide()
        return str(preview)
        
    def generate(self,color):    
        
        if color.startswith('00'):
           r = int(color[2:4], 16)
           g = int(color[4:6], 16)
           b = int(color[6:], 16)

           img = Image.new("RGB",(372,30),(r,g,b))
           img.save(str(MAIN_IMAGE_PATH) + "color.png")
           return str(MAIN_IMAGE_PATH) + "color.png"
        
        elif 'progress' in color:
           return str(MAIN_IMAGE_PATH) + "progress.png"
        elif 'carbon' in color:
           return str(MAIN_IMAGE_PATH) + "carbon.png"
        elif 'lightwood' in color:
           return str(MAIN_IMAGE_PATH) + "lightwood.png"
        elif 'redwood' in color:
           return str(MAIN_IMAGE_PATH) + "redwood.png"
        elif 'slate' in color:
           return str(MAIN_IMAGE_PATH) + "slate.png"
        elif 'brownleather' in color:
           return str(MAIN_IMAGE_PATH) + "brownleather.png"
        elif 'gradient' in color:
           return str(MAIN_IMAGE_PATH) + "gradient.png"
        
    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.ShowPicture()
        self.ShowColor()
    
    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.ShowPicture()
        self.ShowColor()
    
    def keyDown(self):
        self["config"].instance.moveSelection(self["config"].instance.moveDown)
        self.ShowPicture()
        self.ShowColor()
    
    def keyUp(self):
        self["config"].instance.moveSelection(self["config"].instance.moveUp)
        self.ShowPicture()
        self.ShowColor()
        
    def grab_png(self):
        if config.plugins.SevenHD.grabdebug.value:
           os.system('grab -p /tmp/kraven_debug.png')
           self.session.open(MessageBox, _('Debug Picture\n"kraven_debug.png" saved in /tmp\n'), MessageBox.TYPE_INFO)
           
    def defaults(self):
        self.setInputToDefault(config.plugins.SevenHD.BackgroundLeft)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundRight)
        self.setInputToDefault(config.plugins.SevenHD.Line)
        self.setInputToDefault(config.plugins.SevenHD.Border)
        self.setInputToDefault(config.plugins.SevenHD.LineRight)
        self.setInputToDefault(config.plugins.SevenHD.BorderRight)
        self.setInputToDefault(config.plugins.SevenHD.Font1)
        self.setInputToDefault(config.plugins.SevenHD.Font2)
        self.setInputToDefault(config.plugins.SevenHD.ButtonText)
        self.setInputToDefault(config.plugins.SevenHD.ProgressLinePlug)
        self.setInputToDefault(config.plugins.SevenHD.Progress)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundLeftColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.BackgroundRightColorTrans)
        self.setInputToDefault(config.plugins.SevenHD.Logo)
        self.setInputToDefault(config.plugins.SevenHD.GradientMenuTop)
        self.setInputToDefault(config.plugins.SevenHD.GradientMenuBottom)
        self.setInputToDefault(config.plugins.SevenHD.GradientMenuRightTop)
        self.setInputToDefault(config.plugins.SevenHD.GradientMenuRightBottom)
        self.save()

    def setInputToDefault(self, configItem):
        configItem.setValue(configItem.default)

    def showInfo(self):
        self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

    def save(self):
        
        if config.plugins.SevenHD.skin_mode.value > '3':
           if 'back' in config.plugins.SevenHD.BackgroundLeft.value:
              self.setInputToDefault(config.plugins.SevenHD.BackgroundLeft)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
           if 'back' in config.plugins.SevenHD.BackgroundRight.value:
              self.setInputToDefault(config.plugins.SevenHD.BackgroundRight)
              self.session.open(MessageBox, _('Sorry, only Colors allowed.'), MessageBox.TYPE_INFO)
        
        for x in self["config"].list:
            if len(x) > 1:
                x[1].save()
            else:
                pass

        configfile.save()
        self.exit()

    def exit(self):
        for x in self["config"].list:
            if len(x) > 1:
                    x[1].cancel()
            else:
                    pass
        self.close()
    
    def debug(self, what):
        if config.plugins.SevenHD.msgdebug.value:
           try:
              self.session.open(MessageBox, _('[MenuSettings]\n' + str(what)), MessageBox.TYPE_INFO)
           except:
              pass
              
        if config.plugins.SevenHD.debug.value:
           f = open('/tmp/kraven_debug.txt', 'a+')
           f.write('[MenuSettings]' + str(what) + '\n')
           f.close() 