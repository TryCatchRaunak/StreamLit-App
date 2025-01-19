from crewai import Agent, Task, LLM, Crew
from crewai_tools import SerperDevTool
import streamlit as st
from dotenv import load_dotenv

load_dotenv()



#StreamLit page config
st.set_page_config(page_title="Content Rsearcher and Writer", page_icon="📝", layout="wide")

#Title and description
st.title("Content Researcher and Writer, powered by CrewAI.")
st.markdown("Generate blog posts about any topic using AI agents.")



#Sidebar
with st.sidebar:
    st.header("Content Settings")

    #Make the text input take up more space
    topic = st.text_area(
        "Enter Your Topic",
        height=100,
        placeholder="Enter the topic"
    )

    #Add more sidebar controls if needed
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    #Add more spacing
    st.markdown("----")

    #Make the generate button more prominent in the sidebar
    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

    #Add some helpful information
    with st.expander("ℹ️ How to use"):
        st.markdown("""
            1. Enter your desider content topic
            2. Play with the temperature
            3. Click 'Generate Content' to start
            4. Wait for the AI to generate your article
            5. Download the result as a markdown file
            """)


def generate_content(topic):
    llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

    search_tool = SerperDevTool(n_results=10)



    #First Agent: Senior Research Analyst
    senior_research_analyst = Agent(
        role = "Senior Research Analyst",
        goal = f"Research, analyze and synthesize comprehensive information on {topic} from relatable web sources",
        backstory = "You're an expert research analyst with advanced web search skills."
                    "You exel at finding, analysing and synthesizing information from"
                    "across the internet using search tools. You're skilled at"
                    "distinguishing reliable sources form unreliable ones,"
                    "fact-checking, cross-referencing information, and"
                    "identifying key patterns and insights. You provide"
                    "well-organised research briefs with proper citations"
                    "and source verification. Your analysis includes both"
                    "raw data and interpreted insights, making complex"
                    "information accessible and actionable.",
        allow_delegation = False,
        verbose=True,
        tools = [search_tool],
        llm = llm
    )

    #Second Agent: Content Writer
    content_writer = Agent(
        role="Content Writer",
        goal="Transform research findings into engaging blog posts while maintaining accuracy",
        backstory="You're a skilled content writer specialized in creating"
                  "engaging, accessible content from technical research."
                  "Your work closely with senior research analyst and excel and maintaining the perfect"
                  "balance between informative and entertaining writing,"
                  "while ensuring all facts and citations from the research"
                  "are properly incorporated. You have a talent for making"
                  "complex topics approachable without oversimplifying them.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )


    #Research Task
    research_task = Task(
        description = (
            """
            1. Conduct comprehensive research on {topic} including:
                - Recent Developments and News
                - Key industry trends and innovations
                - Expert opinion and analyses
                - Statistical Data and market insights
            2. Evaluate source credibility and fact-check all information
            3. Organize findings into a structured research brief
            4. Include all relevant citations and sources
            """
        ),
        expected_output = """
                        A detailed research report containing:
                            - Executive summary of key findings
                            - Comprehensive analysis of current trends and developments
                            - List of verified facts and statistics
                            - All citations and links to original sources
                            - Clear categorization of main themes and patterns
                        Please format with clear section and bullet points for easy reference.""",
        agent = senior_research_analyst
    )

    #Writing Task
    writing_task = Task(
        description=("""
            Using the research brief provided, create an engaging blog post that:
            1. Transforms technical informtaion into accessible content
            2. Maintains all factual accuracy and citations from the research
            3. Includes:
                - Attention-grabbing introduction
                - Well-structured body sections with clear headings
                - Compelling conclusion
            4. Preserves all source citations in [Source: URL] format
            5. Includes a Referrences section at the end.
        """),
        expected_output="""A polished blog post in markdown format that:
                - Engages readers while maintaining accuracy
                - Contains properly structured sections
                - Includes Inline citations hyperlinked to the original source url
                - Presents information in an accessible yet informative way
                - Follows proper markdown formatting, use H1 for the title and H3 for sub-sections""",
        agent=content_writer
    )



    #Create a crew
    crew = Crew(
        agents=[senior_research_analyst, content_writer],
        tasks=[research_task, writing_task],
        verbose=True
    )

    return crew.kickoff(inputs={"topic": topic})

#Main content area
if generate_button:
    with st.spinner("Generating Content...This may take a moment.."):
        try:
            result = generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            #Add download button
            st.download_button(
                label="Download Content",
                data=result.raw,
                file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


#Footer
st.markdown("----")
st.markdown("Built with CrewAI, Streamlit, Ollama(llama3.2)")