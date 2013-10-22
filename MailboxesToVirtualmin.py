#-------------------------------------------------------------------------------
# Name:        MailboxesToVirtualmin
# Purpose:     Converts the structure of mailboxes to Virtualmin format. Must be run as root!
#
# Author:      Andrew Arsenchuk
#
# Created:     22.10.2013
# Copyright:   (c) Andrew Arsenchuk 2013
# Licence:     WTFPL
#-------------------------------------------------------------------------------
# Актуально для настроек Virtualmin, когда создаются папки и пользователь example, а не example.com
import os
import shutil
import pwd
import grp
# Своровал кусок кода для рекурсивного os.chown
def _chown(path, uid, gid):
        os.chown(path, uid, gid)
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            if os.path.isfile(itempath):
                os.chown(itempath, uid, gid)
            elif os.path.isdir(itempath):
                os.chown(itempath, uid, gid)
                self._chown(itempath, uid, gid)
 
 
# Первая часть домена второго уровня
Domain = 'rost-alko'
# Вторая часть домена второго уровня
DomainEnd = '.ru'
# Старый каталог с папками вида /home/vmail/example.com/username_mailbox
OldRoot = '/home/vmail/' + Domain + DomainEnd
# Новый каталог с папками вида /home/example/homes/username/Mailbox
NewRoot = '/home/' + Domain + '/homes/'
# Получаем список папок == имён пользователей в старом каталоге
UserFolders = os.listdir(OldRoot)
# Основной цикл
for UserName in UserFolders:
    # Формируем старый путь к папке с почтой
    OldPath = OldRoot + '/' + UserName
    # Перемещаем в новую папку, получается /home/example/homes/username/Maildir
    shutil.move(OldPath,NewRoot + UserName + '/Maildir')
    # Перебиваем права, должны быть username@example.com:example
    _chown(NewRoot + UserName + '/' + 'Maildir', pwd.getpwnam(UserName + '@' + Domain + DomainEnd).pw_uid, grp.getgrnam(Domain).gr_gid)
 
# Микродебаг, числа должны совпадать
print('All done,' + len(UserFolders) + ' input boxes processed to ' + len(os.listdir(NewRoot)) + ' output boxes\n')