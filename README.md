# YAML to Mermaid Converter

This software converts a YAML file into a Mermaid diagram.

## Requirements

* Python 3.10

## Install on MacBook

```
$ git clone https://github.com/geocolumbus/yaml-to-mermaid.git
$ cd yaml-to-mermaid
$ python -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

To convert ```files/source.yaml``` to ```chart.html```.

```
$ python -m yamer/core.js
```

Then you can view the chart by opening chart.html in a browser (I used Chrome).

To convert json to yaml, paste the json in ```files/source.json``` and run this ```yq``` command: 

```
yq -P . source.json > source.yaml
```

## TODO

Convert it into a real command line tool.
