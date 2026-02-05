CONFIG = {
    "qa": {
        "base_url": "https://qa.repcard.com"
    },
    "staging": {
        "base_url": "https://staging.repcard.com"
    }
}

def get_config(env):
    return CONFIG.get(env, CONFIG["qa"])
