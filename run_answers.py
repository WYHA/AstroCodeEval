import json
import os
import sys
import gzip
import concurrent.futures as cfuts

from tqdm import tqdm
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def call_openai_api(system_prompt, prompt, temperature, n, model, max_tokens, stop) -> list[str]:
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    while True:
        try:
            result = client.chat.completions.create(
                model=model,
                messages=prompt,
                temperature=temperature,
                n=n,
                max_tokens=max_tokens,
                stop=stop
            )
            break
        except:
            import time; time.sleep(10); pass
    return [result.choices[i].message.content for i in range(n)]

def save_json(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_answers(datas, model):

    def parse_response(response):
        """
        Parse the response to extract JSON and Python code.
        """
        pattern = r"```(python)(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        for data_type, data_content in matches:
            data_content = data_content.strip()
        return data_content

    def get_response(data):
        default_prompt = """
        You are a Python engineer with a focus in astronomy, tasked with generating Python code in response to user instructions provided within the "instruction" field. Users might request tasks related to astronomy, typically requiring the utilization of astropy and astroquery, or general Python code generation tasks. This Python code will be directly executed, and we will provide execution results back to the user. Hence, you are expected to produce complete and executable Python code, entering it within the generate_function() function and using return for the outcomes. Consult the given example for guidance.

        **Output format**
        instruction:
        python_code：
        ```python
        ```

        **Example**
        instruction: Query the GLIMPSE infrared survey catalog for all infrared celestial bodies within a 2 arcminute square area centered on coordinates 13:16:43.64 -62:58:31.39.
        python_code：
        ```python
        def generate_function():
        from astroquery.ipac.irsa import Irsa
        import astropy.units as u
        Irsa.ROW_LIMIT = 10000
        table = Irsa.query_region("13:16:43.64 -62:58:31.39", catalog="glimpse_s07", spatial="Box", width=2*u.arcmin).to_pandas()
        return table
        ```

        **Task**
        instruction：>>> INSTRUCTION <<<
        python_code：
        """
        default_prompt = default_prompt.replace('>>> INSTRUCTION <<<', data['prompt_en'])
        response = call_openai_api(default_prompt)
        code = parse_response(response)
        data['generate_code'] = code
        return data

    responses = []
    with cfuts.ThreadPoolExecutor(
        max_workers=32
    ) as executor:
        futs = []
        for data in datas:
            futs.append(executor.submit(get_response, data))

        for f in tqdm(cfuts.as_completed(futs), total=len(futs)):
            result = f.result()
            responses.append(result)
    save_json(responses,f'data/{model}-answers.jsonl')

if __name__=='__main__':
    datas = json.loads(open("data/dataset.json"))
    datas = datas[:10]
    run_answer(datas, 'gpt-4o-2024-08-06')