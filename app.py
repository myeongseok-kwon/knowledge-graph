# Import necessary libraries
import streamlit as st  # For creating the web application
import networkx as nx  # For creating and manipulating graphs
import matplotlib.pyplot as plt  # For plotting (not used in this code)
from pyvis.network import Network  # For interactive graph visualization
from termcolor import colored  # For colored console output
import streamlit.components.v1 as components  # For embedding custom HTML in Streamlit
import PyPDF2  # For reading PDF files
import xml.etree.ElementTree as ET  # For parsing XML
import base64  # For encoding data for download links
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Asynchronous function to extract entities and relations from text using an AI model
def get_entities_and_relations(text):
    # Define the system message for the AI model
    system_message = """
    You are an expert in natural language processing and knowledge extraction.
    Given a text, identify the main entities and their relationships.
    Return your response in the following XML format:

    <output>
        <entities>
            <entity>Entity1</entity>
            <entity>Entity2</entity>
            ...
        </entities>
        <relations>
            <relation>
                <source>SourceEntity</source>
                <target>TargetEntity</target>
                <type>RelationType</type>
            </relation>
            ...
        </relations>
    </output>

    Ensure that the XML is well-formed and does not contain any syntax errors. 
    You must absolutely at all times return your response in the format presented regardless of how large the document is.
    If the document is long and overwhelming, then still do your best in returning as many entities as you can without making a mistake.
    """

    chat_completion = client.chat.completions.create(
      model="gpt-4o-mini",  # Consider using the latest model that best fits your needs
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Here is the text which you will be analyzing: {text}\nExtract entities and relations from this text in exactly the format presented"}
      ]
    )
    response = chat_completion.choices[0].message.content    
    # Send the text to the AI model for analysis    
    return response

# Asynchronous function to generate a summary of the input text
def get_summary(text):
    system_message = """
    You are an expert summarizer. Your task is to provide a concise (Sentences + bullet points) and informative
    summary of the given text.
    
    Focus on the main ideas, key points, and essential information.
    
    Ensure that your summary is coherent, well-structured, and captures the essence of the original text.
    
    Aim for a summary that is approximately 10-15% of the length of the original text, unless the text is very
    short or long.
    """

    chat_completion = client.chat.completions.create(
      model="gpt-4o",  # Consider using the latest model that best fits your needs
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Please provide a comprehensive summary of the following text: {text}"}
      ]
    )
    response = chat_completion.choices[0].message.content

    return response

# Asynchronous function to extract detailed entity information in JSON format
def get_json_entities(text):
    
    system_message = """
    You are an expert in entity extraction and classification. Your task is to extract entities from the given
    text and return them in ALWAYS a structured JSON format AND ALWAYS in between <output></output> tags.
    
    For each entity, provide the following information:
    
    1. Name: The name or identifier of the entity
    2. Type: The category or class of the entity (e.g., Person, Organization, Location, Event, Concept)
    3. Description: A brief description or context of the entity as it appears in the text
    
    Return your response always in the following JSON format and always in between <output></output> tags:
    <output>
    {
        "entities": [
            {
                "name": "Entity Name",
                "type": "Entity Type",
                "description": "Brief description of the entity",
            },
            ...
        ]
    }
    </output>
    
    Ensure that the JSON is well-formed and does not contain any syntax errors. It is essential that you return
    the JSON in the exact format presented above. If the document is long and overwhelming then still do your
    best in returning as many important entities as you can without making a mistake.
    """

    chat_completion = client.chat.completions.create(
      model="gpt-4o",  # Consider using the latest model that best fits your needs
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Extract and classify entities from this text in the specified JSON format: {text}"}
      ]
    )
    response = chat_completion.choices[0].message.content    
    # Extract JSON content from the response
    json_start = response.find('<output>') + len('<output>')
    json_end = response.rfind('</output>')
    json_content = response[json_start:json_end].strip()
    
    return json_content

# Function to parse the XML output from the AI model
def parse_output(output):
    try:
        # Find the XML content within the response
        xml_start = output.find('<output>')
        xml_end = output.rfind('</output>') + 9  # Length of '</output>'
        
        if xml_start == -1 or xml_end == -1:
            raise ValueError("XML tags not found in the output")
        
        xml_content = output[xml_start:xml_end]

        xml_content = xml_content.replace('&', '&amp;')
        
        # Parse the XML content
        root = ET.fromstring(xml_content)
        
        # Extract entities and relations from the parsed XML
        entities = [entity.text for entity in root.find('entities')]
        
        relations = [
            {
                'source': relation.find('source').text,
                'target': relation.find('target').text,
                'type': relation.find('type').text
            }
            for relation in root.find('relations')
        ]
        
        return entities, relations
    
    except ET.ParseError as e:
        # Handle XML parsing errors
        st.error(f"Error parsing XML: {e}")
        st.error("Raw output:")
        st.code(output)
        return [], []
    
    except ValueError as e:
        # Handle value errors (e.g., missing XML tags)
        st.error(f"Error: {e}")
        st.error("Raw output:")
        st.code(output)
        return [], []

# Function to create a graph from extracted entities and relations
def create_graph(entities, relations):
    G = nx.Graph()
    for entity in entities:
        G.add_node(entity)
    for relation in relations:
        G.add_edge(relation['source'], relation['target'], type=relation['type'])
    return G

# Function to visualize the graph using Pyvis
def visualize_graph(G):
    net = Network(notebook=True, width="100%", height="600px", directed=True)
    for node in G.nodes():
        net.add_node(node)
    for edge in G.edges(data=True):
        net.add_edge(edge[0], edge[1], title=edge[2]['type'])
    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        graph_html = f.read()
    return graph_html

# Function to read text from a PDF file
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to create a download link for content
def get_download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'

# Set up the Streamlit page
st.set_page_config(layout="wide")

st.title("Knowledge Graph from Documents")

# Allow user to choose between pasting text or uploading a file
input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"])

if input_method == "Paste Text":
    text = st.text_area("Enter your text here:")
else:
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            with st.spinner("Loading PDF..."):
                text = read_pdf(uploaded_file)
            st.success("File uploaded successfully!")
        else:
            text = ""

if st.button("Generate Knowledge Graph"):
    if text:
        with st.spinner("Generating graph visualization..."):
            output = get_entities_and_relations(text)
            entities, relations = parse_output(output)
            G = create_graph(entities, relations)
            graph_html = visualize_graph(G)

        st.subheader("Knowledge Graph:")
        components.html(graph_html, height=600)

        # Provide a download link for the graph
        st.markdown(get_download_link(graph_html, "knowledge_graph.html", "Download Knowledge Graph"), unsafe_allow_html=True)
