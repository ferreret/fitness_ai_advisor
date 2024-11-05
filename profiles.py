from db import personal_data_collection, notes_collection


# Usa esta función para obtener los valores iniciales de un perfil,
# como si fuera un esquema de los datos que almacenaremos en el perfil.
def get_values(_id):
    return {
        "_id": _id,
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male",
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 100,
            "carbs": 200,
            "fat": 50,
        },
    }


def create_profile(_id):
    profile_values = get_values(_id)
    result = personal_data_collection.insert_one(profile_values).inserted_id
    return result.inserted_id, result


def get_profile(_id):
    return personal_data_collection.find_one({"_id": {"$eq": _id}})


def get_notes(_id):
    return list(notes_collection.find({"user_id": {"$eq": _id}}))
