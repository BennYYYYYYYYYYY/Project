import textwrap
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import FewShotPromptTemplate, PromptTemplate


import pandas as pd

def definition_prompt_zero_cot():
    content = {
    "Readability":textwrap.dedent('''
    '''),


    "Subjectivity":textwrap.dedent('''
    '''),


    "GreenWashing":textwrap.dedent('''                      
    '''),


    "Ambiguity":textwrap.dedent('''
    '''),


    "Timeliness":textwrap.dedent('''                 
    '''),


    "Sentiment":textwrap.dedent('''
    '''),


    "ESG":textwrap.dedent('''
    ''')
    }
    
    return content


def definition_prompt_for_zero_shot():
    content = {
    "Sentiment":textwrap.dedent('''
    '''),


    "ESG":textwrap.dedent('''
    ''')
    }
    
    return content


def definition_prompt_for_few_shot_prefix():
    content = {  
    "Sentiment":textwrap.dedent('''
    '''),

    "ESG":textwrap.dedent('''    
    ''')
    }
    return content


def definition_prompt_for_few_shot_suffix():
    content = textwrap.dedent('''
    ''')

    return content

    
def system_prompt_cot():
    content = ''
    return content

def system_prompt_without_cot():
    content = ''
    return content


def llms_prompt_zero_shot_cot(topic: str): 
    definition_prompt_use = definition_prompt_zero_cot()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_cot()),
            ("human", definition_prompt_use[topic])
        ]
    )
    return prompt


def llms_prompt_zero_shot(topic: str): 
    definition_prompt_use = definition_prompt_for_zero_shot()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_without_cot()),
            ("human", definition_prompt_use[topic])
        ]
    )
    return prompt


def llms_prompt_few_shot(topic: str, df): 
    definition_prompt_use_prefix = definition_prompt_for_few_shot_prefix()
    # Prompt 模板
    example_prompt = PromptTemplate(
        input_variables= ["text", "label"],
        template = "Example Sentence:{text}\nNumber:{label}" 
    )

    # ExampleSelector 動態挑選範例
    if topic == "Sentiment":        
        sampled_df_0 = df[df["label"]==0].sample(n=1)
        sampled_df_1 = df[df["label"]==1].sample(n=1)
        sampled_df_2 = df[df["label"]==2].sample(n=1)
        sampled_df = pd.concat([sampled_df_0, sampled_df_1, sampled_df_2], ignore_index=True)
        sampled_examples = sampled_df.to_dict("records")
    else:
        sampled_df_0 = df[df["label"]==0].sample(n=1)
        sampled_df_1 = df[df["label"]==1].sample(n=1)
        sampled_df_2 = df[df["label"]==2].sample(n=1)
        sampled_df_3 = df[df["label"]==3].sample(n=1)
        sampled_df = pd.concat([sampled_df_0, sampled_df_1, sampled_df_2, sampled_df_3], ignore_index=True)
        sampled_examples = sampled_df.to_dict("records")
    
    # Few-shot Prompt
    few_shot_prompt = FewShotPromptTemplate(
        examples=sampled_examples,
        example_prompt = example_prompt,
        prefix = definition_prompt_use_prefix[topic],
        suffix = definition_prompt_for_few_shot_suffix(),
        input_variables=["value"],
        example_separator="\n",
        template_format="f-string",
        validate_template=True
    )

    # final_prompt_text = few_shot_prompt.format(value="Your test sentence here")
    # print("final_prompt_text")
    return few_shot_prompt


def get_variable_list():
    content = definition_prompt_zero_cot()
    return list(content.keys())


if __name__ == "__main__":
    # print(llms_prompt("Readability"))
    print(get_variable_list())
    
print(f"Prompt Topic:{get_variable_list()}")