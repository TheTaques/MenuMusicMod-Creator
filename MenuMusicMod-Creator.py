import os
import sys
import shutil
import re
from appJar import gui

#set working directory for appJar icon
if getattr( sys, 'frozen', False ) :
        os.chdir(sys._MEIPASS)
else :
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

dir_path = os.path.dirname(os.path.abspath(__file__))

# return object class for create_folders()
class modloc(object):
    def __init__(self, modroot, name):
        self.modroot = modroot
        self.loc = '{0}/Loc'.format(modroot)
        self.music = '{0}\Assets\music\{1}'.format(modroot, name)


# this function creates every folder needed for the mod
def create_folders(root, name):
    modroot = '{0}\{1}'.format(root, name)
    os.makedirs('{0}\Assets\music\{1}'.format(modroot, name))
    os.mkdir('{0}\Loc'.format(modroot))
    return modloc(modroot, name)


def move_file(modloc, musicfile):
    # move music.movie to modroot/Assets/music/musicname/
    shutil.copy2(musicfile, modloc.music)
    return


def create_main(modloc, filename, super):
    # create main.xml in modroot/
    if super:
        with open('{0}/main.xml'.format(modloc.modroot), 'w') as outfile:
            outfile.write(
                '<table name="{0}">\n    <Localization directory="Loc" default="EN.txt"/>\n    <MenuMusic id="{0}" source="music/{0}.ogg"/>\n</table>'.format(filename))
        return
    else:
        with open('{0}/main.xml'.format(modloc.modroot), 'w') as outfile:
            outfile.write('<table name="{0}">\n    <Localization directory="Loc" default="EN.txt"/>\n    <Music id="{0}" directory="music/{0}" source="{0}" menu="true" heist="false"/>\n</table>'.format(filename))
        return


def create_locale(modloc, filename, musicname):
    # create EN.txt in modroot/Loc/
    with open('{0}/EN.txt'.format(modloc.loc), 'w') as outfile:
        outfile.write('{{\n    "menu_jukebox_{0}" : "{1}",\n    "menu_jukebox_screen_{0}" : "{1}"\n}}'.format(filename, musicname))
    return


# -----------------Main function-----------------
# Function to be called at gui button press.
def makeithappen(button_name):
    modname = app.getEntry('modname')
    moddir = app.getEntry('moddir')
    musicname = app.getEntry('musicname')
    musicfile = app.getEntry('musicfile')
    
    try:
        musicfile_name = re.search('.*/(.*?)\.movie', musicfile).group(1)
    except:
        app.infoBox('ERROR', 'Music file has the wrong format!')
        return

    # check if names are ok
    if modname == '' or re.match('^[a-zA-Z0-9_-]*$', modname) is None:
        app.infoBox('ERROR', 'Invalid mod name!')
        return
    elif musicname == '' or re.match('^[ a-zA-Z0-9_-]*$', musicname) is None:
        app.infoBox('ERROR', 'Invalid music name!')
        return

    # check if mod folder already exists
    if os.path.exists('{0}\{1}'.format(moddir, modname)):
        app.infoBox('ERROR', 'Mod folder already exists!')
        return

    # check if music file exists and is a ".movie" file.
    # also check if music file name contains only alphanumeric characters, underscores and hyphens
    if not os.path.isfile(musicfile):
        app.infoBox('ERROR', 'Music file does not exist!')
        return
    elif musicfile_name == '' or re.match('^[a-zA-Z0-9_-]*$', musicfile_name) is None:
        app.infoBox('ERROR', 'Invalid music file name!')
        return


    # if all checks pass, these functions are called to make the mod
    modfiles = create_folders(moddir, modname)
    move_file(modfiles, musicfile)
    create_main(modfiles, musicfile_name, False)
    create_locale(modfiles, musicfile_name, musicname)

    # display 'Done' message
    app.infoBox('Success!',
                'Your MenuMusicMod has been created.\nYou can find it here:\n{0}\{1}'.format(moddir, modname))

def makeithappen_super(button_name):
    modname = app.getEntry('modname')
    moddir = app.getEntry('moddir')
    musicname = app.getEntry('musicname')
    musicfile = app.getEntry('musicfile')

    try:
        musicfile_name = re.search('.*/(.*?)\.ogg', musicfile).group(1)
    except:
        app.infoBox('ERROR', 'Music file has the wrong format!')
        return

    # check if names are ok
    if modname == '' or re.match('^[a-zA-Z0-9_-]*$', modname) is None:
        app.infoBox('ERROR', 'Invalid mod name!')
        return
    elif musicname == '' or re.match('^[ a-zA-Z0-9_-]*$', musicname) is None:
        app.infoBox('ERROR', 'Invalid music name!')
        return

    # check if mod folder already exists
    if os.path.exists('{0}\{1}'.format(moddir, modname)):
        app.infoBox('ERROR', 'Mod folder already exists!')
        return

    # check if music file exists and is a ".movie" file.
    # also check if music file name contains only alphanumeric characters, underscores and hyphens
    if not os.path.isfile(musicfile):
        app.infoBox('ERROR', 'Music file does not exist!')
        return
    elif musicfile_name == '' or re.match('^[a-zA-Z0-9_-]*$', musicfile_name) is None:
        app.infoBox('ERROR', 'Invalid music file name!')
        return

    # if all checks pass, these functions are called to make the mod
    modfiles = create_folders(moddir, modname)
    move_file(modfiles, musicfile)
    create_main(modfiles, musicfile_name, True)
    create_locale(modfiles, musicfile_name, musicname)

    # display 'Done' message
    app.infoBox('Success!',
                'Your MenuMusicMod has been created.\nYou can find it here:\n{0}\{1}'.format(moddir, modname))


# -----------------GUI-----------------
# create gui and set title
app = gui('MenuMusicMod Creator', '650x150')
app.setIcon('mmmc.gif')
app.setFont('10', font='Verdana')

# add labels and entries to gui
# mod name
app.addLabel('modname_lab', 'Mod name:', 0, 0)
app.addEntry('modname', 0, 1)
# music name
app.addLabel('musicname_lab', 'Music name (shown in-game):', 1, 0)
app.addEntry('musicname', 1, 1)
# music to use
app.addLabel('musicfile_lab', 'Music to use (already in .movie/.ogg format): ', 2, 0)
app.addFileEntry('musicfile', 2, 1)
# mod directory
app.addLabel('moddir_lab', 'Mod folder output directory: ', 3, 0)
app.addDirectoryEntry('moddir', 3, 1)
app.setEntry('moddir', '{0}'.format(dir_path))
# "start" button
app.addButtons(['makeithappen','makeithappen_super'], [makeithappen, makeithappen_super], colspan=2)
app.setButton('makeithappen', 'Create MenuMusicMod\n(Normal BLT .movie)')
app.setButton('makeithappen_super', 'Create MenuMusicMod\n(Super BLT .ogg)')

# run gui
app.go()
