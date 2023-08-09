# Feedback Evaluator

The **Feedback Evaluator** is a Python script designed to analyze feedback data provided in CSV format and generate visualizations and summaries for evaluation. This tool calculates various metrics and produces graphical representations to facilitate the assessment of feedback responses. The generated output is saved as a PDF file for easy sharing and documentation.

## Prerequisites

Before using the Feedback Evaluator, ensure that you have the following libraries installed:

- Pandas (`import pandas as pd`)
- Matplotlib (`import matplotlib.pyplot as plt`)
- Textwrap (`import textwrap`)
- PDFPages from Matplotlib (`from matplotlib.backends.backend_pdf import PdfPages`)
- Pingouin (`import pingouin as pg`)

## Getting Started

1. Clone or download the repository to your local machine.
2. Make sure you have the required libraries installed.
3. Place your feedback data CSV files in the `DataInput` folder.

## Usage

1. Run the script in your preferred Python environment.
2. The script will read the latest CSV file from the `DataInput` folder using Pandas.
3. It will perform calculations to generate summaries and visualizations of different feedback categories.
4. A PDF file containing the analysis results will be generated in the `output` folder.

## Functionality

The script consists of two main functions:

### `readCSVtoPandas()`

- Reads the latest CSV file from the `DataInput` folder using Pandas.
- Returns a Pandas DataFrame containing the feedback data.

### `makeEvaluationAndCreatePdf(pandasDataFrameFromInput, name)`

- Calculates Cronbach's Alpha and mean values for predefined feedback categories.
- Creates visualizations of the mean values and saves them to a PDF.
- Generates an additional page in the PDF for textual feedback.

## Customization

You can customize the script according to your needs, such as modifying the feedback categories and their corresponding columns, adjusting visualization settings, and altering PDF output paths.

## Output

The script generates a PDF report named `Feedback_Results_{name}.pdf` in the `output` folder. The PDF includes the following sections:

1. **Overview**: A cover page with a custom title and a brief description.
2. **Category Analysis**: Bar charts displaying mean values of feedback categories with error bars indicating standard deviations.
3. **Self vs. Others**: Comparison of mean values for self-assessment and feedback given by others.
4. **Textual Feedback**: A page displaying combined text feedback from respondents.

## Acknowledgments

This script utilizes various Python libraries and techniques to streamline the feedback evaluation process. Special thanks to the developers of Pandas, Matplotlib, Textwrap, and Pingouin for providing valuable tools for data analysis and visualization.
