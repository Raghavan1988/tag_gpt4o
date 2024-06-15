# Universal Polyglot

Universal Polyglot is a multilingual, multimodal application leveraging the capabilities of GPT-4o and other advanced models to provide responses to queries in various languages and generate images based on descriptions. This project allows users to ask anything in any language and receive accurate responses or generated images.

<div style="color: #FF3E00; font-size: 2em;">
    This application is based on technique presented in <b> Linux Foundation's Open Source Summit</b>  at Seattle: <I> <b> "Translation Augmented Generation" </b> </i> by Raghavan Muthuregunathan. <br>
    <br>
    Link: https://sched.co/1aBOj 
</div>

## Features

- **Multilingual Translation and Response**: Translate any text input into English, generate a response using Perplexity, and then translate the response back into the original language.
- **Text-to-Image Generation**: Generate images from textual descriptions using advanced image generation models.
- **Image Input Mode**: Upload an image along with a question to get a contextual response.

## Modes

1. **Perplexity Search Engine Mode**: Ask questions in any language and get answers translated back into the original language.
2. **Text to Image Output**: Provide descriptions in any language and generate images based on those descriptions.
3. **Image Input**: Upload an image along with a question to receive a contextual response.

## Usage

### Perplexity Search Engine Mode

1. Enter your question in any language.
2. Click on "Submit".
3. View the response in the local language and debug outputs.

### Text to Image Output

1. Enter the description of the image you want to generate in any language.
2. Click on "Submit".
3. View the generated image.

### Image Input

1. Upload an image.
2. Enter a question related to the image.
3. Click on "Submit".
4. View the contextual response.

## Example Queries

- **(Tamil)**: இந்தியாவில் நெல் வயலில் விளையாடும் ஒரு சிறுவனும் பெண்ணும்
- **(Arabic)**: ما هي المحاصيل التي يمكن زراعتها في شبه الجزيرة العربية خلال موسم الجفاف
- **(Indonesian)**: Apa yang terjadi pada bayinya?

## Streamlit Application

You can access and interact with the Universal Polyglot application through the following Streamlit link:

[Universal Polyglot on Streamlit](https://lablab-gpt4o.streamlit.app/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/universal-polyglot.git
    cd universal-polyglot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com) for the GPT-4o model.
- [Replicate](https://replicate.com) for the image generation model.
- [Perplexity AI](https://perplexity.ai) for the search engine model.

---

Feel free to contribute to the project by opening issues or submitting pull requests. For any questions or suggestions, please contact the author.

Happy querying and image generating with Universal Polyglot!
