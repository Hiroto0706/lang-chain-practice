import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable

from assets.information import return_information
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv()


def create_chain() -> RunnableSerializable[dict, str]:
    summary_template = """
    given the information about a person from linkedin {information},
    and twitter posts {twitter_posts} I want you to create. (Generate content must be japanese):
    1. a short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template
    )

    llm = ChatOpenAI(temperature=1, model_name="gpt-4o-2024-05-13")

    chain = summary_prompt_template | llm | StrOutputParser()

    return chain


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    print(linkedin_data)

    chain = create_chain()

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)


if __name__ == "__main__":
    # # information = return_information()
    # information = scrape_linkedin_profile(
    #     linkedin_profile_url="https://www.linkedin.com/in/hirotokadota0706/", mock=True
    # )
    # res = chain.invoke(input={"information": information})

    # print(res)

    print("Invoke IceBreaker.")
    ice_break_with(name="EdenEmarco177")
