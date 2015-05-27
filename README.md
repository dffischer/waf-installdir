# install_dir waftool

[Waf](http://waf.io) normally only handles files, creating directories on the fly as needed. But some projects also need to ensure special permissions for directories or want to install empty directories. This tool enhances waf with the capability to handle directories during installation.


## Usage

The tool can readily be loaded and used in wafscripts as long as it is found by the python module import mechanism. This is normally done by prepending the directory it resides in to the PYTHONPATH environment variable.
