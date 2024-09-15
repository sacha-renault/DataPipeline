from src.dl_data_pipeline.validator import TypeValidator, ShapeValidator, MinMaxValidator, MeanVarValidator
import numpy as np

s = MeanVarValidator(target_mean=0.5)
s.validate(np.random.rand(100) - 1)
