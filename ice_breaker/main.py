import os
from typing import Tuple
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
from output_parsers import Summary, summary_parser

load_dotenv()


def create_chain() -> RunnableSerializable[dict, str]:
    summary_template = """
    given the information about a person from linkedin {information},
    and twitter posts {twitter_posts} I want you to create. (Generate content must be japanese):
    1. a short summary
    2. two interesting facts about them
    3. recommendation of this person

    User both information from twitter and Linkedin
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0.25, model_name="gpt-4o-2024-05-13")

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    return chain


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    chain = create_chain()

    res: Summary = chain.invoke(
        input={"information": linkedin_data, "twitter_posts": tweets}
    )

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    # # information = return_information()
    # information = scrape_linkedin_profile(
    #     linkedin_profile_url="https://www.linkedin.com/in/hirotokadota0706/", mock=True
    # )
    # res = chain.invoke(input={"information": information})

    # print(res)

    print("Invoke IceBreaker.")
    ice_break_with(name="EdenEmarco177")
