from typing import List

from vkbottle import Keyboard, KeyboardButtonColor, Callback, Text

from ORM import session, BufferType, BuffCmd
from data_typings import BuffPayload, EventPayload
from data_typings.enums import EventPayloadAction
from resources import emoji

from resources.items import buff_classes_dict, buff_races_dict
from utils import now

_remove_payload: EventPayload = {'action': EventPayloadAction.REMOVE, 'data': None}


def _make_buff_payload(data: BuffPayload) -> EventPayload:
    return {'action': EventPayloadAction.BUFF, 'data': data}


def _add_buff_button(kbd: Keyboard, label: str, msg_id: int, chat_id: int, from_id: int, buff_id: int) -> Keyboard:
    return kbd.add(Callback(label,
                            _make_buff_payload({'msg_id': msg_id,
                                                'chat_id': chat_id,
                                                'from_id': from_id,
                                                'buff_id': buff_id})),
                   KeyboardButtonColor.PRIMARY)


def _get_commands(class_id: int) -> List[BuffCmd]:
    with session() as s:
        buffer: BufferType = s.query(BufferType).filter(
            BufferType.buff_type_id == class_id).first()
        buffer_commands: List[BuffCmd] = buffer.buff_commands
    return buffer_commands

def apostol(vk_id: int, msg_id: int, chat_id: int, race1: int, race2: int = None) -> str:
    kbd = Keyboard(inline=True)
    for cmd in _get_commands(buff_classes_dict['apostol']):
        
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
        
        kbd = _add_buff_button(kbd, txt.split()[-1].capitalize(), msg_id, chat_id, vk_id, int(cmd.buff_cmd_id))
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, _remove_payload), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def warlock(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    for cmd in _get_commands(buff_classes_dict['warlock']):
        kbd = _add_buff_button(kbd, cmd.buff_cmd_text.split()[-1].capitalize(), msg_id, chat_id, vk_id, int(cmd.buff_cmd_id))
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, _remove_payload), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def paladin(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    buffer_commands: List[BuffCmd] = _get_commands(buff_classes_dict['paladin'])
    kbd = _add_buff_button(kbd, emoji.clear, msg_id, chat_id, vk_id, int(buffer_commands[0].buff_cmd_id))
    kbd.row()
    kbd.add(Callback(emoji.cancel, _remove_payload), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def crusader(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    buffer_commands: List[BuffCmd] = _get_commands(buff_classes_dict['crusader'])
    
    kbd = _add_buff_button(kbd, emoji.clear, msg_id, chat_id, vk_id, int(buffer_commands[0].buff_cmd_id))
    kbd = _add_buff_button(kbd, emoji.take_trauma, msg_id, chat_id, vk_id, int(buffer_commands[1].buff_cmd_id))
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, _remove_payload), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def light_inc(vk_id: int, msg_id: int, chat_id: int) -> str:
    kbd = Keyboard(inline=True)
    buffer_commands: List[BuffCmd] = _get_commands(buff_classes_dict['light_inc'])
    
    kbd = _add_buff_button(kbd, emoji.clear, msg_id, chat_id, vk_id, int(buffer_commands[0].buff_cmd_id))
    kbd = _add_buff_button(kbd, emoji.heal_trauma, msg_id, chat_id, vk_id, int(buffer_commands[1].buff_cmd_id))
    
    kbd.row()
    kbd.add(Callback(emoji.cancel, _remove_payload), KeyboardButtonColor.NEGATIVE)
    return kbd.get_json()


def announce_restore(note_id: int) -> str:
    kbd = Keyboard(inline=True)
    kbd.add(Text('Восстановить', {'restore': note_id}), KeyboardButtonColor.POSITIVE)
    return kbd.get_json()
