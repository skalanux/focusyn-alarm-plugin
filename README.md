Tomate Alarm Plugin
===================

Tomate Plugin. Plays alarm at session end.


Installation
------------

### Ubuntu (14.04, 14.10)

```
RELEASE=`sed -n 's/VERSION_ID="\(.*\)"/\1/p' /etc/os-release`
sudo wget -O- http://download.opensuse.org/repositories/home:/eliostvs/xUbuntu_$RELEASE/Release.key | sudo apt-key add -
sudo bash -c "echo 'deb http://download.opensuse.org/repositories/home:/eliostvs/xUbuntu_$RELEASE/ ./' > /etc/apt/sources.list.d/tomate.list"
sudo apt-get update && sudo apt-get install tomate-alarm-plugin
```

### Opensuse (13.2)

```
RELEASE=`cat /etc/SuSE-release | sed -n "s/VERSION = \(.*\)$/\1/p"`
sudo zypper ar -f http://download.opensuse.org/repositories/home:/eliostvs/openSUSE_$RELEASE/home:eliostvs.repo
sudo zypper install tomate-alarm-plugin
```

## Fedora (20, 21)

```
RELEASE=`cat /etc/fedora-release | grep -o '[0-9][0-9]*'`
sudo yum-config-manager --add-repo http://download.opensuse.org/repositories/home:/eliostvs/Fedora_$RELEASE/home:eliostvs.repo
sudo yum install tomate-alarm-plugin
```

License
-------

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License version 3, as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranties of
MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.


Audio License
-------------

File downloaded from http://www.freesound.org/people/kwahmah_02/sounds/250629/
created by kwahmah_02 an converted to ogg format.
http://creativecommons.org/licenses/by/3.0/legalcode.