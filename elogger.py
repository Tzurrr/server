import json
import logging
import ecs_logging
import requests
import uuid
import os
import json_parser

def write_logs_to_elastic(event_string):
    conf_dict = json_parser.parse_json_to_var("/home/tzur/client/config.json")
    url_path = conf_dict["kibanas_url"]
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(conf_dict["logfile_path"])
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)
    json_UUID = uuid.uuid4()
    
    logger.info(event_string, extra={"http.request.method": "get", "UUID": json_UUID})
    log_json = json_parser.parse_json_to_var(conf_dict["logfile_path"])

    os.remove(conf_dict["logfile_path"])

    doc_UUID = uuid.uuid4()
    resp = requests.post(url=f"{url_path}/{event_string}/_doc/{doc_UUID}", json=log_json,
                        headers={'Content-Type': 'application/json'})
