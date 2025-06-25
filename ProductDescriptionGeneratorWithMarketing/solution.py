import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import uuid
import streamlit.components.v1 as components
import html

load_dotenv()
GROQ_APIKEY=os.getenv("GROQ_APIKEY")

## Setting ChatGroq with parameters for llm setup
groqAiLLM=ChatGroq(
    api_key=GROQ_APIKEY,
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
) 

##

## Input variable declaration for the prompt

# ProductName=None
# ProductFeature=None
# resultChain1=None
# resultChain2=None
# Platform=None
# SEOKeyword=None
# Tone=None
##

## Title with Streamlit


st.title("Product Description Generator with Marketing Angle 😇")

## Custom copy button function

def create_copy_button(text_to_copy):
    button_id = f"copyButton-{uuid.uuid4().hex}"
    escaped_text = html.escape(text_to_copy).replace('"', '&quot;')
    
    button_html = f"""
    <button id="{button_id}"  style="padding: 5px; display: inline ;border-radius: 25px;" >Copy</button>
    <script>
        let copyButton = document.getElementById("{button_id}")
        if(copyButton){{
            copyButton.addEventListener(`click`, function(){{
                navigator.clipboard.writeText("{escaped_text}").then(() => {{alert("Copied to clipboard!")}}).catch(() => {{alert("Failed to copy")}})
            }})
        }}
    
    </script>
    """
    
    components.html(button_html, height=100)

##


## Function for stramlit output

def StreamlitOutPut(Product_Name,Product_Feature,seo_keyword,tone,platform):
    templateOfTiTle='''
You are a seasoned SEO specialist with deep expertise in digital sales and marketing copywriting.

Your task is to craft a compelling, creative, and attention-grabbing product title that:
- Begins with one or two bold, exclusive, and premium-sounding words that convey a sense of quality and effectiveness to the end user.
- Clearly highlights the product’s key feature.
- Appeals to the target audience’s emotions, needs, or desires.
- Incorporates relevant keywords for optimal SEO visibility.
- Is concise (preferably under 70 characters), yet impactful and engaging.

Use the information below:
- Product Name: {ProductName}
- Key Feature: {ProductFeature}

Respond with only the final product title as plain text—no formatting, explanations, or additional output.
'''

    FinalTiTlePrompt=PromptTemplate(
        input_variables=["ProductName","ProductFeature"],
        template=templateOfTiTle,
    )

    ## Chaining

    chain1=FinalTiTlePrompt| groqAiLLM

    resultChain1=chain1.invoke({
        "ProductName":Product_Name,
        "ProductFeature":Product_Feature
    })
    templateOfDescription='''
You are a seasoned marketing copywriter with expertise in persuasive product descriptions and conversion-focused content.

Your task is to write a compelling, engaging, and benefit-driven product description based on the following product title:
- Product Title: {ProductTitle}

The description should:
- Expand on the product’s key benefits and what makes it stand out.
- Emphasize its value, efficiency, and appeal to the target customer's desires or problems.
- Maintain a confident, persuasive marketing tone.
- Be concise, ideally between 50 to 100 words.
- Be suitable for use on an e-commerce website or digital marketplace.

Respond with only the final product description as plain text—no formatting, explanations, or additional output.

'''
    FinalDescriptionPrompt=PromptTemplate(
        input_variables=["ProductTitle"],
        template=templateOfDescription
    )


    ## Chaining

    chain2=FinalDescriptionPrompt| groqAiLLM

    resultChain2=chain2.invoke({
        "ProductTitle":resultChain1.content
    })

    templateOfCaption = '''
You are a professional social media copywriter skilled in crafting engaging, concise, and brand-aligned captions for various digital platforms.

Your task is to write a high-quality social media caption based on the following product information:

- Product Title: {ProductTitle}
- Product Description: {ProductDescription}

Incorporate the following elements:
- SEO Keyword: {SEOKeyword}
- Tone/Style: {ToneModifier} (e.g., bold, luxurious, minimalist, warm, fun, modern, inspiring)

The caption must:
- Grab attention in the first line.
- Highlight a key benefit, use case, or emotional appeal.
- Seamlessly include the SEO keyword.
- End with a light call-to-action (e.g., try it, learn more, tap to explore).
- Fit within 30–70 words for ideal platform performance.

Platform: {Platform} (e.g., Instagram, LinkedIn, Facebook)

Respond with only the final caption—no formatting, hashtags, or additional commentary.
'''
    FinalCaptionPrompt=PromptTemplate(
        input_variables=["ProductTitle","ProductDescription","SEOKeyword","ToneModifier","Platform"],
        template=templateOfCaption
    )

    ## Chaining

    chain3=FinalCaptionPrompt| groqAiLLM

    resultChain3=chain3.invoke({
        "ProductTitle":resultChain1.content,
        "ProductDescription":resultChain2.content,
        "SEOKeyword":seo_keyword,
        "ToneModifier":tone,
        "Platform":platform
    })
    ## Output for the product title
    if(resultChain1 and resultChain2 and resultChain3):
        col1,col2,col3=st.columns(3)
        with col1:
            st.write("Product Title:")
            colA,colB=st.columns(2)
            with colA:
                st.write(resultChain1.content)
            with colB:
                create_copy_button(resultChain1.content)
        with col2:
            st.write("Product Description:")
            colA,colB=st.columns(2)
            with colA:
                st.markdown(
                        f"""
                            <div style="
                                border: 1px solid #ccc;
                                padding: 10px;
                                height: 300px;
                                overflow-y: auto;
                                background-color: #00000;
                                white-space: pre-wrap;
                                font-family: monospace;
                            ">
                                {resultChain2.content.strip()}
                            </div>
                        """,
                    unsafe_allow_html=True
                )

            # st.write(resultChain2.content)
            with colB:
                create_copy_button(resultChain2.content)
        with col3:
            st.write("Caption:")
            colA,colB=st.columns(2)
            with colA:
                st.write(resultChain3.content)
            with colB:
                create_copy_button(resultChain3.content)

    

   


## Form using Streamlit

with st.container():

    with st.form("my_form"):
        ProductName = st.text_input(
            "Enter Product Name:",   
        )
        ProductFeature=st.text_area("Enter Product Feature:")
        SEOKeyword=st.text_input(
            "Enter SEO keyword :",   
        )
        Tone=st.text_input(
            "Enter tone: "
        )
        Platform=st.selectbox("Select Platform:", ["Instagram", "Twitter", "FaceBook", "Email", "Youtube", "Linkedin"])
        submitted=st.form_submit_button("Submit")
        if (submitted):
            if (not( ProductFeature and  ProductName and  SEOKeyword and  Tone and  Platform)):
                st.warning("Please enter all Features.")
            else:
                ## The prompting and tuning output for the product Title and description
                ## Product Title Prompt tuning
                StreamlitOutPut(Product_Name=ProductName,Product_Feature=ProductFeature,seo_keyword=SEOKeyword,tone=Tone,platform=Platform)
           