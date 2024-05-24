# heavy quark production

This repository contains script that automatically downloads heavy quark initial pT distribution from [FONLL web interface](http://www.lpthe.jussieu.fr/~cacciari/fonll/fonllform.html). These distributions can than be used with [DREENA-A](https://github.com/DusanZigic/DREENA-A) and [ebeDREENA](https://github.com/DusanZigic/ebeDREENA).
Script uses [selenium](https://www.selenium.dev/) python module which is the only dependency with Firefox webdriver.
> [!TIP]
> after installing selenium with pip you might need to download [geckodriver](https://github.com/mozilla/geckodriver/releases) and extract it to /usr/bin/.

### parameters

params.py contains dictionary with collision energy, *sNN* and heavy quark type. These parameters and their values are explained in more detail within the params.py sript.

### output

Output files and directory structure will be compatible with DREENA-A and ebeDREENA.
