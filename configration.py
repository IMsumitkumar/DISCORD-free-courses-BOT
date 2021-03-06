import pandas as pd

URL_DICT = {"Programming Languages":"https://app.real.discount/subcategory/programming-languages/?page={q}",
            "Data Science":"https://app.real.discount/subcategory/data-science/?page={q}",
            "Web Development":"https://app.real.discount/subcategory/web-development/?page={q}",
            "Game Development":"https://app.real.discount/subcategory/game-development/?page={q}",
            "Mobile Development":"https://app.real.discount/subcategory/mobile-development/?page={q}",
            "No code Development":"https://app.real.discount/subcategory/no-code-development/?page={q}",
            "Software Engineering":"https://app.real.discount/subcategory/software-engineering/?page={q}",
            "Database Design Development":"https://app.real.discount/subcategory/database-design-development/?page={q}",
            }

DATAFRAME = pd.read_csv("database/free_courses.csv")

