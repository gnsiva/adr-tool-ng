# Developer guide 

## Local development

### Set up a virtual environment
First you need to create a virtual environment and use it, for example:

```bash
mkdir -p ~/.virtualenvs/
python3 -m venv ~/.virtualenvs/adr
source ~/.virtualenvs/adr/bin/activate

# for easy access later (adr-activate from terminal)
echo 'alias adr-activate="source ~/.virtualenvs/adr/bin/activate"' >> ~/.bashrc
source ~/.bashrc
```

### Install dependencies

Make sure to be in the virtual environment first.

```bash
pip install -r requirements.txt -r requirements-test.txt
```

### Test the code, create and install the executable

```bash
# see available make entries 
make

# run the tests
make test

# create the executable
make build

# install it
sudo make install
```

## Releasing
There is a GitHub Actions pipeline provided that can build the tool and create a release on GitHub.  
To do this, you will need to do the following steps:

* Determine the version, it should be semantic, starting with `v`, e.g. `v0.1.0`
* Create a release notes file in `./docs/release-notes` with the name `<tag>.md` (e.g. `v0.1.0.md`)
* Merge this all into master (making sure tests are passing)
* Tag the commit you want to release on master (e.g. `git tag -a v0.1.0`) 
* Push the tag to GitHub (e.g. `git push origin v0.1.0`)

Then you should see the assets [here](https://github.com/gnsiva/adr-tool-ng/releases).

