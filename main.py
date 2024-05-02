import flet as ft
import Custom_Controls as cs
import requests
from bs4 import BeautifulSoup
import csv
import time
import datetime
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import NLTKTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from dotenv import dotenv_values
import pyperclip
import Custom_Controls as cs





#####################################
###### Author: Muhammed Mo'men ######
#####################################

#####################################
###### Flet GUI Layout ##############
#####################################


#API's Variables Env
env_values=dotenv_values(".ENV")
google_api_key=(env_values["GOOGLE_API_KEY"])








def main(page: ft.Page):
    page.title=("Erudie, your trusted AI job seeker companion (A.I.J.S)")
    page.theme_mode="Dark"
    page.rtl= False

    jobs_data={

    0:{
        "ID":"",
        "Apply":"",   
        "JobTitle":"",
        "Company":"",
        "Location":"",
        "Time":"",
        "Job Type":"",
        "Experience":"",
        "Job Categories":"",
        "Job Skills":"",
    },

    
}

    # Data table attributes & styling & column names
    column_names= [
        "ID","Apply","Job Title","Company","Location","Time","Job Type","Experience","Categories","Skills",
    ]

    #Class Controller to handle data between controls
    class Controller:
        items: dict = jobs_data
        counter: int = len(items)


        @staticmethod
        def get_items():
            # Start from the second item onwards
            return {key: value for key, value in Controller.items.items() if key != 0}

        

        @staticmethod
        def add_items(data: dict):
            Controller.items[Controller.counter]=data
            Controller.counter +=1




    Form_style= {
        "border_radius": 8,
        "bgcolor": "white10",
        "border": ft.border.all(1, "#ebebeb"),
        "padding": 15,

    }

    TextField_Style= {
        "multiline": True,
        "max_lines": 2,
        "label_style": ft.TextStyle(
                                size=14,
                                color="system",
                                font_family="Berlin Sans FB"
                            ),
        "border_color":"transparent",
        "height": 48,
        "text_size": 14,
        "content_padding": 5,
        "cursor_color":"system",
        "cursor_width": 1,
        "cursor_height":18,
        "color":"system",

    }

    dropdown_style={
        "icon":ft.icons.WEB_OUTLINED,
            "border_color":"transparent",
            "height":48,
            "content_padding":0,
            "hint_style":ft.TextStyle(
                size=14,
                font_family="Segoe UI semilight",
                color="System",
                ),
            "text_size":14,
            "color":"system",
            "focused_border_color":"transparent",

    }



    # # Data table attributes & styling & column names
    # column_names= [
    #     "ID","Job Title","Company","Location","Time","Job Type","Experience","Categories","Skills","Apply",
    # ]


    Dt_style= {
        "column_spacing":60.5,
        "expand":False,
        "border_radius": 8,
        "border": ft.border.all(2,"#ebebeb"),
        "horizontal_lines": ft.border.BorderSide(1,"#ebebeb"),
        "heading_row_color": "white70",
        "columns":[
            ft.DataColumn(ft.Text(index, size=12, color="black",weight="bold"))
            for index in column_names
            
        ]

    }
 
    #Function for picking local files
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Resume wasn't picked !"
        )
        selected_path.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Resume wasn't picked !"
        )        

        selected_files.update()
        selected_path.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    selected_path = ft.Text()

    page.overlay.append(pick_files_dialog)

    def fill_data_table(data_table: ft.DataTable):
            controller = Controller()
            df = controller.get_items()

            # Clear the data table rows for new batch
            data_table.rows = []

            # Skip adding the first row if it's empty
            if df.get(0) == {}:
                del df[0]

            for values in df.values():
                data = ft.DataRow()
                cells = []
                for key, value in values.items():
                    if key == "Apply":
                        # Create a button instead of text for the 'Apply' column
                        cells.append(
                            ft.DataCell(
                                ft.ElevatedButton(text="Apply", url=value, on_click=open_url_handler(value)))
                        )
                    else:
                        cells.append(
                            ft.DataCell(
                                ft.Text(str(value), color="bluegrye500",font_family="Berlin Sans FB",size=13)
                            )
                        )
                data.cells = cells
                data_table.rows.append(data)

            # Update the page after adding all rows
            page.update()

    def open_url_handler(url):
        def handle_click(e):
            open_url(url)
            return handle_click

    def open_url(url):
        page.launch_url(url)


        # Function to update the Insights tab content


    class JobScraper:
        def __init__(self, job_title, num_pages, callback):
            self.job_title = job_title
            self.num_pages = num_pages
            self.time = datetime.datetime.now().strftime("%Y-%m-%d- %H_%M")
            self.file_name = f'{job_title.title()} Jobs as of {self.time}.csv'
            self.counter = 1
            self.callback = callback

        def scrape_jobs(self):
            jobs_found = False

            # Open csv file and write header
            with open(self.file_name, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Num', 'JobTitle', 'Company', 'Location', 'Time', 'Job Type',
                                'Experience', 'Job Categories', 'Job Skills', 'Job URL'])

                # Scrape jobs from each page
                for i in range(self.num_pages):
                    url = f'https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q={self.job_title}&start={i}'
                    page = requests.get(url, headers={"Accept-Encoding": "utf-8"})

                    soup = BeautifulSoup(page.content, 'html.parser')
                    jobs = soup.find_all('div', class_="css-1gatmva e1v1l3u10")

                    if len(jobs) == 0:
                        # If no jobs are found
                        if i == 0:
                            jobs_found = False
                            print('No Jobs Found')

                    else:
                        jobs_found = True

                    for job in jobs:
                        # Get job main information
                        job_title = job.find('h2', class_="css-m604qf").text.strip().replace(', ', '-')
                        company_elem = job.find('a', class_="css-17s97q8").text.strip().split()
                        company = ' '.join(company_elem[:-1])
                        location = job.find('span', class_="css-5wys0k").text.strip().replace(', ', '-')
                        time_posted_elem = job.find('div', class_="css-4c4ojb")
                        time_posted = time_posted_elem.text.strip() if time_posted_elem else ''
                        job_url = job.find('a', class_="css-o171kl")['href']
                        job_type_elem = job.find_all('a', class_="css-n2jc4m")
                        job_type = ' | '.join(job_type.text.strip() for job_type in job_type_elem)

                        # Extracting job details
                        details = job.find('div', class_="css-y4udm8")
                        categories = details.find_all('a', class_="css-o171kl")
                        skills = details.find_all('a', class_="css-5x9pm1")
                        experience_elem = categories[0].text.strip()
                        experience_span = details.find_all('span')
                        experience = f'{experience_elem} | {experience_span[1].text[2:].strip()}' if (
                                (len(experience_span) > 1) and 'Yrs' in experience_span[1].text.strip()) else experience_elem

                        job_categories = ' | '.join([category.text[2:].strip() for category in categories[1:]])

                        # Handling skills
                        job_skills = []
                        for skill in skills:
                            if skill.find('span'):
                                # If the skill has a span, extract the text from the span
                                job_skills.append(skill.find('span').text.strip())
                            else:
                                # If there is no span, directly extract the text
                                job_skills.append(skill.text[2:].strip())

                        job_skills_str = ' | '.join(job_skills)

                        # Write job information to csv file
                        writer.writerow([self.counter, job_title, company, location, time_posted, job_type,
                                        experience, job_categories, job_skills_str, job_url])

                        # Create a dictionary for the current job
                        job_info = {
                            "ID": str(self.counter),
                            "Apply": job_url,
                            "JobTitle": job_title,
                            "Company": company,
                            "Location": location,
                            "Time": time_posted,
                            "Job Type": job_type,
                            "Experience": experience,
                            "Job Categories": job_categories,
                            "Job Skills": job_skills_str,
                        }

                        # Append the job information to the jobs_data dictionary
                        jobs_data[self.counter] = job_info
                        print(job_info)

                        # Call the callback function to update the data table with the new job information
                        self.callback(job_info)

                        # Increment the counter
                        self.counter += 1

                        # Add a delay between requests to prevent getting blocked
                        time.sleep(2)

            # Check if at least one job is found before displaying completion message
            if jobs_found:
                print(f'Page {i + 1} scrapped successfully')
                print(f'Scraping for "{self.job_title}" jobs is complete. Data has been written to "{self.file_name}".')

                        
            
            # return self.jobs_data

    
    # Function to extract insights from skills data and visualize using a pie chart
    def generate_skills_insights():
        # Concatenate all job skills into a single string
        all_skills_text = ' '.join(job['Job Skills'] for job in jobs_data.values())

        # Split the skills text into individual skills
        all_skills = all_skills_text.split(' | ')

        # Create a Pandas Series from the list of skills
        skills_series = pd.Series(all_skills)

        # Count the occurrences of each skill
        skills_counts = skills_series.value_counts()

        # Calculate the total count of all skills
        total_skills_count = skills_counts.sum()

        # Get the top 4 recurring skills
        top_skills = skills_counts.head(4)

        
         # Create a color palette for the slices
        colors = ['#A8D8EA', '#AA96DA', '#FCBAD3', '#FFC94A'] # pastel  
        #colors = ['#240A34', '#891652', '#EABE6C', '#FFB38E'] #light greens
        #colors = ['#FF204E', '#A0153E', '#5D0E41', '#00224D'] Dark reds
        normal_radius= [80, 65 , 60, 70]
        # Create data for the pie chart
        global pie_chart_data
        pie_chart_data = []

        for i, (skill, skill_count) in enumerate(top_skills.items()):
            # Calculate the percentage of this skill count relative to the total count of all skills
            
            skill_percentage = (skill_count / total_skills_count) * 100
            # Format the title to include both skill count and percentage
            title = f'({skill_percentage:.1f}%)\n {skill}\n ({skill_count} times)'
            # Create the PieChartSection object and add it to the pie_chart_data list
            pie_chart_data.append(
                ft.PieChartSection(
                    value=skill_count,
                    title=title,
                    title_position=1.8,
                    title_style= ft.TextStyle(size=11, font_family="Berlin Sans FB", color="Black50"),
                    color=colors[i % len(colors)],
                    radius=normal_radius[i % len(normal_radius)]
                )
            )

        # Create the pie chart
        global pie_chart
        pie_chart = ft.PieChart(
            
            sections=pie_chart_data,
            sections_space=3,
            center_space_radius=2,
            center_space_color="#ebebeb",
            expand=True,
            on_chart_event=on_chart_event,
            scale=0.85
            
            
            
        )

        return pie_chart
    
    # Pie chart and insights Styling
    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
        size=12, color=ft.colors.BLUE_GREY_300, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=13,
        color=ft.colors.BLUE_GREY_300,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=1, color=ft.colors.WHITE24),
    )

    def on_chart_event(e: ft.PieChartEvent):
        pie_chart.center_space_radius=60
        for idx, section in enumerate(pie_chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        pie_chart.update()
    
    # Insights tab text of all skills layout
    def generate_all_skills():
        # Concatenate all job skills into a single string
        all_skills_text = ' '.join(job['Job Skills'] for job in jobs_data.values())

        # Split the skills text into individual skills
        all_skills = all_skills_text.split(' | ')

        # Create a Pandas Series from the list of skills
        skills_series = pd.Series(all_skills)

        # Count the occurrences of each skill
        global skills_counts
        skills_counts = skills_series.value_counts()

        # Format the top recurring skills as desired
        top_skills_str = '\n'.join(f"{skill} ({count} times)" for skill, count in skills_counts.items()).strip().title()

        return top_skills_str


    #Inputs fields & buttons layout 
    additional_information_field=ft.TextField(label="Additional Information",**TextField_Style,tooltip= "Used for extra tunning of the answer of chatting tool at Consultant TAB")
    website_dropdown= ft.Dropdown(**dropdown_style,hint_text="Targeted Jobs Website", options= [
                                                                                ft.dropdown.Option("WUZZUF Jobs"),
                                                                            ]
                    )
    job_title_field=ft.TextField(label="Job Title",**TextField_Style , tooltip= "Used for Search Results")
    pages_no_field = ft.TextField(value="1", label="Pages No.",**TextField_Style, tooltip= "Used for Search Results")
    search_button= ft.ElevatedButton(width=220, height=50, text="Search & Save as CSV",on_click=lambda e: scrape_jobs_gui(job_title_field, pages_no_field, e))
    upload_resume= ft.ElevatedButton(height=50, text="Upload Resume",on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False,
                                                                                                                    dialog_title="Pick Resume",
                                                                                                                    allowed_extensions=["pdf"]))
    progress_ring= ft.Stack(visible=False, controls=[ft.Container(bgcolor="transparent",content=ft.ProgressRing(color="bluegrey500", tooltip="Building table of jobs",stroke_width=18))])
    progress_bar= ft.Stack(visible=False, controls=[ft.Container(bgcolor="white70",content=ft.ProgressBar(color="bluegrey500", tooltip="Building table of jobs"))])

    def go_to_search():
        tabs.selected_index=1
    
    def scrape_jobs_gui(job_title_field, pages_no_field, e):
    # Get the value from the job title and pages number text fields
        go_to_search()
        progress_ring.visible=True
        search_button.disabled=True
        progress_bar.visible=True
        page.update()
        job_title = job_title_field.value
        pages_no = pages_no_field.value

        # Define the callback function to update the data table
        def update_data_table(job_info):
            fill_data_table(data_table=data_table)

        # Call the JobScraper class to initiate the scraping process
        job_scraper = JobScraper(job_title=job_title, num_pages=int(pages_no), callback=update_data_table)
        # Scrape jobs based on the input parameters
        job_scraper.scrape_jobs()
        update_insights_tab()
        search_button.disabled=False
        progress_ring.visible=False
        progress_bar.visible=False
        page.update()




    inputs_tab_layout= ft.Column(
            controls=[
                ft.Divider(height=10,color="transparent"),
                ft.Container(**Form_style, content= additional_information_field),
                ft.Row(controls=[ft.Container(**Form_style, content= website_dropdown),
                                        
                                 ft.Container(**Form_style, expand= 3, content=job_title_field),
                                 ft.Container(**Form_style, expand= 2, content= pages_no_field),
                                 ft.Container(expand= 1, content= ft.Column(
                                                                            scroll="always",
                                                                            controls= [
                                                                                    upload_resume,
                                                                                    ft.Divider(thickness=1,color="#C6EBC5"),
                                                                                    selected_files,
                                                                                   ])),
                                 ]),
                ft.Divider(height=15,color="System"),
                ft.Row(
                    controls=[
                    progress_ring,
                    search_button,
                                 ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )
    
    inputs_tab= ft.Container(**Form_style,content= inputs_tab_layout)


    #Initialize data table & preview on a row & column for vertical and horizontal scrolling
    data_table= ft.DataTable(**Dt_style,)
    SearchResults_tab_layout= ft.Row(expand=True,scroll="always",controls=[ft.Column(scroll="Always",controls=[data_table])])



                           
    




    insights_tab= ft.Tab(
                    text="Insights",
                    icon=ft.icons.INSIGHTS_OUTLINED,
                    content=ft.Column(controls=[ft.Card(content= ft.Text(value=" Insights starts automatically after job search is complete ",size=26,font_family="Berlin Sans FB"))],alignment=ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                                        ))
    

                   

    # Function to update the Insights tab content
    def update_insights_tab():
        insights_tab.content = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                    ft.Column(
                                width=500,
                                height=500,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll="always", 
                                controls=[
                                    ft.Text(value="Top 4 skills of searched job title",size=16,font_family="Berlin Sans FB",color="black50"),
                                    ft.Container(content= generate_skills_insights(),**Form_style,width=500),   
                                    ]
                            ),
                    
                    ft.Column(
                                width=500,
                                height=600,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll="always", 
                                controls=[
                                    ft.Text(value="All skills of search Result",size=16,font_family="Berlin Sans FB",color="black50"),
                                    ft.Container(content= ft.Text(value=generate_all_skills(),size=14 ,font_family="Berlin Sans FB",color="black50"),**Form_style,width=500),   
                                    ]
                            )
                    ]
        )


    # Consultant Tab functions & layout
    def go_url(e):
        page.launch_url(e.data)
    
    def copy_to_clipboard(e):
        pyperclip.copy(new_answer.value)
        answer_feedback_buttons.controls[0].value="Copied..."
        page.update()
        time.sleep(5)
        answer_feedback_buttons.controls[0].value=""
        page.update()
        

    # Function to append feedback in CSV file whenever button is pressed.
    def append_p_feedback(e, question, answer):
       
    # Define the CSV file path
        csv_file_path = "./feedback/feedback.csv"

        # Prepare data to be appended
        feedback_data = {
            "datestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "status": "Good",
            "question": question,
            "answer": answer
            }
        # Append data to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=feedback_data.keys())

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writeheader()

            # Write the feedback data
            writer.writerow(feedback_data)
            # msg_to_show
            #notif=ft.SnackBar(ft.Text(f"Your feedback is well received, Thank you!"),open=True,duration=5)
    def append_n_feedback(e, question, answer):
        
    # Define the CSV file path
        csv_file_path = "./feedback/feedback.csv"

        # Prepare data to be appended
        feedback_data = {
            "datestamp": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "status": "Bad",
            "question": question,
            "answer": answer
            }
        # Append data to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=feedback_data.keys())

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writeheader()

            # Write the feedback data
            writer.writerow(feedback_data)
            # msg_to_show
            #notif=ft.SnackBar(ft.Text(f"Your feedback is well received, Thank you!"),open=True,duration=5)



    # Initialize variables & Data source " PDF's Directory" & Load Knowledge base
    def load_and_update_DataSource(e):
        
        progress_ring_upload.visible=True
        prompt.label="Pleas wait while loading data...."
        time.sleep(2)
        prompt.disabled=True
        page.update()

        #llm_loader_pdf= PyPDFDirectoryLoader("./Knowledge_Hub")
        llm_loader_pdf= PyPDFLoader(file_path=selected_path.value)
        knowledge_base=llm_loader_pdf.load()

        # # Using Text splitters to make chunks (NLTK Splitters) for splitting by meaning not sentences or characters.
        text_splitter=NLTKTextSplitter(chunk_size=6650)

        # Storing Splitted texts to chunks
        chunks=text_splitter.split_documents(knowledge_base)

        # Defining & initializing instance of embedding model from Bert.net most fast model (all-MiniLM-L6-v2 )
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        global vectorstore_db
        # Storing chunks againts their correspondent embeddings in a Vector Sotre using (FAISS) Facebook AI Similarity Searching Technique 
        vectorstore_db = FAISS.from_documents(chunks,embedding_function)
        
        prompt.disabled=False
        progress_ring_upload.visible=False
        prompt.label= "Now Ready! How Can I Help You today?"
        page.update()
        
        return vectorstore_db
    

    # question processing
    def process_question(e):
        
        #question to be inputted by user.
        information=additional_information_field.value
        question_holder = prompt.value
        asked_question = question_holder
        search_results= vectorstore_db.similarity_search(asked_question,k=10)
        
        # Creating new question and answer elements to be backed with each prompt
        # Handling user input and generating answer from LLM
        new_question = ft.Text(value=f" \n Muhammed Mo'men: \n\n {prompt.value} \n ",selectable=True,color="system")

        # Question Edit button
        #edit_button = ft.IconButton(icon=ft.icons.EDIT_NOTE_SHARP,tooltip="edit question")
        question_packed=ft.Container(content=new_question,bgcolor="system",border_radius=5,expand=True,shadow=ft.BoxShadow(spread_radius=0.9))
        question_and_buttons=ft.Row([question_packed])
        
        # Appending new question elements to chat_area list view 
        new_question_packed = ft.Card(content=question_and_buttons)
        chat_area.controls.append(new_question_packed)

        # Updating chat_area_holder Card content with the new question
        chat_area_holder.content=chat_area

        # Rendring updates to be reflected on page  
        page.update()
        time.sleep(1)

        prompt.label="Generating answer, Please wait............."
        time.sleep(2)
        prompt.disabled=True
        page.update()


        template = """

        You are AI career coach who can be consulted to give great tips and recommend suitable jobs from the list of jobs hereunder and based on information provided in my resume hereunder also,    
        here are the list of jobs {jobs_data} and here is the resume:{context} and here are some extra information about me {additional_information}.
        
        Now you can answer my question about my career goal which is: {question}, then you can do the following.

        Give a rich answer after checking the list of jobs and the resume then:
        1- If there is mismatch between jobs searched and my current or past career, tell me that jobs are irrelevant.
        2- Recommend Best suitable jobs with their correspondent ID in case it matches my career or career advancement, then justify why you choose those jobs and their ID's.
        3- Recommend tips that align with my resume to improve myself.
        4- Give general tips about being profesionnal in applying to jobs, professional communication with recruiters, to do and not to do.
        ,if answer is professional and accurate enough I will tip 400$.

        

        """

        formatted_prompt=template.format(jobs_data=jobs_data,context=search_results,additional_information=information, question=asked_question)
        llm_response= ft.Text(value= llm.invoke( formatted_prompt ),color="system")
        

        
        global new_answer
        new_answer = ft.Markdown(
            value=f"Erudite AI Consultant:\n " + f"{llm_response.value} \n",
            code_theme="atom-one-dark",
            code_style= ft.TextStyle(font_family="Roboto Mono",color="system"),
            selectable=True,
            extension_set="gitHubFlavored",
            on_tap_link=go_url,
            expand=True
            )

        # Answer feedback buttons
        global answer_feedback_buttons
        answer_feedback_buttons = ft.Row(controls=[ ft.Text(value=None,color="grey500",bgcolor="bluegrey500"),
                                                    ft.IconButton(icon=ft.icons.SENTIMENT_VERY_SATISFIED_OUTLINED, bgcolor="green",icon_color="white",tooltip="Good Answer",
                                                                  on_click=append_p_feedback(e,asked_question,new_answer.value)),

                                                    ft.IconButton(icon=ft.icons.SENTIMENT_DISSATISFIED_SHARP, bgcolor="red",icon_color="white",tooltip="Poor Answer!",
                                                                  on_click=append_n_feedback(e,asked_question,new_answer.value)),

                                                    ft.IconButton(icon=ft.icons.COPY_OUTLINED, bgcolor="white",icon_color="black",tooltip="Copy Answer",
                                                                  on_click=copy_to_clipboard),
        
                                                    ])

        answer_packed=ft.Container(content=new_answer,bgcolor="system",border_radius=5,expand=True, shadow=ft.BoxShadow(spread_radius=0.9))

        answer_and_buttons=ft.Row([answer_packed,answer_feedback_buttons])
        new_answer_card_packed = ft.Card(content=answer_and_buttons)

        # Appending new answer elements to chat_area list view
        chat_area.controls.append(new_answer_card_packed)

        # Updating chat_area_holder Card content with the new generated answer  
        chat_area_holder.update()

        prompt.value= ""
        prompt.label= "Can I help you with something else?"
        prompt.disabled= False
        print(llm_response.value)

        # Rendring updates to be reflected on page  
        page.update()
        
    
    
    


    #Model initialize & General Parameters
    temperature=0.7
    n_of_responses=1
    max_output_tokens=1024
    
    # instance of google gemini pro LLM 
    llm = GoogleGenerativeAI(
                            model="gemini-pro",
                            google_api_key=google_api_key,
                            temperature= temperature,
                            max_output_tokens= max_output_tokens,
                            n= n_of_responses
                            )
    

    
    # User Creds
    user_name= "Muhammed Mo'men"


    ## Layout components ( Chat window , Prompt inputs, Question edit button, Answer feedback buttons ) ##
    # Chat Window & Welcome Message
    welcome_msg = ft.Text(value= f"""\n\n\n\n Hello again {user_name}, \n\n\n Erudite at your service, I am your AI Job Seeker and would be glad to help you get some career coach help """,
                       style=ft.TextThemeStyle.TITLE_LARGE,
                       font_family="Segoe UI Semilight",
                       text_align= ft.TextAlign.CENTER,
                       color="system",
                       
                        )
    welcome_msg_image = ft.Container(ft.Image(
                            src="/Logo.png",
                            width=300,
                            height=100,
                            fit=ft.ImageFit.CONTAIN,
                            border_radius=15,

                            ),
                            url="https://wuzzuf.net/jobs",
                            border_radius=20,

                            )
    
    images = ft.Row(width=500,expand=1, wrap=False, scroll="always")

    for i in range(1, 7):
        images.controls.append(
            ft.Container(ft.Image(
                src=f"/image{i}.png",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(25),
                tooltip="Employment Websites",
                opacity=1,
                ),
                
                
                shadow=ft.BoxShadow(spread_radius=0.25,color="white",),border_radius=25,height=101,
                url_target="Go to the website",
                url="https://wuzzuf.net/jobs"
                )
                
        )
    page.update()
    
    welcome_msg_container=ft.Column(controls=[welcome_msg_image,welcome_msg,images],horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    #
    chat_area = ft.ListView(controls=None, padding=10,spacing=10,auto_scroll=True, expand= True)
    chat_area_holder=ft.Card(content=welcome_msg_container,expand=True,shadow_color="black",width=1500)

    # Prompt inputs
    prompt = ft.TextField(label= " Please press the chat icon button first, to let the AI read your CV, Info & Job results >>>>>  ",
                          label_style= ft.TextStyle(color="grey500",size=12,font_family="Segoe UI Semibold"),
                          multiline=True,
                          min_lines=1,
                          max_lines=4,
                          expand=True,
                          shift_enter=True,
                          enable_suggestions=True,
                          helper_text= " | Please cross validate answers as false answers may be generated |",
                          helper_style=ft.TextStyle(color="grey700",size=9,font_family="Segoe UI Semilight",weight="w600"),
                          )
    
    send_button = ft.IconButton(icon=ft.icons.SEND_SHARP,on_click= process_question,tooltip="Send message to Erudite",icon_color="green")
    file_upload = ft.IconButton(icon=ft.icons.CHAT_SHARP,on_click= load_and_update_DataSource,tooltip=" Let Erudite read your\n CV, Info & Job results  ",icon_color="bluegrey500")
    progress_ring_upload= ft.Stack(visible=False, controls=[ft.Container(bgcolor="transparent",content=ft.ProgressRing(color="bluegrey500", tooltip="Loadin...Please wait",stroke_width=5))])

    input_row = ft.Row(controls=[
        prompt,
        send_button,
        file_upload,
        progress_ring_upload,
        ],alignment=ft.MainAxisAlignment.END)                                        

    tabs = ft.Tabs(
        selected_index=0,
        scrollable=False,
        unselected_label_color="Bluegrey200",
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Inputs",
                icon=ft.icons.INPUT_ROUNDED,
                content=ft.Column(controls=[inputs_tab]),
            ),
            ft.Tab(
                text="Search Results",
                icon=ft.icons.SEARCH_OUTLINED,
                content=ft.Column(controls=[progress_bar,SearchResults_tab_layout]),
            ),
            ft.Tab(
                text="Consultant",
                icon=ft.icons.CHAT_BUBBLE_OUTLINE_OUTLINED,
                content=ft.Column(controls=[chat_area_holder,input_row]),
            ),
            # replaced with variable for more flexibility
            insights_tab,
        ],
        expand=True,
    )

    header= ft.Container(**Form_style,content=ft.Row(alignment=ft.MainAxisAlignment.END,controls=[cs.ThemeSwitch(page)]))

    page.add(header,tabs)

    fill_data_table(data_table=data_table)

ft.app(target=main)
#ft.app(target=main,view=ft.AppView.WEB_BROWSER,name="ajs",port="8000")