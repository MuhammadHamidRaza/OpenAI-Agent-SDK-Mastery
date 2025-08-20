import asyncio

  

async  def  task(name):

print(f"Starting {name}")

await asyncio.sleep(2)

print(f"Finished {name}")

  

async  def  main():

await asyncio.gather(task("Task 1"), task("Task 2"))

  

if  __name__ == "__main__":

asyncio.run(main())
