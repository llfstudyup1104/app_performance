import os
from icebot.utils.config import Configure

config = Configure()
PLATFORM_HOST = os.getenv('PLATFORM_HOST', config.get_config_value('Platform', 'host'))
PLATFORM_PORT = os.getenv('PLATFORM_PORT', config.get_config_value('Platform', 'port'))
AGENT_PORT = os.getenv('AGENT_PORT', config.get_config_value('agent', 'port'))
NJ_REVERSE_SSH_PROXY = os.getenv('NJ_REVERSE_SSH_PROXY', config.get_config_value('Platform', 'nj_ssh_proxy'))
NJ_REVERSE_SSH_PROXY_USER = os.getenv('NJ_REVERSE_SSH_PROXY_USER', config.get_config_value('Platform', 'nj_ssh_proxy_user'))
NJ_REVERSE_SSH_PROXY_KEY = os.getenv('NJ_REVERSE_SSH_PROXY_KEY', config.get_config_value('Platform', 'nj_ssh_proxy_key'))
SC_REVERSE_SSH_PROXY = os.getenv('SC_REVERSE_SSH_PROXY', config.get_config_value('Platform', 'sc_ssh_proxy'))
SC_REVERSE_SSH_PROXY_USER = os.getenv('SC_REVERSE_SSH_PROXY_USER', config.get_config_value('Platform', 'sc_ssh_proxy_user'))
SC_REVERSE_SSH_PROXY_KEY = os.getenv('SC_REVERSE_SSH_PROXY_KEY', config.get_config_value('Platform', 'sc_ssh_proxy_key'))
