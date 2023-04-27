import os
from LLM import complete_text_fast


def understand_file(file_name, things_to_look_for, folder_name = ".", group_by=200):
    lines = open(os.path.join(folder_name,file_name)).readlines()

    # zip lines with line id 
    # lines = [f"{i+1}: {l}" for i, l in enumerate(lines)]
    # group by group_by lines
    blocks = ["\n".join(lines[i:i+group_by]) for i in range(0, len(lines), group_by)]

    descriptions  = []
    for idx, b in enumerate(blocks):
        start_line_number = group_by*idx+1
        end_line_number = group_by*idx+1 + len(b.split("\n"))
        prompt = f"""Given this (partial) file from line {start_line_number} to line {end_line_number}: 

        ``` 
        {b}
        ```

        Here is a detailed description on what to look for and what should returned: {things_to_look_for}

The description should short and also reference crtical lines (numbers and content) in the script relevant to what is being looked for. Only describe what is directly supported by the file content. Do not include additional information not supported. You can say "Nothing Found" if you cannot find anything relevant.
        """

        completion = complete_text_fast(prompt)
        descriptions.append(completion)
    if len(descriptions) == 1:
        return descriptions[0]
    else:
        prompt = f"""Summarize the following descriptions to get a detailed description on: {things_to_look_for}

        {descriptions}
        """

        completion = complete_text_fast(prompt)
        return completion