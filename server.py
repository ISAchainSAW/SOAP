from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


# Модель Event
class Event(ComplexModel):
    id = Integer
    name = Unicode
    price = Integer

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


# База данных
events = [Event(1, 'Борщ купеческий', 399),
          Event(2, 'Грибная похлебка', 360),
          Event(3, 'КимЧикен', 405),
          Event(4, 'Суточные щи', 360),
]


# Сервис Event
class EventService(ServiceBase):
    # Создание события
    @rpc(Unicode, Integer, _returns=Event)
    def create_event(ctx, name, price):
        new_event_id = max([event.id for event in events]) + 1
        new_event = Event(new_event_id, name, price)
        events.append(new_event)
        return new_event

    # Получение всех событий
    @rpc(Unicode, Integer, _returns=Array(Event))
    def read_all_events(ctx, name=None, price=None):
        if name or price is not None:
            filtered_events = []
            for event in events:
                if name and name in event.name:
                    filtered_events.append(event)
                elif price is not None and  price < event.price:
                    filtered_events.append(event)
            return filtered_events
        return events

    # Обновление события по ID
    @rpc(Integer, Unicode, Integer, _returns=Event)
    def update_event(ctx, id, name=None, price=None):
        for event in events:
            if event.id == id:
                if name:
                    event.name = name
                if price:
                    event.price = price
                return event
        return None

    # Удаление события по ID
    @rpc(Integer, _returns=Integer)
    def delete_event(ctx, id):
        for i, event in enumerate(events):
            if event.id == id:
                del events[i]
                return id
        return None


# Создание приложения и добавление сервиса Event
application = Application([EventService], 'http://example.com/event/soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Запуск сервера
if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('localhost', 8000, WsgiApplication(application))
    server.serve_forever()