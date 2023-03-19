import dearpygui.dearpygui as dpg
import time
import numpy as np
w, h, ch, data = dpg.load_image('./img/1_main.jpg')


dpg.create_context()
dpg.create_viewport(title="Diplom", width=w, height=h +
                    50, max_width=w, max_height=h+50)


with dpg.texture_registry(show=False):
    w, h, ch, data = dpg.load_image('./img/1_main.jpg')
    main = dpg.add_static_texture(
        width=w, height=h, default_value=data, tag='img')

    w_t, h_t, ch, data_t = dpg.load_image('./img/sprites_tmp.jpg')
    tmb = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t, tag='tmb')

    w_t, h_t, ch, data_t_off = dpg.load_image('./img/sprites_tmp_off.jpg')
    tmb_off = dpg.add_static_texture(
        width=w_t, height=h_t, default_value=data_t_off, tag='tmb_off')

    w_l, h_l, ch, data_l = dpg.load_image('./img/sprites_led.jpg')
    led = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l, tag='led')

    w_l, h_l, ch, data_l_on = dpg.load_image('./img/sprites_led_on.jpg')
    led_on = dpg.add_static_texture(
        width=w_l, height=h_l, default_value=data_l_on, tag='led_on')

    w_d, h_d, ch, data_d = dpg.load_image('./img/display.jpg')
    display = dpg.add_static_texture(
        width=w_d, height=h_d, default_value=data_d, tag='display')

list_main_menu:list[str] = ["ПАРАМЕТРЫ\n          АC",
            "КОНТРОЛЬ\n ПИТАНИЯ", "РК\n", "ДПК\n"]

list_sub_menu:list[str] = [" AC\n1-24", "  AC\n25-48", "AC\n49", "AC\n50", 
                           "  AC\n55-70", "Трез", "ТМП", "СКТ", 
                           "СЛС", "115 В", "27 В", "ПЧК", "РК"]

list_as_menu:list[str] = [f"АС{i}" for i in range(25, 49)]


list_menu:list[list[str]] = [list_main_menu, list_sub_menu, list_as_menu]


with dpg.font_registry() as main_font_reg:
    with dpg.font("NotoSerifCJKjp-Medium.otf", 40, default_font=True, tag='Main_font'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font('Main_font')

# Координаты для тумблеров включения и текста

tmbs_start_coord = (175, 850)
text_coords = (430, 120)

# Магия чисел с координатами следующих тумблеров (К начальной координате добовляем координату одного тумблера)
coord_tmb_lst = {'pit_tmb': tmbs_start_coord, 'sam1_tmb': (tmbs_start_coord[0] + w_t, tmbs_start_coord[1]),
                 'sil1_tmb': (tmbs_start_coord[0] + w_t*2, tmbs_start_coord[1]), 'sam2_tmb': (tmbs_start_coord[0] + w_t*3, tmbs_start_coord[1]),
                 'sil2_tmb': (tmbs_start_coord[0] + w_t * 4, tmbs_start_coord[1])}
tmb_size = (w_t, h_t)

# Сложить два тьюпла чтобы в draw_image можно было быстро определить pmax и pmin


def sum_tpl(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, ...]:
    return tuple(np.add(x, y))

# Сокращенная запись отрисовки тумблера


def draw_tmb(name: str, tmb_state: int | str =tmb) -> None:
    dpg.draw_image(tmb_state, tuple(coord_tmb_lst[name]), sum_tpl(tmb_size, coord_tmb_lst[name]), uv_min=(0, 0),
                   uv_max=(1, 1), parent='sprites_drawlist', tag=name)

# В ДПГ мы не можем узнать шириниу объекта draw_tex, на глаз было определен размер одного символа (32ед) и теперь мы вычисляем
# ширину строки "ручками" и вычитаем это число из координаты от которой мы строим текст.


def draw_text_width(string: str) -> tuple[float, int]:
    str_list = string.split('\n')
    coord_text_edit_tuple = (len(str_list[0]) / 2 * 32, 0)
    text_coords_edit = (
        text_coords[0] - coord_text_edit_tuple[0], text_coords[1])
    return text_coords_edit

# Отрисовка текста


def draw_text(text=""):
    dpg.delete_item('text')
    dpg.draw_text(draw_text_width(text), text=text, size=60, color=(
        0, 255, 255), parent='sprites_drawlist', tag='text')

# Позиция другая, поэтому отрисовываем тумблер котроля отдельной функциекй


def draw_cntr_tmb(name: str, tmb_s: int | str=tmb) -> None:
    dpg.delete_item(name)
    dpg.draw_image(tmb_s, (680, 540), (w_t+680, h_t+540), uv_min=(0, 0),
                   uv_max=(1, 1), parent='sprites_drawlist', tag=name)

# Самая банальная проверка на "включенность" всех тумблеров (вызывается каждое нажатие на тумблер)


def check_tmb():
    pit = dpg.get_value('bool_pit')
    sam1 = dpg.get_value('bool_sam1')
    sil1 = dpg.get_value('bool_sil1')
    sam2 = dpg.get_value('bool_sam2')
    sil2 = dpg.get_value('bool_sil2')
    if pit and sam1 and sil1 and sam2 and sil2:
        draw_text(dpg.get_value("main_string"))
        time.sleep(1)
        dpg.delete_item('led_img')
        dpg.draw_image(led_on, (250, 380), (w_l+250, h_l+380), uv_min=(0, 0),
                       uv_max=(1, 1), parent='sprites_drawlist', tag='led_img')
        dpg.set_value('pui_status', value=True)
    else:
        dpg.delete_item('led_img')
        dpg.draw_image(led, (250, 380), (w_l+250, h_l+380), uv_min=(0, 0),
                       uv_max=(1, 1), parent='sprites_drawlist', tag='led_img')
        dpg.set_value('pui_status', value=False)
        draw_text()

# Далее работа со стрелами, тоже самый банальный вариант, берем просто счетчик и сбарасываем его каждый раз как дошли до конца списка

counter:int = 0
counter_main:int = 0
counter_sub:int = 0
counter_as:int = 0
input_counter:int = 0

def up_arrow():
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        counter += 1
        if counter >= len(list_menu[dpg.get_value('in_pr')]):
            counter = 0
        print(counter)
        draw_text(list_menu[dpg.get_value('in_pr')][counter])


def dwn_arrow():
    if dpg.get_value('pui_status'):
        global counter_main, counter_sub, counter_as, counter
        if counter == 0:
            counter = len(list_menu[dpg.get_value('in_pr')]) - 1 
        else:
            counter = counter - 1
        draw_text(list_menu[dpg.get_value('in_pr')][counter])
        print(counter)

def in_():
    global counter_main, counter_sub, counter_as, counter
    current_text:str = list_menu[dpg.get_value('in_pr')][counter]
    print(current_text)
    if dpg.get_value('in_pr')  == 2:
        return
    if dpg.get_value('pui_status') and ( current_text == "ПАРАМЕТРЫ\n          АC" or current_text == "  AC\n25-48"):
        dpg.set_value('in_pr', dpg.get_value('in_pr') + 1)
        draw_text(list_menu[dpg.get_value('in_pr')][0])
        counter = 0
    else: 
        return

def out_():
    global counter_main, counter_sub, counter_as, counter
    if dpg.get_value('pui_status') and dpg.get_value('in_pr'):
        dpg.set_value('in_pr', dpg.get_value('in_pr') - 1)
        draw_text(list_menu[dpg.get_value('in_pr')][0])
        counter = 0
    


# Колбэки для тумблеров

def contr_tmp():
    # Узнали в каком сейчас состоянии тумблер
    state = dpg.get_value('bool_contrl')
    if state:
        # Изменили это состояние
        dpg.set_value('bool_contrl', value=False)
        # Удалили старый и нарисовали новый
        draw_cntr_tmb('contrl_tmp')
    else:
        dpg.set_value('bool_contrl', value=True)
        draw_cntr_tmb('contrl_tmp', tmb_s=tmb_off)


def pit_tmb():
    dpg.delete_item('pit_tmb')
    state = dpg.get_value('bool_pit')
    if state:
        dpg.set_value('bool_pit', value=False)
        draw_tmb('pit_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_pit', value=True)
        draw_tmb('pit_tmb', tmb_state=tmb_off)
    check_tmb()


def sam1_tmb():
    dpg.delete_item('sam1_tmb')
    state = dpg.get_value('bool_sam1')
    if state:
        dpg.set_value('bool_sam1', value=False)
        draw_tmb('sam1_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sam1', value=True)
        draw_tmb('sam1_tmb', tmb_state=tmb_off)
    check_tmb()


def sail_tmb():
    dpg.delete_item('sil1_tmb')
    state = dpg.get_value('bool_sil1')
    if state:
        dpg.set_value('bool_sil1', value=False)
        draw_tmb('sil1_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sil1', value=True)
        draw_tmb('sil1_tmb', tmb_state=tmb_off)
    check_tmb()


def sam2_tmb():
    dpg.delete_item('sam2_tmb')
    state = dpg.get_value('bool_sam2')
    if state:
        dpg.set_value('bool_sam2', value=False)
        draw_tmb('sam2_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sam2', value=True)
        draw_tmb('sam2_tmb', tmb_state=tmb_off)
    check_tmb()


def sil2_tmb():
    dpg.delete_item('sil2_tmb')
    state = dpg.get_value('bool_sil2')
    if state:
        dpg.set_value('bool_sil2', value=False)
        draw_tmb('sil2_tmb', tmb_state=tmb)
    else:
        dpg.set_value('bool_sil2', value=True)
        draw_tmb('sil2_tmb', tmb_state=tmb_off)
    check_tmb()

# Нужды ДПГ по отрисовке


with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag="pui_status")
    dpg.add_bool_value(default_value=False, tag="bool_contrl")
    dpg.add_bool_value(default_value=False, tag="bool_pit")
    dpg.add_bool_value(default_value=False, tag="bool_sam1")
    dpg.add_bool_value(default_value=False, tag="bool_sil1")
    dpg.add_bool_value(default_value=False, tag="bool_sam2")
    dpg.add_bool_value(default_value=False, tag="bool_sil2")
    dpg.add_int_value(default_value=0, tag="in_pr")
    dpg.add_string_value(default_value="КОДЕР\nГОТОВ", tag='main_string')

with dpg.viewport_drawlist(front=True, tag='main_img'):
    dpg.draw_image(main, (0, 0), (w, h), uv_min=(
        0, 0), uv_max=(1, 1), tag='show_img')


with dpg.viewport_drawlist(front=True, tag='sprites_drawlist'):
    draw_tmb('pit_tmb')
    draw_tmb('sam1_tmb')
    draw_tmb('sil1_tmb')
    draw_tmb('sam2_tmb')
    draw_tmb('sil2_tmb')
    dpg.draw_image(tmb, (680, 540), (w_t+680, h_t+540),
                   uv_min=(0, 0), uv_max=(1, 1), tag='contrl_tmb')

    dpg.draw_image(led, (250, 380), (w_l+250, h_l+380),
                   uv_min=(0, 0), uv_max=(1, 1), tag='led_img')

    draw_text()

with dpg.window(width=w, height=h, no_background=True, pos=[0, 0], no_move=True):
    dpg.add_button(callback=pit_tmb, width=100, height=100,
                   pos=tuple(coord_tmb_lst['pit_tmb']))
    dpg.add_button(callback=sam1_tmb, width=100, height=100,
                   pos=tuple(coord_tmb_lst['sam1_tmb']))
    dpg.add_button(callback=sail_tmb, width=100, height=100,
                   pos=tuple(coord_tmb_lst['sil1_tmb']))
    dpg.add_button(callback=sam2_tmb, width=100, height=100,
                   pos=tuple(coord_tmb_lst['sam2_tmb']))
    dpg.add_button(callback=sil2_tmb, width=100, height=100,
                   pos=tuple(coord_tmb_lst['sil2_tmb']))
    dpg.add_button(width=90, height=90, pos=[85, 530])
    dpg.add_button(callback=contr_tmp, width=90, height=90, pos=[680, 540])
    dpg.add_button(callback=dwn_arrow, width=90, height=90, pos=[460, 670])
    dpg.add_button(callback=up_arrow, width=90, height=90, pos=[300, 670])
    dpg.add_button(callback= out_, width=90, height=90, pos=[140, 670])
    dpg.add_button(callback= in_, width=90, height=90, pos=[630, 670])

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
