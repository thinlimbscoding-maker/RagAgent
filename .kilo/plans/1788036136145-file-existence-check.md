# Plan: Add File Existence Check After Creation

## Goal
Modify `python/fileHandlling.py` so `createFile()` writes to `notes.txt`, then checks whether the file exists and returns `True` or `False` accordingly.

## Current Code (`python/fileHandlling.py:1-8`)
```python
def createFile():
  with open("notes.txt", "w") as file:
     file.write("hellow first line\n")
     file.write("i am 2nd line2")
     
print(createFile())
```

## Tasks
1. Add `import os` to the imports.
2. After the `with open(...)` block in `createFile()`, add the existence check and return:
   ```python
   if os.path.exists("notes.txt"):
       return True
   else:
       return False
   ```
3. The caller (`print(createFile())`) will print `True` or `False`.
4. Validate by running `cd python && python3 fileHandlling.py` and confirming `notes.txt` is created and the output is `True`.
