# csbom cli tool

This is a cli tool that parses an SBOM outputted by Scribe Security valint tool, formatted as CycloneDX, and creates a csv file containing the following.

### Installation

**Notice:** the tool is still in development, therefore it is suggested not to install it directly to your PATH. Instead, you could create a virtual python environment using python's [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) tool.

With this tool, you can create an environment with the command `virtualenv <env_name>`. virtualenv will create a directory in your current directory named `<env_name>`.

To activate your environment, on Linux/Mac you can run `source <env_name>/bin/activate` and on windows, `.\env_name\Scripts\activate`

To exit the environment, run `deactivate` and your terminal should go back to normal.

While in the venv, do this to install (this way, the tool will only be installed in the virtual environment):

Using the python package manager, run `pip install -i https://test.pypi.org/simple/ csbom==0.0.2`

### Usage & Explanations

`csbom CMD [OPTIONS] ARG`

**General Options**:
--help: display help information
-o (--output): Choose output filename (default `dep/file-analysis.csv`, depending on command)

**Commands**:
dep2table: Given an SBOM as the argument, outputs a table of dependencies
file2table: Given an SBOM as the argument, outputs a table of components of type file

**file2table**
command takes the SBOM and generates a CSV with 5 columns,
`bomref`, `name`, `hash`, `mimetime`, and `mode`.
Each row contains an entry from the `components` array in the SBOM file with the corresponding information. If a component does not contain an entry for any of these 5 categories, it will be marked as None

**dep2table**
command creates a CSV table of depender components mapped to dependee components, with information of `name`, `type`, and `purl` for each component.
