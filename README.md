# ADR Tool

## User guide

### Installation
* Download the appropriate release for your OS from [here](https://github.com/gnsiva/adr-tool-ng/releases). 
* Untar it
* Add the executable to somewhere where it will be picked up (e.g. `sudo cp adr /usr/bin/adr`)

### Usage

```bash
# get more info
adr --help

# create an ADR
adr create "My Important Decision"

# Approve an ADR
adr approve XXXXX-my-important-decision.md
```

### Temporary files
To reduce the chance of a file being wiped, the adr script keeps a backup of the file when it is auto edited.
The backup files are kept in a `.adr-backups` within the same directory. 
You should add this to your `.gitignore` file.


## Developer guide
See [the developer guide](./docs/developer-guide.md).

