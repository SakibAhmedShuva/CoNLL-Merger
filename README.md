# CoNLL-Merger

CoNLL-Merger is a versatile tool for merging CoNLL (Conference on Natural Language Learning) format files while maintaining proper document structure and formatting. It provides both a Python-based Jupyter notebook implementation and a Flask REST API service.

## Features

- Merge multiple CoNLL files while preserving formatting
- Handle document markers (-DOCSTART-) appropriately
- UTF-8 encoding support
- Proper empty line handling between sentences
- Available as both Jupyter notebook and REST API
- Sequential file numbering for merged outputs

## Installation

```bash
# Clone the repository
git clone https://github.com/SakibAhmedShuva/CoNLL-Merger.git
cd CoNLL-Merger

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Jupyter Notebook Implementation

The notebook implementation (`conll_merger.ipynb`) provides a simple interface for merging two CoNLL files:

```python
from conll_merger import merge_conll_files

# Merge two CoNLL files
merge_conll_files(
    'path/to/first.conll',
    'path/to/second.conll',
    'path/to/output.conll'
)
```

### REST API Implementation

The Flask-based REST API (`conll_merger.py`) provides endpoints for merging multiple CoNLL files:

1. Start the server:
```bash
python conll_merger.py
```

2. The server will start on `http://localhost:5004` with the following endpoints:

#### Endpoints

##### POST /merge
Merge multiple CoNLL files

```bash
curl -X POST -F "files=@file1.conll" -F "files=@file2.conll" http://localhost:5004/merge
```

Response:
```json
{
    "success": true,
    "message": "Files merged successfully",
    "file_path": "./data/merged/merged_0001.conll",
    "file_name": "merged_0001.conll",
    "merged_files": ["file1.conll", "file2.conll"],
    "number_of_files_merged": 2,
    "status": "Merged successfully"
}
```

##### GET /list-merged
List all merged files

```bash
curl http://localhost:5004/list-merged
```

##### GET /health
Check API health status

```bash
curl http://localhost:5004/health
```

## File Structure

```
CoNLL-Merger/
├── conll_merger.ipynb      # Jupyter notebook implementation
├── conll_merger.py         # Flask API implementation
├── requirements.txt        # Project dependencies
├── data/                   # Data directory
│   └── merged/            # Directory for merged files
└── README.md              # This file
```

## Technical Details

### File Processing

- Handles `-DOCSTART-` markers appropriately
- Maintains proper empty line separation between sentences
- Ensures consistent UTF-8 encoding
- Validates input file format and encoding
- Generates sequentially numbered output files

### Error Handling

The API includes comprehensive error handling for:
- Invalid file types
- Missing files
- Encoding issues
- File processing errors

## Requirements

- Python 3.6+
- Flask
- Jupyter Notebook (for notebook implementation)
- See `requirements.txt` for complete list

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Inspired by the need for efficient CoNLL file processing in NLP tasks
- Thanks to the NLP community for standardizing the CoNLL format
