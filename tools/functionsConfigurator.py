class functionsConfigurator:

    def getRecomendedDestinationConfiguration(self):
        return {
            "type": "function",
            "function": {

                "name": "get_offers",
                "description": "Retrive the recomended hotel based on user input",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "destination": {
                            "type": "string",
                            "description": "the destination where you would like to find recomended hotel"
                        }
                    },
                    "required": ["destination"]
                }
            }
        }

    def maorTest(self):
        print("maor")
