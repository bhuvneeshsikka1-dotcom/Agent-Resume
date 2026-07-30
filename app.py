#============LOAD MODULES===============
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
import langchain_community
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

#=========API KEYS================
# Step 2: API Keys
TAVILY_API_KEY = "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"
GOOGLE_API_KEY = "AQ.Ab8RN6JwRM6VAtsJdZxOxJLBkQitUMBz3YaRuCH4CCzFZYLyag"
GROQ_API_KEY = "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"

#=======================MODEL==========
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)
response = model.invoke("Hello Buddy!")
response.content[-1]['text']

#===============TOOL=================
def search_latest_news_jobs(query):
  """This function helps to fetch latest news or jobs related article using
  tavily"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

#=================AGENT CREATION===============
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs])
agent

#==========(MAIN AGENT - WHICH WILL HANDLE ALL SUBAGENTS)
def main_agent(agent, query):
  """This is main agent, or leader agent
  orchestrate sub agents"""
  # Giving prompt to create detailed prompt for code generation
  prompt = """You are AI assistant and below given is a prompt, your task is
  to give detailed prompt for this.
  You are a professional Resume generator where user will give their personal
  info, you have to create detailed Resume for students or professional one,
  it must be with dynamic UI and UX and, with advanced CSS Professional
  Designing, make sure to give output in HTML format only no markdowns allowed
  """
  response = agent.invoke({'messages':[{'role':'user',
                                        'content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']
  # Save Prompt using File Handling
  with open('prompt.txt', 'w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below given is a user details generate Resume based on that,
  if not given keep: Default Resume: Python Developer
  user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION
  response = agent.invoke({'messages':[{'role':'user',
                                        'content':final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

code = main_agent(agent, "BHUVNEESH SIKKA, GEN AI EXPERT with 5 years experience in leading projects in FAANG, BCA Grad from GGSIPU Delhi, MCA from Symbiosis University Pune")
from IPython import display as DISPLAY
DISPLAY.HTML(code)

# Fetch Latest Domain Related Jobs using Tavily
def get_jobs(agent, Location = "Noida, Delhi",
Profile = "Data Analysts, AI Engineer"):
  Location = "Noida, Delhi"
  Profile = "Data Analysts, AI Engineer"
  prompt = f"""Based on user given Job Profile,
  fetch latest jobs or job apply article using Naukri, Linkedin,
  Indeed, or all popular job apply platforms, show results with Job Profile Name,
  Location, Salary, Company Name, Show jobs only related to given {Location} and
  {Profile} Output must be in Professional HTML Naukri theme cards with
  Dynamic Design
  Show atleast to 10-20 results with direct apply link"""
  response = agent.invoke({'messages':[{'role':'user',
                                          'content':prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

code = get_jobs(agent)
DISPLAY.HTML(code)