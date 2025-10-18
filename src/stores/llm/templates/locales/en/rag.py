from string import Template

system_prompt = Template(
    "\n".join(
        [
            "You are an assistant to generate a response for the user.",
            "You will be provided by a set of documents that are relevant to the user's question.",
            "You will need to use the documents to generate a response for the user.",
            "You have to generate response based on documents provided",
            "Ignore the documents that are not relevant to the user's query.",
            "You have to generate the response in the same language as the user's query.",
            "Be concise and to the point.",
            "Use markdown to format your response.",
            "Be Polite and Friendly.",
            "Be professional and knowledgeable.",
            "Avoid unnecessarly information",
        ]
    )
)


### Document ###
document_prompt = Template(
    "\n".join(
        [
            "## Document $doc_num",
            "### Content: $chunk_text",
        ]
    )
)


### Footer ###
footer_prompt = Template(
    "\n".join(
        [
            "Based Only on the above documents, please generate an answer for the user.",
            "## Answer: ",
        ]
    )
)
