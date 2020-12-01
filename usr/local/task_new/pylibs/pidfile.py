# 
# -*- coding: KOI8-R -*-

import sys
import os
import fcntl

"""
Модуль блокировки от запуска второго процесса программы. Осуществляется через
сохранение информации о запущенном процессе в отдельном PID файле с flock
блокировкой.
"""

class pidfile:
    def __init__(self, path):
        assert type(path) is str and path, path
        self._pidfile_path = path
        self._pidfile_fd = -1
        self._pid = 0
        self._os_close = os.close
        self._os_unlink = os.unlink
        self._exc_clear = sys.exc_clear

    def pidfile_start(self):
        """
        Создает и блокирует файл процесса. Если процесс уже запущен,
        возвращается False. В случае успешной блокировки - True.
        """
        old_fd = self._pidfile_fd
        if old_fd < 0:
            path = self._pidfile_path
        else:
            path = self._pidfile_path + ".update"
        self._pidfile_fd = os.open(path, os.O_CREAT|os.O_RDWR, 0600)
        try:
            fcntl.flock(self._pidfile_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except IOError:
            self.pidfile_forget()
            return False
        if not (old_fd < 0):
            try:
                old_fd = self._pidfile_fd
                os.rename(path, self._pidfile_path)
            except OSError:
                self._exc_clear()
        pid = os.getpid()
        os.write(self._pidfile_fd, "%d\n" % pid)
        self._pid = pid
        return True

    def pidfile_kill(self, signo):
        """
        Посылает номер сигнала signo работающему процессу.
        """
        if not (self._pidfile_fd < 0):
            return False
        try:
            self._pidfile_fd = os.open(self._pidfile_path, os.O_RDWR)
        except OSError:
            self.pidfile_forget()
            return False
        try:
            fcntl.flock(self._pidfile_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
            return False
        except IOError:
            self._exc_clear()
            try:
                pid = int(os.read(self._pidfile_fd, 21).strip(), 10)
                os.ftruncate(self._pidfile_fd, 0)
                os.kill(pid, signo)
                fcntl.flock(self._pidfile_fd, fcntl.LOCK_EX)
                return True
            except:
                self.pidfile_forget()
                return None

    def pidfile_stop(self):
        """
        Удаляет и закрывает файл с информацией о работающем процессе.
        """
        if getattr(self, '_pidfile_fd', -1) >= 0:
            try:
                if self._pid == os.getpid():
                    self._os_unlink(self._pidfile_path)
            except:
                pass
            self.pidfile_forget()

    def pidfile_forget(self):
        """
        Забыть об удалении файла и снять блокировку для текущего процесса.
        """
        self._exc_clear()
        if getattr(self, '_pidfile_fd', -1) >= 0:
            self._os_close(self._pidfile_fd)
            self._pidfile_fd = -1

    __del__ = pidfile_stop
