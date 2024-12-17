# Astronomical Code Generation Evaluation Dataset

## Dataset Summary
The Astronomical Code Generation Evaluation Dataset is a specialized collection of 652 programming problems designed to evaluate code generation models within the field of astronomy. Each data in the dataset features a natural language instruction (prompt) paired with a canonical solution—an expected code output—and a test code to validate the generated code.

## Supported Tasks and Leaderboards
### Languages
The tasks are written in Python, and the natural language instructions are in English.

## Dataset Structure
The dataset adheres to a straightforward JSON format with the following fields:

```json
{
    "test_id": "test/0",
    "prompt": "",
    "canonical_solution": "",
    "test_code": "",
    "data_source": "astropy/astroquery"
}
```

### Data Fields
- **test_id**: An identifier for the data sample.
- **prompt**: A natural language instruction that describes the coding task.
- **canonical_solution**: The correct implementation for the task outlined in the prompt.
- **test_code**: A code designed to validate the generated code.
- **data_source**: Indicates the source of the dataset, such as `astropy` or `astroquery`.

## Dataset Creation
### Source Data

The dataset was created by extracting complete code blocks from the documentation of the Python libraries [Astropy](https://docs.astropy.org/en/stable/index_user_docs.html) and [Astroquery](https://astroquery.readthedocs.io/en/latest/#). For this purpose, we utilized GPT-4 to extract code blocks that accomplish specific tasks and ensured that the extracted code blocks were deduplicated.

For the natural language prompts, we also employed GPT-4 to generate descriptive instructions that reflect the intent of each code block. These prompts were subsequently reviewed and refined by human experts to ensure clarity and precision.

To construct the test code, we categorized the return results of the code according to their Python type and generated the test code using GPT-4, which was then manually verified for accuracy.


### Personal and Sensitive Information
None.

### Considerations for Using the Data
When evaluating generated Python code against this dataset, execute it in a safe and controlled environment to prevent any potential risks associated with executing untrusted code.

## File Structure
To maintain an organized and comprehensive structure for your dataset repository, consider the following file and folder structure:

```
astronomical_code_generation_dataset/
│
├── data/
│   ├── dataset.json                # The main dataset file in JSON format
│
├── tests/
│   ├── test_cases.py               # Unit tests to validate the test_code against canonical solutions
│
├── examples/
│   ├── example_usage.py            # Examples of how to use the dataset
│
├── README.md                       # This README file
│
└── requirements.txt                # Dependencies for running tests or examples (e.g., astropy, astroquery)
```

## License
This dataset is provided under [Your Chosen License]. Please ensure you understand the terms before using or distributing the dataset.

This structure will help you keep your dataset organized and make it easier for users to navigate and understand how to use the dataset effectively.