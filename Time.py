import time

def process_subscription(subscription_text, current_unix_time):
    # Разбиваем текст на строки
    lines = subscription_text.strip().split('\n')
    
    # Ищем строку с expire
    expire_line = None
    for line in lines:
        if line.startswith('#subscription-userinfo:'):
            expire_line = line
            break
    
    if not expire_line:
        # Если не нашли expire, возвращаем оригинал
        return subscription_text
    
    # Извлекаем expire из строки
    try:
        expire_str = expire_line.split('expire=')[1].split(';')[0]
        expire_unix = int(expire_str)
    except (IndexError, ValueError):
        # Если не получилось извлечь expire, возвращаем оригинал
        return subscription_text
    
    # Проверяем, истекла ли подписка
    if current_unix_time >= expire_unix:
        # Подписка истекла — оставляем только первый vless ключ с новой меткой
        result_lines = []
        first_vless_found = False
        
        for line in lines:
            if line.startswith('#'):
                # Все метаданные сохраняем
                result_lines.append(line)
            elif line.startswith('vless://') and not first_vless_found:
                # Первый vless ключ — заменяем метку
                base_key = line.split('#')[0]  # Берём часть до #
                new_line = f"{base_key}#‼️ Подписка истекла ‼️"
                result_lines.append(new_line)
                first_vless_found = True
            # Остальные vless ключи пропускаем
        
        return '\n'.join(result_lines)
    else:
        # Подписка ещё действует — возвращаем оригинал
        return subscription_text

# Пример использования
subscription_data = '''#profile-title: ZL3YY VPN⚡
#profile-update-interval: 2
#support-url: https://t.me/News_ZL3YY
#announce: Самый лутший VPN в России для обхода белых списков ⚡
#subscription-userinfo: upload=0; download=0; total=0; expire=1761744000

vless://a41da912-1ad3-4897-880c-fa6228255288@ni.yurichdelaet.ru:443?encryption=none&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=pwrZYfLntgE9L7OGL53DGpLFRXcXyzoMjJcND9c5fys&sni=ni.yurichdelaet.ru&sid=a117ee845bcb2246&type=tcp&headerType=none#🇳🇱 Нидерланды
vless://7f7372ef-37db-47ef-a980-e1642daaab7a@87.121.162.181:54443?security=tls&encryption=none&alpn=http/1.1&fp=chrome&type=tcp&headerType=none&sni=max.ru&allowInsecure=1#🇦🇱 Албания
vless://7f7372ef-37db-47ef-a980-e1642daaab7a@193.42.11.94:54443?security=tls&encryption=none&alpn=http/1.1&fp=chrome&type=tcp&headerType=none&sni=yandex.ru&allowInsecure=1#🇩🇪 Германия'''

# Текущее время на GitHub (из вашего запроса)
current_time = 1773262800

# Обрабатываем подписку
result = process_subscription(subscription_data, current_time)
print(result)
