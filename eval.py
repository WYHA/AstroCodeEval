import os
import json
import argparse
import pandas as pd
from tqdm import tqdm
from execute import execute_programs

def eval_custom_dataset(answer_path):
    datas = json.load(open(answer_path))
    results = []
    
    for dic in tqdm(datas):
        canonical_solution = dic['canonical_solution'] 
        generate_code = dic['generate_code'] 
        test_code = dic['test_code']
        data_source = dic['data_source']

        canonical_tag, canonical_result, canonical_answer, check_program = execute_programs(canonical_solution=canonical_solution)
        
        if isinstance(canonical_answer, tuple):
            for index, canonical_answer_item in enumerate(canonical_answer):
                test_tag, test_result, test_answer, check_program = execute_programs(
                    canonical_solution=canonical_solution,
                    generate_code=generate_code,
                    test_code=test_code[index],
                    tuple=True,
                    tuple_index=index
                )
                if test_tag == False:
                    break
        else:
            test_tag, test_result, test_answer, check_program = execute_programs(
                canonical_solution=canonical_solution,
                generate_code=generate_code,
                test_code=test_code[0]
            )
        
        results.append({
            "data_source": data_source,
            "score": 1 if test_tag else 0
        })

    # 创建DataFrame并汇总结果
    df_res = pd.DataFrame.from_records(results)
    pd.set_option('display.precision', 3)

    # 分组计算均值和数量
    summary = df_res.groupby('data_source')['score'].agg(['count', 'mean']).reset_index()
    
    return summary.to_string(index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-4o-2024-08-06", help="which model to test")
    args = parser.parse_args()
    summary = eval_custom_dataset(f'data/{args.model}-answers.jsonl')
    with open(f'results/{args.model}-result.txt', 'w') as f:
        f.write(summary)