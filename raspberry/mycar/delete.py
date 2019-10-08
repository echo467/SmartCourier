import donkeycar as dk


cfg = dk.load_config()
k = dk.utils.get_model_by_type(cfg.DEFAULT_MODEL_TYPE, cfg)
print(k.model.get_layer())