# Nodules to import
MODULES = [
    'modules.quite_edible',
    'modules.foreca'
]

# Settings file
SETTINGS_FILE = './settings.json'

# GPT4All model
# -============-
# If not already present, will be downloaded to ~/.cache/gpt4all/
# Leave empty, if you don't want to use GPT functionality
# -============-
# Best chat based model: mistral-7b-openorca.Q4_0 
# - Size: 3.83 GB
# - RAM requirement: 8 GB
# -============-
# Explore models here: https://gpt4all.io/index.html
GPT_MODEL = 'mistral-7b-openorca.Q4_0.gguf'

# The processing unit on which the GPT4All model will run
# Options: 'cpu', 'gpu', 'amd', 'intel', 'nvidia'
GPT_MODEL_DEVICE = 'cpu'

# GPT4All model location
GPT_MODEL_PATH= './gpt4all'

