# For a new basic set of CRUD operations you could just do

``` python
from .base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
```
