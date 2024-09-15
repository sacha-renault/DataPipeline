from src.dl_data_pipeline.validator import TypeValidator, ShapeValidator, MinMaxValidator, MeanVarValidator
from src.dl_data_pipeline.pipeline.data_pipeline import Pipeline

from src.dl_data_pipeline.process_functions import any_process
import numpy as np

pipe = Pipeline()
pipe.add_forward(any_process.rescale, min_value=-1, max_value=2)

pre_data = np.random.rand(25)

post_data = pipe.forward(pre_data)

print(f"Pre data. Min : {np.min(pre_data)} ;  Max : {np.max(pre_data)}")
print(f"Post data. Min : {np.min(post_data)} ;  Max : {np.max(post_data)}")