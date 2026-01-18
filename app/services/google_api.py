from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.constants import FORMAT
from app.core.config import settings
from app.services.reports import calculate_duration_days

TABLE_HEADER_TEMPLATE = [
    ['Отчёт от', '{date}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора (дней)', 'Описание'],
]
TO_MUTCH_COLUMNS = (
    'Передано колонок: {in_columns}, максимально допустимо: {max_columns}'
)
TO_MUTCH_ROWS = 'Передано строк: {in_rows}, максимально допустимо: {max_rows}'

SHEET_ROWS = 100
SHEET_COLUMNS = 11

SPREADSHEET_TEMPLATE = dict(
    properties=dict(
        title='Отчёт от {date}',
        locale='ru_RU',
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Лист1',
                gridProperties=dict(
                    rowCount=SHEET_ROWS,
                    columnCount=SHEET_COLUMNS,
                ),
            )
        )
    ],
)


async def create_spreadsheets(
    wrapper_services: Aiogoogle,
) -> tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = deepcopy(SPREADSHEET_TEMPLATE)

    now_date = datetime.now().strftime(FORMAT)
    spreadsheet_body['properties']['title'] = (
        spreadsheet_body['properties']['title'].format(date=now_date)
    )

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    return (
        response['spreadsheetId'],
        response['spreadsheetUrl'],
    )


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permission.create(
            fieldId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def update_spreadsheets_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')

    header = [
        [cell.format(date=datetime.now().strftime(FORMAT)) for cell in row]
        for row in TABLE_HEADER_TEMPLATE
    ]

    rows = [
        list(map(
            str,
            (
                project.name,
                calculate_duration_days(
                    project.create_date,
                    project.close_date
                ),
                project.description,
            )
        ))
        for project in projects
    ]

    table_values = [
        *header,
        *rows,
    ]

    rows_count = len(table_values)
    columns_count = max(len(row) for row in table_values)

    if rows_count > SHEET_ROWS:
        raise ValueError(
            TO_MUTCH_ROWS.format(in_rows=rows_count, max_rows=SHEET_ROWS)
        )

    if columns_count > SHEET_COLUMNS:
        raise ValueError(
            TO_MUTCH_COLUMNS.format(
                in_columns=columns_count,
                max_columns=SHEET_COLUMNS
            )
        )

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheet_Id=spreadsheet_id,
            range=f'R1C1:R{rows_count}C{columns_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values,
            }
        )
    )
