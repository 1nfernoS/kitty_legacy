from typing import List

from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text

from ORM import session, BufferType, BuffCmd
from resources import emoji

from resources.items import buff_classes_dict, buff_races_dict
from utils import now


def apostol(vk_id: int, msg_id: int, chat_id: int, race1: int, race2: int = None) -> str:
    kbd = Keyboard(inline=True)
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == buff_classes_dict['apostol']).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
    for cmd in buffer_commands:
        
        if cmd.buff_cmd_id == 12:
            if not ((now().date().month == 12
                     and now().date().day > 20)  # from xxx0-12-20
                    or (now().date().month == 1
                        and now().date().day < 7)):  # to xxx1-01-07
                continue
        
        if kbd.buttons and len(kbd.buttons[-1]) // 3 == 1:
            kbd.row()
        
        txt = cmd.buff_cmd_text
        if txt.split()[-1] == 'race1':
            txt = txt.replace('race1', buff_races_dict[race1])
        
        if txt.split()[-1] == 'race2':
            if not race2:
                continue
            txt = txt.replace('race2', buff_races_dict[race2])
        
        payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': cmd.buff_cmd_id}
        kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, {'action': 'remove'}), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def warlock(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == buff_classes_dict['warlock']).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
    for cmd in buffer_commands:
        txt = cmd.buff_cmd_text
        payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': cmd.buff_cmd_id}
        kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, {'action': 'remove'}), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def paladin(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == buff_classes_dict['paladin']).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
        
    buff = buffer_commands[0].buff_cmd_id
    
    payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': buff}
    kbd.add(Callback(emoji.clear, payload), KeyboardButtonColor.PRIMARY)
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, {'action': 'remove'}), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def crusader(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == buff_classes_dict['crusader']).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
        
    buff = buffer_commands[0].buff_cmd_id
    txt = emoji.clear
    payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': buff.buff_cmd_id}
    kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    buff = buffer_commands[1].buff_cmd_id
    txt = emoji.take_trauma
    payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': buff.buff_cmd_id}
    kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, {'action': 'remove'}), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def light_inc(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == buff_classes_dict['light_inc']).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
    
    buff = buffer_commands[0].buff_cmd_id
    txt = emoji.clear
    payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': buff.buff_cmd_id}
    kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    buff = buffer_commands[1].buff_cmd_id
    txt = emoji.heal_trauma
    payload = {'action': 'buff', 'msg_id': msg_id, 'chat_id': chat_id, 'from': vk_id, 'buff': buff.buff_cmd_id}
    kbd.add(Callback(txt.split()[-1].capitalize(), payload), KeyboardButtonColor.PRIMARY)
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, {'action': 'remove'}), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def announce_restore(note_id: int) -> str:
    kbd = Keyboard(inline=True)
    kbd.add(Text('Восстановить', {'restore': note_id}), KeyboardButtonColor.POSITIVE)
    return kbd.get_json()
