from zeep import Client


def get_documentation(wsdl):
    import operator
    for service in wsdl.services.values():
        print(str(service))
        for port in service.ports.values():
            print(" " * 4, str(port))
            print(" " * 8, "Operations:")
            operations = sorted(port.binding._operations.values(), key=operator.attrgetter("name"))
            for operation in operations:
                print("%s%s" % (" " * 12, str(operation)))
            print("")


if __name__ == '__main__':
    url = 'http://localhost:8000/event/soap?wsdl'
    client = Client(url)
    get_documentation(client.wsdl)
    print('Получение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.price)

    print('\nСоздание события')
    new_event = client.service.create_event('Новое блюдо', 55)
    print('Создано событие:', new_event.id, new_event.name, new_event.price)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.price)

    print('\nОбновление события по ID')
    event_id = new_event.id
    update_event = client.service.update_event(event_id, name='Обновленное блюдо', price=9999)
    print('Обновлено событие:', update_event.id, update_event.name, update_event.price)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.price)

    print('\nУдаление события по ID')
    event_id = new_event.id
    delete_id = client.service.delete_event(event_id)
    print('Удалено событие с ID', delete_id)

    print('\nПолучение всех событий')
    events = client.service.read_all_events()
    for event in events:
        print(event.id, event.name, event.price)

