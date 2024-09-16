# Build the doc

- step 1 build package and install it :

```sh
python3 setup.py sdist bdist_wheel
pip install .
```

- go into docs folder

```sh
cd docs
```

- build doc

```sh
sphinx-apidoc -o source/ ../src
```
