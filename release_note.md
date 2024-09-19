## [v0.1.0] - 2024-09-18

### First Release 🎉

This is the first release of dl_data_pipeline!

# Key Features:

- Build flexible data pipelines using a graph-based structure.
- Supports deferred execution for dynamic, reusable pipelines.
- Basic processing functions like open_rgb_image and padding_2d included.
- Custom validators for data validation at each step.
  Thanks for checking it out, and feel free to contribute or report any issues!

## [v0.1.1] - 2024-09-19

### 🚀 New Features:

- Added instant_execution context manager to force function execution without deferred mode.
- PipelineNode.unwrap() allow to use **iter**() on nodes before we know length at runtime.
- PipelineNode now supports iteration with **iter**().
- Added new pooling process functions.
