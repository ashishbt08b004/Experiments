
from crewai import Agent, Task, Crew



terraform_developer = Agent(
role="Senior Terraform Developer",
goal="Write Terraform scripts for {topic}",
backstory="""
You're a seasoned Terraform engineer with a knack for writing Terraform scripts for executing tasks in cloud environments..
Known for your ability to write Terraform scripts for given tasks.
""",
llm='ollama/incept5/llama3.1-claude'
)

# 2. Animal Description Agent (to describe the animal in the image)

terraform_reviewer = Agent(
role="Senior Terraform Reviewer",
goal="Review Terraform scripts for {topic}",
backstory="""
You are a seasoned cloud engineer with an eye for spotting issues in Terraform scripts. 
Known for your ability to review Terraform scripts for {topic} and make it more robust and secure.
""",
llm='ollama/incept5/llama3.1-claude'
)


develop = Task(
    description="Write Terraform scripts for {topic}.Make sure you write the most accurate and relevant Terraform scripts for {topic}",
    expected_output="An executable Terraform script for {topic}.",
    agent=terraform_developer,
    output_file="terraform_script.tf"
)

review = Task(
    description="Review the Terraform script you got and make sure it is correct and robust. Find out and correct any issues in the script.\
    Make sure the script is detailed and contains any and all relevant information.",
    expected_output="An executable Terraform script for {topic} with corrections and improvements.",
    agent=terraform_reviewer,
    output_file="terraform_script_corrected.tf"
)

crew = Crew(
    agents=[terraform_developer, terraform_reviewer],
    tasks=[develop,review],
    verbose=True
)

# Execute the tasks with the provided image path
result = crew.kickoff(inputs={'topic': 'Create 5 EC2 machines with at least 16GB RAM in the most cost efficient manner on AWS'})
