from prompts.policy import PolicyPrompt


def get_prompt(domain: str):

    if domain == "policy":
        return PolicyPrompt()


    return PolicyPrompt()  # default fallback
