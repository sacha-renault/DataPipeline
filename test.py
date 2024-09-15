from src.dl_data_pipeline.validator import TypeValidator


v = TypeValidator(int, float)
v.validate(3.0)
v.validate(3)
v.validate([])