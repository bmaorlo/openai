import time
from tools.hfConnector import hfConnector as hfConnector
class openAiHelper:
    def sendMessage(self,client,assistant_id, threadId, messageToSend):
        # Step 3: Add a Message to a Thread
        message = client.beta.threads.messages.create(
            thread_id=threadId,
            role="user",
            content=messageToSend
        )
        # Step 4: Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistant_id,
            instructions="Please great the user always ask for his name"
        )
        return run

    def listen(self, client, assistant_id, threadId, run):
        while True:
            # Wait for 5 seconds
            time.sleep(5)

            # Retrieve the run status
            run_status = client.beta.threads.runs.retrieve(
                thread_id=threadId,
                run_id=run.id
            )
            #print(run_status.model_dump_json(indent=4))

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=threadId
                )

                # Loop through messages and print content based on role
                msg = messages.data[0]
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
                        hfCon = hfConnector()
                        output = hfCon.getOffers(destination=arguments['destination'])
                        #output = get_offers(destination=arguments['destination'])
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