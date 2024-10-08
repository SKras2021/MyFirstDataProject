#SCOREgame
# Часть 1 Бизнес Анализ
## Цели проекта
### Общее
Целью проекта являеться разработка рекомендательной системы, которая анализируя данные пользователей может предсказать наиболее привлекательные для них продукты.
Также работая с данными пользователей система по непрямым признакам будет высчитывать кредитный рейтинг пользователя, что бы в случае рейтинг удоволетворительный предложить ему
рассрочку с кастомными условиями. Таким образом мы поможем увеличить продажи игр, а так же охват.
### Организационная структура
Организационая структура тривиальна. Над проектом работаю только я (Савва Краснокутский). При необходимости пользуюсь консультацией специалистов из karpov courses. Где karpov courses
выступает в роле "заказчика" услуги (финальный проект), а я в роле исполнителя.
### Бизнес цель
Бизнес цель проекта такога - увеличение охвата дистрибуторов компьютерных игр (steam), за счёт привлечения мало-платёжноспособной аудитории через рассрочки и free trial подписки.
Бизнес гипотеза состоит в том, что существует много людей, которые готовы покупать игры, но не могут из-за слишком большой цены. Мы помогаем им решить эту проблему. Во первых наш
сервис предоставит им точные рекомендации, которых вероятно из заинтересуют, а дальше будут представленны сгенерированные специально для него предложение о кредите/подписке/рассрочке.
Однако необходимо учитывать, что это не должно вылиться price discrimination, так что при разработке сервиса необходимо учитывать законодательное регулирование данного явления.
### Существующие решения
В сервисе steam уже существует рекомендательная система, однако она не высчитывает кредитный рейтинг и не предлогает рассрочки. Ранне steam не работал в этом направление. Это создаст 
некоторые трудности для создание решение. Но зато создаст конкурентное преимущество перед уже существующими системами в случае успеха.

## Текущая ситуация
### Железо
На данный момент имееться персональный компьютер, планируеться использовать ресурсы kaggle (cpu boost) и google collab. Однако в случае необходимости ресурсы возможно будет докупить.
Для создания пилотного демострационого продукта, этого будет достаточно.
### Ситуация с данными
Ситуация с данными тяжелая. Steam оффициально не публикует свои данные. Имееться несколько небольших и разрозненных датасетов на kaggle, один об поведение пользователей, другой об играх.
Их недостатком в их старости, небольшом размере и несвязности между собой. Также имееться библиотека в питоне для работы со steam. Планируеться использовать её для добора недостоющей информации.
Также предпринята попытка выхода на контакт по почте с администрацией сайта steam db, касаемо предоставление частичного доступа к имеющимся у них базах данным, но ответа пока получено не было.
### Консультации с заказчиком
В процесси работы над проектом будут проводиться консультации с экспертами karpov courses. В случае возникновения не предвиденных ранее проблем возможно незначительные и не структурные 
изменения оригинального тех-задания.
### Риски
У проекта на данном этапе существуют следующие риски (в порядки значимости)
1.Нету таргета (так как рассрочки раннее не выдавались)
2.Проблема с данными. (Данных катастрофически мало и они не полны)
3.Недостаточно признаков для подсчёта кредитного рейтинга пользователя
4.Не возможность построения адекватной модели в виду отсутствия закономерности
5.Нехватка времени/провал сроков.

## План решения задачи (Аналитика)
### Оценка
1.Система рекомендации (Изменено)
Оценка. Используем метрику, которую применяли при создание рекомендательной системы для netflix. Делаеться 5 рекомендаций, если минимум одной пользователь заинтересовался ставим 1 иначе 0.
Можно сделать бользе реккомендаций, так как покупка игры более серьёзный выбор в сравнение с решением о просмотре фильма (когда все фильмы уже оплачивает подписка)

Критерий успешности. Пользователь заинтересовался (купил) 1 из 5 предложенных игр. Hitrate.

Далее на этапах обучения будем испольовать F1 score: TP - Рекомендовано, пользователю понравилось. TN - Не рекомендовано, пользователю понравилось бы. FP - рекомендовано, пользователю непонравилось бы. FN - не рекомендовано, пользователю не понравилось бы.

2.Рассрочка
Придёться делать псевдо таргет (так как не имеем реального), где найдём похожий датасет, с имеющемеся результатами и сделаем на нём модель, в последующем экстраполируя её на наши данные. Поскольку ранее функции рассрочек у стима не было, то и данных на проверку их эффективности нет. Так, что оценить можно только после deployment-a.

### Критерий успешности (Изменено)
1.Система рекомендации
Из 6 предложенных игр, пользователь покупает 1. HITRATE > 0.05 (Низкий так как покупко игры серьёзнее чем просмотр фильма)

2.Система рассрочки

Три критерия.

1 - ratio успешно выплаченных рассрочек (для успеха > 0.90 так как если всё хорошо не должно пойти не так)

2 - ratio согласия на предложение о рассрочке (для успеха > 0.001 , можем позволить себе низкую значение метруки так как мы можем делать предложения миллионам игроков)

3 - общее ratio покупок в рассрочку с момента введение функции (втростепенная метрика на случай, покупок не по реккомендации а самостоятельного выбора этой опции пользователями)


## План проекта
1.Бизнес анализ
См выше.

2.Анализ данных
Собрать, привести к стандарту имеющеся в открытом доступе данные.
Провести первичный анализ, статистический (pandas numpy spicy).

3.Подготовка данных
Отбобрать и очистить имеющиеся данные, отбросить негодные.

4.Моделирования
Создать пользуясь методами глубоково машинного обучения, а также другими методами которые мы проходили на курсах, модель, для создание рекомендаций игр, а также для анализа пользователей.
Сначала анализируем пользователя, определяем его платёжеспособность, потом на основе анализа пользователя выдаём рекомендации и (или нет) предложение рассрочки.

5.Оценка Результата (Изменино)
Провести тесты исходя из описсаных выше метрик. Hitrate - для рекомендаций.

6.Внедрение
Вывести продукт на рынок. Собрать больше информации, что бы иметь возможность провести адекватную оценку поведения моделей.
