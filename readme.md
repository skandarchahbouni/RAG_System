## Docs Manager (DM)
    - params:
        - file 
    - returns
        - None
    - features: 
        - calculate embedding of a document (reflect deletion as well and update)
## Information Retrieval (IR)
    - params: 
        - user prompt 
    - returns: 
        - context: matched chuncks
    - features:
        - select the promising chuncks based on user prompt by calculating cosine similarity.
## Response Generation (RG)
    - params:
        - context
        - user prompt
    - returns:
        - response
    - features:
        - use an LLM to generate a response using a prompt template that contains the congtext + usger prompt.
## Queries Manager (QM)
    - params:
        - user prompt
    - returns:
        - response
    - features:
        - orchestrate the whole process, first it calls the IR microservice to get the context, than calls  the RG microservice to get the response, and displays the response to the user.
    

 ## Example questions:
    - What does the lighthouse light represent in the story?
    - What does Clara ask Elias to make for her?
    - What does the woman in the garden ask Mira to do?
    - What do the Whispering Shadows tell Hannah she needs?