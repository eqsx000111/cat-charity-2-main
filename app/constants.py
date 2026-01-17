DATABASE_URL = 'sqlite+aiosqlite:///./fastapi.db'
APP_TITLE = 'Благотворительный фонд поддержки котиков QRKot'
DESCRIPTION = 'Сервис для поддержки котиков'

TO_MUTCH_COLUMNS = 'Слишком много колонок для таблицы'
TO_MUTCH_ROWS = 'Слишком много строк для таблицы'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_FULLY_INVESTED = 'Закрытый проект нельзя редактировать!'
PROJECT_EDIT_FULL_AMOUNT = 'Нельзя установить сумму меньше уже вложенной!'
DELETE_INVESTED_PROJECT = (
    'Нельзя удалить проект, в который уже были инвестированы средства.'
)
PROJECT_NAME_EXIST = 'Проект с таким названием уже существует!'
FORMAT = '%Y/%m/%d %H:%M:%S'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SHEET_ROWS = 100
SHEET_COLUMNS = 11
