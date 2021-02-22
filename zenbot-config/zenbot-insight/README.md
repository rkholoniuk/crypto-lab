## Description

This script runs every night in a cronjob. It runs simulations on the previous day using all zenbot default strategies. It then saves all the results into a csv file every day for historical analysis.

## Setup

You will need Python and Pip installed. You can then install the `virtualenv` tool and create an isolated Python environment

```sh
$ sudo pip install virtualenv
```

```sh
$ virtualenv venv
```

To activate the virtual environment:

 ```sh
 $ . venv/bin/activate
 ```

To install requirements:

 ```sh
 $ pip install -r requirements.txt
 ```

