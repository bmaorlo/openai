import requests
import json
class hfConnector:

    host = "https://www.holidayfinder.co.il/api_no_auth/holiday_finder/offers/?data="
    parameters = "{%22locale%22:%22he%22,%22currency%22:%22USD%22,%22fromwhere%22:%22TLV%22,%22engine%22:{%22market%22:4,%22where%22:[19,21,33,20,25,18,30,51,17,333,113,52,87,135,86,124,97,37,80,60,68,129,115,133,63,31,71,75,74,130],%22when%22:{%22months%22:{%22periods%22:[],%22min%22:null,%22max%22:null,%22nights%22:[]}},%22who%22:{%22adult%22:2,%22child%22:0,%22room%22:1,%22childAges%22:[]},%22what%22:[],%22whereTxt%22:[%22Rome,%20Metropolitan%20City%20of%20Rome,%20Italy%22,%22Vienne,%20Austria%22,%22Amsterdam,%20Netherlands%22,%22Berlin,%20Germany%22,%22Madrid,%20Spain%22,%22Milano,%20Metropolitan%20City%20of%20Milan,%20Italy%22,%22Barcelona,%20Spain%22,%22London,%20UK%22,%22Paris,%20France%22,%22Bologna,%20Metropolitan%20City%20of%20Bologna,%20Italy%22,%22Sicily,%20Italy%22,%22Lisbon,%20Portugal%22,%22Tenerife,%20Spain%22,%22Frankfurt,%20Germany%22,%22D%C3%BCsseldorf,%20Germany%22,%22Brussels,%20Belgium%22,%22Napoli,%20Metropolitan%20City%20of%20Naples,%20Italy%22,%22Florence,%20Metropolitan%20City%20of%20Florence,%20Italy%22,%22Como%20Lake,%20Bellagio,%20Province%20of%20Como,%20Italy%22,%22Munich,%20Germany%22,%22Z%C3%BCrich,%20Switzerland%22,%22Manchester,%20UK%22,%22Dolomite%20Mountains,%20Canazei,%20Trentino,%20Italy%22,%22Geneva,%20Switzerland%22,%22Stockholm,%20Sweden%22,%22Venice,%20Metropolitan%20City%20of%20Venice,%20Italy%22,%22Nice,%20France%22,%22Lake%20Garda,%20Garda,%20Italy%22,%22Porto,%20Portugal%22,%22Nice,%20France%22],%22whatTxt%22:[],%22destinationGroups%22:[{%22id%22:10,%22name%22:%22%D7%9E%D7%A2%D7%A8%D7%91%20%D7%90%D7%99%D7%A8%D7%95%D7%A4%D7%94%22,%22name_en%22:%22Western%20Europe%22,%22priority%22:174,%22types%22:[3,10,12,13,16,33],%22active%22:true,%22hideByType%22:false}]},%22filters%22:{%22rating%22:[],%22stops%22:[],%22refundable%22:false,%22board%22:[],%22amenities%22:[],%22amenitiesTxt%22:[]},%22sort%22:{%22best%22:-1},%22limit%22:20,%22offset%22:0,%22searchUserProfile%22:0}"
    
    
    # method to calculate area
    def run(self):
        print("test 123")

    def getRequest(self):
    	print(self.host+self.parameters)

    def printResponse(self, testObj):
    	print(testObj)

    def getOffers(self, destination):
    	response = requests.get(url = self.host+self.parameters)
    	#self.printResponse(response.content)
    	jsonObjResponse = json.loads(response.content)
    	for offer in jsonObjResponse["data"]["offers"]:
    		return offer["hotel"]["name"]

    def test(self):
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
