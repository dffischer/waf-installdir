# install_dir waftool

[Waf](http://waf.io) normally only handles files, creating directories on the fly as needed. But some projects also need to ensure special permissions for directories or want to install empty directories. This tool enhances waf with the capability to handle directories during installation.


## Usage

The tool can readily be loaded and used in wafscripts as long as it is found by the python module import mechanism. This is normally done by prepending the directory it resides in to the PYTHONPATH environment variable.


## Installation

The following command can be used to build an executable from the Waf Git repository including this tool.

```bash
git clone https://github.com/waf-project/waf
cd waf
git clone https://github.com/dffischer/waf-installdir
./waf-light configure --prefix=/usr \
  build --make-waf --tools='waf-installdir/installdir.py'
```
