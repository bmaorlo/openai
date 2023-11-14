import openai
import time
from tools.hfConnector import hfConnector as hfConnector
from tools.functionsConfigurator import functionsConfigurator as functionsConfigurator

functionConfigHelper = functionsConfigurator()
def get_offers(destination: str) -> str:
    hfCon = hfConnector()
    hotelName = hfCon.getOffers()
    return hotelName

#response = get_offers()
#print(response)
#raise SystemExit

tools_list = [
    functionConfigHelper.getRecomendedDestinationConfiguration()
]


# Initialize the client
client = openai.OpenAI()
print("Create Assistant")

# Step 1: Create an Assistant

newAssistant = 1
newThread = 1
assistant_id = "asst_f4N68RO5Zh9dkBh8MPkgnILC"
threadId = "thread_ufoLhtd06azdjhdTQIGDhmmz"
messageToSend = "I am traveling to Rome"


if newAssistant == 1:
    assistant = client.beta.assistants.create(
        name="Recomended hotel assistant",
        instructions="you are a travel agent who recomended for hotels in a destination",
        tools=tools_list,
        model="gpt-4-1106-preview",
    )
    assistant_id = assistant.id
    print("Assistant ID : ",assistant_id)


if newThread == 1:
    # Step 2: Create a Thread
    thread = client.beta.threads.create()
    threadId = thread.id
    print("Thread ID : ",threadId)


# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=threadId,
    role="user",
    content=messageToSend
)

print("run")
# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=threadId,
    assistant_id=assistant_id,
    instructions="Please address the user as Mervin Praison."
)

print(run.model_dump_json(indent=4))

while True:
    # Wait for 5 seconds
    time.sleep(5)

    # Retrieve the run status
    run_status = client.beta.threads.runs.retrieve(
        thread_id=threadId,
        run_id=run.id
    )
    print(run_status.model_dump_json(indent=4))

    # If run is completed, get messages
    if run_status.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=threadId
        )

        # Loop through messages and print content based on role
        for msg in messages.data:
            role = msg.role
            content = msg.content[0].text.value
            print(f"{role.capitalize()}: {content}")

        break
    elif run_status.status == 'requires_action':
        print("Function Calling")
        required_actions = run_status.required_action.submit_tool_outputs.model_dump()
        print(required_actions)
        tool_outputs = []
        import json
        for action in required_actions["tool_calls"]:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            
            if func_name == "get_offers":
                output = get_offers(destination=arguments['destination'])
                tool_outputs.append({
                    "tool_call_id": action['id'],
                    "output": output
                })
            else:
                raise ValueError(f"Unknown function: {func_name}")
            
        print("Submitting outputs back to the Assistant...")
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=threadId,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    else:
        print("Waiting for the Assistant to process...")
        time.sleep(5)