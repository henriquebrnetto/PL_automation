# Prairie Data Module

This project provides a Python package for interacting with the PrairieLearn API. It includes functions for retrieving and manipulating course data, such as gradebooks and assessments.

## Installation

To install the package, clone the repository and run the following command in the terminal:

```
pip install -e .
```

This will install the package in editable mode, allowing you to make changes to the code without needing to reinstall.

## Requirements

Make sure to install the required dependencies listed in `requirements.txt`:

```
pip install -r requirements.txt
```

## Usage

You can use the functions provided in the `funcs.py` module to interact with the PrairieLearn API. Here are some examples:

```python
from praire_data.funcs import get_gradebook, get_assessments

# Example usage
gradebook = get_gradebook(course_id, token)
assessments = get_assessments(course_id, token)
```

## Functions

- `get_gradebook(course_id, token)`: Retrieves the gradebook for a specified course.
- `get_assessments(course_id, token)`: Retrieves the assessments for a specified course.
- `get_assessment_instance(course_id, token, assessment_id)`: Retrieves a specific assessment instance.
- `compare_grades(gradebook, assessments)`: Compares grades for specified assessments.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.