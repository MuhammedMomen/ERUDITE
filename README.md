## Erudite: Your AI Job Seeker Companion

Erudite is an innovative AI-driven application designed to revolutionize the job search experience. With simple UI and exploiting Google Pro Gemini AI  to add GenAI feature, Erudite aims to empower job seekers with personalized guidance and support throughout their career advancements.


## Inspiration

The inspiration behind Erudite derived from the realization of the challenges individuals face during the job search process. Recognizing the need for a more easy and personalized approach, so I had envisioned an AI-powered solution that could empower job seekers with tailored guidance and support.

## What it does

Erudite is an AI-powered job seeker application based on Gemini Pro AI from Google, designed to assist users throughout their career journey. It gathers data from users, including their CV, preferences, and targeted job titles, to provide personalized recommendations and insights. Users can explore job opportunities, receive tailored advice, and gain valuable insights.

## How it was built

Erudite was built in Python language and exploited the Gemini Pro model from Google as the (LLM) large language model to role-play the AI consultant, and LangChain framework for orchestrating the data flow from the user input to the response from the LLM. Moreover, Beautiful-Soup framework for some publicly posted jobs data scrapped to be fed to the model as a knowledge base. Finally, FLET framework that uses flutter concepts but in python and was used for putting things together in a modern-looking UI.

######################################################################################################

### Erudite User Guide

Welcome to Erudite, your AI-powered job seeker companion! Below are the instructions for using the app effectively:

---

**1. Getting Started**

- Upon launching Erudite, you'll be greeted with four main tabs: Inputs, Search Results, Consultant, and Insights.

**2. Inputs Tab**

- In this tab, you'll provide necessary data for the job search process:
  - **Upload CV Copy**: Upload your resume to help Erudite tailor its recommendations.
  - **Select Targeted Recruitment Website**: Choose the website(s) from which you want to scrape job data.
  - **Title to Search**: Enter the job title or keyword you're interested in.
  - **Number of Pages to Scrape**: Specify the number of pages of job listings to scrape.
  - **Extra Information**: Share any additional preferences or hobbies for more personalized recommendations.
  - 
- Click the "**Search**" button after inputting your data.

**3. Search Results Tab**

- In this tab, you'll find the results of the job search displayed in a table format.
- Click on the "Apply" button to redirect to the job page for further details.

**4. Consultant Tab**

- Engage in a conversation with the AI consultant to receive personalized advice:
  - Discuss job relevance based on your career history.
  - Receive recommendations for suitable job opportunities.
  - Get tips for improving your resume.
  - Learn about professional etiquette in job applications.

**5. Insights Tab**

- Explore insights into the job market:
  - Discover skills required for various job roles.
  - View frequency of skills across job listings.
  - Gain a summary of similarities in job descriptions.

---

### Disclaimer

**Note:** Jobs scraped from publicly posted job listings are owned solely by their host websites. Erudite is developed for research purposes only, with no intention to redistribute or use the scraped data for commercial purposes.
