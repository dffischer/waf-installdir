# install_dir waftool

[Waf](http://waf.io) normally only handles files, creating directories on the fly as needed. But some projects also need to ensure special permissions for directories or want to install empty directories. This tool enhances waf with the capability to handle directories during installation.


## Deprecation Notice

The installdir module only works up to Waf 1.9.0pre1, more specifically until commit [1eaa87413da96295d727407cb04e64e8f6cd348c](https://github.com/waf-project/waf/commit/1eaa87413da96295d727407cb04e64e8f6cd348c). Later versions leave no opening to add custom installation methods. To use a recent Waf version, instead of using this tool it is recommended

- to install an empty hidden file to the otherwise empty directory
- permissions can be set using post-installation hooks using [the *BuildContext.add_post_fun* function](https://waf.io/apidocs/Build.html?highlight=post#waflib.Build.BuildContext.add_post_fun).


## Usage

[The included example](example/wscript) shows how to use the module in a wafscript.

The tool can readily be loaded and used in wafscripts as long as it is found by the python module import mechanism. This is normally done by prepending the directory it resides in to the PYTHONPATH environment variable.


## Installation

The following command can be used to build an executable from the Waf Git repository including this tool.

```bash
git clone https://github.com/waf-project/waf
checkout waf-1.9.0pre1
cd waf
git clone https://github.com/dffischer/waf-installdir
./waf-light configure --prefix=/usr \
  build --make-waf --tools='waf-installdir/installdir.py'
```

To make it available to a system-wide waf installation, the included waf script can be used to place it into the waf library.
