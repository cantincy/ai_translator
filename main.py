import streamlit
import streamlit as st
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

options = ["中文（Chinese）", "英语（English）", "日语（Japanese）",
           "韩语（Korean）", "法语（French）", "德语（German）", "俄语（Russian）",
           "西班牙语（Spanish）", "意大利语（Italian）", "葡萄牙语（Portuguese）", "阿拉伯语（Arabic）"]


@streamlit.cache_resource
def get_chain():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
            you are a helpful assistant that translates text.
            you can translate {original_language} to {target_language}.
            """),
            ("human", "{input}"),
        ]
    )

    parser = StrOutputParser()

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_parser=parser,
        verbose=True
    )

    return chain


def main():
    if "target_text" not in st.session_state:
        st.session_state.target_text = ""

    original_language = st.selectbox("original language", options)
    target_language = st.selectbox("target language", options)

    original_text = st.text_area("original text", max_chars=1000)

    st.text_area("target text", value=st.session_state.target_text)

    if st.button("translate"):
        if original_language and target_language and original_text:
            if original_language == target_language:
                res = original_text
            else:
                chain = get_chain()
                user_input = f"""
                    the original text is:
                    ```
                    {original_text}
                    ```
                    you need to translate the original text to the target language.
                    just return the translated text, do not add any explanation.
                    if the original text is not in the original language, just return nothing.
                    """

                res = chain.invoke({
                    "original_language": original_language,
                    "target_language": target_language,
                    "input": user_input,
                })["text"]

            st.session_state.target_text = res
            st.rerun()
        else:
            st.warning("please fill in all the fields")


if __name__ == "__main__":
    main()
