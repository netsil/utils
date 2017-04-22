# CLI Setup on Mac
Following steps have been tested on macOS 10.12

``` bash 
git clone https://github.com/netsil/utils.git   #clone netsil utils repo
```
``` bash
cd /your_clone_of_netsil_utisl/cli    #change to the cli directory
```

``` bash 
sudo pip install virtualenv        #install virtualenv
```
```bash 
virtualenv venv       #launch a virtual env in the cli/ folder
```

```bash
. venv/bin/activate   #Activate virtual env
```
```bash
source package.sh     #Install dependencies and netsil_aoc cli
```
``` bash
export AOC_USER=<aoc_username>                          #(set your aoc username)
export AOC_PWD=<aoc_password>                          #(set your aoc password) 
export AOC_URL=https://your.netsil.url                 #(leave out the end '/')
```
``` bash
netsil_aoc --help     #All set if you see below message

(venv) $ netsil_aoc --help
Usage: netsil_aoc [OPTIONS] COMMAND [ARGS]...

  Netsil AOC CLI

Options:
  --help  Show this message and exit.

Commands:
  alert    Netsil AOC Alert Commands
  service  Netsil AOC Service Commands
```

