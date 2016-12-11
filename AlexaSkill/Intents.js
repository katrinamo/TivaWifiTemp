{
  "intents": [
    {"intent": "remoteTempChange",
     "slots":[
        {"name": "changed_temp",
        "type": "AMAZON.NUMBER"}
     ]
    },
     {"intent": "remoteTempRead",
     "slots":[
        {"name": "current_temp",
        "type": "AMAZON.NUMBER"}
     ]
    },
    {"intent": "AMAZON.HelpIntent"},
    {"intent": "AMAZON.CancelIntent"},
    {"intent": "AMAZON.StopIntent"}
     ]
}