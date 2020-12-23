import pymongo

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.store_inventory

db.produce.drop()

db.produce.insert_many(
    [
      {
      "type": "apples",
      "cost": .23,
      "stock": 333
      },
      {"type": "oranges",
      "cost": .55,
      "stock": 500
      },
      {"type": "bananas",
      "cost": .75,
      "stock": 100
      },
      {"type": "kiwis",
      "cost": .15,
      "stock": 360
      },
      {"type": "dragon fruit",
      "cost": .80,
      "stock": 50
      }
      ]
    )