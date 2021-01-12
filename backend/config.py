""" Configuration loading for YAML files."""
import os
import re
from typing import Iterable
import logging
from logging.config import dictConfig
from confuse import Configuration

INDEX_MERGED_YAML = 0

# Adapt for new environment variable links
dic_env_var = {
    # database settings
    "MONGODB_SETTINGS": {"host": "MONGO_URI"},   
    
}

### Adapt to make fields merging available
to_flatten_fields = [
    ["SITE_CONFIG"],
    ["DEFAULT_COMPONENTS_CONFIG", "video_analyzer", "cameras"],
]

to_flatten_fields_tags = ["site_cfg", "va_cam"]

# Logging configuration
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(threadName)s] [%(levelname)s] %(name)s: %(message)s"  # pylint: disable=line-too-long  # noqa
            }
        },
        "handlers": {
            "wsgi": {"class": "logging.StreamHandler", "formatter": "default"}
        },
        "loggers": {
            "backend": {"level": "DEBUG"},
            "boto3": {"level": "WARN"},
            "werkzeug": {"level": "DEBUG"},
        },
        "root": {"level": "WARN", "handlers": ["wsgi"]},
    }
)


logger = logging.getLogger(__name__)


class Struct:
    """ Adaptable class."""

    def __init__(self, **entries):
        self.__dict__.update(entries)


def fill_dict_env(entry):
    """ Completes configuration with environment variables."""

    if isinstance(entry, str):
        return os.getenv(entry)

    if isinstance(entry, dict):
        res = {}
        for key in entry:
            value = fill_dict_env(entry[key])
            if value is not None:
                res[key] = value
        return res if len(res) > 0 else None

    raise ValueError(
        "dic_env_var error while trying to retrieve values of type: " + str(type(entry))
    )


def merge_files(files):
    """ Merge fiels with references."""
    global INDEX_MERGED_YAML

    if len(files) == 1:
        return files[0]
    merge_file = "merged_yaml_{}.yml".format(INDEX_MERGED_YAML)
    INDEX_MERGED_YAML += 1

    with open(merge_file, "w+") as outfile:
        for names in files:
            with open(names) as infile:
                outfile.write(infile.read())
            outfile.write("\n\n")
    return merge_file


def flatten(list_items: list):
    """ Turn embedded lists into 1D list."""
    res = []
    for elem in list_items:
        if isinstance(elem, list):
            res += elem
        else:
            res += [elem]
    return res


def flatten_filter(cfg: dict, fields: list):
    """ Solves references in YAML files."""
    for field in fields:
        value = cfg
        for sub_field in field[:-1]:
            value = value[sub_field] if sub_field in value else None
            if not value:
                break
        if value and field[-1] in value and value[field[-1]]:
            value[field[-1]] = flatten(
                value[field[-1]]
            )  # Flatten list in case of alias use
    return cfg


def load_config(
    additional_config_files: Iterable[str] = None, additional_config_dict: dict = None
):
    """
    Load configuration from multiple YAML files and dictionaries.
    Override priority (highest in the list overrides others fields):
    - Dictionaries (from last to first)
    - Files (from last to first)
    - default_config.yml
    """

    cfg = Configuration("backend", read=False)
    module_dir = os.path.dirname(__file__)

    cfg.set_file(os.path.join(module_dir, "default_config.yml"))

    if additional_config_files:
        for config in additional_config_files:
            if os.path.getsize(config) != 0:
                cfg.set_file(config)

    if additional_config_dict:
        cfg.set_args(additional_config_dict)

    env_vars_dict = fill_dict_env(dic_env_var)
    if env_vars_dict:
        cfg.set_args(env_vars_dict)

    return cfg


def load_config_as_object(
    additional_config_files: str = None, additional_config_dict: dict = None
):
    """ Load configuration from YAML files and dictionaries to object."""
    global INDEX_MERGED_YAML
    logger.debug(
        "Found configuration: Files:'%s', Dicts: %s.",
        additional_config_files,
        additional_config_dict,
    )
    if additional_config_files is not None:

        additional_config_files_cleaned = re.split(" *, *", additional_config_files)

        logger.debug("Config files parsed as : %s", additional_config_files_cleaned)
        for i in range(  # pylint: disable=consider-using-enumerate
            len(additional_config_files_cleaned)
        ):
            additional_config_files_cleaned[i] = merge_files(
                re.split(r" *\| *", additional_config_files_cleaned[i])
            )
    else:
        additional_config_files_cleaned = None

    cfg = load_config(additional_config_files_cleaned, additional_config_dict)
    for i in range(INDEX_MERGED_YAML):
        os.remove("merged_yaml_{}.yml".format(i))
    INDEX_MERGED_YAML = 0
    res_cfg = {}
    for key in cfg:
        if not key.startswith(tuple(to_flatten_fields_tags)):
            res_cfg[key] = cfg[key].get()
    logger.debug("Cleaned temporary YAML files and merging keys.")
    res_cfg = flatten_filter(res_cfg, to_flatten_fields)
    logger.debug("Loaded successfully configuration.")
    return Struct(**res_cfg)
