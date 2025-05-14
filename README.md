# subtitles2text

## Description

Convert subtitles files (vtt, srt, PDF) and any files supported by Docling (DOCX, PPTX, XLSX, images PNG/JPG/JPEG, web pages HTML/XHTML) from any metadata to only leave the text content. This is especially useful to feed to genAI models such as LLMs and GPTs.

It is made possible by `vtt2txt-ng`, a fork of `vtt2txt`, and `docling`.

## Installation

```bash
pip install subtitles2text
```

## Usage

```bash
subtitles2text
```

This will launch a Tk GUI where you can select the files you want to convert.

The app supports OCR.

## License

MIT License.

## Author

This app was coded using `Roo Code` with `Gemini 2.0 flash thinking exp 01-21` under the architecture specified by Stephen Karl Larroque.
