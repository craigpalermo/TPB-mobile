TPB-mobile
==========

A mobile front-end for TPB searches that allows users to save desired links in a queue that will automatically be downloaded on their desktop running the client application.

Setup (Windows)
==========
1. Install Python 2.7.5
2. Install [easy_install](https://pypi.python.org/packages/source/s/setuptools/setuptools-1.3.2.tar.gz#md5=441f2e58c0599d31597622a7b9eb605f)
3. Extract the tar.gz and navigate to dist/setuptools-1.3.2 in a terminal.
4. git clone git@github.com:unscsprt/TPB-mobile.git
5. cd tpb-mobile
6. Run: 

<pre>
python setup.py install
easy_install pip
pip install -r miscellaneous/deps
</pre>

7. Install [lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
    * Install either lxml-3.2.4.win-amd64-py2.7.exe or lxml-3.2.4.win32-py2.7.exe for 64/32-bit.
8. Run:

    cd server/tpb_mobile
    python manage.py runserver 0.0.0.0:8000
