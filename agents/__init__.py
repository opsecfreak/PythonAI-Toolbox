from .code_agent import get_config as get_code_config
from .writing_agent import get_config as get_writing_config
# Add imports for other agents here (e.g., social_media_agent, seo_optimizer_agent)

def get_agents():
    return {
        "code": get_code_config(),
        "writing": get_writing_config(),
        # Add other agents here
    }