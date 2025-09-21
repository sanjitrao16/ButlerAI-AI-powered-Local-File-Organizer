# ButlerAI: AI-Powered Local File Organizer
ButlerAI is an CLI based AI-powered local file organizer which automatically renames, categorizes, and organizes your files and directory using AI. So you can now take a huge sigh of relief and the next time you won't
be lost in your huge cluttered and unorganized file directory. Since, the utilization of AI happens completely locally (on your system, without internet), you can also not worry about your confidential informations and credentials being
leaked away or getting exposed to the internet. All the data stays on your computer and the system respects user privacy.

## Features
The application has a wide range of features which work together in providing a clean and structured output.
1. **Content extraction from text files**
   - The application suppports a variety of text files (supported text files are specified below), which are further extracted and analysed by the AI-model to provide with better file names and folder names.
2. **Image categorization**
   - Distinguishes between natural/raw photos (e.g: landscapes, potraits, posters, artworks etc) and photos which are text-heavy (e.g: screenshots, document photos, receipts etc).
   - Uses OCR (Optical Character Recognition) to extract text from images when necessary.
3. **Parallel Processing**
   - Optimizes the whole process which involves separating, understanding, extracting and generating files contents through parallel processing resulting in faster outputs and minimal delay in processing huge amount of
   files.
4. **JSON-based outputs**
   - Mapping files and folders as structured JSON ensuring easy parsing and integration.
5. **Simple yet modular architecture**
   - A modular design, which can further be extended by plugging new advance models and also implement custom rules and other efficient strategies.
6. **Multiple organization methods**
   - The application offers 3 different directory organization methods which are *by content*, *by file type* and *by date*.

## How it works:

This powerful and intelligent file organizer utilizes the capabilities of the advanced AI models to smartly rename your files and categorize them into meaningful folders, ultimately keeping your directory clean and
easy to navigate. The application is predominantly developed using the **Ollama platform** which offers a variety of Large Language Models(LLMs) to be run locally. For the development of this application, the
`gemma3:4b` vision-model is leveraged. The workflow of the application is stated below:

- Gets a file directory path as an input.
- Separates, understands and extracts the contents of the various files present in the directory.
- Content extraction is separated for text based and image based files, where the former leverages various python libraries to extract content from different file types.

The application follows the following approach in understanding file contents:
- **Text Files**: Using the `gemma3:4b` model, relevant file descriptions, file names are suggested based on the content extracted earlier.
- **Image Files**: For image based files, the application first categorizes the files on how text-heavy the file is based on **OCR analysis**, and with that relevant image captions, file names are suggested by utilizing the
  model's capability of processing image based files.

- Furthermore, based on the above approach, relevant folder names are generated and then properly categorize the files into them. 

## About the model
The AI model which is being used in the application is the `gemma3:4b` vision-model developed by **Google**. This is a multimodal AI model that processes both text and image inputs and generating text outputs. This
model perfectly suites the purpose and scope of this project given its capability to process variety of input files. The model also offers a large 128K token context window allowing it to process longer inputs which
generally is the case, considering either files can have a large amount of data or the number of files in the directory might be many. Furthermore, the model used has 4-billion parameters and that is due to certain
computational power and resource constraints. However, with a better infrastructure the same application can be developed using even more powerful models.

Link to the model: [`gemma3:4b`](https://ollama.com/library/gemma3)

## System Requirements
### Hardware Requirements:
- Operating System: Currently the application is compatible with Windows.
- CPU: Intel i5 or AMD Ryzen 5 series onwards.
- RAM: 16GB minimum, recommended 32GB.
- GPU:
  CUDA support required for GPU acceleration. 4GB VRAM minimum required.

### Software Requirements
- Python version: 3.10+.
- Ollama local model server with Gemma3:4b model downloaded and ready.
- Tesseract OCR Engine required for extracting text from images.
- Git for cloning the repository.

## Supported File Types
The application supports a variety of file types from text based to image based files. A detailed list is given below:
1. Text Files: `.txt`, `.md`, `.docx`, `.doc`
2. Presentations: `.pptx`, `.ppt`
3. Spreadsheets: `.csv`, `.xlsx`, `.xls`
4. PDFs: `.pdf`
5. Image Files: `.jpeg`, `.jpg`, `.png`, `.webp`, `.gif`

The application also identifies other file types like video files (e.g: `.mp4`) and audio files (e.g: `.mp3`), however, it doesn't analyze the files and its content instead it categorizes such files into generic folders like `Videos` and `Audios` respectively.

# Future Improvements
1. Create a full application with an UI for better accessibility.
2. Implementation of log files to store application related info/logs.
3. Further expansion by analysizing other file types or carry out efficient and better strategies to categorize additional file types.
4. Caching data to avoid frequent model requests and save time and resource.
5. Suggesting multiple file directory structures instead of just one.
6. Alternative approach for folder generation, other than JSON based.

# Guide on installing and running the application
### Pre-requisties
Before diving into the installation guide, please make sure you satisfy the above hardware and software requirements mentioned above. It is necessary for the Tesseract OCR Engine to be installed for carrying out OCR based operations. Download links:
1. [Python](https://www.python.org/downloads/)
2. [Ollama](https://ollama.com/download/windows) 
3. [Tesseract OCR Engine (Windows)](https://github.com/UB-Mannheim/tesseract/wiki)
4. [Gemma3:4b Model](https://ollama.com/library/gemma3)

### Guide

#### 1. Clone the repository
Clone the repository to your local machine using Git.

```
git clone https://github.com/sanjitrao16/ButlerAI-AI-powered-Local-File-Organizer
```

or download the repository as ZIP file and extract the contents.

#### 2. Create a virtual environment

- Open the folder in any code editor, and create a virtual environment with Python 3.12 from the terminal.

```python
python -m venv butlerai python=3.12
```

- Activate the environment

```python
butlerai/Scripts/activate
```

#### 3. Install dependancies

In the root of the directory, install the requried dependancies

```python
pip install -r requirements.txt
```

#### 4. Run the Ollama model
Before running the application, make sure the ollama model is set-up and running in the background.

#### 5. Run the application

```python
python main.py
```
