from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class Translator:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                    you are a helpful assistant that translates text.
                    you can translate {original_language} to {target_language}.
                    """),
                ("human", """
                    the original text is:
                    ```
                    {original_text}
                    ```
                    you need to translate the original text to the target language.
                    just return the translated text, do not add any explanation.
                    if the original text is not in the original language, just return nothing.
                    """),
            ]
        )

        llm = ChatOpenAI()

        parser = StrOutputParser()

        chain = prompt | llm | parser

        self.chain = chain

    def translate(self, original_language, target_language, original_text):
        if original_text and target_language and original_language:
            if original_language == target_language:
                return original_text

            try:
                res = self.chain.invoke(
                    {
                        "original_language": original_language,
                        "target_language": target_language,
                        "original_text": original_text
                    })

                return res
            except Exception as e:
                return e

        return None
