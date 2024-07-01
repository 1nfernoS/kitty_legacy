from typing import List

from sqlalchemy import ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ORM import Base, session

__all__ = ["PuzzleType", "PuzzleAnswer"]


class PuzzleType(Base):
    __tablename__ = 'puzzle_type'

    type_id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(63), nullable=False)

    puzzle_type_answers: Mapped[List["PuzzleAnswer"]] = relationship(back_populates='puzzle_type', lazy='immediate')

    def __str__(self):
        return f"<PuzzleType ({self.type_id}): {self.type_name}>"

    def __repr__(self):
        return f"<PuzzleType ({self.type_id}): {self.type_name}>"


class PuzzleAnswer(Base):
    __tablename__ = 'puzzle_answer'

    answer_id: Mapped[int] = mapped_column(primary_key=True)
    puzzle_type_id: Mapped[int] = mapped_column(ForeignKey(PuzzleType.type_id), nullable=False)
    puzzle_question: Mapped[str] = mapped_column(String(255), nullable=False)
    puzzle_answer: Mapped[str] = mapped_column(String(255), nullable=False)

    puzzle_type: Mapped[PuzzleType] = relationship(back_populates='puzzle_type_answers', lazy='immediate')

    def __str__(self):
        return f"<PuzzleAnswer ({self.puzzle_type_id}): {self.answer_id}>"

    def __repr__(self):
        return f"<PuzzleAnswer ({self.puzzle_type_id}): {self.answer_id}>"


# noinspection PyUnusedLocal
@event.listens_for(PuzzleType.__table__, "after_create")
def default_puzzle_types(*a, **kw):
    with session() as s:
        s.add(PuzzleType(type_id=1, type_name='travel'))
        s.add(PuzzleType(type_id=2, type_name='pages'))
        s.add(PuzzleType(type_id=3, type_name='door'))
        s.add(PuzzleType(type_id=4, type_name='cross'))
        s.commit()


# noinspection PyUnusedLocal
@event.listens_for(PuzzleAnswer.__table__, "after_create")
def default_puzzle_answers(*a, **kw):
    with session() as s:
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Впереди все спокойно.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Впереди не видно никаких препятствий.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Время пересечь мост через реку.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Вы бодры как никогда.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Густые деревья шумят на ветру.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Густые заросли травы по правую руку.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Дорога ведет прямиком к приключениям.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Дорога проходит мимо озера.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Идти легко, как никогда.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='На небе ни единого облачка.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Не время останавливаться!',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Ничего не предвещает беды.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Нужно двигаться дальше.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='От широкой дороги ветвится небольшая тропинка.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Пение птиц доносится из соседнего леса.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Погода просто отличная.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Самое время найти еще что-то интересное.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Солнечная поляна виднеется впереди.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Стрекот сверчков заглушает другие звуки.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Только вперед!',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Тропа ведет в густой лес.',
                           puzzle_answer='safe'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Вас клонит в сон от усталости...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Возможно, стоит повернуть назад?..',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Вдалеке слышны страшные крики...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Местность становится все опаснее и опаснее...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Нужно быть предельно осторожным...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Нужно ли продолжать путь...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Опасность может таиться за каждым деревом...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Путь становится все труднее...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='С каждым шагом чувство тревоги нарастает...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Становится сложно разглядеть дорогу впереди...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Сердце громко стучит в груди...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Туман начинает сгущаться...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Тучи сгущаются над дорогой...',
                           puzzle_answer='warn'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Боль разрывает Вас на части...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='В воздухе витает отчетливый запах смерти...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Воздух просто гудит от опасности...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Вы уже на пределе...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Еще немного, и Вы падаете без сил...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Кажется, конец близок...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Крик отчаяния вырывается у Вас из груди...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Ноги дрожат от предчувствия беды...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Нужно бежать отсюда!',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Силы быстро Вас покидают...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Смерть таится за каждым поворотом...',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Чувство тревоги бьет в колокол!',
                           puzzle_answer='danger'))
        s.add(PuzzleAnswer(puzzle_type_id=1, puzzle_question='Еще немного, и Вы падете без сил...',
                           puzzle_answer='danger'))

        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='только в неожиданный момент, свободной от оружия рукой, в незащищенную зону',
                           puzzle_answer='Грязный удар'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='эти бойцы не носили, однако это позволяло полностью сосредоточиться на агрессии в бою, имея',
                           puzzle_answer='Гладиатор'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='даже, казалось бы, всего одно умение, но именно оно может стать серьезным козырем',
                           puzzle_answer='Инициативность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='использовать особые пластины в доспехе, чтобы прикрыть эти места',
                           puzzle_answer='Прочность '))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='самое эффективное из них, позволяющее ослабить противника прямо во время',
                           puzzle_answer='Проклятие тьмы'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не брезговать осмотреть каждый карман, даже если с первого взгляда кажется, что',
                           puzzle_answer='Мародер'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='обитают ближе ко дну, чаще скрываясь в водорослях',
                           puzzle_answer='Рыбак'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='истинный путь, в зависимости от совершенных деяний и поступков',
                           puzzle_answer='Воздаяние'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='более важен размах, который усилит тяжесть удара и позволит пробить',
                           puzzle_answer='Дробящий удар'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='выследить их можно по особым магическим знакам, которые оставляют только хранители',
                           puzzle_answer='Охотник за головами'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='главное - точно соблюдать время между ними, и тогда появится возможность повторного',
                           puzzle_answer='Расчётливость '))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='поможет сэкономить время при перевязке, уменьшив',
                           puzzle_answer='Быстрое восстановление'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='если они небольшие - затянутся сами собой, даже в бою, не требуя дополнительного лечения',
                           puzzle_answer='Регенерация'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='такую позу, которая максимально подчеркнет опасность',
                           puzzle_answer='Устрашение'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='падал, но снова вставал, продолжая путь к своей цели',
                           puzzle_answer='Упорность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не столько длина пореза, сколько его глубина',
                           puzzle_answer='Кровотечение'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='своевременно и быстро совершенное - может спасти жизнь от любого, даже смертельного удара',
                           puzzle_answer='Подвижность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='использовать собственный факел даже в том случае, если вокруг нет ни единого другого источника',
                           puzzle_answer='Огонек надежды'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='иногда важнее, чем атака. Переждав несколько ударов, можно восстановить',
                           puzzle_answer='Защитная стойка'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='но не стоит страшиться - ведь Вам, в отличие от противника, он не причинит вреда, а наоборот',
                           puzzle_answer='Целебный огонь'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='если связывать их в одну охапку, то они займут меньше места в',
                           puzzle_answer='Запасливость'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='и пусть эти приметы и не всегда будут полезны, но в случае, когда',
                           puzzle_answer='Суеверность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='прямой удар острием вперед. Лезвие должно войти достаточно',
                           puzzle_answer='Колющий удар'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='грязь под ногами, как самый простой вариант. Цельтесь в глаза, чтобы',
                           puzzle_answer='Слепота'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='позволит быстро откупорить крышку и одним глотком осушить',
                           puzzle_answer='Водохлеб'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='нанести удар вдоль, максимально сблизившись с противником, чтобы он точно не смог',
                           puzzle_answer='Режущий удар'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='следить за каждым движением, которое может оказаться врагом, меньше обращая внимания на окружающее',
                           puzzle_answer='Бесстрашие'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='отрешившись от внешнего мира, однако при этом не надейтесь избежать',
                           puzzle_answer='Стойка сосредоточения'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='резким взмахом, едва задевая самым острием по широкому',
                           puzzle_answer='Рассечение'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='в сочленение между пластинами, и только тогда они',
                           puzzle_answer='Раскол'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не обязательно настроены агрессивно, многих из них можно обойти просто',
                           puzzle_answer='Исследователь'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='проникает в саму кровь врага, отравляя ее и не позволяя',
                           puzzle_answer='Заражение'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='убедиться, что вокруг нет ни единого источника света, и собрать вокруг',
                           puzzle_answer='Сила теней'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='переродиться из пепла, но только в том случае, если',
                           puzzle_answer='Феникс'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='будет достигнут только если противник находится при смерти, и уже не может',
                           puzzle_answer='Расправа'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не подставляя свои слабые точки под вероятную траекторию',
                           puzzle_answer='Неуязвимый'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='жизненные силы вокруг себя и направить их поток в свое тело',
                           puzzle_answer='Слабое исцеление'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не только следить за всем, происходящим вокруг, но и не забывать о собственных карманах',
                           puzzle_answer='Внимательность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='и всю накопленную за это время силу высвободить в одном',
                           puzzle_answer='Мощный удар'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='и кровь, заливающая глаза, придаст силы и ярости для одного',
                           puzzle_answer='Берсеркер'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='очистить разум от посторонних мыслей, сосредоточившись на',
                           puzzle_answer='Непоколебимый'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='вонзить в плоть, незащищенную броней. Лучшей точкой является шея, если',
                           puzzle_answer='Удар вампира'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='резкий и громкий звук, который собьет концентрацию противника',
                           puzzle_answer='Ошеломление'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='позволит быстрее перетаскивать камни, разбирая обвалившийся участок',
                           puzzle_answer='Расторопность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='не всегда ценность находки может быть видна сразу, иногда приходится',
                           puzzle_answer='Собиратель'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='и если провести удар прямо в этот момент, то противник попросту не успеет',
                           puzzle_answer='Контратака'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='спасительной жидкостью, которая, иногда, является полезнее любого заклинания',
                           puzzle_answer='Ведьмак'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='впитывать знания в любой ситуации, совершенствуя свои',
                           puzzle_answer='Ученик'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='дополнительный вес, придающий силу удара вместе с разгоном',
                           puzzle_answer='Таран'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='разрезать вдоль, аккуратно поддев ножом внутреннюю часть',
                           puzzle_answer='Браконьер'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='зарисовать на бумаге, каждый поворот, каждую',
                           puzzle_answer='Картограф'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='выверенные движения позволят снять пробку быстрее и сократить время',
                           puzzle_answer='Ловкость рук'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='в нужный момент подставить свой клинок под удар, отведя',
                           puzzle_answer='Парирование'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='пригнувшись максимально мягко ступая по каменному',
                           puzzle_answer='Незаметность'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='правильно напрягая мышцы, чтобы позволить им',
                           puzzle_answer='Атлетика'))
        s.add(PuzzleAnswer(puzzle_type_id=2, puzzle_question='иммунитет организма, таким образом отравление не сможет',
                           puzzle_answer='Устойчивость'))

        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Похоже, нужно поставить фигурку на определенный участок карты...',
                           puzzle_answer='Темнолесье'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Итак, как же звали воина...',
                           puzzle_answer='Гер, Натаниэль, Эмбер'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Видимо, этот камень нужно вложить в одну из вытянутых рук.',
                           puzzle_answer='Человек'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='В груди моей горел пожар, но сжег меня дотла. Ты имя назови мое, и получи сполна...',
                           puzzle_answer='Роза'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Итак, эльфа нужно расположить...',
                           puzzle_answer='Северо-восток, Северо-запад, Юг материка'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Сяэпьчео рущэр',
                           puzzle_answer='Берем строку, прогоняем по шифру Цезаря... \nЛадно, это "Гробница веков"'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Начнем с юркого гоблина...',
                           puzzle_answer='Разрезать мечом, Ударить молотом, Уколоть кинжалом'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Видимо, порядок этих барельефов как-то связан с рычагами...',
                           puzzle_answer='Грах, Ева, Трор, Смотритель'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Итак, главным реагентом добавим...',
                           puzzle_answer='Пещерный корень, Первозданная вода, Рыбий жир'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='КАКОВ ЦВЕТ СЕРДЦА?',
                           puzzle_answer='Фиолетовый'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Где в настоящее время находится истинный спуск на путь к Сердцу Глубин?',
                           puzzle_answer='Темнолесье'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='Возможно, нужно что-то произнести? Или нет?..',
                           puzzle_answer='Уйти. Да, просто уйти'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='В каком же порядке активировать плиты?..',
                           puzzle_answer='Осень, Зима, Весна, Лето'))
        s.add(PuzzleAnswer(puzzle_type_id=3, puzzle_question='ВСЕ ИСПОЛЬЗУЮТ ЗЕЛЬЕ ПАМЯТИ',
                           puzzle_answer='Цены последнего купленного зелья памяти \n10k - 3, 100k - 4, 1kk - 5 и т.д.'))

        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди засада',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='осторожно, сверху',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди атаковать из засады',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется атака',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='почему опять враг?',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='атака не поможет?',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется внимание',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='слабый враг? неожиданно...',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется выманивание',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется взяться за всех сразу',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='слабый враг, о слабый враг',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='отдых пока не здесь...',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='ближний бой является в видениях...',
                           puzzle_answer='враг'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='почему опять ловушка?',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='вероятно нечто потрясающее',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди подсадная утка',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди подсадная утка отсутствует',
                           puzzle_answer='Ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди сокровище',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди смотри внимательно',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди ценный предмет',
                           puzzle_answer='ловушка,сундук,руины,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди ловушка',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='осторожно, ловушка',
                           puzzle_answer='ловушка'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='смотри внимательно, и тогда - сундук с сокровищем!',
                           puzzle_answer='сундук,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди экипировка',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='осторожно, мимикрия',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди мимикрия отсутствует',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='да славится сундук с сокровищем!',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='сокровище является в видениях...',
                           puzzle_answer='сундук,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, ценный предмет!',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='может, это мимикрия?',
                           puzzle_answer='сундук'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='восславь солнце!',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди отдых',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди контрольная точка',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='смотри внимательно, и тогда - утраченная благодать!',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='отдых не требуется?',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='отдых сейчас не помешает',
                           puzzle_answer='целебный источник,первозданный целебный источник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди враг отсутствует',
                           puzzle_answer='целебный источник,первозданный целебный источник,горшочек с золотом,торговец,лабиринт,пещера чудес,загадка со страницей,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди лжец',
                           puzzle_answer='контрабандист,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди торговец',
                           puzzle_answer='контрабандист,торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди друг',
                           puzzle_answer='контрабандист,торговец,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='осторожно, друг',
                           puzzle_answer='контрабандист,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='будь у меня трофеи?',
                           puzzle_answer='контрабандист'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='лжец? неожиданно...',
                           puzzle_answer='контрабандист,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='друг? неожиданно...',
                           puzzle_answer='контрабандист,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='лжец, о лжец',
                           puzzle_answer='контрабандист'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='вероятно лжец',
                           puzzle_answer='контрабандист,отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется золото',
                           puzzle_answer='торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди лжец отсутствует',
                           puzzle_answer='торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется золото, и тогда - ценный предмет',
                           puzzle_answer='торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='вероятно торговец',
                           puzzle_answer='торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='Впереди требуется золото, и тогда - ценный предмет',
                           puzzle_answer='торговец'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не сдавайся!',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='помогите...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='я хочу домой...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='это похоже на сон...',
                           puzzle_answer='лабиринт,угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не верю...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='это немыслимо...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='сюда...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='снова...',
                           puzzle_answer='лабиринт,загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не вышло...',
                           puzzle_answer='загадка со страницей,лабиринт,пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='это невыносимо...',
                           puzzle_answer='лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не думай...',
                           puzzle_answer='лабиринт,загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется ключ',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='камень не поможет?',
                           puzzle_answer='испытание,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='ключ не требуется?',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='дверь? неожиданно...',
                           puzzle_answer='испытание,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='ты не имеешь права, о ты не имеешь права!',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='будь у меня ключ?',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='да славится ключ!',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется кулак',
                           puzzle_answer='испытание'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди пещера',
                           puzzle_answer='пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, нечто потрясающее',
                           puzzle_answer='пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='удачи!',
                           puzzle_answer='пещера чудес,загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='слушай внимательно...',
                           puzzle_answer='пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='подумай хорошенько!',
                           puzzle_answer='пещера чудес,загадка со страницей,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='молодец!',
                           puzzle_answer='пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не сдавайся...',
                           puzzle_answer='пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='подумай хорошенько...',
                           puzzle_answer='пещера чудес,загадка со страницей,дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='камень? неожиданно...',
                           puzzle_answer='рунный камень'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='может, это нечто потрясающее?',
                           puzzle_answer='рунный камень'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='камень является в видениях...',
                           puzzle_answer='рунный камень'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='рунный камень, о рунный камень',
                           puzzle_answer='рунный камень'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='можно начинать?',
                           puzzle_answer='рунный камень'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди нечто потрясающее',
                           puzzle_answer='угодья,озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='дальний бой не поможет?',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется скрытность',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='красиво...',
                           puzzle_answer='угодья,озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='действуй!',
                           puzzle_answer='угодья,руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='так держать, и тогда - ценный предмет!',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='спокойно...',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='сюда!',
                           puzzle_answer='угодья,пещера чудес'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди собака',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='осторожно, стадо',
                           puzzle_answer='угодья'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='будь у меня удочка?',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется лодка',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, озеро!',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='озеро является в видениях...',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='рыбалка сейчас не помешает...',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='удочка не требуется?',
                           puzzle_answer='озеро'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='сперва - смотри внимательно',
                           puzzle_answer='руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется смотри внимательно, и тогда - боевая экипировка!',
                           puzzle_answer='руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='выглядит знакомым...',
                           puzzle_answer='руины,лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='вероятно, руины',
                           puzzle_answer='руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='выглядит знакомым....',
                           puzzle_answer='руины,лабиринт'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='слишком высоко',
                           puzzle_answer='руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди ловушка отсутствует',
                           puzzle_answer='загадка со страницей,руины'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='не сюда!',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='горшок? неожиданно...',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='может, это золото?',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='золото сейчас не помешает',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди золото',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='да славится горшок!',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='золото не требуется?',
                           puzzle_answer='горшочек с золотом'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди древность',
                           puzzle_answer='загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, нечто!',
                           puzzle_answer='загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется смотри внимательно',
                           puzzle_answer='загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='враг отсутствует',
                           puzzle_answer='загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='да будет книга!',
                           puzzle_answer='загадка со страницей'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, друг!',
                           puzzle_answer='отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='так одиноко...',
                           puzzle_answer='отшельник'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='удачи не требуется?',
                           puzzle_answer='дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='узри, дверь!',
                           puzzle_answer='дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='впереди требуется дверь',
                           puzzle_answer='дверь'))
        s.add(PuzzleAnswer(puzzle_type_id=4, puzzle_question='требуется мудрец',
                           puzzle_answer='дверь'))

        s.commit()
