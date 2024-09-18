==================================
Introduction
==================================

The dl_data_pipeline package is designed to help you build flexible, dynamic, and efficient data processing pipelines. With an easy-to-use graph-based structure, you can define input nodes, pass them through a series of processing functions, and validate the results at each stage. The package supports deferred execution, allowing you to define pipelines with reusable components and dynamic processing logic.

Whether you're working with images, numerical data, or custom processing tasks, dl_data_pipeline gives you the tools to construct complex workflows with minimal effort.

.. contents:: Table of Contents
   :depth: 2
   :local:

Installation
============

.. code-block:: bash

    # Install the required package using pip
    pip install dl_data_pipeline

    # Alternatively, you can install it from the source
    git clone https://github.com/sacha-renault/DataPipeline.git
    cd DataPipeline
    pip install -r requirements_dist.txt
    pip install python3 setup.py sdist bdist_wheel

Example
=======

This section provides a simple example demonstrating the core functionality of the package. Follow the steps below to see how it works.

Create a basic pipeline
--------------------------

Start by importing the necessary module.

.. code-block:: python

    # Import the necessary module
    import dl_data_pipeline as dp 
    from dl_data_pipeline.process_functions import process_2d

    # Define the inputs for the pipeline
    input_node1 = dp.InputNode(name="1")

    # Pass the input through functions to create the graph
    x = process_2d.open_rgb_image(input_node1)
    out1 = process_2d.padding_2d(x, (256,256), fill_value = 0.0)

    # Create the pipeline by specifying the inputs and outputs
    pipe = dp.Pipeline(inputs=[input_node1], outputs=[out1]) # pipe with one input one output

    # Call the pipeline with the required inputs and get the outputs
    img = pipe("path/to/image.png")

Create a pipeline with more than 1 input
-----------------------------------------
.. code-block:: python
    
    # import process 2d package
    import dl_data_pipeline as dp 
    from dl_data_pipeline.process_functions import process_2d

    # dummy add function
    @deferred_execution
    def my_sum(v1, v2):
        return v1 + v2

    # Define the inputs for the pipeline
    input_node1 = dp.InputNode(name="1")
    input_node2 = dp.InputNode(name="2")

    # open an image with some noise to add
    image = process_2d.open_rgb_image(input_node1)
    noise = process_2d.open_rgb_image(input_node2)

    noised_image = my_sum(image, noise)
    pipe = dp.Pipeline(inputs=[input_node1, input_node2], outputs=[noised_image])
    
    result = pipe("path/to/image.png", "path/to/ noise.png") # pipeline must now be called with two arguments
    

Create a pipeline with more than 1 output
-----------------------------------------
.. code-block:: python
    
    # import process 2d package
    import dl_data_pipeline as dp 

    # Define the inputs for the pipeline
    input_node1 = dp.InputNode(name="1")

    # define a graph here
    ... 
    output1 = some_function(x)
    output2 = some_other_function(x)

    # create the pipeline
    pipe = dp.Pipeline(inputs=[input_node1], outputs=[output1, output2])

    # the pipeline returns now more than 1 result
    input_value = ... # any value that matches the required argument
    res1, res2 = pipe(input_value)

Add some validator
--------------------------
.. code-block:: python
    
    # import process 2d package
    from dl_data_pipeline.validator import MinMaxValidator, ShapeValidator

    # define a pipeline
    ...

    # with this, we ensure image will always be formatted the correct way
    pipe.add_validator(MinMaxValidator(0, 255), output_index = 0)
    pipe.add_validator(ShapeValidator(256,256,3), output_index = 0)

    # now any call of the pipeline will raise an error if the output doesn't match the requirements


.. tip::

    For pipelines with more than one output, you can set `output_index` 
    to validate any specific output independently.


Excecute the pipeline
--------------------------

.. code-block:: python

    processed_data = pipe("path/to/data.png") 

.. note::
    Any error raise in a function of the graph will raise a RuntimeError.
    The name of the function is display in the RuntimeError.

Existing functions
-------------------
Some basic preprocess functions are already defined. See more in process_functions documention.

Create your own functions
--------------------------

To create your own function to excecute in the graph, you have to create deferred functions

.. code-block:: python

    # first create the function normally and test it with normal values
    def my_function(data, shape, *args):
        ... # function definition

Once it works as expected, decorate the function with `deferred_execution`

.. code-block:: python

    @deferred_execution
    def my_function(data, shape, *args):
        ... # function definition

.. warning::

   Once `deferred_execution` is applied to a function, it expects at least one `PipelineNode` argument. 
   Any arguments that are dynamic (i.e., `PipelineNode` instances) and change during execution 
   should be placed **before** static arguments.

Illustration of the warning. Dynamic is same as Node

.. code-block:: python

    @deferred_execution
    def my_function(data1, shape, data2):   # NOT OK ! static agument before a dynamic argument
        ...

    # this is wrong because data1 and data2 represent values in the graph, and are separated
    # with `shape`, correct signature would be :
    @deferred_execution
    def my_function(data1, data2, shape):   # OK ! dynamic argument must be always first
        ...

    # When creating the graph:
    input_node1 = InputNode(name="1")
    input_node2 = InputNode(name="2")

    # This is NOT OK because dynamic arguments (PipelineNodes) should be positional:
    output = my_function(input_node1, data2=input_node1, shape=(256, 256))  # **NOT OK** !!

    # Dynamic (PipelineNode) arguments should be positional:
    output = my_function(input_node1, input_node1, shape=(256, 256))  # **OK** !!


Creating Custom Validators
---------------------------

You can define your own data validators by subclassing the Validator class. This allows you to implement custom validation logic tailored to your specific needs.

To create a custom validator, subclass Validator and override the validate method. The validate method should raise a ValidationError if the data doesn't meet the required validation criteria.

.. code-block:: python

    from dl_data_pipeline.validator import Validator, ValidationError

    class CustomRangeValidator(Validator):
        def __init__(self, min_value, max_value):
            self.min_value = min_value
            self.max_value = max_value

        def validate(self, data):
            if not (self.min_value <= data <= self.max_value):
                raise ValidationError(f"Data {data} is out of range [{self.min_value}, {self.max_value}]")

The following validators are already provided in the package, and you can use them directly in your pipeline:

.. code-block:: python

    from dl_data_pipeline.validator import (
        TypeValidator,     # Validates the type of the data
        ShapeValidator,    # Ensures the data matches a specific shape
        MinMaxValidator,   # Validates that the data falls within a specified range
        MeanVarValidator,  # Ensures the data's mean and variance meet specified criteria
        ValidationError    # Custom exception raised when validation fails
    )

Conclusion
===========

With the dl_data_pipeline package, you can easily create customizable and efficient data processing pipelines. 
By defining input nodes, chaining processing functions, and applying validation logic, you can create robust pipelines for handling complex workflows. 
Additionally, the package allows for deferred execution, providing a more dynamic and flexible approach to building graphs.

Whether you're using the built-in processing functions and validators or creating your own, 
the dl_data_pipeline package ensures that you have the tools to handle diverse data processing tasks with ease.

For further information on specific functions and more advanced usage, please refer to the full documentation.