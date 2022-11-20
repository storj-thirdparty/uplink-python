# usage: python3 install-golang.py platform machine
import os
import sys
import platform
import tarfile
import wget

from subprocess import call

cibuildwheel_to_go_platform = {
    'x86_64' : 'amd64',
    '686' : '386'
}




_platform = sys.platform



print("Installing go for ", _platform, "/", platform.machine())

''' Download golang archive and extract it '''
GOLANG_URL = 'https://storage.googleapis.com/golang/go1.19.2.linux-amd64.tar.gz'
if platform.machine() == "i686":
    GOLANG_URL = 'https://storage.googleapis.com/golang/go1.19.2.linux-386.tar.gz'


filename = wget.download(GOLANG_URL, 'go.tar.gz')
print("Golang archive filename = ", filename)
file = tarfile.open(filename)
file.extractall("/usr/bin/")
file.close()
cmd = ['chmod','a+x', '/usr/bin/go/bin/go']
out = call(cmd)
if out != 0:
    raise CompileError('Go build failed')
