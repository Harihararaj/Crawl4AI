# Method of Procedure:

- [Documentation](/references/documentation.md)
- [SampleOutput](/references/result.md)

> [!IMPORTANT]
> Tested Environment: `Python 3.13.7`

## Steps:
1. Create a Python Virtual Environment:
```
python3 -m venv .crawl
```
2. Activate the Environment:
```
source .crawl/bin/activate
```
3. Check for the python version using following command:
```
python3 --version
```

> [!WARNING]
> Crawl4AI requires Python 3.9 or higher

4. Install the requirements:
```
pip3 install -r requirements.txt
```

5. Create an .env file and populate the `OPEN_API_KEY`

6. Run 
```
python3 src/crawl.py
```
7. Find the result in the `references/result.md`


