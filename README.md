# Image Search Engine

A simple search Engine to search among images with text using semantic embeddings and keyword search.

## Installation

First you need to set your TogetherAI api key. it will give you some free credit the first time you sign up.

```bash
export TOGETHER_API_KEY=your_key
```
then clone the repository:
```bash
git clone https://github.com/aminghani/SearchEngine.git
```
after installation, navigate to the directory:
```bash
cd SearchEngine
```

and finally, run the application:
```bash
bash ./run.sh
```

the first time you run above code, it will download images and store information in qdrant and meilisearch. also in the first run,
clip and a mt model will be downloaded, then you can access the app using localhost:8000:
```
http://localhost:8000
```