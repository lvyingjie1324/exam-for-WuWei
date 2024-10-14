import json
import pandas as pd
import time

def parse_questions_answers(input_entry):
    pairs = input_entry.split(';')
    qa_pairs = []
    for pair in pairs:
        try:
            question, answer = pair.split(':')
            qa_pairs.append({
                "Question": question.strip(),
                "Answer": answer.strip()
            })
        except ValueError:
            print(f"错误的格式：{pair}")
    return qa_pairs

def main():
    dataset_path = r"C:\Users\17462\Desktop\exam-reptile\hangzhou_housing_data.csv"
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"找不到文件：{dataset_path}")
        return

    results = []
    start_time = time.time()

    for index, row in df.iterrows():
        input_entry = row.get('input_column', '')
        qa_pairs = parse_questions_answers(input_entry)
        for qa in qa_pairs:
            results.append({
                "id": f"qa_{index}_{results.index(qa)}",
                **qa
            })

    output_path = r'C:\Users\17462\Desktop\exam-reptile\reformatted_dataset.json'
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)
        end_time = time.time()
        total_pairs = len(results)
        print(f"总问答对数量: {total_pairs}")
        print(f"完成数据集清理和转换过程所花费的时间: {end_time - start_time:.2f} 秒")
    except IOError as e:
        print(f"写入 JSON 文件时出现错误：{e}")

if __name__ == "__main__":
    main()