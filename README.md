# Astronomical Code Generation Evaluation Dataset

## Dataset Summary
The Astronomical Code Generation Evaluation Dataset is a specialized collection of 652 programming problems designed to evaluate code generation models within the field of astronomy. Each data in the dataset features a natural language instruction (prompt) paired with a canonical solution—an expected code output—and a test code to validate the generated code.

## Supported Tasks and Leaderboards
### Languages
The tasks are written in Python, and the instructions are provided in both English and Chinese.  

## Dataset Structure
The dataset adheres to a straightforward JSON format with the following fields:

```json
{
    "test_id": 0,
        "prompt_en": "Smooth the array [1, 4, 5, 6, 5, 7, 8] using a one-dimensional Gaussian filter with a standard deviation of 2, and treat the boundary as extended mode during the convolution calculation. Return the array after processing.",
        "prompt_zh": "使用标准差为2的一维高斯滤波器对数组[1, 4, 5, 6, 5, 7, 8]进行平滑处理，并在卷积计算时将边界视为扩展模式，返回处理后的数组。\n",
        "canonical_solution": "def canonical_solution():\n  from astropy.convolution import Gaussian1DKernel, convolve\n  gauss = Gaussian1DKernel(stddev=2)\n  return convolve([1, 4, 5, 6, 5, 7, 8], gauss, boundary='extend')\n\n\n",
        "test_code": [
            "\nimport numpy as np\n\ndef test_code(data1, data2):\n    # 检查形状是否相同\n    if data1.shape != data2.shape:\n        return False\n    # 检查内容是否相同\n    # 使用 np.allclose 而不是 np.array_equal 来处理可能的浮点误差\n    return np.allclose(data1, data2, atol=1e-8, equal_nan=True)\n\n"
        ],
        "data_source": "Astropy"
}
```

### Data Fields
- **test_id**: An identifier for the data sample.
- **prompt_en**: A natural language instruction in English that describes the coding task.
- **prompt_zh**: A natural language instruction in Chinese that describes the coding task.
- **canonical_solution**: The correct implementation for the task outlined in the prompt.
- **test_code**: A code designed to validate the generated code.
- **data_source**: Indicates the source of the dataset, such as `astropy` or `astroquery`.

## Usage
To use the dataset, follow these steps:

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. To run the code generation and evaluation:
   ```bash
   python run_answers.py 
   python eval.py
   ```
   
## Dataset Creation
### Source Data

The dataset was created by extracting complete code blocks from the documentation of the Python libraries [Astropy](https://docs.astropy.org/en/stable/index_user_docs.html) and [Astroquery](https://astroquery.readthedocs.io/en/latest/#). For this purpose, we utilized GPT-4 to extract code blocks that accomplish specific tasks and ensured that the extracted code blocks were deduplicated.

For the natural language prompts, we also employed GPT-4 to generate descriptive instructions that reflect the intent of each code block. These prompts were subsequently reviewed and refined by human experts to ensure clarity and precision.

To construct the test code, we categorized the return results of the code according to their Python type and generated the test code using GPT-4, which was then manually verified for accuracy.


### Personal and Sensitive Information
None.

### Considerations for Using the Data
When evaluating generated Python code against this dataset, execute it in a safe and controlled environment to prevent any potential risks associated with executing untrusted code.

## License
This dataset is provided under [Your Chosen License]. Please ensure you understand the terms before using or distributing the dataset.

This structure will help you keep your dataset organized and make it easier for users to navigate and understand how to use the dataset effectively.