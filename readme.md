# dl_data_pipeline

`dl_data_pipeline` is a flexible and dynamic Python package for building data processing pipelines. It allows you to create pipelines using input nodes, chain them through various processing functions, and validate the outputs at different stages. The package supports deferred execution for dynamic graph building.

## Installation

You can install `dl_data_pipeline` via `pip`:

```bash
pip install dl_data_pipeline
```

Or, you can install it from the source:

```bash
git clone https://github.com/sacha-renault/DataPipeline.git
cd DataPipeline
pip install -r requirements_dist.txt
pip install python3 setup.py sdist bdist_wheel
```

## Basic example

Here’s a quick example to demonstrate how to set up and run a basic pipeline:

```python
# Import the necessary module
import dl_data_pipeline as dp
from dl_data_pipeline.process_functions import process_2d

# Define the inputs for the pipeline
input_node1 = dp.InputNode(name="1")

# Pass the input through functions to create the graph
x = process_2d.open_rgb_image(input_node1)
out1 = process_2d.padding_2d(x, (256,256), fill_value = 0.0)

# Create the pipeline by specifying the inputs and outputs
pipe = dp.Pipeline(inputs=[input_node1], outputs=[out1])

# Call the pipeline with the required inputs and get the outputs
img = pipe("path/to/image.png")
```

## documentation

For more advanced usage, including adding multiple inputs/outputs, custom validators, and deferred execution, please check the full documentation [here](https://sacha-renault.github.io/DataPipeline/).

## Contributing

We welcome anyone interested in adding their own preprocess functions to the package! If you have an idea or useful transformation you'd like to share, feel free to contribute by submitting a pull request. Your contributions are always appreciated!
