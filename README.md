# 📄 PDF Outline Extractor

**Adobe India Hackathon 1A - Round 1A: Understand Your Document**

*Connecting the Dots Through Docs*

---


## 🎯 Project Overview

A robust, intelligent PDF outline extraction system that transforms unstructured PDF documents into clean, hierarchical JSON outlines. Built for the Adobe India Hackathon, this solution extracts titles and headings (H1, H2, H3) with precise page numbers, enabling smarter document experiences for semantic search, recommendation systems, and insight generation.

### ✨ Key Features

- 🔍 **Smart Title Detection**: Extracts document titles from metadata or intelligently identifies them from content
- 📊 **Hierarchical Heading Extraction**: Identifies H1, H2, and H3 headings with advanced pattern recognition
- 🌐 **Multilingual Support**: Handles documents in multiple languages including Japanese
- ⚡ **High Performance**: Processes 50-page PDFs in under 10 seconds
- 🐳 **Containerized Solution**: Docker-ready with AMD64 architecture support
- 🔒 **Offline Operation**: No internet connectivity required
- 📏 **Lightweight**: Under 200MB total footprint

---

## 🏆 Team

- **Jiya**
- **Abhinav Rathee**

---

## 🏗️ Architecture

Our solution employs a multi-layered approach to PDF document understanding:

```
📁 Project Structure
├── 🐳 Dockerfile              # AMD64-compatible container configuration
├── 🔧 process_pdfs.py         # Main processing orchestrator
├── 📋 requirements.txt        # Python dependencies
├── ✅ validate_schema.py      # JSON schema validation
├── 📂 src/
│   ├── 🧠 outline_extractor.py  # Core extraction logic
│   ├── 📄 pdf_processor.py      # PDF handling and coordination
│   ├── 🔍 schema_validator.py   # Output validation
│   └── 🛠️ utils.py              # Utility functions and analyzers
├── 📥 input/                  # PDF input directory
└── 📤 output/                 # JSON output directory
```

### 🧩 Core Components

1. **PDF Processor** (`pdf_processor.py`)
   - Document loading and metadata extraction
   - Page-by-page content analysis
   - Result coordination and validation

2. **Outline Extractor** (`outline_extractor.py`)
   - Advanced font and formatting analysis
   - Multi-pattern heading detection
   - Title extraction algorithms

3. **Utility Modules** (`utils.py`)
   - Font size and style analysis
   - Text processing and cleaning
   - Pattern matching utilities

---

## 🚀 Quick Start

### Prerequisites

- Docker with AMD64 support
- Input PDF files (up to 50 pages each)

### Build & Run

1. **Build the Docker image:**
   ```bash
   docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
   ```

2. **Run the extraction:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     pdf-outline-extractor:latest
   ```

### Input/Output

**Input:** Place PDF files in the `input/` directory
**Output:** Structured JSON files generated in `output/` directory

**Example Output Format:**
```json
{
  "title": "Understanding Artificial Intelligence",
  "outline": [
    { "level": "H1", "text": "Introduction to AI", "page": 1 },
    { "level": "H2", "text": "Machine Learning Fundamentals", "page": 3 },
    { "level": "H3", "text": "Neural Networks Overview", "page": 5 },
    { "level": "H2", "text": "Deep Learning Applications", "page": 8 }
  ]
}
```

---

## 🔬 Technical Approach

### Intelligent Heading Detection

Our solution goes beyond simple font-size heuristics, employing:

- **Multi-pattern Recognition**: Detects numbered lists, Roman numerals, lettered sections, and formatting-based headings
- **Contextual Analysis**: Considers surrounding text, positioning, and document structure
- **Font Characteristic Analysis**: Examines font size, weight, and style patterns
- **Hierarchical Classification**: Intelligently assigns heading levels based on document structure

### Title Extraction Strategy

1. **Metadata Priority**: First attempts extraction from PDF metadata
2. **Content Analysis**: Analyzes first page for title candidates using:
   - Font size analysis
   - Position-based detection
   - Capitalization patterns
   - Length and content heuristics
3. **Fallback Mechanism**: Uses filename as last resort

### Performance Optimizations

- **Efficient PDF Processing**: Uses PyMuPDF for fast, memory-efficient PDF parsing
- **Selective Text Analysis**: Focuses on relevant text blocks to reduce processing time
- **Optimized Pattern Matching**: Compiled regex patterns for faster text processing
- **Minimal Dependencies**: Streamlined library usage for faster container startup

---

## 📊 Performance Metrics

| Metric | Specification | Our Performance |
|--------|---------------|-----------------|
| **Processing Time** | ≤ 10s for 50-page PDF | ✅ ~3-7s average |
| **Model Size** | ≤ 200MB | ✅ ~50MB total |
| **Architecture** | AMD64 CPU only | ✅ Fully compatible |
| **Network** | Offline operation | ✅ No internet required |
| **Memory** | 16GB RAM available | ✅ <1GB usage |

---

## 🛠️ Dependencies

- **PyMuPDF (1.23.14)**: High-performance PDF processing
- **regex (2023.12.25)**: Advanced pattern matching
- **jsonschema (4.17.3)**: Output validation

---

## 🔍 Testing & Validation

Our solution has been tested with:
- ✅ Simple structured documents
- ✅ Complex multi-section reports
- ✅ Documents with mixed formatting
- ✅ Multilingual content (including Japanese)
- ✅ Large documents (up to 50 pages)

### Schema Validation

Every output is validated against the required JSON schema:
- Title presence and format validation
- Heading level verification (H1, H2, H3)
- Page number accuracy
- Text content validation

---

## 📈 Future Enhancements

- **Table of Contents Integration**: Leverage existing PDF TOC when available
- **Image-based Heading Detection**: OCR integration for scanned documents
- **Custom Training**: Domain-specific heading pattern learning
- **Batch Processing Optimization**: Parallel processing for multiple PDFs

---

## 🤝 Contributing

This project was developed for the Adobe India Hackathon. For questions or collaboration:

- **Team Contact**: Jiya & Abhinav Rathee
- **Competition**: Adobe India Hackathon 1A
- **Track**: Round 1A - Document Understanding

---

## 📄 License

Developed for Adobe India Hackathon 1A - Educational and Competition Use

---

## 🙏 Acknowledgments

- Adobe India for organizing this innovative hackathon
- PyMuPDF team for excellent PDF processing capabilities
- Open source community for supporting libraries

---

<div align="center">

**Built with ❤️ for Adobe India Hackathon**

*Connecting the Dots Through Docs*

</div>
