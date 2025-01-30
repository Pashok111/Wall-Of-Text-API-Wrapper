# Python wrapper for the [Wall Of Text API](https://github.com/Pashok111/Wall-Of-Text-API)  
Little project for uploading and reading some texts and comments for them.

You can check this API at https://pashok11.tw1.su/apis/wall_of_text/docs
## How to use
Just use pip: `pip install wall_of_text_api_wrapper`
## Example
```python
from wall_of_text_api_wrapper import WallOfTextAPIWrapperLatest

api_server = "https://pashok11.tw1.su/apis/wall_of_text"
api = WallOfTextAPIWrapperLatest(api_server)

for t in api.get_texts():
    print(t)
```