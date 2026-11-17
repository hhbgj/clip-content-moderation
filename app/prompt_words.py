# Text prompts per category for zero-shot CLIP. "Normal" needs a wide spread of everyday scenes:
# with only a few, ordinary pictures that look like none of them drift to a sensitive category.
PROMPT_DICT = {
    "Normal": [
        "a person reading a book",
        "a cat sleeping on the couch",
        "a child playing in the park",
        "a man walking on a street",
        "a dog running on grass",
        "a teacher in a classroom",
        "a woman using a laptop",
        "a group of friends taking a selfie",
        "a plate of food on a table",
        "a landscape with mountains and sky",
        "a city street with buildings",
        "a page of printed text",
        "a screenshot of a website",
        "a cartoon illustration",
        "a 3D rendered toy figure",
        "a product photo on a white background",
        "a family sitting together at home",
        "a doctor talking with a patient",
        "people working in an office",
        "a person exercising in a gym",
        "a couple holding hands",
        "a portrait photo of a person's face",
        "a chart or diagram"
    ],
    "Porn": [
        "a naked person",
        "a pornographic sex scene",
        "graphic adult content",
        "a couple having sex",
        "explicit nudity",
        "nude woman on bed",
        "erotic scene in bedroom",
        "two naked people"
    ],
    "Terrorism": [
        "a terrorist holding a gun",
        "a bomb explosion in public",
        "a man with a suicide vest",
        "a person pointing a gun",
        "hostage situation in building"
    ],
    "Violence": [
        "a bloody fight",
        "a dead body on the ground",
        "a man covered in blood",
        "a crime scene with blood",
        "a violent street protest"
    ]
}
