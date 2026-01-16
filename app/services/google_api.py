from datetime import datetime

from aiogoogle import Aiogoogle

from app.constants import FORMAT
from app.core.config import settings
from app.services.reports import calculate_duration_days


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {datetime.now().strftime(FORMAT)}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permission.create(
            fieldId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def update_spreadsheets_value(
    spreadsheetid: str,
    charity_projects: list,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', datetime.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора (дней)', 'Описание']
    ]

    for project in charity_projects:
        duration = calculate_duration_days(
            project.create_date,
            project.close_date
        )

        new_row = [
            project.name,
            str(duration),
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
