import logging
import ecs_logging
import requests
import uuid
import os
import json_parser


def write_logs_to_elastic(event_string):
    conf_dict = json_parser.parse_json_to_var("/home/tzur/server/config.json")
    url_path = conf_dict["kibanas_url"]
    logfile_path = conf_dict["logfile_path"]

    if len(url_path) == 0:
        return

    # configure logger
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(conf_dict["logfile_path"])
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)

    # output to the local log
    logger.info(event_string, extra={"http.request.method": "get"})

    # send to elastic
    log_json = json_parser.parse_json_to_var(logfile_path)
    os.remove(logfile_path)
    doc_uuid = uuid.uuid4()
    requests.post(url=f"{url_path}/{event_string}/_doc/{doc_uuid}", json=log_json,
                  headers={'Content-Type': 'application/json'})
