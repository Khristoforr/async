import asyncio
import time
from email.message import EmailMessage
import aiosmtplib
import aiosqlite
import config


async def send_email(user_email, first_name, last_name):
    message = EmailMessage()
    message['From'] = 'root@localhost'
    message['To'] = user_email
    message['Subject'] = 'Благодарность'
    message.set_content(f"Уважаемый {first_name} {last_name}!\nCпасибо, что пользуетесь нашим сервисом объявлений.")
    connection = aiosmtplib.SMTP(hostname=config.hostname, port=config.port)
    await connection.connect()
    await connection.login(config.login, config.password)
    await connection.send_message(message)
    time.sleep(0.5)


async def get_contacts():
    async with aiosqlite.connect('contacts.db') as db:
        async with db.execute("SELECT * FROM contacts") as cursor:
            async for row in cursor:
                yield row


async def main():
    async for row in get_contacts():
        await send_email(row[3], row[1], row[2])


if __name__ == '__main__':
    asyncio.run(main())
