# Astronomical Code Generation Evaluation Dataset

## Dataset Summary

The Astronomical Code Generation Evaluation Dataset contains 652 unique task instances designed to evaluate code generation models within the context of astronomy. Each instance includes prompts in natural language and their corresponding canonical code solutions, utilizing two widely-used Python libraries: **Astropy** and **Astroquery**. This dataset is structured to facilitate the assessment of model performance using the pass@k metric, thus providing researchers and developers with reliable benchmarks for evaluating code generation capabilities.

## Supported Tasks and Leaderboards

- **Language:** Python
- **Libraries Used:** Astropy and Astroquery
- **Evaluation Metric:** pass@k

## Dataset Structure

The dataset is structured as follows:

```plaintext
astronomy_code_eval/
    ├── README.md
    ├── dataset.json
    ├── examples/
    │   └── example_0.json
    └── scripts/
        └── evaluation_script.py
```

### Files and Directories

- **`README.md`**: This file provides an overview of the dataset, its usage, and any relevant information regarding its structure and content.
  
- **`dataset.json`**: This JSON file contains all 652 instances in the dataset, structured in the following format:

  ```json
  {
      "test_id": "test/0",
      "prompt": "Create a function to retrieve the latest astronomical data using Astroquery.",
      "canonical_solution": "def get_latest_data():\n    from astroquery.jplhorizons import Horizons\n    obj = Horizons(id='1994pc', location='500', epochs={'et': [2459200]})\n    return obj.ephemerides()",
      "test_code": "def check(candidate):\n    assert candidate() is not None",
      "data_source": "astropy/astroquery"
  }
  ```

- **`examples/`**: Directory containing example instances of the dataset, formatted as JSON files. Each file demonstrates a single data instance for clarity and understanding.

- **`scripts/`**: This directory includes scripts for evaluating the model's performance against the dataset. For example, `evaluation_script.py` may contain functions for calculating the pass@k metric based on generated outputs.

## Data Instances

Each instance in the dataset follows this structure:

- **`test_id`**: A unique identifier for the data sample.
- **`prompt`**: A natural language description of the coding task.
- **`canonical_solution`**: The expected solution, expressed in proper Python code.
- **`test_code`**: A test function to validate the correctness of the generated code.
- **`data_source`**: Specifies the libraries utilized in the solution (in this case, "astropy/astroquery").

## Dataset Creation

### Curation Rationale

This dataset was created to provide a comprehensive evaluation framework for code generation models within the astronomy domain. Given that many models are often trained on generalized datasets, a specialized dataset helps ensure that evaluations are relevant and meaningful for astronomy-related applications.

### Source Data

The dataset was meticulously crafted by domain experts in both astronomy and machine learning, ensuring rigorous attention to detail in how each prompt and solution was formulated.

### Considerations for Using the Data

As with any code generation tasks, ensure that any generated Python code is executed in a safe environment to mitigate risks associated with running unverified code.

### Licensing Information

This dataset is licensed under the MIT License, allowing for broad usage within both academic and commercial environments.

## Citation Information

If you find this dataset useful, please cite it as follows:

```bibtex
@misc{astronomy_code_eval,
      title={Astronomical Code Generation Evaluation Dataset},
      author={Your Name},
      year={2023},
      url={https://github.com/yourusername/astronomy_code_eval}
}
```
