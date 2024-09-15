from src.dl_data_pipeline.validator import TypeValidator, ShapeValidator, MinMaxValidator
import numpy as np

s = MinMaxValidator(0, 1)
s.validate(np.random.rand(100) - 1)
