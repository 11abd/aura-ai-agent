from app.config.llm import get_llm

def test_llm():
    llm = get_llm()


    response = llm.invoke("Say hello like a professional AI system.")

    print("LLM Response:")
    print(response.content)


if __name__ == "__main__":
    test_llm()
