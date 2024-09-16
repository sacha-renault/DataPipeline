==================================
Introduction
==================================

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

Create a pipeline
--------------------------

Start by importing the necessary module.

.. code-block:: python

    #import module
    import dl_data_pipeline as dp 

    # create a base pipeline
    pipe = dp.Pipeline()

Add some forward functions
--------------------------
.. code-block:: python
    
    # import process 2d package
    from dl_data_pipeline.process_functions import process_2d

    # in this example we use process function for images
    pipe.add_forward_process(process_2d.open_rgb_image) # functions that takes only one argument (the data)
    pipe.add_forward_process(process_2d.padding_2d, (256,256), fill_value = 0.0)    # functions that takes args or / and kwargs 
                                                                                    # can receive extra args like this

Add some forward validator
--------------------------
.. code-block:: python
    
    # import process 2d package
    from dl_data_pipeline.validator import MinMaxValidator, ShapeValidator

    # with this, we ensure image will always be formatted the correct way
    pipe.add_forward_validator(MinMaxValidator(0, 255))
    pipe.add_forward_validator(ShapeValidator(256,256,3))

.. tip::

    Same thing can be done with add_backward_validator and add_backward_process

Excecute the pipeline
--------------------------

.. code-block:: python

    processed_data = pipe.forward("path/to/data.png") 

.. note::
    Previous example use a string as argument for the pipeline, that's because first function
    load an array from path. You can customize the pipeline and use it with any type.

deferred excecution
------------------------

To have a more user friendly interface. it's possible to use deferred excecution function. 
We can find the function under deferred package.

.. code-block:: python

    # import deferred functions
    from dl_data_pipeline import DATA_PLACEHOLDER as DPH
    from dl_data_pipeline.deferred import use_deferred_execution

    use_deferred_execution() # all processing function are now deferred

    # we use function as if we call them directly, with a placeholder for data
    pipe.add_forward_process(process_2d.rescale(DPH, 0, 1)) # we pass placeholder instead of data, and the rest is normal

.. caution::

   Once `use_deferred_execution()` is called once, module has to be reloaded to restore function normal states.

Create your own functions
--------------------------

Finally, you can code any function you like to fit your goal. If you prefere using deferred function instead of classic function, 
You can define them with the deferred decorator. The only requirement is that the data is first argument (VAR_ONLY).

.. code-block:: python

    from dl_data_pipeline import deferred_execution

    @deferred_execution
    def your_processing_function(data: Any, *args, **kwargs) -> Any:
        ... # your code