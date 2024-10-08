import aio_pika
import httpx
import json
import asyncio
import logging


log_path = "worker.log"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),  # Логи будут сохраняться в указанный файл
        logging.StreamHandler()  # Логи также будут выводиться в консоль
    ]
)

logger = logging.getLogger(__name__)


async def start_rabbitmq_worker():
    logger.info("Starting RabbitMQ worker...")
    try:
        # Подключаемся к RabbitMQ серверу
        connection = await aio_pika.connect_robust("amqp://localhost/")
        async with connection:
            channel = await connection.channel()  # Создаем канал
            logger.info("Connected to RabbitMQ and channel created.")

            # Объявляем очереди
            request_queue = await channel.declare_queue('request_queue')
            await channel.declare_queue('response_queue')

            async def callback(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        logger.info("Received a message.")
                        # Декодируем сообщение
                        request_data = json.loads(message.body)
                        endpoint = request_data['endpoint']
                        method = request_data.get('method', 'GET').upper()  # Метод запроса (по умолчанию GET)
                        params = request_data.get('params', {})  # Параметры запроса
                        data = request_data.get('data', None)  # Тело запроса для POST/PUT

                        # Отправляем асинхронный запрос к FastAPI
                        async with httpx.AsyncClient() as client:
                            if method == 'GET':
                                response = await client.get(
                                    f"http://localhost:8000{endpoint}",
                                    params=params
                                )
                            elif method == 'POST':
                                response = await client.post(
                                    f"http://localhost:8000{endpoint}",
                                    json=data  # Тело запроса для POST в формате JSON
                                )
                            elif method == 'PUT':
                                response = await client.put(
                                    f"http://localhost:8000{endpoint}",
                                    json=data
                                )
                            elif method == 'PATCH':
                                response = await client.patch(
                                    f"http://localhost:8000{endpoint}",
                                    json=data
                                )
                            elif method == 'DELETE':
                                response = await client.delete(
                                    f"http://localhost:8000{endpoint}"
                                )
                            else:
                                raise ValueError(f"Unsupported method: {method}")

                            response.raise_for_status()  # Проверка на успешный ответ

                        # Формируем результат
                        result = {
                            'status_code': response.status_code,
                            'content': response.json()
                        }
                        logger.info(f"Request to {endpoint} succeeded with status code {response.status_code}.")
                    except Exception as exc:
                        # Обработка исключений и создание сообщения об ошибке
                        result = {
                            'status_code': 500,
                            'content': {'error': str(exc)}
                        }
                        logger.error(f"Error processing message: {exc}")

                    # Отправляем результат обратно в response_queue
                    await channel.default_exchange.publish(
                        aio_pika.Message(body=json.dumps(result).encode()),
                        routing_key='response_queue'
                    )
                    logger.info("Sent response data to response_queue.")

            # Устанавливаем callback для обработки сообщений из request_queue
            await request_queue.consume(callback)

            logger.info(' [*] Waiting for messages. To exit press CTRL+C')
            await asyncio.Future()  # Блокируем выполнение, ожидая сообщений
    except Exception as e:
        logger.critical(f"Failed to start RabbitMQ worker: {e}")
