import json
import os

class Config:
    def __init__(self, config_file=None):
        self.config = {}
        if config_file and os.path.exists(config_file):
            self.load(config_file)
    
    def load(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
    
    def save(self, config_file):
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
    
    @property
    def provider_type(self):
        return self.config.get('provider_type', 'openai')
    
    @property
    def provider_config(self):
        return self.config.get('provider_config', {})
    
    @property
    def benchmark_file(self):
        return self.config.get('benchmark_file', '')
    
    @property
    def output_file(self):
        return self.config.get('output_file', 'results.json')
    
    @property
    def max_iterations(self):
        return self.config.get('max_iterations', 5)