from uagents import Agent, Context, Model
from asyncio import Future
import time
 
class Message(Model):
    message: str
 
 
RECIPIENT_ADDRESS = (
    "agent1qd8ymq4najh5wycvhvhcw3l5lmkgkvkrqevrs6wpp5ll0khfdq6v2cq6859"
)

class Request(Model):
    text: str

class Response(Model):
    timestamp: int
    text: str
    agent_address: str

SenderAgent = Agent(
    name="SenderAgent",
    port=8000,
    seed="SenderAgent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

print(SenderAgent.address)
 
choice = {
    'rock' : 3,
    'paper' : 1,
    'scissors' : 2
}
future = None

@SenderAgent.on_rest_post("/rest/post", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    ctx.logger.info("Received POST request")
    print(req.text)
    
    global future
    future  =  Future()
    await ctx.send(RECIPIENT_ADDRESS, Message(message=""))
    playerChoice = req.text
    playerChoice = playerChoice.lower()
    result = await future
    print(playerChoice)
    print(result)
    pNum = choice[playerChoice]
    decider = pNum - int(result)
    if decider == 0:
        finish = 'you tie'
    elif decider == 1 or decider == -2:
        finish = 'you win'
    else:
        finish = 'you lose'
    print(finish)


    return Response(
        text=finish,
        agent_address=ctx.agent.address,
        timestamp=int(time.time()),
    )

@SenderAgent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"move from the agent was: {sender}: {msg.message}")
    future.set_result(msg.message)
 
if __name__ == "__main__":
    SenderAgent.run()