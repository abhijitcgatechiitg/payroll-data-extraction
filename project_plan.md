Payroll Data Extraction

Goal: To create a extraction system for payroll data which can work accross different report types and is able to extract information into a global schema system. Global schema is a fixed schema which caters to all report types ideally. 

Given: 
I have provided a few examples in the sample_pdfs folder. 
global_schema.py which can be edited as we proceed.

Idea:
We will build a two pass system where first we will extract the information from the pdf using pymupdf.
Let's skip the section detection part from previous code as I will pass the exact pdf required for this purpose. 
Once we have the text from the pdf, we will then use LLM and a prompt to extract an interim json. This will be a raw extraction of the text and no mapping is done yet. Just a simple read and creating a interim json schema

Once we have the schema, we will map it to global schema using another LLM PASS, this doing a 2 pass system which helps with accuracy. 
Once it is mapped, it will be saved to a output folder. 
Mapping is done using LLM knowledge of payroll as well as some rules or guidelines in prompt. 

As we do each step, i would like to create a folder for a pdf, that way all the intermidiate and the final output will be saved in a folder by the name of the pdf. 

