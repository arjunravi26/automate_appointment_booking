from agno.models.groq import Groq
from typeguard import typechecked
from dotenv import load_dotenv
load_dotenv()

@typechecked
def create_model()->Groq:
    '''Function to create agent'''
    model_name = "llama-3.3-70b-versatile"
    return Groq(id=model_name)

if __name__ =="__main__":
    create_model()