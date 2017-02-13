# CLI Setup on Mac
Following have been tested on macOS 10.12

* Clone the Netsil Utils repo
``` bash 
git clone https://github.com/netsil/utils.git
```
* Change directory to the cli: cd /your_clone_of_netsil_utisl/cli

* Install virtualenv 
``` bash 
sudo pip install virtualenv
```
* Create a virtual env in the cli directory 
```bash 
virtualenv venv
```

* Activate virtal env
```bash
. venv/bin/activate
```
* Run package.sh
```bash
source package.sh
```
* Test
``` bash
netsil_aoc --help

(venv) $ netsil_aoc --help
Usage: netsil_aoc [OPTIONS] COMMAND [ARGS]...

  Netsil AOC CLI

Options:
  --help  Show this message and exit.

Commands:
  alert    Netsil AOC Alert Commands
  service  Netsil AOC Service Commands
```

